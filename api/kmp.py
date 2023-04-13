from afn import AFN, Symbol, State
from typing import List, Tuple


class KMP(AFN):
    def __init__(self, list_states: List[State]) -> None:
        super().__init__(list_states)

    # def create_AFN(self, pattern: List[Symbol]):
    #     for i in range(len(pattern) - 1):

    def sub_str(self, chain: List[Symbol], pattern: List[Symbol]) -> Tuple[bool, int]:
        pointer = self.initial_state
        end_idx = 0

        for i in range(len(chain)):
            if pointer in self.final_states:
                end_idx = i

            current_state = self.get_states(pointer, chain[i])
            pointer = current_state.copy().pop()

        if pointer in self.final_states:
            print(len(pattern), end_idx)
            return True, end_idx - len(pattern) + 1

        return False, -1
