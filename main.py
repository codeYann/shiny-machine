from api.afn import AFN

N = AFN(["q0", "q1", "q2", "q3"])

N.add_transition("q0", "0", "q0")
N.add_transition("q0", "1", "q1")
N.add_transition("q1", "0", "q1")
N.add_transition("q1", "1", "q2")
N.add_transition("q2", "0", "q3")
N.add_transition("q2", "1", "q3")
N.add_transition("q3", "1", "q0")
N.add_transition("q3", "0", "q0")
N.set_final_states(["q3"])

if __name__ == "__main__":
    # print(N.transitions)
    print(N.counting_patterns("111111"))
    # print(N.counting_patterns("aaaabbabbabbabbabbb"))
