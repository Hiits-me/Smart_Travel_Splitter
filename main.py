from models import Trip
from calculator import calculate_settlements, format_settlement_summary
import pyperclip

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
    5. Add payment
    6. Edit payment
    7. Delete payment
    8. Calculate & settle
    9. Exit
    '''
    print(menu)

def valid_input(prompt, input_type=str, allow_empty=False) -> str|int|float:
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and not allow_empty:
                print("Input cannot be empty. Please try again.")
                continue
            if not user_input and allow_empty:
                return user_input
                
            if input_type is int:
                if int(user_input) <= 0:
                    print("Input cannot be negative. Please input positive number.")
                    continue
                return int(user_input)
            
            elif input_type is float:
                if float(user_input) <= 0:
                    print("Input cannot be negative. Please input positive number.")
                    continue
                return float(user_input)
            else:
                return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
    

def handle_add_payment(trip) -> None:
    if not trip.members:
        print('No members in this group. Add a member first.\n')
        return
    payer = valid_input("Payer: ")
    amount = valid_input("Amount: $", input_type=float)
    description = valid_input("Description: ", input_type=str, allow_empty=True)
    split_choice = valid_input("Split among specific members? (y/n): ").lower()

    involved = None
    if split_choice == 'y':
        print("Enter member names separated by commas (or press Enter for all): ")
        involved_input = input().strip()
        if involved_input:
            involved = [name.strip() for name in involved_input.split(',')]
    try:
        trip.add_payment(payer, amount, description, involved)
    except ValueError as e:
        print(f"Error: {e}")


def handle_edit_payment(trip) -> None:
    if not trip.payments:
        print("No payments to edit.\n")
    trip.list_payments()
    print()

    payment_id = valid_input("Enter payment ID to edit: ", input_type=int)
    payment_to_edit = trip.search_payment(payment_id)
    if payment_to_edit is None:
        return
    
    print("Leave blank to keep current value.")
    new_amount = input("New amount (or press Enter to skip): ").strip()
    try:
        new_amount = float(new_amount) if new_amount else None
    except ValueError:
        print('Invalid amount. Please enter number.')
    
    new_description = input("New description (or press Enter to skip): ").strip()
    edit_members_choice = valid_input("Edit involved members? (y/n): ", allow_empty=True).lower()
    new_involved = None
    if edit_members_choice == 'y':
        print(f"Current members in trip: {', '.join(trip.members.keys())}")
        print("Enter member names separated by commas:")
        involved_input = input().strip()
        if involved_input:
            new_involved = [name.strip() for name in involved_input.split(',')]

    
    trip.edit_payment(payment_id, new_amount, new_description, new_involved)
    print()


def handle_delete_payment(trip) -> None:
    if not trip.payments:
        print("No payments to delete.\n")
    trip.list_payments()
    print()

    payment_id = valid_input("Enter payment ID to delete: ", input_type=int)
    trip.delete_payment(payment_id)
    print()


def handle_settlement(trip) -> None:
    if not trip.payments:
        print("No payments recorded yet.")
        return
    print("\n" + "=" * 50, "Settletment Summary", "=" * 50,  sep='\n')

    avg_per_person = trip.calculate_balances()
    total_spent = sum(p.amount for p in trip.payments)

    print(f"\nTotal spent: ${total_spent:.2f}", f"Per person (if all shared): ${avg_per_person:.2f}", "\nResult:", sep='\n')
    
    # Build the result text for clipboard
    result_text = f"💰 Settlement for {trip.trip_name}\n\n"
    result_text += f"Total spent: ${total_spent:.2f}\n"
    result_text += f"Per person (if all shared): ${avg_per_person:.2f}\n\n"
    result_text += "Balances:\n"
    
    for name, member in trip.members.items():
        if member.balance > 0.01:
            print(f"    {name}: ${member.balance:.2f} (is owed)")
            result_text += f"  {name}: ${member.balance:.2f} (is owed)\n"
        elif member.balance < -0.01:
            print(f"    {name}: ${member.balance:.2f} (owes)")
            result_text += f"  {name}: ${abs(member.balance):.2f} (owes)\n"
        else:
            print(f"    {name}: $0.00 (settled)")
            result_text += f"  {name}: $0.00 (settled)\n"
    
    balance_list = trip.get_balance_list()
    final_balances, settlements = calculate_settlements(balance_list)

    print()
    summary = format_settlement_summary(final_balances, settlements)
    print(summary)
    print(f"\nTotal transactions needed: {len(settlements)}\n")
    
    # Add settlements to clipboard text
    result_text += "\nRequired Transactions:\n"
    for s in settlements:
        result_text += f"  {s['debtor']} → {s['creditor']}: ${s['amount']:.2f}\n"
    result_text += f"\nTotal transactions: {len(settlements)}"
    
    # Copy to clipboard
    copy_choice = valid_input("\nCopy result to clipboard? (y/n): ", allow_empty=True).lower()
    if copy_choice == 'y':
        try:
            pyperclip.copy(result_text)
            print("✅ Copied to clipboard!")
        except Exception as e:
            print(f"Failed to copy: {e}")
    print()
    

    balance_list = trip.get_balance_list()
    final_balances, settlements = calculate_settlements(balance_list)

    print()
    print(format_settlement_summary(final_balances, settlements))


def main():
    print(BANNER)

    trip_name = input("Group name (or press Enter for 'My Trip'): ").strip()
    trip = Trip(trip_name or 'My Trip')
    print(f"\n✅ Trip '{trip.trip_name}' created!\n")

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
                
                case 4:
                    trip.list_payments()
                    print()
                
                case 5:
                    handle_add_payment(trip)
                
                case 6:
                    handle_edit_payment(trip)

                case 7:
                    handle_delete_payment(trip)

                case 8:
                    handle_settlement(trip)

                case 9:
                    print("Thanks for using Smart Travel Splitter! See you mate👋")
                    break
                
                case _:
                    print('Invalid option. Please select 1-9.\n')

        except KeyboardInterrupt:
            print("\n\nExiting... Thanks for using Smart Travel Splitter!👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == '__main__':
    main()