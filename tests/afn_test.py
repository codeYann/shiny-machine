import pytest
import string
from api.afn import AFN


class TestAFN:
    def test_initial_state(self) -> None:
        afn = AFN(["1", "2", "3", "$"])
        assert afn.initial_state == "1"

    def test_final_states(self) -> None:
        afn = AFN(["1", "2", "3", "$"])
        afn.set_final_states(["3", "$"])
        assert afn.final_states == set(["3", "$"])

    def test_transition(self) -> None:
        afn = AFN(["1", "2", "3", "$"])
        afn.add_transition("1", "a", "2")

        assert afn.transitions == {"1": {"a": {"2"}}}
        assert afn.final_states == set()

    def test_get_state(self) -> None:
        afn = AFN(["1", "2", "3", "$", "x", "z"])
        afn.add_transition("1", "b", "z")
        afn.add_transition("z", "b", "1")

        z_transition_value = afn.get_states("z", "b")
        one_transition_value = afn.get_states("1", "b")

        assert z_transition_value == set("1")
        assert one_transition_value == set("z")

        # This test if src_state is not in transitions table
        with pytest.raises(Exception):
            afn.get_states("y", "b")

        # This test if symbol is not in transitions[state]
        with pytest.raises(Exception):
            afn.get_states("1", "k")

    def test_accepts(self) -> None:
        afn = AFN(["q0", "q1", "q2"])
        afn.add_transition("q0", "0", "q1")
        afn.add_transition("q1", "1", "q1")
        afn.add_transition("q1", "0", "q2")
        afn.set_final_states(["q2"])

        assert afn.accepts("01111111110") == True
        assert afn.accepts("0") == False
        assert afn.accepts("010") == True
        with pytest.raises(Exception):
            afn.accepts("1")

    def test_couting_patterns(self) -> None:
        afn = AFN(["q0", "q1", "q2"])
        afn.add_transition("q0", "0", "q1")
        afn.add_transition("q1", "1", "q1")
        afn.add_transition("q1", "0", "q2")
        afn.set_final_states(["q2"])
        assert afn.counting_patterns("01111111111100111111111110") == 2

        with pytest.raises(Exception):
            afn.counting_patterns("222222")

    def test_couting_patterns_in_numbers(self) -> None:

        exclude_options = "".join([string.digits, "+", "-", "."])
        others_case = "".join(
            [char for char in string.printable if char not in exclude_options]
        )

        afn = AFN(["q0", "q1", "q2", "int", "q4", "q5", "float"])
        afn.add_transition("q0", "+", "q1")
        afn.add_transition("q0", "-", "q1")
        afn.add_transition("q0", string.digits, "q1")
        afn.add_transition("q1", string.digits, "q2")
        afn.add_transition("q2", string.digits, "q2")
        afn.add_transition("q2", others_case, "int")
        afn.add_transition("q2", ".", "q4")
        afn.add_transition("q4", string.digits, "q5")
        afn.add_transition("q5", string.digits, "q5")
        afn.add_transition("q5", others_case, "float")

        afn.final_states(["q2", "q5"])
        afn.set_pattenrs(["int", "float"])

        response = afn.recognize_patterns("+155", others_case)

        assert response == {"int": 1, "float": 0}
