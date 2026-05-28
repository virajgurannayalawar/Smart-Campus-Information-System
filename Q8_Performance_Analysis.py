import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

try: 
    df = pd.read_csv("student_performance.csv") 
    print("\n--- Raw Data ---") 
    print(df.head()) 
    
    print("\n--- Statistical Summary ---") 
    print(df.describe()) 
    
    scores = df[["Math", "Science", "English"]].to_numpy() 
     
    mean_scores = np.mean(scores, axis=0) 
    median_scores = np.median(scores, axis=0) 
    std_dev_scores = np.std(scores, axis=0) 
    
    print("\n--- NumPy Analysis ---") 
    print(f"Mean Scores (Math, Science, English): {mean_scores}") 
    print(f"Median Scores (Math, Science, English): {median_scores}") 
    print(f"Standard Deviation (Math, Science, English): {std_dev_scores}") 
    
    top_math = df.loc[df["Math"].idxmax(), "Name"] 
    top_science = df.loc[df["Science"].idxmax(), "Name"] 
    top_english = df.loc[df["English"].idxmax(), "Name"] 
    
    print("\n--- Top Performers ---") 
    print(f"Math: {top_math}") 
    print(f"Science: {top_science}") 
    print(f"English: {top_english}") 
    
    subjects = ["Math", "Science", "English"] 
    plt.bar(subjects, mean_scores, color=["blue", "green", "orange"]) 
    plt.title("Average Scores per Subject") 
    plt.xlabel("Subjects") 
    plt.ylabel("Average Score") 
    plt.show() 
    
    df.plot(x="Name", y=["Math", "Science", "English"], kind="bar") 
    plt.title("Student Performance Comparison") 
    plt.ylabel("Scores") 
    plt.show() 
    
except FileNotFoundError: 
    print("Error: The CSV file was not found. Please check the file path.") 
except Exception as e: 
    print(f"Unexpected Error: {e}") 
