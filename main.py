from api.afnp import AFNP
from string import digits

afnp = AFNP(["q0", "q1", "q2", "int", "q4", "q5", "float"])
afnp.add_transition("q0", "+", "q1")
afnp.add_transition("q0", "-", "q1")
afnp.add_transition("q0", digits, "q2")
afnp.add_transition("q2", digits, "q2")
afnp.add_transition("q1", digits, "q2")
afnp.add_transition("q2", afnp.else_case, "int")
afnp.add_transition("q2", ".", "q4")
afnp.add_transition("int", afnp.else_case, "q0")
afnp.add_transition("int", digits, "q0")
afnp.add_transition("q4", digits, "q5")
afnp.add_transition("q5", digits, "q5")
afnp.add_transition("q5", afnp.else_case, "float")
afnp.add_transition("float", digits, "q0")
afnp.add_transition("float", afnp.else_case, "q0")


afnp.set_final_states(["int", "float"])
afnp.set_patterns(["int", "float"])

if __name__ == "__main__":
    try:
        input = "+128312a29123910-23123b-222b+1555.03a"
        response = afnp.counting_patterns(input)
        print(f"input => {input} \noutput => {response}")
    except Exception as e:
        print(e)
