students = []

# This function is for displaying the menu
def display():
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student by Name")
    print("4. Update Student Marks")
    print("5. Delete Student")
    print("6. Exit")


# Main function (single definition)
def main():
    max_choice = 6
    # import core functions here, only when running main
    from .core import add_student, view_all, search_student, update_student, delete_student, validate_choice

    while True:
        try:
            display()
            choice = int(input("Enter your choice: "))
            choice = validate_choice(choice, max_choice)

            if choice == 1:
                add_student(students)
            elif choice == 2:
                if len(students) == 0:
                    print("Database is Empty")
                else:
                    view_all(students)
            elif choice == 3:
                search_student(students)
            elif choice == 4:
                update_student(students)
            elif choice == 5:
                delete_student(students)
            else:  # choice == 6
                confirm = input("Are you sure you want to exit? (yes/no): ").lower()
                if confirm == "yes":
                    print("Thank You for using Student Manager System")
                    break

        except Exception as e:
            print(f"Error: {e}")


# Only run when executed as a script/module
if __name__ == "__main__":
    main()
