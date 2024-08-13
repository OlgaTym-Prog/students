from typing import List, Dict


class Student:

    def __init__(self, name: str, surname: str, gender: str):
        self.name: str = name
        self.surname: str = surname
        self.gender: str = gender
        self.finished_courses: List[str] = []
        self.courses_in_progress: List[str] = []
        self.grades: Dict[str, List[int]] = {}

    # Метод выставления оценок лекторам
    def rate_lecturer(self, lecturer: 'Lecturer', course: str, grade: int) -> None:
        try:
            if (isinstance(lecturer, Lecturer) and course in self.courses_in_progress
                    and course in lecturer.courses_attached):
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                raise ValueError('Лектор не прикреплен к этому курсу или студент не изучает этот курс')
        except Exception as ex:
            print(f'Ошибка: {ex}')

    # Средняя оцнека
    def _rate_average(self) -> float:
        total_grades = sum(sum(grades) for grades in self.grades.values())
        count_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / count_grades if count_grades != 0 else 0.0

    def __str__(self) -> str:
        return (f"Имя: {self.name}\nФамилия: {self.surname}"
                f"\nСредняя оценка за лекции: {self._rate_average()}"
                f"\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}"
                f"\nЗавершенные курсы: {', '.join(self.finished_courses)}")

    def __eq__(self, other: 'Student') -> bool:
        return self._rate_average() == other._rate_average()

    def __lt__(self, other: 'Student') -> bool:
        return self._rate_average() < other._rate_average()

    def __gt__(self, other: 'Student') -> bool:
        return self._rate_average() > other._rate_average()


class Mentor:

    def __init__(self, name: str, surname: str):
        self.name: str = name
        self.surname: str = surname
        self.courses_attached: List[str] = []


class Lecturer(Mentor):

    def __init__(self, name: str, surname: str):
        super().__init__(name, surname)
        self.grades: Dict[str, List[int]] = {}

    def _rate_average(self) -> float:
        total_grades = sum(sum(grades) for grades in self.grades.values())
        count_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / count_grades if count_grades != 0 else 0.0

    def __str__(self) -> str:
        return (f"Имя: {self.name}\nФамилия: {self.surname}"
                f"\nСредняя оценка за лекции: {self._rate_average()}")

    def __eq__(self, other: 'Lecturer') -> bool:
        return self._rate_average() == other._rate_average()

    def __lt__(self, other: 'Lecturer') -> bool:
        return self._rate_average() < other._rate_average()

    def __gt__(self, other: 'Lecturer') -> bool:
        return self._rate_average() > other._rate_average()


class Reviewer(Mentor):

    def rate_hw(self, student: Student, course: str, grade: int) -> None:
        try:
            if (isinstance(student, Student) and course in self.courses_attached
                    and course in student.courses_in_progress):
                if course in student.grades:
                    student.grades[course] += [grade]
                else:
                    student.grades[course] = [grade]
            else:
                raise ValueError('Студент не изучает этот курс или курс не привязан к рецензенту')
        except Exception as ex:
            print(f'Ошибка: {ex}')

    def __str__(self) -> str:
        return f"Имя: {self.name}\nФамилия: {self.surname}"


#  Функция для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса
def average_grade_for_course(students: List[Student], course: str) -> float:
    total_grades = 0
    count_grades = 0
    for student in students:
        if course in student.grades:
            total_grades += sum(student.grades[course])
            count_grades += len(student.grades[course])
    return total_grades / count_grades if count_grades != 0 else 0.0


# Функция для подсчета средней оценки за лекции всех лекторов в рамках курса
def average_lecture_grade_for_course(lecturers: List[Lecturer], course: str) -> float:
    total_grades = 0
    count_grades = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades += sum(lecturer.grades[course])
            count_grades += len(lecturer.grades[course])
    return total_grades / count_grades if count_grades != 0 else 0.0


student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Bob', 'Smith', 'male')
student2.courses_in_progress += ['Python']
student2.finished_courses += ['Введение в программирование']

lecturer1 = Lecturer('Lola', 'Johns')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Olga', 'Green')
lecturer2.courses_attached += ['Python']

reviewer1 = Reviewer('Paola', 'Hooks')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Molly', 'Hooks')
reviewer2.courses_attached += ['Python']

# Выставление оценок студентам
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 4)
reviewer1.rate_hw(student1, 'Python', 9)

reviewer2.rate_hw(student2, 'Python', 5)
reviewer2.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 8)

# Выставление оценок лекторам
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)

student2.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Python', 9)
student2.rate_lecturer(lecturer2, 'Python', 6)


print(student1.grades)
print(student2.grades)

print(lecturer1.grades)
print(lecturer2.grades)

# Красивый вывод
print(reviewer1)
print(lecturer1)
print(student1)
print(reviewer2)
print(lecturer2)
print(student2)

# Сравнение студентов
print(student1 == student2)
print(student1 < student2)
print(student1 > student2)

# Сравнение лекторов
print(lecturer1 == lecturer2)
print(lecturer1 < lecturer2)
print(lecturer1 > lecturer2)

# Подсчет средней оценки за домашние задания по всем студентам на курсе "Python"
students = [student1, student2]
average_hw_grade = average_grade_for_course(students, 'Python')
print(f"Средняя оценка у студентов на курсе Python: {average_hw_grade}")

# Подсчет средней оценки за лекции по всем лекторам на курсе "Python"
lecturers = [lecturer1, lecturer2]
average_lecturer_grade = average_lecture_grade_for_course(lecturers, 'Python')
print(f"Средняя оценка у лекторов на курсе Python: {average_lecturer_grade}")
