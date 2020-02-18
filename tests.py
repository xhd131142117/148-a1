import itertools
import unittest
from course import Student, Course
from criterion import *
from survey import Answer, Survey, Question, MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, CheckboxQuestion
import random
from grouper import random as grouper_random
from grouper import Group, Grouper, GreedyGrouper, AlphaGrouper, Grouping, WindowGrouper, RandomGrouper
from grouper import slice_list, windows
from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists

"""
 --- test for course.py ---
"""


def test_student_to_string() -> None:
    """A test for ___str__ in class student."""
    s = Student(123, 'Mike')
    assert type(str(s)) is str


def test_student_get_answer() -> None:
    """A test for get_answer() in class student."""
    s = Student(123, 'Mike')
    ans = Answer(False)
    que = Question(2, 'F')
    s.set_answer(que, ans)
    test_ans = s.get_answer(que)
    assert ans == test_ans


def test_student_set_answer() -> None:
    """A test for set_answer() in class student."""
    s = Student(123, 'Mike')
    ans = Answer(False)
    que = Question(2, 'F')
    s.set_answer(que, ans)
    s.set_answer(que, 'True')
    test_ans = s.get_answer(que)
    assert ans is not False


def test_student_has_answer() -> None:
    """A test for has_answer() in class student."""
    s = Student(123, 'Mike')
    que = Question(2, 'F')
    assert s.has_answer(que) is False


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])
