import pytest
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

        assert afn.accepts("01111111110") is True
        assert afn.accepts("0") is False
        assert afn.accepts("010") is True
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
