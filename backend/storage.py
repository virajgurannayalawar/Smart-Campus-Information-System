import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent

STUDENTS_FILE = DATA_DIR / "students.csv"
COURSES_FILE = DATA_DIR / "courses.csv"
FEES_FILE = DATA_DIR / "fees.csv"
PERFORMANCE_FILE = DATA_DIR / "performance.csv"

FEE_AMOUNTS = {
    "tuition": 50000,
    "hostel": 30000,
    "transportation": 10000,
}

STUDENT_FIELDS = ["id", "name", "age", "score", "grade", "remark", "events"]
COURSE_FIELDS = ["student_id", "course_name", "credits"]
FEE_FIELDS = ["student_id", "tuition_paid", "hostel_paid", "transportation_paid"]
PERFORMANCE_FIELDS = ["student_id", "name", "Math", "Science", "English"]


def ensure_csv_files():
    create_file(STUDENTS_FILE, STUDENT_FIELDS)
    create_file(COURSES_FILE, COURSE_FIELDS)
    create_file(FEES_FILE, FEE_FIELDS)
    create_file(PERFORMANCE_FILE, PERFORMANCE_FIELDS)


def create_file(path, fieldnames):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def read_rows(path):
    ensure_csv_files()
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_rows(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_grade(score):
    if 90 <= score <= 100:
        return "A", "Excellent"
    if score >= 75:
        return "B", "Very Good"
    if score >= 60:
        return "C", "Good"
    if score >= 40:
        return "D", "Average"
    return "F", "Needs Improvement"


def next_student_id():
    students = read_rows(STUDENTS_FILE)
    if not students:
        return 100
    return max(int(student["id"]) for student in students) + 1


def get_students(event_filter=None):
    students = read_rows(STUDENTS_FILE)
    students.sort(key=lambda student: int(student["id"]))
    if event_filter and event_filter != "All":
        students = [
            student
            for student in students
            if event_filter in split_events(student.get("events", ""))
        ]
    return students


def split_events(events_text):
    return [event.strip() for event in events_text.split(";") if event.strip()]


def all_events():
    events = set()
    for student in read_rows(STUDENTS_FILE):
        events.update(split_events(student.get("events", "")))
    return sorted(events)


def find_student(student_id):
    for student in read_rows(STUDENTS_FILE):
        if int(student["id"]) == student_id:
            return student
    return None


def create_student(name, age, score, events):
    student_id = next_student_id()
    grade, remark = evaluate_grade(score)
    events_text = ";".join(event.strip() for event in events if event.strip())
    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "score": score,
        "grade": grade,
        "remark": remark,
        "events": events_text,
    }

    students = read_rows(STUDENTS_FILE)
    students.append(student)
    write_rows(STUDENTS_FILE, STUDENT_FIELDS, students)

    fees = read_rows(FEES_FILE)
    fees.append(
        {
            "student_id": student_id,
            "tuition_paid": "False",
            "hostel_paid": "False",
            "transportation_paid": "False",
        }
    )
    write_rows(FEES_FILE, FEE_FIELDS, fees)

    performance_rows = read_rows(PERFORMANCE_FILE)
    performance_rows.append(
        {
            "student_id": student_id,
            "name": name,
            "Math": score,
            "Science": score,
            "English": score,
        }
    )
    write_rows(PERFORMANCE_FILE, PERFORMANCE_FIELDS, performance_rows)

    return student


def get_courses(student_id):
    rows = read_rows(COURSES_FILE)
    return [row for row in rows if int(row["student_id"]) == student_id]


def add_course(student_id, course_name, credits):
    if not find_student(student_id):
        raise ValueError("Student ID was not found.")
    if credits <= 0:
        raise ValueError("Credits must be a positive number.")
    courses = get_courses(student_id)
    if len(courses) >= 5:
        raise ValueError("Maximum course limit reached. A student can enroll in 5 courses.")

    rows = read_rows(COURSES_FILE)
    course = {
        "student_id": student_id,
        "course_name": course_name,
        "credits": credits,
    }
    rows.append(course)
    write_rows(COURSES_FILE, COURSE_FIELDS, rows)
    return course


def fee_status(student_id):
    student = find_student(student_id)
    if not student:
        raise ValueError("Student ID was not found.")

    rows = read_rows(FEES_FILE)
    row = next((item for item in rows if int(item["student_id"]) == student_id), None)
    if not row:
        row = {
            "student_id": student_id,
            "tuition_paid": "False",
            "hostel_paid": "False",
            "transportation_paid": "False",
        }
        rows.append(row)
        write_rows(FEES_FILE, FEE_FIELDS, rows)

    items = []
    total_fees = sum(FEE_AMOUNTS.values())
    total_paid = 0
    for fee_name, amount in FEE_AMOUNTS.items():
        paid = row[f"{fee_name}_paid"] == "True"
        if paid:
            total_paid += amount
        items.append({"name": fee_name, "amount": amount, "paid": paid})

    return {
        "student": student,
        "items": items,
        "total_fees": total_fees,
        "total_paid": total_paid,
        "remaining_balance": total_fees - total_paid,
    }


def pay_fees(student_id, selected_fees):
    rows = read_rows(FEES_FILE)
    row = next((item for item in rows if int(item["student_id"]) == student_id), None)
    if row is None:
        raise ValueError("Student fee record was not found.")

    for fee_name in selected_fees:
        if fee_name not in FEE_AMOUNTS:
            raise ValueError(f"Unknown fee type: {fee_name}")
        row[f"{fee_name}_paid"] = "True"

    write_rows(FEES_FILE, FEE_FIELDS, rows)
    return fee_status(student_id)


def upsert_performance(student_id, math, science, english):
    student = find_student(student_id)
    if not student:
        raise ValueError("Student ID was not found.")

    rows = read_rows(PERFORMANCE_FILE)
    row = next((item for item in rows if int(item["student_id"]) == student_id), None)
    if row is None:
        row = {"student_id": student_id, "name": student["name"]}
        rows.append(row)

    row["name"] = student["name"]
    row["Math"] = math
    row["Science"] = science
    row["English"] = english
    write_rows(PERFORMANCE_FILE, PERFORMANCE_FIELDS, rows)
    return row
