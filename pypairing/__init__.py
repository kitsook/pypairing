from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, Tuple, Dict, Set
import random

class Candidate(ABC):
    @abstractmethod
    def prefer_over(self, left: Candidate, right: Candidate) -> bool:
        pass

    @abstractmethod
    def get_preferences(self) -> Sequence[Candidate]:
        pass

Pair = Tuple[Candidate, Candidate]

def check_stability(pairs: Sequence[Pair]) -> bool:
    # for each pair (a, b), there should NOT exist another pair (a', b') such that
    # (a prefers b' over b and b' prefers a over a') or
    # (b prefers a' over a and a' prefers b over b')
    for i in range(len(pairs)):
        a: Candidate
        b: Candidate
        a, b = pairs[i]
        for j in range(i+1, len(pairs)):
            a_prime: Candidate
            b_prime: Candidate
            a_prime, b_prime = pairs[j]
            if (a.prefer_over(b_prime, b) and b_prime.prefer_over(a, a_prime)) or \
                    (b.prefer_over(a_prime, a) and a_prime.prefer_over(b, b_prime)):
                return False
    return True

def generate_stable_pairs(group_a: Sequence[Candidate], group_b: Sequence[Candidate]) -> Sequence[Pair]:
    free_a = set(group_a)
    free_b = set(group_b)

    a_has_proposed: Dict[Candidate, Set[Candidate]] = dict()
    for a in group_a:
        a_has_proposed[a] = set()

    b_engaged_dict = dict()

    while free_a:
        # see who in group a is free and hasn't proposed to all yet
        can_still_propose = [a for a in free_a if len(a_has_proposed[a]) < len(group_b)]
        if not can_still_propose:
            break

        a = random.sample(can_still_propose, 1)[0]
        a_can_propose_to = [b for b in a.get_preferences() if b not in a_has_proposed[a]]

        # propose to the one that is top on pref list
        first_choice = a_can_propose_to[0]
        a_has_proposed[a].add(first_choice)
        if first_choice in free_b:
            b_engaged_dict[first_choice] = a
            free_a.remove(a)
            free_b.remove(first_choice)
        else:
            b_engaged_to = b_engaged_dict[first_choice]
            if first_choice.prefer_over(a, b_engaged_to):
                b_engaged_dict[first_choice] = a
                free_a.add(b_engaged_to)
                free_a.remove(a)

    return [(a, b) for b, a in b_engaged_dict.items()]

