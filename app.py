"""
Travel Splitter App - Streamlit GUI Version
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
from models import Trip
from calculator import calculate_settlements, format_settlement_summary

# Page config
st.set_page_config(
    page_title="Travel Splitter",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'trip' not in st.session_state:
    st.session_state.trip = None
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main header with muted gradient */
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        color: #e2e8f0;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling - stronger override for primary buttons */
    .stButton button, .stFormSubmitButton button {
        width: 100%;
        background-color: #5a7a9e !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover, .stFormSubmitButton button:hover {
        background-color: #4a6a8e !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Override Streamlit's primary button red color */
    .stFormSubmitButton button[kind="primary"] {
        background-color: #5a7a9e !important;
        border-color: #5a7a9e !important;
    }
    
    .stFormSubmitButton button[kind="primary"]:hover {
        background-color: #4a6a8e !important;
        border-color: #4a6a8e !important;
    }
    
    /* Payment cards with soft, muted colors */
    .payment-card {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        margin: 0.8rem 0;
        color: #2d3748;
        border-left: 4px solid #718096;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .payment-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        color: #4a5568;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4a5568;
        color: white;
    }
    
    /* Form elements */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #f7fafc;
        border: 1px solid #cbd5e0;
        border-radius: 6px;
        color: #2d3748;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2d3748;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>✈️ Smart Travel Splitter</h1>
        <p>Bill splitting, without the confusion</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for trip creation
with st.sidebar:
    st.header("🎒 Trip Setup")
    
    if st.session_state.trip is None:
        trip_name = st.text_input("Trip Name", placeholder="e.g., Tokyo Weekend")
        if st.button("Create Trip", type="primary"):
            if trip_name.strip():
                st.session_state.trip = Trip(trip_name.strip())
                st.success(f"✅ Trip '{trip_name}' created!")
                st.rerun()
            else:
                st.error("Please enter a trip name")
    else:
        st.success(f"📍 **{st.session_state.trip.trip_name}**")
        st.write(f"👥 Members: {len(st.session_state.trip.members)}")
        st.write(f"💰 Payments: {len(st.session_state.trip.payments)}")
        
        if st.button("🔄 Reset Trip", type="secondary"):
            st.session_state.trip = None
            st.rerun()

# Main content
if st.session_state.trip is None:
    st.info("👈 Create a trip to get started!")
else:
    trip = st.session_state.trip
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Members", "💳 Payments", "✏️ Edit/Delete", "💰 Settlement"])
    
    # TAB 1: Members Management
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Add Member")
            new_member = st.text_input("Member Name", key=f"new_member_{st.session_state.form_key}", placeholder="e.g., Alice")
            if st.button("Add Member", type="primary"):
                if new_member.strip():
                    if trip.add_member(new_member.strip()):
                        st.success(f"✅ {new_member} added!")
                        st.session_state.form_key += 1  # Increment to refresh form
                        st.rerun()
                else:
                    st.error("Please enter a name")
        
        with col2:
            st.subheader("Current Members")
            if trip.members:
                for name in trip.members.keys():
                    col_name, col_btn = st.columns([3, 1])
                    with col_name:
                        st.write(f"👤 {name}")
                    with col_btn:
                        if st.button("❌", key=f"remove_{name}"):
                            trip.remove_member(name)
                            st.rerun()
            else:
                st.info("No members yet")
    
    # TAB 2: Add Payments
    with tab2:
        st.subheader("Record New Payment")
        
        if not trip.members:
            st.warning("⚠️ Add members first before recording payments!")
        else:
            # Checkbox outside form to make it interactive
            split_specific = st.checkbox("Split among specific members only", value=False, key="split_choice")
            
            # Show multiselect if splitting among specific members
            involved = None
            if split_specific:
                st.write("**Who is involved in this expense?**")
                involved = st.multiselect(
                    "Select members",
                    options=list(trip.members.keys()),
                    label_visibility="collapsed",
                    key="involved_members"
                )
            
            with st.form(f"payment_form_{st.session_state.form_key}", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    payer = st.selectbox("Who paid?", options=list(trip.members.keys()))
                
                with col2:
                    description = st.text_input("Description", placeholder="e.g., Hotel booking")
                
                amount = st.number_input("Amount ($)", value=0.01, step=0.01, format="%.2f", key=f"amount_{st.session_state.form_key}")
                
                submitted = st.form_submit_button("Add Payment", type="primary")
                
                if submitted:
                    try:
                        # Validate amount first
                        if amount <= 0:
                            st.error("❌ Amount must be greater than $0!")
                        # Validate members selection
                        elif split_specific and not involved:
                            st.error("Please select at least one member to split with!")
                        else:
                            # Ensure payer is included if specific split
                            if split_specific and involved and payer not in involved:
                                involved.append(payer)
                            
                            trip.add_payment(payer, amount, description, involved if split_specific else None)
                            st.success(f"✅ Payment recorded: {payer} paid ${amount:.2f}")
                            st.session_state.form_key += 1  # Increment to refresh form
                            st.rerun()
                    except ValueError as e:
                        st.error(f"Error: {e}")
        
        # Display all payments
        st.divider()
        st.subheader("All Payments")
        
        if trip.payments:
            for payment in trip.payments:
                involved_str = ", ".join(payment.involved_members) if payment.involved_members else "all"
                desc_text = payment.description if payment.description else "(no description)"
                st.markdown(f"""
                    <div class="payment-card">
                        <strong>#{payment.id}</strong> | 
                        <strong>{payment.payer_name}</strong> paid 
                        <strong>${payment.amount:.2f}</strong> - 
                        {desc_text}<br>
                        <small>👥 Split between: {involved_str}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No payments recorded yet")
    
    # TAB 3: Edit/Delete Payments
    with tab3:
        if not trip.payments:
            st.info("No payments to edit or delete")
        else:
            st.subheader("Edit or Delete Payments")
            
            # Show all payments with actions
            for payment in trip.payments:
                involved_str = ", ".join(payment.involved_members) if payment.involved_members else "all"
                with st.expander(f"#{payment.id}: {payment.payer_name} - ${payment.amount:.2f} - {payment.description} (split: {involved_str})"):
                    col1, col2 = st.columns([2, 2])
                    
                    with col1:
                        new_amount = st.number_input(
                            "New Amount",
                            value=float(payment.amount),
                            step=0.01,
                            key=f"edit_amount_{payment.id}"
                        )
                    
                    with col2:
                        new_desc = st.text_input(
                            "New Description",
                            value=payment.description,
                            key=f"edit_desc_{payment.id}"
                        )
                    
                    # Edit involved members
                    st.write("**Involved Members:**")
                    new_involved = st.multiselect(
                        "Select members involved in this expense",
                        options=list(trip.members.keys()),
                        default=payment.involved_members,
                        key=f"edit_involved_{payment.id}"
                    )
                    
                    col_save, col_delete = st.columns([1, 1])
                    
                    with col_save:
                        if st.button("💾 Save Changes", key=f"save_{payment.id}", use_container_width=True):
                            if new_amount <= 0:
                                st.error("Amount must be greater than 0")
                            elif not new_involved:
                                st.error("At least one member must be involved")
                            else:
                                trip.edit_payment(payment.id, new_amount, new_desc, new_involved)
                                st.success(f"✅ Payment #{payment.id} updated!")
                                st.rerun()
                    
                    with col_delete:
                        if st.button(f"🗑️ Delete", key=f"delete_{payment.id}", type="secondary", use_container_width=True):
                            trip.delete_payment(payment.id)
                            st.success(f"✅ Payment #{payment.id} deleted!")
                            st.rerun()
    
    # TAB 4: Settlement
    with tab4:
        st.subheader("💰 Calculate Settlement")
        
        if not trip.payments:
            st.warning("⚠️ No payments recorded yet!")
        else:
            if st.button("Calculate Settlement", type="primary", use_container_width=True):
                # Calculate balances
                avg_per_person = trip.calculate_balances()
                total_spent = sum(p.amount for p in trip.payments)
                
                # Display summary
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Spent", f"${total_spent:.2f}")
                with col2:
                    st.metric("Per Person (if all shared)", f"${avg_per_person:.2f}")
                
                st.divider()
                
                # Display balances
                st.subheader("Current Balances")
                
                for name, member in trip.members.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{name}**")
                    with col2:
                        if member.balance > 0.01:
                            st.success(f"${member.balance:.2f} (owed)")
                        elif member.balance < -0.01:
                            st.error(f"${abs(member.balance):.2f} (owes)")
                        else:
                            st.info("$0.00 (settled)")
                
                st.divider()
                
                # Calculate settlements
                balance_list = trip.get_balance_list()
                final_balances, settlements = calculate_settlements(balance_list)
                
                # Display settlements
                st.subheader("💸 Required Transactions")
                
                # Build clipboard text
                clipboard_text = f"💰 Settlement for {trip.trip_name}\n\n"
                clipboard_text += f"Total spent: ${total_spent:.2f}\n"
                clipboard_text += f"Per person (if all shared): ${avg_per_person:.2f}\n\n"
                clipboard_text += "Balances:\n"
                for name, member in trip.members.items():
                    if member.balance > 0.01:
                        clipboard_text += f"  {name}: ${member.balance:.2f} (is owed)\n"
                    elif member.balance < -0.01:
                        clipboard_text += f"  {name}: ${abs(member.balance):.2f} (owes)\n"
                    else:
                        clipboard_text += f"  {name}: $0.00 (settled)\n"
                
                clipboard_text += "\nRequired Transactions:\n"
                
                if settlements:
                    for i, s in enumerate(settlements, 1):
                        st.markdown(f"""
                            <div class="payment-card">
                                <strong>{i}.</strong> 
                                {s['debtor']} → {s['creditor']}: 
                                <strong>${s['amount']:.2f}</strong>
                            </div>
                        """, unsafe_allow_html=True)
                        clipboard_text += f"  {i}. {s['debtor']} → {s['creditor']}: ${s['amount']:.2f}\n"
                    
                    st.success(f"✅ Total transactions needed: {len(settlements)}")
                    clipboard_text += f"\nTotal transactions: {len(settlements)}"
                else:
                    st.success("✅ Everyone is settled up!")
                    clipboard_text += "  Everyone is settled up!"
            
                