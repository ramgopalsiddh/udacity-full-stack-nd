import pytest
from source.school import Classroom, Teacher, Student, ToManyStudents

# Define fixtures
@pytest.fixture
def harry_potter_teacher():
    return Teacher("Harry Potter")

@pytest.fixture
def potion_classroom(harry_potter_teacher):
    students = [Student(f"Student_{i}") for i in range(10)]
    return Classroom(harry_potter_teacher, students, "Potion Class")

# Test adding students to the classroom
@pytest.mark.parametrize("num_students", [1, 5, 10])
def test_add_students_to_classroom(potion_classroom, num_students):
    new_students = [Student(f"New_Student_{i}") for i in range(num_students)]
    for student in new_students:
        try:
            potion_classroom.add_student(student)
        except ToManyStudents:
            assert len(potion_classroom.students) == 10
            break
    else:
        assert len(potion_classroom.students) == num_students + len(potion_classroom.students)


# Test adding too many students to the classroom
def test_add_too_many_students_to_classroom(potion_classroom):
    with pytest.raises(ToManyStudents):
        for i in range(15):
            potion_classroom.add_student(Student(f"New_Student_{i}"))

# Test removing a student from the classroom
def test_remove_student_from_classroom(potion_classroom):
    student_to_remove = potion_classroom.students[0]
    potion_classroom.remove_student(student_to_remove.name)
    assert student_to_remove not in potion_classroom.students

# Test changing the teacher of the classroom
def test_change_teacher_of_classroom(potion_classroom):
    new_teacher = Teacher("Severus Snape")
    potion_classroom.change_teacher(new_teacher)
    assert potion_classroom.teacher == new_teacher
