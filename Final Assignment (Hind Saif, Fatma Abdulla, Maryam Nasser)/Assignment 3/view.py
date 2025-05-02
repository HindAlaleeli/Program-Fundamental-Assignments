import tkinter as tk  # Tkinter for GUI components
from tkinter import messagebox  # to show popup alerts

# View class responsible for displaying all GUI components
class TicketBookingView:
    ''' a class that is responsible for displaying all GUI components'''
    def __init__(self, root, controller):
        self.root = root  #reference to the Tkinter root window
        self.controller = controller  #reference to the controller

        self.root.title("Grand Prix Ticket Booking System")  #set window title

        #store the logged-in user for session tracking
        self.logged_in_user = None

        #the main GUI container (Frame)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        #the default selections for ticket type and payment method
        self.selected_ticket = tk.StringVar()
        self.selected_ticket.set("Single Race Pass")  #default ticket option

        self.payment_method = tk.StringVar()
        self.payment_method.set("Credit Card")  #default payment option

        self.quantity_entry = None  #entry widget to input how many tickets the customer wants to get

        #display main menu at launch
        self.build_main_menu()

    #clear all the widgets from the current frame (for navigation)
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ------------------- The Main Menu -------------------
    def build_main_menu(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Grand Prix Ticket Booking System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Account Management", command=self.controller.show_account_menu).pack(pady=5)
        tk.Button(self.main_frame, text="Ticket Purchasing", command=self.controller.show_ticket_menu).pack(pady=5)
        tk.Button(self.main_frame, text="Admin Dashboard", command=self.controller.show_admin_menu).pack(pady=5)

    # ------------------- Account Management Screens -------------------
    def build_account_menu(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Account Management", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Add Account", command=self.controller.add_account_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Login", command=self.controller.login_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Edit Account", command=self.controller.edit_account_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Delete Account", command=self.controller.delete_account_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Display Customer Details", command=self.controller.display_customer_details).pack(pady=5)
        tk.Button(self.main_frame, text="Delete Orders", command=self.controller.delete_orders_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.build_main_menu).pack(pady=10)

    #generic form to handle add, edit, login operations
    def account_form(self, title, button_text, action_callback):
        self.clear_frame()
        tk.Label(self.main_frame, text=title).pack(pady=5)

        #username input
        username_entry = tk.Entry(self.main_frame)
        tk.Label(self.main_frame, text="Username").pack()
        username_entry.pack()

        #password input (hidden for security)
        password_entry = tk.Entry(self.main_frame, show="*")
        tk.Label(self.main_frame, text="Password").pack()
        password_entry.pack()

        #a submit button
        tk.Button(self.main_frame, text=button_text,
                  command=lambda: action_callback(username_entry.get(), password_entry.get())).pack(pady=10)

        #back to account menu button
        tk.Button(self.main_frame, text="Back", command=self.build_account_menu).pack(pady=5)

    #a form to delete a user account (you only need to write the username that you want it to be deleted)
    def delete_account_form(self, action_callback):
        self.clear_frame()
        tk.Label(self.main_frame, text="Delete Account").pack(pady=5)

        username_entry = tk.Entry(self.main_frame)
        tk.Label(self.main_frame, text="Username").pack()
        username_entry.pack()

        tk.Button(self.main_frame, text="Delete",
                  command=lambda: action_callback(username_entry.get())).pack(pady=10)

        tk.Button(self.main_frame, text="Back", command=self.build_account_menu).pack(pady=5)

    #display the list of customers and how many orders they placed
    def display_customers(self, customer_list):
        self.clear_frame()
        tk.Label(self.main_frame, text="Customer Details", font=("Arial", 14)).pack(pady=10)
        for customer, orders in customer_list.items():
            tk.Label(self.main_frame, text=f"{customer} - {orders} orders").pack()
        tk.Button(self.main_frame, text="Back", command=self.build_account_menu).pack(pady=10)

    #show all the orders and allow the user (not the customer) to delete any of them
    def display_orders(self, orders_list, delete_callback):
        self.clear_frame()
        tk.Label(self.main_frame, text="Delete Orders", font=("Arial", 14)).pack(pady=10)

        if not orders_list:
            tk.Label(self.main_frame, text="No orders found.").pack(pady=5)
        else:
            for i, order in enumerate(orders_list):
                order_text = f"{i+1}. {order['username']} - {order['ticket_type']} x{order['quantity']} (${order['total_cost']})"
                tk.Button(self.main_frame, text=order_text, command=lambda idx=i: delete_callback(idx)).pack(pady=2)

        tk.Button(self.main_frame, text="Back", command=self.build_account_menu).pack(pady=10)

    # ------------------- Ticket Purchase Screen -------------------
    def build_ticket_menu(self, tickets):
        self.clear_frame()
        tk.Label(self.main_frame, text="Ticket Purchasing", font=("Arial", 14)).pack(pady=10)

        #show all the ticket types
        for ticket_type, info in tickets.items():
            text = f"{ticket_type} - ${info['price']} ({info['validity']})\nFeatures: {info['features']}"
            tk.Radiobutton(self.main_frame, text=text, variable=self.selected_ticket,
                           value=ticket_type, justify="left").pack(anchor="w")

        #quantity input
        tk.Label(self.main_frame, text="Select Quantity").pack()
        self.quantity_entry = tk.Entry(self.main_frame)
        self.quantity_entry.pack(pady=5)

        #the payment method selection
        tk.Label(self.main_frame, text="Payment Method").pack()
        tk.Radiobutton(self.main_frame, text="Credit Card", variable=self.payment_method, value="Credit Card").pack()
        tk.Radiobutton(self.main_frame, text="Debit Card", variable=self.payment_method, value="Debit Card").pack()

        #the submit purchase button
        tk.Button(self.main_frame, text="Submit Purchase", command=self.controller.purchase_ticket).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.build_main_menu).pack(pady=10)

    # ------------------- Admin Dashboard Screen -------------------
    def build_admin_menu(self, ticket_sales_summary):
        self.clear_frame()
        tk.Label(self.main_frame, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Tickets Sold Per Day", font=("Arial", 12, "underline")).pack(pady=5)

        #show the grouped sales by date and type
        for date, sales in ticket_sales_summary.items():
            tk.Label(self.main_frame, text=f"Date: {date}", font=("Arial", 10, "bold")).pack()
            for ticket_type, qty in sales.items():
                tk.Label(self.main_frame, text=f"  {ticket_type}: {qty} tickets").pack()

        #the buttons to apply or disable discounts
        tk.Label(self.main_frame, text="\nDiscount Options", font=("Arial", 12, "underline")).pack(pady=10)
        tk.Button(self.main_frame, text="Apply 50% Discount to ALL Tickets", command=self.controller.apply_discount).pack(pady=5)
        tk.Button(self.main_frame, text="Disable Discount for ALL Tickets", command=self.controller.disable_discount).pack(pady=5)

        #a button to return to the main menu
        tk.Button(self.main_frame, text="Back", command=self.build_main_menu).pack(pady=20)

    # ------------------- the popups messages -------------------
    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)  # show a success/info message

    def show_error(self, title, msg):
        messagebox.showerror(title, msg)  # show a error message