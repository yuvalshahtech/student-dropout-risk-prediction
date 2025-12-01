class InvalidAgeError(Exception):
    '''This class is for Invalid age'''
    pass
class InvalidNameError(Exception):
    '''This class is for Invalid name'''
    pass
class InvalidMarksError(Exception):
    '''This class is for Invalid marks'''
    pass
class InvalidChoiceError(Exception):
    '''This class is for Invalid choice'''
    pass

#This function is for deleting a record
def delete_student(students):
    try:
        deleted=False
        delete_name=validate_non_empty(input("Enter name to delete: "))
        for index,item in enumerate(students):
            if item["Name"]==delete_name:
                confirm = input("Are you sure you want to delete? (yes/no): ").lower()
                if confirm == "yes":
                    del students[index]
                    deleted=True
                    break
        if deleted==False:
            print("No such student exists.")
    except InvalidNameError as e:
        print(f"Error: {e}")
        
#This function is for updating a record
def update_student(students):
    try:
        updated=False
        update_name=validate_non_empty(input("Enter name to update marks: "))
        for index,item in enumerate(students):
            if item["Name"]==update_name:
                x=int(input("Enter new marks for the student: "))
                students[index]["Marks"]=validate_marks(x)
                students[index]["GPA"]=calculate_gpa(x)
                updated=True
                break
        if updated==False:
            print("No such student exists.")
    except (InvalidNameError,InvalidMarksError) as e:
        print(f"Error: {e}")
        
#This function is for searching a record
def search_student(students):
    try:
        found=False
        search_name=validate_non_empty(input("Enter name to search: "))
        for index,item in enumerate(students):
            if item["Name"]==search_name:
                for key,value in item.items():
                    print(f"{key}: {value}")
                print("---------------------")
                found=True
                break
        if found==False:
            print("No such student exists.")
    except InvalidNameError as e:
        print(f"Error: {e}")
        
#This function is for viewing all the records
def view_all(students):
    for index,item in enumerate(students):
        print(f"------Student {index+1}------")
        for key,value in item.items():
            print(f"{key}: {value}")
        print("---------------------")
        
#This function is for calculating gpa
def calculate_gpa(marks):
    gpa=marks/10
    return gpa

#This function is for validating marks
def validate_marks(marks):
    if marks<0 or marks>100:
        raise InvalidMarksError("Marks should be from 0-100")
    return marks

#This function is for validating age
def validate_age(age):
    if age<0:
        raise InvalidAgeError("Age cannot be negative")
    return age

#This function is for validating the text is not empty
def validate_non_empty(input_name):
    if input_name.strip() == "":
        raise InvalidNameError("Name cannot be empty")
    return input_name.title()

#This function is for adding a record
def add_student(students):
    try:
        name=validate_non_empty(input("Enter your name: "))
        age=validate_age(int(input("Enter your age: ")))
        subject=validate_non_empty(input("Enter subject name: "))
        marks=validate_marks(int(input(f"Enter your marks in {subject}: ")))
        gpa=calculate_gpa(marks)
        new_student={
        "Name": name,
        "Age": age,
        "Subject": subject,
        "Marks": marks,
         "GPA": gpa
        }
        students.append(new_student)
    except (InvalidAgeError,InvalidNameError,InvalidMarksError) as e:
        print(f"Error: {e}")

#This function is validating the choice
def validate_choice(choice,max_choice):
    if choice<1 or choice>max_choice:
        raise InvalidChoiceError(f"Valid Choices are only 1-{max_choice}")
    return choice