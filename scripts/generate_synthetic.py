import json, csv, os, random

#Generate Synthetic Student Data
def generate_students(n=200):
    genders = ["M", "F"]
    courses = ["Maths", "AI", "ML", "DBMS", "DSA"]
    notes_list = [
        "Consistent performer",
        "Needs improvement in assignments",
        "Excellent attendance",
        "Weak in theory subjects",
        "Strong in practicals"
    ]
    students = []

    for i in range(1, n+1):
        course_history = random.sample(courses, random.randint(2, 5))
        assignment_scores = [random.randint(40, 100) for _ in range(5)]

        student = {
            "student_id": i,
            "age": round(random.normalvariate(21, 3), 1),
            "gender": random.choice(genders),
            "attendance_pct": round(random.uniform(40, 100), 1),
            "course_history": json.dumps(course_history),
            "assignment_scores": json.dumps(assignment_scores),
            "final_grade": random.choice(["A", "B", "C", "D", "F"]),
            "notes": random.choice(notes_list)
        }

        #Inject Missing Values
        if random.random() < 0.08:
            student["notes"] = None

        students.append(student)
    return students
    
#Saving to CSV
def save_to_csv(data, path="data/sample_students.csv"):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} rows into {path}")

if __name__=="__main__":
    data = generate_students()
    save_to_csv(data)