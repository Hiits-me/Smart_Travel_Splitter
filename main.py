from models import Trip
from calculator import calculate_settlements, format_settlement_summary

BANNER = '''
    =========================================
    ✈️  Smart Travel Splitter (CLI MVP)
    =========================================
    Bill splitting, without the confusion.
'''

def show_menu():
    """Display the main menu options"""
    menu = '''
    Options:
    1. List members
    2. Add a member
    3. Remove a member
    4. List all payments
    5. Record payment
    6. Edit payment
    7. Delete payment
    8. Calculate & settle
    9. Exit
    '''
    print(menu)

def valid_input(prompt, input_type=str, allow_empry=False):
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and not allow_empry:
                print("Input cannot be empty. Please try again.")
                continue
            if not user_input and allow_empry:
                return user_input
                
            if input_type is int:
                return int(user_input)
            elif input_type is float:
                return float(user_input)
            else:
                return
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def main():
    print(BANNER)

    trip_name = input("Group name (or press Enter for 'My Trip'): ").strip()
    trip = Trip(trip_name or 'My Trip')
    print(f"\n✅ Trip '{trip_name}' created!\n")

    while True:
        show_menu()
        try:
            option = valid_input("Select an option (1-9): ", input_type = int)
            print()

            match option:
                case 1:
                    trip.list_members()
                    print()
                
                case 2:
                    name = valid_input("Enter member name: ")
                    trip.add_member(name)
                    print()

                case 3:
                    trip.list_members()
                    print()
                    name = valid_input("Enter name of member to remove: ")
                    trip.remove_member(name)
                
                # case 4:
                
                # case 5:
                
                # case 6:

                # case 7:
                
                # case 8:
                
                case 9:
                    print("Thanks for using Smart Travel Splitter! See you mate👋")
                    break
                
                case _:
                    print('Invalid option. Please select1-9.\n')

        except KeyboardInterrupt:
            print("\n\nExiting... Thanks for using Smart Travel Splitter!👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == '__main__':
    main()