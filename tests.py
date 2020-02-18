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
    """A test for ___str__ in class Student."""
    s = Student(123, 'Mike')
    assert type(str(s)) is str


def test_student_get_answer() -> None:
    """A test for get_answer() in class Student."""
    s = Student(123, 'Mike')
    ans = Answer(False)
    que = Question(2, 'F')
    s.set_answer(que, ans)
    test_ans = s.get_answer(que)
    assert ans == test_ans


def test_student_set_answer() -> None:
    """A test for set_answer() in class Student."""
    s = Student(123, 'Mike')
    ans = Answer(False)
    que = Question(2, 'F')
    s.set_answer(que, ans)
    s.set_answer(que, 'True')
    test_ans = s.get_answer(que)
    assert ans is not False


def test_student_has_answer() -> None:
    """A test for has_answer() in class Student."""
    s = Student(123, 'Mike')
    que = Question(2, 'F')
    assert s.has_answer(que) is False


def test_course_enroll_student() -> None:
    """A test for enroll_student() in class Course."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    c = Course('CS')
    c.enroll_students([s1, s2])
    assert s1 in c.students and s2 in c.students


def test_course_enroll_student_same_id() -> None:
    """A test for enroll_student() in class Course."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(1, 'C')
    c = Course('CS')
    c.enroll_students([s1, s2])
    c.enroll_students([s3])
    assert s3 not in c.students


def test_course_enroll_student_empty() -> None:
    """A test for enroll_student() in class Course."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, '')
    c = Course('CS')
    c.enroll_students([s1, s2])
    c.enroll_students([s3])
    assert s3 not in c.students


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])
