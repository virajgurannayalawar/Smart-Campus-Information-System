# Student Registration and Grade Evaluation

student_name = input("Enter student name: ")                  
score = float(input("Enter exam score (0-100): ")) 

if score >= 90 and score <= 100: 
    grade = "A" 
    remark = "Excellent" 
elif score >= 75: 
    grade = "B" 
    remark = "Very Good" 
elif score >= 60: 
    grade = "C" 
    remark = "Good" 
elif score >= 40: 
    grade = "D" 
    remark = "Average" 
else: 
    grade = "F" 
    remark = "Needs Improvement" 

print("\n--- Student Report ---") 
print("Name:", student_name) 
print("Score:", score) 
print("Grade:", grade) 
print("Performance Remark:", remark) 
