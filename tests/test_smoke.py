"""The dependency is installed and can actually build and solve a model."""

from timetable.smoke import COURSES, SLOTS, solve_smoke


def test_the_toy_case_is_solved():
    result = solve_smoke()

    assert result.status_name == "OPTIMAL"
    assert result.solved


def test_every_course_gets_exactly_one_slot():
    result = solve_smoke()

    assert set(result.assignment) == set(COURSES)
    assert all(slot in SLOTS for slot in result.assignment.values())


def test_two_courses_never_share_the_one_room():
    result = solve_smoke()

    slots = list(result.assignment.values())
    assert len(set(slots)) == len(slots)


def test_more_courses_than_slots_is_reported_infeasible_not_raised():
    # Three courses, two slots, one room. Nothing to find, and the point is that
    # this comes back as a status rather than an exception.
    result = solve_smoke(courses=("maths", "physics", "chemistry"), slots=(0, 1))

    assert result.status_name == "INFEASIBLE"
    assert not result.solved
    assert result.assignment == {}
