import string
from api.afnp import AFNP


class TestAFNP:
    """Creating a bunch of unit test in AFNP Class"""

    def test_afnp_attributes(self) -> None:
        """
        Testing if there's any substr of string.digits and . in afnp.else_case
        """
        afnp = AFNP(["q0", "q1", "q2"])
        invalid_chars = [c for c in "".join([string.digits, "."])]
        assert any(c in afnp.else_case for c in invalid_chars) is False

    def test_afnp_get_states(self) -> None:
        """
        AFNP's get_states method has a several differences beetwen AFN class.

        Here do we need to check if the symbol is in string.digits
        and if digits are in src_state keys list.

        We also check if the symbol is in afnp.else_case
        and if else_case are in src_state keys list.

        If any of this conditional are sastisfied then we return
        self.transition[src_state][digits] or
        self.transition[src_state][afnp.else_case]
        """

        afnp = AFNP(["q0", "q1", "q2"])
        afnp.add_transition("q0", afnp.else_case, "q1")
        response = afnp.get_states("q0", "$")
        print(afnp.transitions)
        assert response == {"q1"}
