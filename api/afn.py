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
        count = 0
        i = 0
        while i < len(chain):
            pointer = self.initial_state
            last_symbol = None
            while i < len(chain):
                current_state = self.get_states(pointer, chain[i])
                if current_state:
                    last_symbol = chain[i]
                    pointer = current_state.copy().pop()
                    i += 1
                else:
                    break
            if pointer in self.final_states and last_symbol is not None:
                count += 1
                # Recover last symbol and move back to initial state
                current_state = self.get_states(pointer, last_symbol)
                pointer = current_state.copy().pop()
            else:
                # Move back to initial state without recovering last symbol
                pointer = self.initial_state
            if pointer not in self.transitions:
                break

        return count
