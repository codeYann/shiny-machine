from typing import List, Dict, Set

State = int


class AFN:
    def __init__(self, list_states: List[State]) -> None:
        self.list_states: List[State] = list_states
        self.final_states: Set[State] = set()
        self.transitions: Dict[State, Dict[str, Set[State]]] = {}
        self.initial_state: State = list_states[0]

    def add_transition(self, src_state: State, symbol: str, dst_state: State) -> None:
        if src_state not in self.list_states:
            raise Exception(f"{src_state} state is not in set of state")

        if dst_state not in self.list_states:
            raise Exception(f"{dst_state} state is not in set of state")

        if src_state not in self.transitions:
            self.transitions[src_state] = {}

        self.transitions[src_state].setdefault(symbol, set()).add(dst_state)

    def set_final_states(self, states: List[State]) -> None:
        self.final_states = set(states)

    def get_states(self, src_state: State, symbol: str) -> Set[State]:
        if src_state not in self.transitions:
            raise Exception(f"This {src_state} was not previusly added.")

        if symbol not in self.transitions[src_state]:
            raise Exception(f"This {symbol} in {src_state} is not accepted")

        return self.transitions[src_state][symbol]

    def accepts(self, chain: str) -> bool:
        state_pointer = self.initial_state

        for i in range(len(chain)):
            current_state = self.get_states(state_pointer, chain[i])
            state_pointer = current_state.copy().pop()

        if state_pointer in self.final_states:
            return True

        return False

    def counting_patterns(self, chain: str) -> int:
        state_pointer = self.initial_state
        counter = 0
        for i in range(len(chain)):
            current_state = self.get_states(state_pointer, chain[i])
            state_pointer = current_state.copy().pop()

            if state_pointer in self.final_states:
                counter += 1
                state_pointer = self.initial_state

        return counter
