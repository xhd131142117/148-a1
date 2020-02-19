import itertools
import unittest
from course import Student, Course
from criterion import Criterion, HomogeneousCriterion, HeterogeneousCriterion, LonelyMemberCriterion
from survey import Answer, Survey, Question, MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, CheckboxQuestion
import random
from grouper import random as grouper_random
from grouper import Group, Grouper, GreedyGrouper, AlphaGrouper, Grouping, WindowGrouper, RandomGrouper
from grouper import slice_list, windows
from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists

"""
    ---------------------------------------------------------
    ------------------ test for course.py -------------------
    ---------------------------------------------------------
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


def test_course_all_answered() -> None:
    """A test for all_answered() in class Course."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    c = Course('CS')
    c.enroll_students([s1, s2])
    q1 = YesNoQuestion(2, 'F')
    q2 = YesNoQuestion(3, 'K')
    a1 = Answer(True)
    a2 = Answer(False)
    survey = Survey([q1, q2])
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s2.set_answer(q1, a1)
    s2.set_answer(q2, a2)
    assert c.all_answered(survey) is True


def test_course_get_students() -> None:
    """A test for get_students() in class Course."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    c = Course('CS')
    c.enroll_students([s3, s1, s2])
    test_tup = c.get_students()
    assert test_tup == (s1, s2, s3)


"""
    ---------------------------------------------------------
    ------------------ test for survey.py -------------------
    ---------------------------------------------------------
"""


def test_survey_multi_to_string() -> None:
    """A test for _str__() in class MultipleChoiceQuestion."""
    q = MultipleChoiceQuestion(1, 'ABC', ['A', 'B'])
    assert type(str(q)) is str


def test_survey_multi_valid_answer() -> None:
    """A test for validate_answer() in class MultipleChoiceQuestion."""
    q = MultipleChoiceQuestion(1, 'ABC', ['A', 'B'])
    a = Answer('A')
    assert q.validate_answer(a)


def test_survey_multi_invalid_answer() -> None:
    """A test for validate_answer() in class MultipleChoiceQuestion."""
    q = MultipleChoiceQuestion(1, 'ABC', ['A', 'B'])
    a = Answer('C')
    assert q.validate_answer(a) is False


def test_survey_multi_similarity_same() -> None:
    """A test for get_similarity() in class MultipleChoiceQuestion."""
    q = MultipleChoiceQuestion(1, 'ABC', ['A', 'B'])
    a = Answer('A')
    b = Answer('A')
    assert type(q.get_similarity(a, b)) is float
    assert q.get_similarity(a, b) == 1.0


def test_survey_multi_similarity_different() -> None:
    """A test for get_similarity() in class MultipleChoiceQuestion."""
    q = MultipleChoiceQuestion(1, 'ABC', ['A', 'B'])
    a = Answer('A')
    b = Answer('B')
    assert q.get_similarity(a, b) == 0.0


def test_survey_num_to_string() -> None:
    """A test for __str__() in class NumericQuestion."""
    q = NumericQuestion(1, 'ABC', 0, 10)
    assert type(str(q)) is str


def test_survey_num_valid_answer() -> None:
    """A test for validate_answer() in class NumericQuestion."""
    q = NumericQuestion(1, 'ABC', 0, 10)
    a = Answer(2)
    assert q.validate_answer(a)


def test_survey_num_invalid_answer_first() -> None:
    """A test for validate_answer() in class NumericQuestion."""
    q = NumericQuestion(1, 'ABC', 0, 10)
    a = Answer(11)
    assert q.validate_answer(a) is False


def test_survey_num_invalid_answer_second() -> None:
    """A test for validate_answer() in class NumericQuestion."""
    q = NumericQuestion(1, 'ABC', 0, 10)
    a = Answer(7.5)
    assert q.validate_answer(a) is False


def test_survey_num_similarity() -> None:
    """A test for get_similarity() in class NumericQuestion."""
    q = NumericQuestion(1, 'ABC', 0, 10)
    a1 = Answer(8)
    a2 = Answer(4)
    assert q.get_similarity(a1, a2) == 0.6


def test_survey_yesno_to_string() -> None:
    """A test for __str__() in class YesNoQuestion."""
    q = YesNoQuestion(1, 'ABC')
    assert type(str(q)) is str


def test_survey_yesno_valid_answer() -> None:
    """A test for validate_answer() in class YesNoQuestion."""
    q = YesNoQuestion(1, 'ABC')
    a = Answer(True)
    assert q.validate_answer(a)


def test_survey_yesno_invalid_answer() -> None:
    """A test for validate_answer() in class YesNoQuestion."""
    q = YesNoQuestion(1, 'ABC')
    a = Answer(2)
    assert q.validate_answer(a) is False


def test_survey_yesno_similarity_same() -> None:
    """A test for get_similarity() in class YesNoQuestion."""
    q = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(True)
    assert q.get_similarity(a1, a2) == 1.0


def test_survey_yesno_similarity_different() -> None:
    """A test for get_similarity() in class YesNoQuestion."""
    q = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(False)
    assert q.get_similarity(a1, a2) == 0.0


def test_survey_checkbox_to_string() -> None:
    """A test for __str__() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    assert type(str(q)) is str


def test_survey_checkbox_valid_answer() -> None:
    """A test for validate_answer() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a = Answer(['a', '1'])
    assert q.validate_answer(a)


def test_survey_checkbox_invalid_answer_empty() -> None:
    """A test for validate_answer() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a = Answer([])
    assert q.validate_answer(a) is False


def test_survey_checkbox_invalid_answer_not_in() -> None:
    """A test for validate_answer() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a = Answer(['a', '2'])
    assert q.validate_answer(a) is False


def test_survey_checkbox_invalid_answer_duplicate() -> None:
    """A test for validate_answer() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a = Answer(['a', 'a'])
    assert q.validate_answer(a) is False


def test_survey_checkbox_similarity() -> None:
    """A test for get_similarity() in class CheckboxQuestion."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a1 = Answer(['a', 'b'])
    a2 = Answer(['b', 'c', 'd'])
    assert q.get_similarity(a1, a2) == 0.25


def test_survey_answer_is_valid_yes() -> None:
    """A test for is_valid() in class Answer."""
    q = YesNoQuestion(1, 'ABC')
    a = Answer(True)
    assert a.is_valid(q)


def test_survey_answer_is_valid_no() -> None:
    """A test for is_valid() in class Answer."""
    q = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    a = Answer(['b'])
    assert a.is_valid(q) is False


def test_survey_survey_len() -> None:
    """A test for __len__() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    assert len(s) == 2


def test_survey_survey_contain() -> None:
    """A test for __contain__() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    assert q1 in s


def test_survey_survey_to_string() -> None:
    """A test for __str__() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    assert type(str(s)) is str


def test_survey_survey_get_questions() -> None:
    """A test for get_questions() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    lst = s.get_questions()
    assert q1 in lst and q2 in lst


def test_survey_survey_set_weight_valid() -> None:
    """A test for set_weight() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    assert s.set_weight(2.0, q1)


def test_survey_survey_set_weight_invalid() -> None:
    """A test for set_weight() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1])
    assert s.set_weight(2.0, q2) is False


def test_survey_survey_set_criterion_valid() -> None:
    """A test for set_criterion() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1, q2])
    c = HomogeneousCriterion()
    assert s.set_criterion(c, q1)


def test_survey_survey_set_criterion_invalid() -> None:
    """A test for set_criterion() in class Survey."""
    q1 = CheckboxQuestion(1, 'ABC', ['a', '1', ','])
    q2 = YesNoQuestion(2, 'BBC')
    s = Survey([q1])
    c = HomogeneousCriterion()
    assert s.set_criterion(c, q2) is False


def test_survey_survey_score_student() -> None:
    """A test for score_student() in class Survey."""
    q1 = YesNoQuestion(1, 'BBC')
    q2 = MultipleChoiceQuestion(2, 'ABC', ['A', 'B', 'C'])
    a1 = Answer(True)
    a2 = Answer('A')
    a3 = Answer(True)
    a4 = Answer('C')
    stu1 = Student(100, 'Jack')
    stu2 = Student(200, 'Mike')
    stu1.set_answer(q1, a1)
    stu1.set_answer(q2, a2)
    stu2.set_answer(q1, a3)
    stu2.set_answer(q2, a4)
    s = Survey([q1, q2])
    c = HomogeneousCriterion()
    s.set_weight(2.0, q1)
    s.set_criterion(c, q1)
    s.set_criterion(c, q2)
    assert s.score_students([stu1, stu2]) == 1.0


def test_survey_survey_score_grouping() -> None:
    """A test for score_grouping() in class Survey."""
    q1 = YesNoQuestion(1, 'BBC')
    q2 = MultipleChoiceQuestion(2, 'ABC', ['A', 'B', 'C'])
    a1 = Answer(True)
    a2 = Answer('A')
    a3 = Answer(True)
    a4 = Answer('C')
    a5 = Answer(True)
    a6 = Answer('B')
    a7 = Answer(False)
    a8 = Answer('C')
    stu1 = Student(100, 'Jack')
    stu2 = Student(200, 'Mike')
    stu3 = Student(300, 'Diana')
    stu4 = Student(400, 'Tom')
    stu1.set_answer(q1, a1)
    stu1.set_answer(q2, a2)
    stu2.set_answer(q1, a3)
    stu2.set_answer(q2, a4)
    stu3.set_answer(q1, a5)
    stu3.set_answer(q2, a6)
    stu4.set_answer(q1, a7)
    stu4.set_answer(q2, a8)
    s = Survey([q1, q2])
    c = HomogeneousCriterion()
    s.set_weight(2.0, q1)
    s.set_criterion(c, q1)
    s.set_criterion(c, q2)
    g1 = Group([stu1, stu2])
    g2 = Group([stu3, stu4])
    grouping = Grouping()
    grouping.add_group(g1)
    grouping.add_group(g2)
    assert s.score_grouping(grouping) == 0.5


"""
    ---------------------------------------------------------
    ------------------ test for criterion.py ----------------
    ---------------------------------------------------------
"""


def test_criterion_homo_score_answer_valid_one() -> None:
    """A test for score_answer() in class HomogeneousCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    c = HomogeneousCriterion()
    assert c.score_answers(q1, [a1]) == 1.0


def test_criterion_homo_score_answer_valid() -> None:
    """A test for score_answer() in class HomogeneousCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(True)
    a3 = Answer(True)
    a4 = Answer(True)
    a5 = Answer(False)
    a6 = Answer(False)
    c = HomogeneousCriterion()
    #    a1 a2 a3 a4 a5 a6
    # a1 NA 1  1  1  0  0
    # a2 1  NA 1  1  0  0
    # a3 1  1  NA 1  0  0
    # a4 1  1  1  NA 0  0
    # a5 0  0  0  0  NA 1
    # a6 0  0  0  0  1  NA
    # score = 0.466666...
    assert 0.46 < c.score_answers(q1, [a1, a2, a3, a4, a5, a6]) < 0.47


def test_criterion_hetero_score_answer_valid_one() -> None:
    """A test for score_answer() in class HeterogeneousCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    c = HeterogeneousCriterion()
    assert c.score_answers(q1, [a1]) == 0.0


def test_criterion_hetero_score_answer_valid() -> None:
    """A test for score_answer() in class HeterogeneousCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(True)
    a3 = Answer(True)
    a4 = Answer(True)
    a5 = Answer(False)
    a6 = Answer(False)
    c = HeterogeneousCriterion()
    #    a1 a2 a3 a4 a5 a6
    # a1 NA 1  1  1  0  0
    # a2 1  NA 1  1  0  0
    # a3 1  1  NA 1  0  0
    # a4 1  1  1  NA 0  0
    # a5 0  0  0  0  NA 1
    # a6 0  0  0  0  1  NA
    # score = 0.533333...
    assert 0.53 < c.score_answers(q1, [a1, a2, a3, a4, a5, a6]) < 0.54


def test_criterion_lonely_score_answer_valid_same() -> None:
    """A test for score_answer() in class LonelyMemberCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(True)
    a3 = Answer(True)
    c = LonelyMemberCriterion()
    assert c.score_answers(q1, [a1, a2, a3]) == 1.0


def test_criterion_lonely_score_answer_valid_different() -> None:
    """A test for score_answer() in class LonelyMemberCriterion."""
    q1 = YesNoQuestion(1, 'ABC')
    a1 = Answer(True)
    a2 = Answer(False)
    a3 = Answer(False)
    c = LonelyMemberCriterion()
    assert c.score_answers(q1, [a1, a2, a3]) == 0.0


"""
    ---------------------------------------------------------
    ------------------- test for grouper.py -----------------
    ---------------------------------------------------------
"""


def test_grouper_slice_list() -> None:
    """A test for helper function slice_list()."""
    assert slice_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_grouper_windows() -> None:
    """A test for helper function windows()."""
    assert windows([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]


def test_grouper_alpha_make_grouping() -> None:
    """A test for make_grouping() in class AlphaGrouper."""
    q = MultipleChoiceQuestion(1, 'abc', ['a'])
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    c = Course('CS')
    c.enroll_students([s3, s4, s2, s1])
    a = AlphaGrouper(2)
    s = Survey([q])
    result = a.make_grouping(c, s).get_groups()
    assert s1 in result[0] and s2 in result[0]
    assert s3 in result[1] and s4 in result[1]


def test_grouper_random_make_grouping() -> None:
    """A test for make_grouping() in class RandomGrouper."""
    q = MultipleChoiceQuestion(1, 'abc', ['a'])
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    c = Course('CS')
    c.enroll_students([s3, s4, s2, s1])
    a = RandomGrouper(2)
    s = Survey([q])
    result = a.make_grouping(c, s).get_groups()
    assert s1 in result[0] or s1 in result[1]
    assert s2 in result[0] or s2 in result[1]
    assert s3 in result[0] or s3 in result[1]
    assert s4 in result[0] or s4 in result[1]


def test_grouper_greedy_make_grouping() -> None:
    """A test for make_grouping() in class GreedyGrouper."""
    q1 = YesNoQuestion(1, 'BBC')
    q2 = MultipleChoiceQuestion(2, 'ABC', ['A', 'B', 'C'])
    a1 = Answer(True)
    a2 = Answer('A')
    a3 = Answer(True)
    a4 = Answer('C')
    a5 = Answer(True)
    a6 = Answer('B')
    a7 = Answer(False)
    a8 = Answer('C')
    stu1 = Student(100, 'Jack')
    stu2 = Student(200, 'Mike')
    stu3 = Student(300, 'Diana')
    stu4 = Student(400, 'Tom')
    stu1.set_answer(q1, a1)
    stu1.set_answer(q2, a2)
    stu2.set_answer(q1, a3)
    stu2.set_answer(q2, a4)
    stu3.set_answer(q1, a5)
    stu3.set_answer(q2, a6)
    stu4.set_answer(q1, a7)
    stu4.set_answer(q2, a8)
    greedy = GreedyGrouper(2)
    survey = Survey([q1, q2])
    course = Course('CS')
    cri = HomogeneousCriterion()
    survey.set_weight(2.0, q1)
    survey.set_criterion(cri, q1)
    survey.set_criterion(cri, q2)
    course.enroll_students([stu1, stu2, stu3, stu4])
    result = greedy.make_grouping(course, survey).get_groups()
    assert stu1 in result[0]
    assert stu2 in result[0]
    assert stu3 in result[1]
    assert stu4 in result[1]


def test_grouper_window_make_grouping() -> None:
    """A test for make_grouping() in class WindowGrouper."""
    q1 = YesNoQuestion(1, 'BBC')
    q2 = MultipleChoiceQuestion(2, 'ABC', ['A', 'B', 'C'])
    a1 = Answer(True)
    a2 = Answer('A')
    a3 = Answer(True)
    a4 = Answer('B')
    a5 = Answer(True)
    a6 = Answer('B')
    a7 = Answer(False)
    a8 = Answer('C')
    stu1 = Student(100, 'Jack')
    stu2 = Student(200, 'Mike')
    stu3 = Student(300, 'Diana')
    stu4 = Student(400, 'Tom')
    stu1.set_answer(q1, a1)
    stu1.set_answer(q2, a2)
    stu2.set_answer(q1, a3)
    stu2.set_answer(q2, a4)
    stu3.set_answer(q1, a5)
    stu3.set_answer(q2, a6)
    stu4.set_answer(q1, a7)
    stu4.set_answer(q2, a8)
    window = WindowGrouper(2)
    survey = Survey([q1, q2])
    course = Course('CS')
    cri = HomogeneousCriterion()
    survey.set_weight(2.0, q1)
    survey.set_criterion(cri, q1)
    survey.set_criterion(cri, q2)
    course.enroll_students([stu1, stu2, stu3, stu4])
    result = window.make_grouping(course, survey).get_groups()
    assert stu1 in result[1]
    assert stu2 in result[0]
    assert stu3 in result[0]
    assert stu4 in result[1]


def test_grouper_group_to_string() -> None:
    """A test for __str__() in class Group."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g = Group([s1, s2, s3, s4])
    assert type(str(g)) is str


def test_grouper_group_len() -> None:
    """A test for __len__() in class Group."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g = Group([s1, s2, s3, s4])
    assert len(g) == 4


def test_grouper_group_contains() -> None:
    """A test for __contains__() in class Group."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g = Group([s1, s2, s3, s4])
    assert s1 in g


def test_grouper_group_get_members() -> None:
    """A test for get_members() in class Group."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g = Group([s1, s2, s3, s4])
    result = g.get_members()
    assert s1 in result
    assert s2 in result
    assert s3 in result
    assert s4 in result


def test_grouper_grouping_to_string() -> None:
    """A test for __str__() in class Grouping."""
    grouping = Grouping()
    assert type(str(grouping)) is str


def test_grouper_grouping_len() -> None:
    """A test for __len__() in class Grouping."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g1 = Group([s1, s2])
    g2 = Group([s3, s4])
    grouping = Grouping()
    grouping.add_group(g1)
    grouping.add_group(g2)
    assert len(grouping) == 2


def test_grouper_grouping_add_group_valid() -> None:
    """A test for add_group() in class Grouping."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g1 = Group([s1, s2])
    g2 = Group([s3, s4])
    grouping = Grouping()
    assert grouping.add_group(g1)
    assert grouping.add_group(g2)


def test_grouper_grouping_add_group_empty() -> None:
    """A test for add_group() in class Grouping."""
    g1 = Group([])
    grouping = Grouping()
    assert grouping.add_group(g1) is False


def test_grouper_grouping_add_group_duplicate() -> None:
    """A test for add_group() in class Grouping."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s4 = Student(4, 'D')
    g1 = Group([s1, s2])
    g2 = Group([s1, s4])
    grouping = Grouping()
    assert grouping.add_group(g1)
    assert grouping.add_group(g2) is False


def test_grouper_grouping_get_groups() -> None:
    """A test for get_groups() in class Grouping."""
    s1 = Student(1, 'A')
    s2 = Student(2, 'B')
    s3 = Student(3, 'C')
    s4 = Student(4, 'D')
    g1 = Group([s1, s2])
    g2 = Group([s3, s4])
    grouping = Grouping()
    grouping.add_group(g1)
    grouping.add_group(g2)
    result = grouping.get_groups()
    assert g1 in result
    assert g2 in result


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])
