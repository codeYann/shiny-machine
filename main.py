from api.afn import AFN

N = AFN([0, 1, 2, 3])

N.add_transition(0, "a", 0)
N.add_transition(0, "b", 1)
N.add_transition(1, "a", 1)
N.add_transition(1, "b", 2)
N.add_transition(2, "a", 3)
N.add_transition(2, "b", 3)
N.add_transition(3, "", 0)
N.set_final_states([2])

if __name__ == "__main__":
    print(N.transitions)
    print(N.accepts("aaabb"))
    print(N.counting_patterns("aaaabbabbabbabbabbb"))
