import pandas as pd
import os
from datetime import datetime

# === Custom Exceptions ===
class InvalidAgeError(Exception):
    '''Age validation error'''
    pass

class InvalidGPAError(Exception):
    '''GPA validation error'''
    pass

class InvalidStressIndexError(Exception):
    '''Stress index validation error'''
    pass

class InvalidRangeError(Exception):
    '''Range validation error'''
    pass

class InvalidPercentageError(Exception):
    '''Percentage validation error'''
    pass

class InvalidChoiceError(Exception):
    '''Choice validation error'''
    pass

class InvalidInputError(Exception):
    '''General input validation error'''
    pass

# === Validation Functions ===
def validate_age(age):
    """Validate age (must be between 15 and 80)."""
    try:
        age = float(age)
        if age < 15 or age > 80:
            raise InvalidAgeError("Age must be between 15 and 80")
        return age
    except ValueError:
        raise InvalidAgeError("Age must be a valid number")

def validate_gpa(gpa, min_val=0, max_val=4.0):
    """Validate GPA (default 0-4.0 scale)."""
    try:
        gpa = float(gpa)
        if gpa < min_val or gpa > max_val:
            raise InvalidGPAError(f"GPA must be between {min_val} and {max_val}")
        return gpa
    except ValueError:
        raise InvalidGPAError("GPA must be a valid number")

def validate_percentage(value, field_name="Value"):
    """Validate percentage (0-100)."""
    try:
        value = float(value)
        if value < 0 or value > 100:
            raise InvalidPercentageError(f"{field_name} must be between 0 and 100")
        return value
    except ValueError:
        raise InvalidPercentageError(f"{field_name} must be a valid number")

def validate_positive_number(value, field_name="Value", max_val=None):
    """Validate positive number."""
    try:
        value = float(value)
        if value < 0:
            raise InvalidRangeError(f"{field_name} cannot be negative")
        if max_val and value > max_val:
            raise InvalidRangeError(f"{field_name} cannot exceed {max_val}")
        return value
    except ValueError:
        raise InvalidRangeError(f"{field_name} must be a valid number")

def validate_choice(choice, max_choice):
    """Validate menu choice."""
    try:
        choice = int(choice)
        if choice < 1 or choice > max_choice:
            raise InvalidChoiceError(f"Valid choices are 1-{max_choice}")
        return choice
    except ValueError:
        raise InvalidChoiceError("Choice must be a valid number")
    
def validate_stress_index(value):
    """Validate stress index (0-10)."""
    try:
        value = float(value)
        if value < 0 or value > 10:
            raise InvalidStressIndexError("Stress Index must be between 0 and 10")
        return value
    except ValueError:
        raise InvalidStressIndexError("Stress Index must be a valid number")

def validate_select(value, valid_options, field_name="Option"):
    """Validate selection from list (case and spacing insensitive)."""
    value = value.strip().lower()
    normalized_options = [opt.lower() for opt in valid_options]
    if value not in normalized_options:
        raise InvalidChoiceError(f"{field_name} must be one of {valid_options}")
    return value

# === Data Collection Function ===
def collect_student_data():
    """Collect student data interactively (matching Streamlit fields)."""
    print("\n" + "="*60)
    print("📋 STUDENT DROPOUT RISK PREDICTION - DATA ENTRY")
    print("="*60)
    
    data = {}
    
    try:
        # === ACADEMIC TAB ===
        print("\n📘 ACADEMIC INFORMATION")
        print("-" * 40)
        data["Age"] = validate_age(input("Enter Age (15-80): "))
        data["GPA"] = validate_gpa(input("Enter GPA (0-4.0): "))
        data["CGPA"] = validate_gpa(input("Enter CGPA (0-4.0): "))
        data["Semester_GPA"] = validate_gpa(input("Enter Semester GPA (0-4.0): "))
        data["Study_Hours_per_Day"] = validate_positive_number(
            input("Enter Study Hours Per Day: "), "Study Hours"
        )
        data["Assignment_Delay_Days"] = validate_positive_number(
            input("Enter Assignment Delay Days: "), "Assignment Delay Days"
        )
        data["Attendance_Rate"] = validate_percentage(
            input("Enter Attendance Rate (0-100%): "), "Attendance Rate"
        )
        data["Travel_Time_Minutes"] = validate_positive_number(
            input("Enter Travel Time (Minutes): "), "Travel Time"
        )
        
        # === ENVIRONMENT TAB ===
        print("\n🌍 ENVIRONMENTAL & SOCIOECONOMIC INFORMATION")
        print("-" * 40)
        data["Family_Income"] = validate_positive_number(
            input("Enter Family Income: "), "Family Income"
        )
        data["Internet_Access"] = validate_select(
            input("Internet Access (Yes/No): ").strip().capitalize(),
            ["Yes", "No"],
            "Internet Access"
        )
        data["Scholarship"] = validate_select(
            input("Has Scholarship (Yes/No): ").strip().capitalize(),
            ["Yes", "No"],
            "Scholarship"
        )
        data["Part_Time_Job"] = validate_select(
            input("Has Part Time Job (Yes/No): ").strip().capitalize(),
            ["Yes", "No"],
            "Part Time Job"
        )
        data["Stress_Index"] = validate_stress_index(
            input("Enter Stress Index (0-10.0): ")
        )
        
        # === INSTITUTION TAB ===
        print("\n🏫 INSTITUTIONAL INFORMATION")
        print("-" * 40)
        data["Semester"] = validate_select(
            input("Select Semester (Year 1/Year 2/Year 3/Year 4): "),
            ["Year 1", "Year 2", "Year 3", "Year 4"],
            "Semester"
        )
        data["Department"] = validate_select(
            input("Select Department (Science/Arts/Business/CS/Engineering): "),
            ["Science", "Arts", "Business", "CS", "Engineering"],
            "Department"
        )
        data["Parental_Education"] = validate_select(
            input("Parental Education (High School/Bachelor/Master/PhD): ").strip().lower(),
            ["High School", "Bachelor", "Master", "PhD"],
            "Parental Education"
        )
        
        data["Timestamp"] = datetime.now().isoformat()

        return data
        
    except (InvalidAgeError, InvalidGPAError, InvalidRangeError, InvalidStressIndexError,
            InvalidPercentageError, InvalidChoiceError, InvalidInputError) as e:
        print(f"\n❌ Error: {e}")
        return None

# === Display & Approval Function ===
def display_and_approve(data):
    """Display collected data and ask for approval before saving."""
    if data is None:
        return False
    
    print("\n" + "="*60)
    print("📊 REVIEW YOUR DATA")
    print("="*60)
    
    for key, value in data.items():
        if key != "Timestamp":
            print(f"  {key:.<30} {value}")
    print(f"  {'Timestamp':.<30} {data['Timestamp']}")
    
    print("\n" + "-"*60)
    while True:
        confirm = input("Approve and save this data? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            return True
        elif confirm in ["no", "n"]:
            print("❌ Data entry cancelled.")
            return False
        else:
            print("⚠️  Please enter 'yes' or 'no'")

# === CSV Management Function ===
def save_to_cli_data(data):
    """Save collected data to data/cli_data.csv."""
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "cli_data.csv")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Load existing data or create new
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Create with expected columns
        df = pd.DataFrame()
    
    # Convert single record to DataFrame and append
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    print(f"✅ Data saved to {csv_path}")
    return True

# === View Saved Data Function ===
def view_saved_data():
    """View all saved CLI data."""
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "cli_data.csv")
    
    if not os.path.exists(csv_path):
        print("❌ No saved data found.")
        return
    
    df = pd.read_csv(csv_path)
    print("\n" + "="*60)
    print(f"📊 SAVED DATA ({len(df)} records)")
    print("="*60)
    print(df.to_string(index=False))
    print("="*60)