class Member:
    '''
    Represents a trip member
    '''
    def __init__(self, name:str) -> None:
        self.name = name
        self.balance = 0 # positive = owed money, negative = owes money
    
    def __str__(self):
        return f"Name: {self.name}, Balance: {self.balance}"
    
    def __repr__(self):
        return f"Member(name = '{self.name}', balance = '{self.balance}')"


class Payment:
    '''
    Represents a payment made by a member
    '''
    payment_id = 1
    def __init__(self, payer_name:str, amount:float, description="", involved_members=None) -> None:
        self.id = Payment.payment_id
        Payment.payment_id += 1
        self.payer_name = payer_name
        self.amount = float(amount)
        self.description = description
        # If no involved members specified, assume it's split among all trip members
        self.involved_members = involved_members if involved_members else []
    
    def __repr__(self):
        involved = f", invloved = {self.involved_members}" if self.involved_members else ""
        return f"Payment(payer = '{self.payer_name}, amount = '{self.amount}', desc = '{self.description}'{involved}"


class Trip:
    '''
    Represents a trip with members and payments.
    '''
    def __init__(self, trip_name:str):
        self.trip_name = trip_name
        self.members = {} # name: Member object
        self.payments = []

    def list_members(self) -> None:
        if len(self.members) == 0:
            print("No member in this group.")
        else:
            print('Members: ', end=' ')
            for member in self.members:
                print(member, end=', ')
    
    def add_member(self, name:str) -> bool:
        if not isinstance(name, str):
            return False
        if name not in self.members:
            self.members[name] = Member(name)
            print(f"{name} is successfully added.")
            return True
        print(f"{name} is already in the group.")
        return False
    
    def remove_member(self, name:str) -> None:
        if not isinstance(name, str):
            return 
        if name not in self.members:
            print(f"{name} doesn't exist in this group.")
            return
        self.members.pop(name)
        print(f"{name} is successfully removed.")

    def list_payments(self) -> None:
        if len(self.payments) == 0:
            print("No payment records found.")
            return
        print(f"Payments for {self.trip_name}:")
        for payment in self.payments:
            involved_str = ", ".join(payment.involved_members) if payment.involved_members else "all"
            print(f"  #{payment.id}: {payment.payer_name} paid ${payment.amount:.2f} - {payment.description} (split: {involved_str})")
    
    
    def search_payment(self, payment_id: int) -> Payment:
        for payment in self.payments:
            if  payment.id == payment_id:
                return payment
        print(f"Payment #{payment_id} not found.")
        return None
    
    def add_payment(self, payer_name, amount, description="", involved_members=None) -> Payment:
        '''
        Add a payment made by a member

        Args:
            payer_name: Name of the person who paid
            amount: Amount paid
            description: Description of the payment
            involved_members: List of member names who share this expense. If none, all members share it.
        '''
        if payer_name not in self.members:
            raise ValueError(f"Member '{payer_name}' not found in trip")
        
        if involved_members is None:
            involved_members = list(self.members.keys())
        else:
            # validate all involved members exist
            for name in involved_members:
                if name not in self.members:
                    raise ValueError(f"'{name}' not found in trip")
                # ensure the payer is in involved list
            if payer_name not in involved_members:
                involved_members.append(payer_name)
        
        payment = Payment(payer_name, amount, description, involved_members)
        self.payments.append(payment)
        return payment
    
    
    def edit_payment(self, payment_id: int, new_amount: float, new_description: str, new_involved_members: list = None) -> None:
        payment_to_edit = self.search_payment(payment_id)
        if payment_to_edit is None:
            return
        if new_amount is not None:
            try:
                payment_to_edit.amount = float(new_amount)
                print(f'Payment #{payment_id} amount is successfully updated.')
            except ValueError:
                print(f"Invalid amount: {new_amount}")
        if new_description is not None:
            payment_to_edit.description = new_description
            print(f'Payment #{payment_id} description is successfully updated.')
        
        if new_involved_members is not None:
            for name in new_involved_members:
                if name not in self.members:
                    print(f'Error: \'{name}\' not found in trip')
                    return
            payment_to_edit.involved_members = new_involved_members
            print(f"Payment #{payment_id} involved members successfully updated.")
    

    def delete_payment(self, payment_id: int) -> None:
        payment_to_delete = self.search_payment(payment_id)
        if payment_to_delete is None:
            return
        self.payments.remove(payment_to_delete)
        print(f'Payment #{payment_id} is successfully deleted.')
    

    def calculate_balances(self):
        '''
        Calculate how much each member should pay or recieve
        '''
        for member in self.members.values():
            member.balance = 0

        # process each payment
        for payment in self.payments:
             # calculate per-person share for this payment
            num_involved = len(payment.involved_members)
            per_person_share = payment.amount / num_involved

            # the payer gets credited for the full amount
            self.members[payment.payer_name].balance += payment.amount

            # each involved member (including payer) gets debited their share
            for member_name in payment.involved_members:
                self.members[member_name].balance -= per_person_share
        
        # return average spent per person
        total = sum(p.amount for p in self.payments)
        return total / len(self.members) if self.members else 0
    

    def get_balance_list(self):
        '''
        Get list of balances in the format needed for settlemnet calculation
        '''
        return [
            {'member_name': name, 'price_to_get': member.balance}
            for name, member in self.members.items()
        ]
    
    def __repr__(self):
        return f"Trip(trip_name = '{self.trip_name}', members = {len(self.members)}, payments = {len(self.payments)})"