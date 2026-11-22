import streamlit as st # to run the application
import pandas as pd #handles data
from datetime import datetime # for the current time and date for sales

# First the files are all stored here at the top
#This is because i do not need to refer to it several times
MENU_FILE = "menu.csv"
SALES_FILE = "point_of_sales.csv"
SALES_LOG_FILE = "sales_log.csv"

#Dictionary (list of pairs)
SET_MENU = {    
    "Espresso": "Hot Coffee",
    "Americano": "Hot Coffee",
    "Latte": "Hot Coffee",
    "Cappuccino": "Hot Coffee",
    "Flat White": "Hot Coffee",
    "Mocha": "Hot Coffee",
    "Iced Latte": "Iced",
    "Iced Americano": "Iced",
    "Iced Mocha": "Iced",
    "Cold Brew": "Iced",
    "Karak": "Tea",
    "Green Tea": "Tea",
    "Chai Latte": "Tea",
    "Mint Tea": "Tea",
    "Croissant": "Pastry",
    "Muffin": "Pastry",
    "Cookie": "Pastry",
    "Cinnamon Roll": "Pastry",
}
# The allowed sizes and categories
#tuple
#Used to ensure the values in the table are valid and to fill the dropdown in the form
SIZES = ("Small", "Medium", "Large")
CATEGORIES = ("Hot Coffee", "Iced", "Tea", "Pastry")


# this finds the item (drink/pastry) from the set menu 
#strip() removes spacing 
#.lower() so if i were to write "latte" capital or lower letters would not affect the result
def find_drink(typed_name):
    for name in SET_MENU:
        if name.lower() == typed_name.strip().lower(): #checks if it matches what was typed
            return name
    return ""


#
st.set_page_config(page_title="MUGSHOT Café") #text on the browser tab



if "menu" not in st.session_state: #session state prevents normal variables from getting wiped each time.
    try:
        st.session_state["menu"] = pd.read_csv(MENU_FILE)
    except FileNotFoundError:
        st.session_state["menu"] = pd.DataFrame(columns=["Name", "Size", "Price", "Category"]) #

if "point_of_sales" not in st.session_state:
    try:
        st.session_state["point_of_sales"] = pd.read_csv(SALES_FILE)
    except FileNotFoundError:
        st.session_state["point_of_sales"] = pd.DataFrame(
            columns=["Date", "Time", "Item", "Size", "Quantity", "Unit Price", "Total"]
        )

if "cart" not in st.session_state:
    st.session_state["cart"] = [] #This is an empty list, items go in while a customer orders, and they only become real sales when you click Finalize.


with st.sidebar:
    st.image("coffee.png", width=180)
    st.title("MUGSHOT Café")
    page_chosen = st.radio(
        "Navigation",
        ("About Us","Manage Menu", "Point of Sale", "Daily Dashboard", "Sales log"),

    )


                                                                #MANAGE MENU PAGE
if page_chosen == "Manage Menu":
    st.title("Manage Menu")
    st.write("CHOOSE YOUR DRINK☕️!!!!")

    # shows the set menu at the top so I know what names I can type
    with st.expander("Set Menu (items we have)"):
        set_menu_table = pd.DataFrame(list(SET_MENU.items()), columns=["Item", "Category"])
        st.dataframe(set_menu_table, use_container_width=True, hide_index=True)

    with st.form("add_drink_form"):
        drink_name = st.text_input("Item")

        drink_size = st.selectbox("Size", SIZES)

        drink_price = st.number_input("Price", min_value=0.0, step=0.25)

        drink_category = st.selectbox("Category", CATEGORIES)

        submitted = st.form_submit_button("Add Items")

    if submitted:
        clean_name = find_drink(drink_name)
        menu = st.session_state["menu"]

        already_exists = (
            (menu["Name"].str.lower() == clean_name.lower())
            & (menu["Size"] == drink_size)
        ).any()

        if drink_name.strip() == "":
            st.error("Must enter a valid drink")
        elif clean_name == "":
            st.error(f"Sorry, we don't have '{drink_name}'. Check the Set Menu above.")
        elif drink_category != SET_MENU[clean_name]:
            st.error(f"{clean_name} belongs in '{SET_MENU[clean_name]}', not '{drink_category}'.")
        elif drink_price <= 0:
            st.error("Price must be greater than 0.")
        elif already_exists:
            st.error("That drink and size is already on the menu.")

        else:
            new_row = pd.DataFrame(
                {
                    "Name": [clean_name],
                    "Size": [drink_size],
                    "Price": [drink_price],
                    "Category": [drink_category],
                }
            )
            st.session_state["menu"] = pd.concat([menu, new_row], ignore_index=True)
            st.session_state["menu"].to_csv(MENU_FILE, index=False)
            st.success(f"{clean_name} ({drink_size}) was added to the menu!")
    st.divider()
    st.subheader("Current Menu")
    st.caption("Select cell to edit or delete item:)")

    edited_menu = st.data_editor(
        st.session_state["menu"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn(
                "Price", min_value=0.0, format="$%.2f"
            )
        },
    )

    # check every row of the edited menu before saving it
    errors = []
    for i in range(len(edited_menu)):
        row = edited_menu.iloc[i]

        if pd.isna(row["Name"]) or str(row["Name"]).strip() == "":
            continue

        name = find_drink(str(row["Name"]))

        if name == "":
            errors.append(f"Row {i + 1}: we don't have '{row['Name']}' on the set menu.")
        elif row["Category"] != SET_MENU[name]:
            errors.append(f"Row {i + 1}: {name} must be in category '{SET_MENU[name]}'.")

        if row["Size"] not in SIZES:
            errors.append(f"Row {i + 1}: size must be Small, Medium or Large.")

        if pd.isna(row["Price"]) or row["Price"] <= 0:
            errors.append(f"Row {i + 1}: price must be greater than 0.")

    if len(errors) > 0:
        for error in errors:
            st.error(error)
        st.warning("Changes NOT saved until the errors are fixed.")
    else:
        st.session_state["menu"] = edited_menu
        st.session_state["menu"].to_csv(MENU_FILE, index=False)

    menu_csv = st.session_state["menu"].to_csv(index=False)
    st.download_button(
        "Download menu.csv",
        data=menu_csv,
        file_name="menu.csv",
        mime="text/csv",

    )
    
    uploaded = st.file_uploader("Upload a menu CSV", type="csv")
    if uploaded is not None:
        if st.button("Load uploaded menu"):
            st.session_state["menu"] = pd.read_csv(uploaded)
            st.session_state["menu"].to_csv(MENU_FILE, index=False)
            st.rerun()


                                                                    #POINT OF SALE

elif page_chosen == "Point of Sale":
    st.title("Point of Sale")
    st.write("Select a drink and add it to the order.")

    menu = st.session_state["menu"]

    if menu.empty:
        st.warning("The menu is empty. Add item in Manage Menu first.")
    else:
        # Build the list of options like "Latte (Medium)"
        options = []
        for i in range(len(menu)):
            options.append(menu.iloc[i]["Name"] + " (" + menu.iloc[i]["Size"] + ")")

        left, right = st.columns(2)

        with left:
            st.subheader("Add Item")
            choice = st.selectbox("Drink", options)
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)

            if st.button("Add to Order"):
                row = menu.iloc[options.index(choice)]
                item = {
                    "Item": row["Name"],
                    "Size": row["Size"],
                    "Quantity": quantity,
                    "Unit Price": row["Price"],
                }
                st.session_state["cart"].append(item)
                st.success(f"Added {quantity} x {choice}")

        with right:
            st.subheader("Current Order")

            cart = st.session_state["cart"]

            if len(cart) == 0:
                st.write("No items yet.")
            else:
                order_total = 0

                for i, item in enumerate(cart):
                    line_total = item["Quantity"] * item["Unit Price"]
                    order_total = order_total + line_total

                    text_col, button_col = st.columns([3, 1])
                    with text_col:
                        st.write(f"{item['Quantity']} x {item['Item']} ({item['Size']}) - ${line_total:.2f}")
                    with button_col:
                        if st.button("Remove", key=f"remove_{i}"):
                            cart.pop(i)
                            st.rerun()

                st.divider()
                st.write(f"**Order Total: ${order_total:.2f}**")


                if st.button("Finalize Transaction"):
                    now = datetime.now()
                    rows = []

                    for item in cart:
                        rows.append(
                            {
                                "Date": now.strftime("%Y-%m-%d"),
                                "Time": now.strftime("%H:%M"),
                                "Item": item["Item"],
                                "Size": item["Size"],
                                "Quantity": item["Quantity"],
                                "Unit Price": item["Unit Price"],
                                "Total": item["Quantity"] * item["Unit Price"],
                            }
                        )

                    new_sales = pd.DataFrame(rows)
                    st.session_state["point_of_sales"] = pd.concat(
                        [st.session_state["point_of_sales"], new_sales],
                        ignore_index=True,
                    )
                    st.session_state["point_of_sales"].to_csv(SALES_FILE, index=False)
                    st.session_state["cart"] = []
                    st.rerun()

                                                                    #DAILY DASHBOARD

elif page_chosen == "Daily Dashboard":
    st.title("Daily Dashboard")

    sales = st.session_state["point_of_sales"]

    picked_date = st.date_input("Select a date", value=datetime.now())
    date_text = picked_date.strftime("%Y-%m-%d")

    day_sales = sales[sales["Date"] == date_text]

    if day_sales.empty:
        st.info("No sales on this date.")
    else:
        items_sold = day_sales["Quantity"].sum()
        revenue = day_sales["Total"].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Items Sold", int(items_sold))
        with col2:
            st.metric("Total Revenue", f"${revenue:.2f}")

        st.divider()
        st.subheader("Bar Chart of Most Popular Items")

        popular = day_sales.groupby("Item")["Quantity"].sum()
        popular = popular.sort_values(ascending=False)

        st.bar_chart(popular, x_label="Drinks", y_label="Amount Sold", color = "#FF7782")
# STUDENTS CHOICE INNOVATION: I have decided to implement a second bar chart showcasing the most busiest timings during the day
        st.divider()
        st.subheader("Peak Hours")

        day_sales = day_sales.copy()
        day_sales["Hour"] = day_sales["Time"].str[:2]

        by_hour = day_sales.groupby("Hour")["Quantity"].sum()

        # message telling me the peak hours
        top_hours = by_hour.sort_values(ascending=False).head(3)
        busiest_hour = int(top_hours.index[0])

        st.success(
            f"Peak hour: {busiest_hour:02d}:00 - {busiest_hour + 1:02d}:00 "
            f"with {int(top_hours.iloc[0])} items sold"
        )

        st.write("Top busiest hours today:")
        for hour, amount in top_hours.items():
            st.write(f"- {int(hour):02d}:00 - {int(hour) + 1:02d}:00 → {int(amount)} items")

        all_hours = [f"{h:02d}" for h in range(6, 21)]
        by_hour = by_hour.reindex(all_hours, fill_value=0)

        hour_chart = by_hour.reset_index()
        hour_chart.columns = ["Hour", "Items Sold"]
        hour_chart["Hour"] = hour_chart["Hour"] + ":00"

        st.bar_chart(
        hour_chart,
        x="Hour",
        y="Items Sold",
        x_label="Hour of Day",
        y_label="Items Sold",
        color="#6F4E37",
)



                                                                        #SALES LOG



elif page_chosen == "Sales log":
    st.title("Sales Log")

    sales = st.session_state["point_of_sales"]

    if sales.empty:
        st.info("No transactions yet.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            item_options = ["All"] + sorted(sales["Item"].unique())
            item_filter = st.selectbox("Filter by item", item_options)

        with col2:
            use_date = st.checkbox("Filter by date")
            date_filter = st.date_input("Pick a date", value=datetime.now())

        filtered = sales

        if item_filter != "All":
            filtered = filtered[filtered["Item"] == item_filter]

        if use_date:
            date_text = date_filter.strftime("%Y-%m-%d")
            filtered = filtered[filtered["Date"] == date_text]

        st.write(f"Showing {len(filtered)} transactions")
        st.dataframe(filtered, use_container_width=True)

        if st.button("Save this view to CSV"):
            filtered.to_csv(SALES_LOG_FILE, index=False)
            st.success("Saved as sales_log.csv in your folder!")


                                                 #ABOUT US PAGE (second student choice innovation)

elif page_chosen == "About Us":
    st.title("About Us")

    st.image("aboutus.png", use_container_width=True)

    st.write("""
    ### WELCOME TO MUGSHOT ☕️☕️☕️☕️☕️☕️☕️
    **You are not allowed to leave.....EVER....until you finish your coffee!**

    ### Our Story
    Back in 1955, this site was a prison facility. After it was demolished,
    I decided to build something much better where people enjoy being trapped 

    ### Enter freely and of your own free will(by dracula)..... but once you enter you must follow these rules or face your doom!!
    - No escaping before you finish your drink.
    - Every cup is a life sentence of flavor.
    - Good behavior is rewarded with probation.

    ### Meet the Owner
    I'm Alya Awachi, the owner and head warden of MUGSHOT, and now we have a cafe in every country all around the world!!!

    ### Visit Us
    Open daily: [all hours]
    Find us at: [around the world]
""")