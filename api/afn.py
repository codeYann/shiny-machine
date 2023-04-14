from re import S
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
        self.patterns: Set[State] = set()

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

    def set_pattenrs(self, patterns: List[State]) -> None:
        self.patterns = set(patterns)
        
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
        pointer = self.initial_state
        current_state: Set[State] | None = None
        for j in range(len(chain)):
            current_state = self.get_states(pointer, chain[j])
            pointer = current_state.copy().pop()
            if pointer in self.final_states:
                count += 1
                pointer = self.initial_state
        return count


    def recognize_patterns(self, chain: List[Symbol], other_case: List[Symbol]) -> Dict[State, int]
        pointer = self.initial_state
        counter: Dict[State, int] = {}

        for i in self.patterns:
            counter[i] = 0

        for j in range(len(chain)):
            symbol = chain[j]
            if pointer in self.final_states and symbol in other_case:
                current_state = self.get_states(pointer, symbol)
                new_pointer = current_state.copy().pop()
                counter[new_pointer] = int(counter[new_pointer]) + 1

            current_state = self.get_states(pointer, symbol)
            pointer = current_state.copy().pop()

        return counter
