import random
from typing import Sequence
from unittest import TestCase

from pypairing import Candidate, Pair, generate_stable_pairs, check_stability

class Person(Candidate):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return self._name

    def set_preferences(self, choices: Sequence[Candidate]) -> None:
        self._choices = choices

    def get_preferences(self) -> Sequence[Candidate]:
        return self._choices

class TestGeneral(TestCase):
    def setUp(self) -> None:
        self.nIsTwo = dict()
        self.nIsTwo['Simon'] = Person("Simon")
        self.nIsTwo['Peter'] = Person("Peter")
        self.nIsTwo['Jane'] = Person("Jane")
        self.nIsTwo['Mary'] = Person("Mary")

        self.nIsTwo['Simon'].set_preferences([self.nIsTwo['Jane'], self.nIsTwo['Mary']])
        self.nIsTwo['Peter'].set_preferences([self.nIsTwo['Jane'], self.nIsTwo['Mary']])
        self.nIsTwo['Jane'].set_preferences([self.nIsTwo['Simon'], self.nIsTwo['Peter']])
        self.nIsTwo['Mary'].set_preferences([self.nIsTwo['Simon'], self.nIsTwo['Peter']])

    def test_empty(self) -> None:
        assert len(generate_stable_pairs([], [])) == 0

    def test_candidate_creation(self) -> None:
        assert self.nIsTwo['Simon'].prefer_over(self.nIsTwo['Jane'], self.nIsTwo['Mary'])
        assert not self.nIsTwo['Simon'].prefer_over(self.nIsTwo['Mary'], self.nIsTwo['Jane'])

    def test_not_in_list(self) -> None:
        with self.assertRaises(Exception) as context:
            self.nIsTwo['Simon'].prefer_over(self.nIsTwo['Peter'], self.nIsTwo['Simon'])
        assert 'not on list' in str(context.exception)

class TestCheckStability(TestCase):
    def setUp(self) -> None:
        self._simon = Person("Simon")
        self._peter = Person("Peter")
        self._jane = Person("Jane")
        self._mary = Person("Mary")

    def test_stability_simple(self) -> None:
        self._simon.set_preferences([self._jane, self._mary])
        self._peter.set_preferences([self._mary, self._jane])
        self._jane.set_preferences([self._simon, self._peter])
        self._mary.set_preferences([self._peter, self._simon])

        assert not check_stability([(self._simon, self._mary), (self._peter, self._jane)])
        assert check_stability([(self._simon, self._jane), (self._peter, self._mary)])

    def test_stability_simple2(self) -> None:
        self._simon.set_preferences([self._jane, self._mary])
        self._peter.set_preferences([self._jane, self._mary])
        self._jane.set_preferences([self._simon, self._peter])
        self._mary.set_preferences([self._peter, self._simon])

        assert not check_stability([(self._simon, self._mary), (self._peter, self._jane)])
        assert check_stability([(self._simon, self._jane), (self._peter, self._mary)])

    def test_stability_all_cases_stable(self) -> None:
        self._simon.set_preferences([self._jane, self._mary])
        self._peter.set_preferences([self._mary, self._jane])
        self._jane.set_preferences([self._peter, self._simon])
        self._mary.set_preferences([self._simon, self._peter])

        assert check_stability([(self._simon, self._mary), (self._peter, self._jane)])
        assert check_stability([(self._simon, self._jane), (self._peter, self._mary)])

    def test_stability_empty(self) -> None:
        assert check_stability([])
        assert check_stability(generate_stable_pairs([], []))

    def test_stability_random(self) -> None:
        num_trial = 100
        max_pair = 50
        for _ in range(0, num_trial):
            a_list = []
            b_list = []
            count = random.randrange(10, max_pair)
            # create candidates in two lists
            for i in range(count):
                a_list.append(Person("a_"+str(i)))
                b_list.append(Person("b_"+str(i)))
            # randomly set prefernces for each candidate
            for a in a_list:
                pref = b_list[:]
                random.shuffle(pref)
                a.set_preferences(pref)
            for b in b_list:
                pref = a_list[:]
                random.shuffle(pref)
                b.set_preferences(pref)

            pairs = generate_stable_pairs(a_list, b_list)
            assert len(pairs) == count
            assert len(set([a for a, b in pairs])) == count
            assert len(set([b for a, b in pairs])) == count
            if not check_stability(pairs):
                dump_dict = {}
                for a in a_list:
                    dump_dict[str(a)] = a.get_preferences()
                for b in b_list:
                    dump_dict[str(b)] = b.get_preferences()
                dump_dict['pairs'] = pairs
                print(dump_dict)
            assert check_stability(pairs)

class TestOnlyOnePosibility(TestCase):
    def setUp(self) -> None:
        self.nIsTwo = dict()
        self.nIsTwo['Simon'] = Person("Simon")
        self.nIsTwo['Peter'] = Person("Peter")
        self.nIsTwo['Jane'] = Person("Jane")
        self.nIsTwo['Mary'] = Person("Mary")

        self.nIsTwo['Simon'].set_preferences([self.nIsTwo['Jane'], self.nIsTwo['Mary']])
        self.nIsTwo['Peter'].set_preferences([self.nIsTwo['Jane'], self.nIsTwo['Mary']])
        self.nIsTwo['Jane'].set_preferences([self.nIsTwo['Simon'], self.nIsTwo['Peter']])
        self.nIsTwo['Mary'].set_preferences([self.nIsTwo['Simon'], self.nIsTwo['Peter']])

    def test_stable_result_for_two(self) -> None:
        left = [self.nIsTwo['Simon'], self.nIsTwo['Peter']]
        right = [self.nIsTwo['Jane'], self.nIsTwo['Mary']]
        pairs: Sequence[Pair] = generate_stable_pairs(left, right)

        assert len(pairs) == 2
        assert (self.nIsTwo['Simon'], self.nIsTwo['Jane']) in pairs
        assert (self.nIsTwo['Peter'], self.nIsTwo['Mary']) in pairs
        assert check_stability(pairs)

class TestMoreThanOnePosibility(TestCase):
    def setUp(self) -> None:
        self.nIsTwo = dict()
        self.nIsTwo['Simon'] = Person("Simon")
        self.nIsTwo['Peter'] = Person("Peter")
        self.nIsTwo['Jane'] = Person("Jane")
        self.nIsTwo['Mary'] = Person("Mary")

        # in this case, any combination will be stable
        self.nIsTwo['Simon'].set_preferences([self.nIsTwo['Jane'], self.nIsTwo['Mary']])
        self.nIsTwo['Peter'].set_preferences([self.nIsTwo['Mary'], self.nIsTwo['Jane']])
        self.nIsTwo['Jane'].set_preferences([self.nIsTwo['Peter'], self.nIsTwo['Simon']])
        self.nIsTwo['Mary'].set_preferences([self.nIsTwo['Simon'], self.nIsTwo['Peter']])

    def test_stable_result_for_two(self) -> None:
        left = [self.nIsTwo['Simon'], self.nIsTwo['Peter']]
        right = [self.nIsTwo['Jane'], self.nIsTwo['Mary']]
        pairs: Sequence[Pair] = generate_stable_pairs(left, right)
        assert check_stability(pairs)

class TestSameSeedProduceSameResult(TestCase):
    def setUp(self) -> None:
        self.a_list = []
        self.b_list = []
        self.count = 20

        # create candidates in two lists
        for i in range(0, self.count):
            self.a_list.append(Person("a_"+str(i)))
            self.b_list.append(Person("b_"+str(i)))
        # randomly set prefernces for each candidate
        for a in self.a_list:
            pref = self.b_list[:]
            random.shuffle(pref)
            a.set_preferences(pref)
        for b in self.b_list:
            pref = self.a_list[:]
            random.shuffle(pref)
            b.set_preferences(pref)

    def test_same_seed(self) -> None:
        seed = 42
        prev_result = None
        for _ in range(0, 100):
            pairs = generate_stable_pairs(self.a_list, self.b_list, seed)
            if prev_result:
                assert prev_result == pairs
            prev_result = pairs
            assert len(pairs) == self.count
            assert len(set([a for a, b in pairs])) == self.count
            assert len(set([b for a, b in pairs])) == self.count
            assert check_stability(pairs)