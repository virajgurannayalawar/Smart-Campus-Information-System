# Course Enrollment Management System 

courses = []   # list to store (course_name, credits) 
max_courses = 5 
print("=== Course Enrollment System ===") 

while True: 
    if len(courses) >= max_courses: 
        print("Maximum course limit reached!") 
        break 
    course_name = input("Enter course name (or 'done' to finish): ") 
    if course_name.lower() == "done": 
        break 
    credits = input("Enter credit value: ") 
    
    if not credits.isdigit(): 
        print("Invalid credit value! Skipping entry...") 
        continue 
    credits = int(credits) 
    if credits <= 0: 
        print("Credit must be positive! Skipping entry...") 
        continue 
        
    courses.append((course_name, credits)) 
    print(f"Course '{course_name}' with {credits} credits added.\n") 

print("\n--- Enrollment Report ---") 
for course, credit in courses: 
    print(f"Course: {course}, Credits: {credit}") 
print("Total courses enrolled:", len(courses)) 
