# Program: Sorting and Searching Student IDs 

student_ids = [105, 102, 110, 108, 101, 115] 
print("Original IDs:", student_ids) 

# Bubble Sort 
n = len(student_ids) 
for i in range(n): 
    for j in range(0, n-i-1): 
        if student_ids[j] > student_ids[j+1]: 
            temp = student_ids[j] 
            student_ids[j] = student_ids[j+1] 
            student_ids[j+1] = temp 
print("Sorted IDs (Bubble Sort):", student_ids) 

# Selection Sort 
student_ids2 = [105, 102, 110, 108, 101, 115] 
n = len(student_ids2) 
for i in range(n): 
    min_index = i 
    for j in range(i+1, n): 
        if student_ids2[j] < student_ids2[min_index]: 
            min_index = j 
    temp = student_ids2[i] 
    student_ids2[i] = student_ids2[min_index] 
    student_ids2[min_index] = temp 
print("Sorted IDs (Selection Sort):", student_ids2) 

# Linear Search 
target = 108 
found_index = -1 
for i in range(len(student_ids)): 
    if student_ids[i] == target: 
        found_index = i 
        break 
if found_index != -1: 
    print("Linear Search: ID", target, "found at index", found_index) 
else: 
    print("Linear Search: ID not found") 

# Binary Search 
low = 0 
high = len(student_ids) - 1 
found_index = -1 
while low <= high: 
    mid = (low + high) // 2 
    if student_ids[mid] == target: 
        found_index = mid 
        break 
    elif student_ids[mid] < target: 
        low = mid + 1 
    else: 
        high = mid - 1 
if found_index != -1: 
    print("Binary Search: ID", target, "found at index", found_index) 
else: 
    print("Binary Search: ID not found") 
