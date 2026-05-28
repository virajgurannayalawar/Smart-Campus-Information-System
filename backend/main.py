from typing import List

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import storage

app = FastAPI(title="Smart Campus Lab API")
storage.ensure_csv_files()


class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0)
    score: float = Field(ge=0, le=100)
    events: List[str] = []


class CourseCreate(BaseModel):
    student_id: int
    course_name: str = Field(min_length=1)
    credits: int = Field(gt=0)


class FeePayment(BaseModel):
    student_id: int
    selected_fees: List[str]


class PerformanceUpdate(BaseModel):
    student_id: int
    math: float = Field(ge=0, le=100)
    science: float = Field(ge=0, le=100)
    english: float = Field(ge=0, le=100)


@app.get("/")
def home():
    return {"message": "Smart Campus Lab API is running"}


@app.post("/students")
def register_student(student: StudentCreate):
    return storage.create_student(student.name, student.age, student.score, student.events)


@app.get("/students")
def list_students(event: str = "All"):
    return storage.get_students(event_filter=event)


@app.get("/events")
def list_events():
    return ["All"] + storage.all_events()


@app.post("/courses")
def enroll_course(course: CourseCreate):
    try:
        return storage.add_course(course.student_id, course.course_name, course.credits)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/courses/{student_id}")
def list_courses(student_id: int):
    return storage.get_courses(student_id)


@app.get("/fees")
def list_fee_students():
    return storage.get_students()


@app.get("/fees/{student_id}")
def get_fee_status(student_id: int):
    try:
        return storage.fee_status(student_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.post("/fees/pay")
def make_fee_payment(payment: FeePayment):
    try:
        return storage.pay_fees(payment.student_id, payment.selected_fees)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/performance")
def save_performance(performance: PerformanceUpdate):
    try:
        return storage.upsert_performance(
            performance.student_id,
            performance.math,
            performance.science,
            performance.english,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/performance")
def performance_summary():
    rows = storage.read_rows(storage.PERFORMANCE_FILE)
    if not rows:
        return {"records": [], "summary": {}, "numpy_analysis": {}, "top_performers": {}}

    df = pd.DataFrame(rows)
    subjects = ["Math", "Science", "English"]
    df[subjects] = df[subjects].astype(float)
    scores = df[subjects].to_numpy()

    top_performers = {
        subject: df.loc[df[subject].idxmax(), "name"]
        for subject in subjects
    }

    mean_scores = np.mean(scores, axis=0).round(2).tolist()
    median_scores = np.median(scores, axis=0).round(2).tolist()
    std_scores = np.std(scores, axis=0).round(2).tolist()

    return {
        "records": df.to_dict(orient="records"),
        "summary": df[subjects].describe().round(2).to_dict(),
        "numpy_analysis": {
            "mean": dict(zip(subjects, mean_scores)),
            "median": dict(zip(subjects, median_scores)),
            "standard_deviation": dict(zip(subjects, std_scores)),
        },
        "top_performers": top_performers,
    }
