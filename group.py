
class Payment:
    pay_id = 1
    def __init__(self, payer: str, amount: float, involves: set[str], purpose: str = "", currency: str = "AUD"):
        self.id = Payment.pay_id
        Payment.pay_id += 1
        self.payer = payer
        self.amount = float(amount)
        self.involves = set(involves) # faster for searching and name have to be unique in a group
        self.purpose = purpose
        self.currency = currency # for currency converter
    
    def currency_convert(self, currency):
        print()


class Group:
    def __init__(self, name: str):
        self.name = name
        self.members = set()
        self.payments = []
    

    def __str__(self):
        return f"Group name: {self.name}"
    

    def list_members(self):
        if len(self.members) == 0:
            print("No member in this group.")
        else:
            for member in self.members:
                print(member, end=' ')

    
    def add_member(self, member_name: str) -> None:
        if member_name in self.members:
            print(f"{member_name} is already in the group.")
        else:
            self.members.add(member_name)
            print(f"{member_name} is successfully added.")
    

    def remove_member(self, member_name: str) -> None:
        if member_name not in self.members:
            print(f"{member_name} doesn't exist in this group.")
        else:
            self.members.remove(member_name)
            print(f"{member_name} is successfully removed.")

    def list_payment(self) -> None:
        if len(self.payments) == 0:
            print("No payment records found.")
        else:
            print(f"{self.name}:", end=' ')
            for payment in self.payments:
                print({payment})

    def search_payment(self, pay_id: int) -> Payment:
        for paid in self.payments:
            if pay_id == paid.id:
                return paid
            else:
                print(f"Payment #{pay_id} not found.")


    def add_payment(self, payer: str, amount: float, involves: set, purpose: str = "") -> int:
        if payer not in self.members:
            print(f"{payer} not in group.")
        else:
            paid = Payment(payer, amount, involves, purpose)
            self.payments.append(paid)
            return paid.id # for display
    

    def edit_payment(self, pay_id: int, new_amount: float, new_purpose: str) -> None:
        paid = self.search_payment(pay_id)
        if new_amount is not None and new_amount.isdigit():
            paid.amount = float(new_amount)
        if new_purpose is not None:
            paid.purpose = new_purpose
    

    def delete_payment(self, pay_id: int) -> None:
        paid = self.search_payment(pay_id)
        self.payments.remove(paid)
    

    def total_by_member(self) -> dict:
        totals = {}
        # {
        #     "A": 23000,   # A paid hotel + taxi
        #     "B": 12000,   # B paid dinners
        #     "C":  5000,
        #     "D":      0
        # }
        for member_name in self.members:
            totals[member_name] = 0


    
