from string import digits, printable
from typing import Set, List, Dict

from .afn import AFN, State, Symbol


class AFNP(AFN):
    def __init__(self, list_states: List[State]) -> None:
        super().__init__(list_states)
        exclude_options = "".join([digits, "."])
        self.else_case = "".join([c for c in printable if c not in exclude_options])
        self.patterns: Set[State] = set()

    def set_patterns(self, patterns: List[State]) -> None:
        self.patterns = set(patterns)

    def get_states(self, src_state: State, symbol: Symbol) -> Set[State]:
        if (
            digits in [keys for keys in self.transitions[src_state].keys()]
            and symbol in digits
        ):
            symbol = digits
            return self.transitions[src_state][symbol]

        if (
            self.else_case in [keys for keys in self.transitions[src_state].keys()]
            and symbol in self.else_case
        ):
            symbol = self.else_case
            return self.transitions[src_state][symbol]

        if src_state not in self.transitions:
            raise Exception(
                f"This {src_state} was not previusly added in transition table."
            )

        if symbol not in self.transitions[src_state]:
            raise Exception(f"{src_state} has not a transition for symbol => {symbol}")

        return self.transitions[src_state][symbol]

    def counting_patterns(self, chain: List[Symbol]) -> Dict[State, int]:
        dict_counter: Dict[State, int] = {}

        for pattern in self.final_states:
            dict_counter[pattern] = 0

        pointer = self.initial_state
        current_state = None

        for idx, symbol in enumerate(chain):
            current_state = self.get_states(pointer, symbol)
            pointer = current_state.copy().pop()
            if pointer in self.final_states:
                dict_counter[pointer] += 1
                symbol = chain[idx - 1]
                pointer = self.initial_state
        return dict_counter
