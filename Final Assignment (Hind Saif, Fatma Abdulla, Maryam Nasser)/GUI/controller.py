import tkinter as tk  #for creating the main application window
from model import TicketBookingModel  # Import the model layer
from view import TicketBookingView  # Import the view layer

class TicketBookingController:
    ''' a class that connects the model and view'''
    def __init__(self, root):
        #create instances of model and view
        self.model = TicketBookingModel()  # this will handle the data (accounts, tickets, orders)
        self.view = TicketBookingView(root, self)  #and this will handle the GUI, passing self as the controller

    # ------------------- Navigation Functions -------------------

    #show the Account Management menu
    def show_account_menu(self):
        self.view.build_account_menu()

    #show the Ticket Purchasing screen (only if user is logged in)
    def show_ticket_menu(self):
        if not self.view.logged_in_user:
            # Show error and redirect to login if user is not logged in
            self.view.show_error("Access Denied", "You must be logged in to purchase tickets!")
            self.login_screen()
        else:
            # Otherwise, it will show ticket selection screen
            self.view.build_ticket_menu(self.model.get_ticket_info())

    #show the Admin Dashboard
    def show_admin_menu(self):
        #generate a summary of all ticket sales and pass it to the view
        ticket_sales = self.generate_ticket_sales_summary()
        self.view.build_admin_menu(ticket_sales)

    # ------------------- Account Management Logic -------------------

    #navigate to Add Account screen
    def add_account_screen(self):
        self.view.account_form("Add Account", "Create Account", self.add_account)

    #create a new account with provided credentials
    def add_account(self, username, password):
        # Check for missing input
        if not username or not password:
            self.view.show_error("Error", "Username and Password cannot be empty.")
            return

        #try adding the account via the model
        if self.model.add_account(username, password):
            self.view.show_message("Success", "Account created successfully.")
        else:
            self.view.show_error("Error", "Account already exists.")
        self.show_account_menu()

    #navigate to Login screen
    def login_screen(self):
        self.view.account_form("Login", "Login", self.login)

    #aalidate the login credentials
    def login(self, username, password):
        if self.model.validate_login(username, password):
            # Set session user in view
            self.view.logged_in_user = username
            self.view.show_message("Success", f"Welcome {username}!")
            self.view.build_main_menu()
        else:
            self.view.show_error("Login Failed", "Invalid username or password.")

    #navigate to Edit Account screen
    def edit_account_screen(self):
        self.view.account_form("Edit Account", "Update Password", self.edit_account)

    #update the password for existing account
    def edit_account(self, username, new_password):
        if self.model.edit_account(username, new_password):
            self.view.show_message("Success", "Password updated.")
        else:
            self.view.show_error("Error", "Account not found.")
        self.show_account_menu()

    #navigate to Delete Account screen
    def delete_account_screen(self):
        self.view.delete_account_form(self.delete_account)

    #delete a user account
    def delete_account(self, username):
        if self.model.delete_account(username):
            self.view.show_message("Deleted", "Account deleted successfully.")
        else:
            self.view.show_error("Error", "Account not found.")
        self.show_account_menu()

    #display the list of all customers and their order count
    def display_customer_details(self):
        #duild a dictionary: {username: number of orders}
        customers = {user: self.model.get_customer_orders_count(user)
                     for user in self.model.get_all_customers()}
        self.view.display_customers(customers)

    #show screen to delete individual orders
    def delete_orders_screen(self):
        orders = self.model.get_orders()
        self.view.display_orders(orders, self.delete_order)

    #delete a specific order by index
    def delete_order(self, index):
        if self.model.delete_order(index):
            self.view.show_message("Deleted", "Order deleted successfully.")
        else:
            self.view.show_error("Error", "Could not delete order.")
        self.delete_orders_screen()

    # ------------------- Ticket Purchasing Logic -------------------

    #this handle the ticket purchasing process
    def purchase_ticket(self):
        try:
            #converting quantity input to integer
            quantity = int(self.view.quantity_entry.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            self.view.show_error("Error", "Enter a valid quantity.")
            return

        #gather all details from view
        ticket_type = self.view.selected_ticket.get()
        payment_method = self.view.payment_method.get()
        username = self.view.logged_in_user

        #process purchase in model and get total cost
        total_cost = self.model.purchase_ticket(username, ticket_type, quantity, payment_method)
        self.view.show_message("Purchase Successful", f"Total cost: ${total_cost}")
        self.view.build_main_menu()

    # ------------------- Admin Discount Logic -------------------

    #apply 50% discount to all ticket types
    def apply_discount(self):
        self.model.apply_discount_to_all()
        self.view.show_message("Discount Applied", "All tickets are now 50% off.")

    #remove the discount and restore original ticket prices
    def disable_discount(self):
        self.model.disable_discount_to_all()
        self.view.show_message("Discount Disabled", "Ticket prices restored.")

    # ------------------- Group Sales Summary -------------------

    #create a report of all ticket sales grouped by date and type
    def generate_ticket_sales_summary(self):
        summary = {}  # Format: {date: {ticket_type: quantity}}

        for order in self.model.get_orders():
            date = order.get("date", "Unknown")
            ticket_type = order.get("ticket_type", "Unknown")
            quantity = order.get("quantity", 0)

            if date not in summary:
                summary[date] = {}
            summary[date][ticket_type] = summary[date].get(ticket_type, 0) + quantity

        return summary

# ------------------- Main Program Entry Point -------------------

#start the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    TicketBookingController(root)  # Instantiate the controller (this triggers the whole app)
    root.mainloop()  # Start the Tkinter event loop (GUI runs here)