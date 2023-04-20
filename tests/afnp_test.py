# import pytest
from string import digits
from api.afnp import AFNP


class TestAFNP:
    def test_get_states(self) -> None:
        afnp = AFNP(["q0", "q1", "q2"])
        afnp.add_transition("q0", digits, "q0")

        assert afnp.get_states("q0", "1") == set("q0")
