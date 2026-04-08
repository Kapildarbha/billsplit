import streamlit as st

st.set_page_config(page_title="Fair Share Bill Splitter", page_icon="💸")

st.title("💸 Fair Share Splitter")
st.write("Split bills fairly with taxes and discounts applied proportionally.")

# --- Sidebar for Global Settings ---
st.sidebar.header("Bill Settings")
flat_tax = st.sidebar.number_input(
    "Total Tax Amount ($)", min_value=0.0, value=0.0, step=0.1)
discount_perc = st.sidebar.slider("Total Discount (%)", 0, 100, 0)

# --- Data Initialization ---
if 'items' not in st.session_state:
    st.session_state.items = []

# --- Input Form ---
with st.form("item_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    item_name = col1.text_input("Item Name (e.g., Pizza)")
    item_price = col2.number_input("Price ($)", min_value=0.0, step=0.1)
    people_names = st.text_input("Who shared this? (comma separated names)")

    submitted = st.form_submit_button("Add Item")
    if submitted and item_name and people_names:
        names_list = [n.strip() for n in people_names.split(",") if n.strip()]
        st.session_state.items.append({
            "name": item_name,
            "price": item_price,
            "people": names_list
        })

# --- Display and Calculate ---
if st.session_state.items:
    st.subheader("Current Items")
    for idx, item in enumerate(st.session_state.items):
        st.write(
            f"**{item['name']}**: ${item['price']:.2f} (Shared by: {', '.join(item['people'])})")

    if st.button("Clear All Items"):
        st.session_state.items = []
        st.rerun()

    # Calculations
    subtotal = sum(item['price'] for item in st.session_state.items)

    if subtotal > 0:
        pre_discount_total = subtotal + flat_tax
        multiplier = 1 - (discount_perc / 100)
        final_total = pre_discount_total * multiplier
        ratio = final_total / subtotal

        # Individual shares
        personal_subtotals = {}
        for item in st.session_state.items:
            split = item['price'] / len(item['people'])
            for person in item['people']:
                personal_subtotals[person] = personal_subtotals.get(
                    person, 0) + split

        # Final Summary
        st.divider()
        st.header("Final Breakdown")
        st.metric("Grand Total to Pay", f"${final_total:.2f}")

        for person, food_share in personal_subtotals.items():
            st.write(f"👤 **{person}**: ${food_share * ratio:.2f}")
