import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def api_get(path, default=None):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        st.error(f"API request failed: {error}")
        return default


def api_post(path, payload):
    try:
        response = requests.post(f"{API_URL}{path}", json=payload, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.HTTPError:
        return None, response.json().get("detail", "Request failed")
    except requests.RequestException as error:
        return None, str(error)


def student_options(students):
    return {
        f'{student["id"]} - {student["name"]}': int(student["id"])
        for student in students
    }


st.set_page_config(page_title="Smart Campus Lab", layout="wide")
st.title("Smart Campus Information System")
st.caption("FastAPI backend + Streamlit frontend + CSV file storage")

tabs = st.tabs(
    [
        "Register New Student",
        "Course Enrollment",
        "Student Records",
        "Fees Section",
        "Performance",
    ]
)

with tabs[0]:
    st.subheader("Register New Student")
    with st.form("student_registration", clear_on_submit=True):
        name = st.text_input("Student name")
        age = st.number_input("Age", min_value=1, max_value=100, value=18)
        score = st.number_input("Exam score", min_value=0.0, max_value=100.0, value=75.0)
        events_text = st.text_input("Events participated in", placeholder="Hackathon, Sports Day")
        submitted = st.form_submit_button("Register")

    if submitted:
        events = [event.strip() for event in events_text.split(",") if event.strip()]
        result, error = api_post(
            "/students",
            {"name": name, "age": age, "score": score, "events": events},
        )
        if error:
            st.error(error)
        else:
            st.success(
                f'Registered {result["name"]} with Student ID {result["id"]}. '
                f'Grade: {result["grade"]}, Remark: {result["remark"]}'
            )

with tabs[1]:
    st.subheader("Course Enrollment")
    students = api_get("/students", [])
    options = student_options(students)

    if not options:
        st.info("Register a student before adding courses.")
    else:
        selected_label = st.selectbox("Student", list(options.keys()))
        selected_id = options[selected_label]

        with st.form("course_enrollment", clear_on_submit=True):
            course_name = st.text_input("Course name")
            credits = st.number_input("Credits", min_value=1, max_value=10, value=3)
            submitted = st.form_submit_button("Add Course")

        if submitted:
            result, error = api_post(
                "/courses",
                {
                    "student_id": selected_id,
                    "course_name": course_name,
                    "credits": credits,
                },
            )
            if error:
                st.error(error)
            else:
                st.success(f'Added {result["course_name"]} ({result["credits"]} credits).')

        courses = api_get(f"/courses/{selected_id}", [])
        if courses:
            st.dataframe(pd.DataFrame(courses), use_container_width=True, hide_index=True)
        else:
            st.info("No courses enrolled yet. Maximum allowed courses: 5.")

with tabs[2]:
    st.subheader("Student Records")
    events = api_get("/events", ["All"])
    event_filter = st.selectbox("Filter by event participation", events)
    students = api_get(f"/students?event={event_filter}", [])

    if students:
        records = pd.DataFrame(students)
        records["id"] = records["id"].astype(int)
        records = records.sort_values("id")
        selected_name = st.selectbox("Select a student", records["name"].tolist())
        st.dataframe(records, use_container_width=True, hide_index=True)
        st.write("Selected student")
        st.json(records[records["name"] == selected_name].iloc[0].to_dict())
    else:
        st.info("No matching student records found.")

with tabs[3]:
    st.subheader("Fees Section")
    students = api_get("/fees", [])
    options = student_options(students)

    if not options:
        st.info("Register a student before viewing fees.")
    else:
        selected_label = st.selectbox("Student name", list(options.keys()), key="fee_student")
        selected_id = options[selected_label]
        fee_status = api_get(f"/fees/{selected_id}", {})

        if fee_status:
            fee_items = fee_status["items"]
            selectable = [
                item for item in fee_items if not item["paid"]
            ]
            st.write(f'Total fees: Rs. {fee_status["total_fees"]:,}')
            st.write(f'Total paid: Rs. {fee_status["total_paid"]:,}')
            st.write(f'Remaining balance: Rs. {fee_status["remaining_balance"]:,}')

            selected_fees = []
            for item in fee_items:
                label = f'{item["name"].title()} - Rs. {item["amount"]:,}'
                if item["paid"]:
                    st.checkbox(label, value=True, disabled=True)
                else:
                    checked = st.checkbox(label, key=f'fee_{selected_id}_{item["name"]}')
                    if checked:
                        selected_fees.append(item["name"])

            selected_total = sum(
                item["amount"] for item in selectable if item["name"] in selected_fees
            )
            st.info(f"Selected payment total: Rs. {selected_total:,}")

            if st.button("Pay", disabled=not selected_fees):
                result, error = api_post(
                    "/fees/pay",
                    {"student_id": selected_id, "selected_fees": selected_fees},
                )
                if error:
                    st.error(error)
                else:
                    st.success(
                        f'Payment saved. Remaining balance: Rs. {result["remaining_balance"]:,}'
                    )
                    st.rerun()

with tabs[4]:
    st.subheader("Performance")
    students = api_get("/students", [])
    options = student_options(students)

    if options:
        selected_label = st.selectbox("Student", list(options.keys()), key="performance_student")
        selected_id = options[selected_label]
        with st.form("performance_form"):
            math = st.number_input("Math", min_value=0.0, max_value=100.0, value=75.0)
            science = st.number_input("Science", min_value=0.0, max_value=100.0, value=75.0)
            english = st.number_input("English", min_value=0.0, max_value=100.0, value=75.0)
            submitted = st.form_submit_button("Save Performance")

        if submitted:
            result, error = api_post(
                "/performance",
                {
                    "student_id": selected_id,
                    "math": math,
                    "science": science,
                    "english": english,
                },
            )
            if error:
                st.error(error)
            else:
                st.success("Performance marks saved.")
    else:
        st.info("Register students before entering performance marks.")

    performance = api_get("/performance", {})
    if performance and performance.get("records"):
        records = pd.DataFrame(performance["records"])
        st.dataframe(records, use_container_width=True, hide_index=True)

        subjects = ["Math", "Science", "English"]
        averages = records[subjects].astype(float).mean()
        st.bar_chart(averages)

        col1, col2 = st.columns(2)
        with col1:
            st.write("NumPy Analysis")
            st.json(performance["numpy_analysis"])
        with col2:
            st.write("Top Performers")
            st.json(performance["top_performers"])
    else:
        st.info("No performance records available yet.")
