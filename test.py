def print_vend(snacks: dict):
    '''
    Prints the contents of the vending machine.

    Parameter:
    snacks(dict): pairs of snack name and its quantity in the vending machine
    '''
    if len(snacks) == 0:
        print("Your vending machine is empty!")
    else:
        for i, item in enumerate(snacks):
            print(f"{i+1}: {item} [{snacks[item]}]")


def add(snacks: dict, item: str, quantity: int):
    '''
    Adds the snacks to the vending machine. 
    If the snack is already in the machine, just tell that to users and won't add it. If the quantity is zero or less, warn the user. 

    Return:
    Technically it doesn't return anything but modifies the snack dict.
    '''
    if item in snacks:
        print("You already have this snack!")
    else:
        if quantity <= 0:
            print("Quantity must be positive!")
        else:
            snacks[item] = quantity
            print(f"Added: {item} [{quantity}]")


def remove(snacks: dict, index: int):
    '''
    Removes snacks at the designated index if the index is in the range.

    Returns:
    This function does'nt return anything but modifies the snack dictionary.
    '''
    if index > len(snacks) or index <= 0:
        print("Invalid index!")
    else:
        items = list(snacks.keys())    # Extracts only items from snacks dictionary and convert them into a lsit
        snacks.pop(items[index-1])     # Now we can access to snack with index
        print(f"Removed: {items[index-1]}")


print("Welcome to the VMIM System!")
snacks = {}
keep_running = True
while keep_running:
    commands = input("\nEnter command: ").split()
    command = commands[0].upper()
    
    match command:
        case 'HELP':
            if len(commands) != 1:
                print("Invalid command!")
            else:
                print("ADD <snack> <quantity>", "REMOVE <index>", "PRINT", "HELP", "EXIT", sep='\n')

        case 'EXIT':
            if len(commands) != 1:
                print("Invalid command!")
            else:
                print("Exiting VMIM System.")
                keep_running = False

        case 'PRINT':
            if len(commands) != 1:
                print("Invalid command!")
            else:
                print_vend(snacks)

        case 'ADD':
            if len(commands) != 3:
                print("Invalid command!")
            else:
                item = commands[1]    # Assuming snack is always one word
                quantity = int(commands[2])    # Assuming the quantity is always an integer
                add(snacks, item, quantity)

        case 'REMOVE':
            if len(commands) != 2:
                print("Invalid command!")
            else:
                index = int(commands[1])    # Assuming the index for a remove command is always an integer
                remove(snacks, index)

        case _:
            print("Invalid command!")