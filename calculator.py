'''
Settlement calculation logic for minimizing transactions
'''

def calculate_settlements(balance_list: list[dict]) -> tuple:
    '''
    Calculate minimum transactions needed to settel all debts

    Args:
        balance_list: List of dicts with member_name and price_to_get
            Positive values = creditor
            Negative values = debtor
    
    Returns:
        tuple: (final_balances, settlements)
            - final_balances: List of remaining balances
            - settlements: List of transactions needed
    '''
    if not isinstance(balance_list, list):
        raise TypeError(f"balance_list must be a list, got {type(balance_list)}.")
    for balance in balance_list:
        if not isinstance(balance, dict):
            raise TypeError(f'Each balance must be a dict.')
        if 'member_name' not in balance or 'price_to_get' not in balance:
            raise KeyError("Each balance dict must have 'member_name' and 'price_to_get'.")
        
    balances = [{'member_name': b['member_name'], 'price_to_get': b['price_to_get']}
                for b in balance_list]
    return calculate_recursive(balances, [])


def calculate_recursive(balances, settlements):
    '''
    Recursive fucntion to calculate settlements
    Uses greedy algorithm: always settle largest creditor with largest debtor
    '''

    # Sort highest to lowest 
    balances = sorted(balances, key=lambda b: b['price_to_get'], reverse = True)
    creditor = balances[0]
    debtor = balances[-1]

    amount = min(creditor['price_to_get'], abs(debtor['price_to_get']))

    # Base case: no more settlements needed
    if amount == 0:
        return (balances, settlements)
    
    # Updates
    creditor['price_to_get'] -= amount
    debtor['price_to_get'] += amount

    # Records
    settlements.append({
        'debtor': debtor['member_name'],
        'creditor': creditor['member_name'],
        'amount': amount
    }
    )
    return calculate_recursive(balances, settlements)

def format_settlement_summary(balances, settlements) -> str:
    '''
    Format settlement information as a readable string
    '''

    if not isinstance(balances, list):
        raise TypeError(f'balances must be a list.')
    if not isinstance(settlements, list):
        raise TypeError(f'settlements must be a list.')
    
    lines = []
    lines.append('='*50)
    lines.append('SETTLEMENT SUMMARY')
    lines.append('='*50)
    lines.append("\nTransactions needed:")
    lines.append("-" * 50)
    if settlements:
        for s in settlements:
            lines.append(f"{s['debtor']} → {s['creditor']}: ${s['amount']:.2f}")
    else:
        lines.append("No transactions needed - all settled!")
    
    lines.append("\nFinal balances (should be ~0):")
    lines.append("-" * 50)
    for b in balances:
        lines.append(f"{b['member_name']}: ${b['price_to_get']:.2f}")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)