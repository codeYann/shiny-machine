from typing import List, Dict, Set
from collections import defaultdict

State = int | str
Symbol = str


class AFN:
    def __init__(self, list_states: List[State]) -> None:
        self.list_states: List[State] = list_states
        self.final_states: Set[State] = set()
        self.transitions: Dict[State, Dict[Symbol, Set[State]]] = defaultdict(
            lambda: defaultdict(set)
        )
        self.initial_state: State = list_states[0]

    def add_transition(
        self, src_state: State, symbol: Symbol, dst_state: State
    ) -> None:
        if src_state not in self.list_states:
            raise ValueError(f"{src_state} state is not in set of state")

        if dst_state not in self.list_states:
            raise ValueError(f"{dst_state} state is not in set of state")

        if src_state not in self.transitions:
            self.transitions[src_state] = {}

        self.transitions[src_state].setdefault(symbol, set()).add(dst_state)

    def set_final_states(self, states: List[State]) -> None:
        self.final_states = set(states)

    def get_states(self, src_state: State, symbol: Symbol) -> Set[State]:
        if src_state not in self.transitions:
            raise Exception(f"This {src_state} was not previusly added.")

        if symbol not in self.transitions[src_state]:
            raise Exception(f"This {symbol} in {src_state} is not accepted")

        return self.transitions[src_state][symbol]

    def accepts(self, chain: List[Symbol]) -> bool:
        pointer = self.initial_state

        for i in range(len(chain)):
            current_state = self.get_states(pointer, chain[i])
            pointer = current_state.copy().pop()

        if pointer in self.final_states:
            return True

        return False

    def counting_patterns(self, chain: List[Symbol]) -> int:
        print(f"len chain: {len(chain)}")
        count = 0
        pointer = self.initial_state
        current_state: Set[State] | None = None
        for j in range(len(chain)):
            if pointer in self.final_states:
                print(f"index: {j}")
                count += 1
                current_state = self.get_states(pointer, chain[j - 1])
                pointer = current_state.copy().pop()

            current_state = self.get_states(pointer, chain[j])
            pointer = current_state.copy().pop()
            print(
                f"current_state => {current_state} symbol: {chain[j]} pointer => {pointer}, index => {j}"
            )

        return count
