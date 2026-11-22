# Project-1--Applications: Coffee Shop Tracker
In this project, I developed a web application using Streamlit to manage and monitor a café’s daily operations. The application was designed to fulfil four key requirements, including managing the drinks and pastry menu, recording point-of-sale transactions, and monitoring daily sales and revenue. Additionally, I incorporated extra features to enhance the application's functionality.

- Deployment App link:
- Video Demonstration link: 

# Problem Statement
A local cafe has hired you to build a dual-purpose web system that manages their drink menu and tracks daily point-of-sale transactions and revenue.

# Features 
- About Us:	The cafe's story, house rules and owner introduction, with an image.
- Manage Menu:	A form to add drinks (Name, Size, Price, Category), an editable menu table, CSV download and CSV upload.
- Point of Sale:	Pick a drink and quantity, add it to the order, remove items before finalizing, then finalize the transaction.
- Daily Dashboard:	For a chosen date: items sold, total revenue, a bar chart of the most popular items, and a Peak Hours section.
- Sales Log:	A table of every historical transaction, with filters by item and by date.

# The Advanced Reuirments:
- Generate a bar chart showing the most popular items sold
- Implement a "Remove from Order" function in the Point of Sale view before a transaction is finalized.

# Student's Choice Innovation
- Another bar chart in the Daily board section showcasing peak hours: A message of the busiest hour, a list of the busiest hours, and the bar chart of items sold per hour of the day.
- About Us page: A fake backstory was added to show the history of the cafe 

# Data Storage (CSV)

The web app uses st.session_state to hold the menu, sales and current order while the app is running, and saves to CSV files.

File	Contents	When it is saved
- menu.csv: 	Name, Size, Price, Category	When a drink is added, edited or deleted
- point_of_sales.csv:	Date, Time, Item, Size, Quantity, Unit Price, Total	When a transaction is finalized
- sales_log.csv:	The currently filtered Sales Log view	When "Save this view to CSV" is clicked

Upload / Edit / Download loop: download the menu with Download menu.csv, edit it in Excel or Numbers, then load it back with Upload a menu CSV and Load uploaded menu. An uploaded file must have the columns Name, Size, Price and Category.

# How to run:
From terminal to open jypter and run streamlit:
- Open up the jypter notebook "python3 -m notebook" - then go to desktop where the main coffee_shop_tracker.py folder is located
- To run streamlit, navigate the folder "cd Desktop" - "cd coffee_shop_tracker" - then "streamlit run coffee_shop_tracker"



# Project Structure
```
coffee_shop_tracker/
├── coffee_shop_tracker.py    # the whole app
├── menu.csv                  # saved menu (created automatically)
├── point_of_sales.csv        # saved transactions (created automatically)
├── README.md
└── images/
    ├── coffee.png            # sidebar logo
    └── aboutus.png           # About Us image
```

# How to Use
- Manage Menu: type a drink from the Set Menu, choose size, price and category, then click Add Items. Edit prices or delete rows directly in the table.
- Point of Sale: choose a drink and quantity, click Add to Order, use Remove to take an item out, then click Finalize Transaction.
- Daily Dashboard: pick a date to see items sold, revenue, the most popular items, and the peak hours.
- Sales Log: filter by item or date, and save the filtered view to CSV if needed.
