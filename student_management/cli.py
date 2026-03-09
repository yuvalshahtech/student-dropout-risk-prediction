from colorama import init, Fore, Style

from .core import (
    collect_student_data,
    display_and_approve,
    save_to_cli_data,
    view_saved_data,
    validate_choice
)

init(autoreset=True)

# Terminal icon set (ASCII-safe, CI-compatible)
ICO_OK = f"{Fore.GREEN}{Style.BRIGHT}[*]{Style.RESET_ALL}"
ICO_ERR = f"{Fore.RED}{Style.BRIGHT}[x]{Style.RESET_ALL}"
ICO_INFO = f"{Fore.CYAN}{Style.BRIGHT}[i]{Style.RESET_ALL}"
ICO_WARN = f"{Fore.YELLOW}{Style.BRIGHT}[!]{Style.RESET_ALL}"
ICO_ADD = f"{Fore.GREEN}{Style.BRIGHT}[+]{Style.RESET_ALL}"
ICO_VIEW = f"{Fore.CYAN}{Style.BRIGHT}[>]{Style.RESET_ALL}"
ICO_EXIT = f"{Fore.YELLOW}{Style.BRIGHT}[-]{Style.RESET_ALL}"
ICO_APP = f"{Fore.CYAN}{Style.BRIGHT}[#]{Style.RESET_ALL}"


def display_menu():
    """Display the CLI menu."""
    print("\n" + "="*60)
    print(f"  {ICO_APP} {Fore.CYAN}{Style.BRIGHT}STUDENT DROPOUT RISK PREDICTION{Style.RESET_ALL}")
    print("="*60)
    print(f"  1. {ICO_ADD}  Add New Student (for Dropout Prediction)")
    print(f"  2. {ICO_VIEW}  View All Saved Students")
    print(f"  3. {ICO_EXIT}  Exit")
    print("="*60)

def main():
    """Main CLI loop."""
    print(f"\n  {ICO_APP} {Fore.CYAN}{Style.BRIGHT}Welcome to Student Dropout Risk Prediction{Style.RESET_ALL}")
    print("      Select an option below to get started...")
    
    while True:
        try:
            display_menu()
            choice = int(input("  Enter your choice (1-3): "))
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
                        print(f"  {ICO_INFO} Entry discarded.")
            
            elif choice == 2:
                # View saved data
                view_saved_data()
            
            elif choice == 3:
                # Exit
                confirm = input("\n  Are you sure you want to exit? (yes/no): ").strip().lower()
                if confirm in ["yes", "y"]:
                    print(f"\n  {ICO_OK} Thank you for using Student Dropout Risk Prediction!")
                    print("      Goodbye!\n")
                    break
        
        except ValueError:
            print(f"  {ICO_ERR} Please enter a valid number")
        except Exception as e:
            print(f"  {ICO_ERR} An error occurred: {e}")

# Only run when executed as a script/module
if __name__ == "__main__":
    main()
