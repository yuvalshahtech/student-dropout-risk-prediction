from .core import (
    collect_student_data,
    display_and_approve,
    save_to_cli_data,
    view_saved_data,
    validate_choice
)

def display_menu():
    """Display the CLI menu."""
    print("\n" + "="*60)
    print("🎓 STUDENT MANAGEMENT SYSTEM - CLI")
    print("="*60)
    print("1. ➕  Add New Student (for Dropout Prediction)")
    print("2. 👀  View All Saved Students")
    print("3. 🚪  Exit")
    print("="*60)

def main():
    """Main CLI loop."""
    print("\n🎯 Welcome to Student Management System!")
    print("   Select an option below to get started...")
    
    while True:
        try:
            display_menu()
            choice = int(input("Enter your choice (1-3): "))
            choice = validate_choice(choice, 3)
            
            if choice == 1:
                # Collect student data
                data = collect_student_data()
                
                if data is not None:
                    # Show preview and ask for approval
                    if display_and_approve(data):
                        # Save to CSV
                        save_to_cli_data(data)
                    else:
                        print("ℹ️  Entry discarded.")
            
            elif choice == 2:
                # View saved data
                view_saved_data()
            
            elif choice == 3:
                # Exit
                confirm = input("\nAre you sure you want to exit? (yes/no): ").strip().lower()
                if confirm in ["yes", "y"]:
                    print("\n✅ Thank you for using Student Management System!")
                    print("   Goodbye! 👋\n")
                    break
        
        except ValueError:
            print("❌ Please enter a valid number")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

# Only run when executed as a script/module
if __name__ == "__main__":
    main()
