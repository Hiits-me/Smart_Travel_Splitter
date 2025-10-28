
banner = ''' 
    =========================================
    ✈️  Smart Travel Splitter (CLI MVP)
    =========================================
    Bill splitting, without the confusion.
    '''

def commands()-> None:
    options = '''
    Options:
    1. list members
    2. add a member
    3. list all payment
    4. record payment
    5. settle
    6. exit
    '''
    print(options)

    

def main():
    print(banner)
    trip = Group(input("Group name: ").strip() or "My Trip")
    
    while True:
        commands()
        option = int(input("Select an option in number: ")) # gives me an error when entering string

        match option:
            case 1:
                trip.list_members()
                print()
            case 2:
                new_member = input("Type their name: ").strip()
                trip.add_member(new_member)
                print(f"{new_member} is added")
            case 3:
                trip.list_payments()
            case 4:
                new_payment = input("usage: <payer name> <amount> <purpose> <for who>\n").strip().split()
                trip.add_payment(new_payment[0], float(new_payment[1]), new_payment[2], new_payment[3:])
                print(f"{new_payment[0]} paid {new_payment[1]} for {new_payment[2:]}")
            case 6:
                break
        pass

if __name__ == "__main__":
    main()