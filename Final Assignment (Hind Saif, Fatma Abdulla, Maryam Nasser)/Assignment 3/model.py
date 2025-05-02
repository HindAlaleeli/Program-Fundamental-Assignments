# Import necessary modules
import pickle  # this is used for serializing (saving) and deserializing (loading) Python objects to/from files
from datetime import datetime  # this is used to get the current date and time

# ---------- File Utility Functions ----------

#a function to save data to a binary (.pkl) file
def save_data(file_name, data):
    #Save data to a pickle file
    try:
        with open(file_name, 'wb') as file:  # open the file in write-binary mode
            pickle.dump(data, file)  # save the Python object to the file
    except Exception as e:  # catch any errors during saving
        raise IOError(f"Could not save data: {e}")  # Raise an error

#a function to load data from a binary (.pkl) file
def load_data(file_name):
    #Load data from a pickle file
    try:
        with open(file_name, 'rb') as file:  # open the file in read-binary mode
            data = pickle.load(file)  # load the object from the file

            # check what type of object is expected based on the filename
            if 'accounts' in file_name:
                return data if isinstance(data, dict) else {}  # expect a dictionary for accounts
            elif 'orders' in file_name:
                return data if isinstance(data, list) else []  # expect a list for orders
            return data
    except FileNotFoundError:  # if the file does not exist
        return {} if 'accounts' in file_name else []  # return an empty structure depending on file type
    except Exception as e:  # catch all other errors
        raise IOError(f"Could not load data: {e}")  # Raise error

# ---------- Classes ----------

class TicketBookingModel:
    ''' a class the represents the data logic for ticket booking'''
    def __init__(self):
        #define filenames for storing account and order data
        self.accounts_file = "accounts.pkl"
        self.orders_file = "orders.pkl"

        #load the existing data from files (or initialize empty if not found)
        self.accounts = load_data(self.accounts_file)  # Dictionary: {username: password}
        self.orders = load_data(self.orders_file)  # List of order dictionaries

        #define the available ticket types and their details
        self.tickets = {
            "Single Race Pass": {
                "price": 120,
                "validity": "One Day",
                "features": "Access to one race",
                "discount": False
            },
            "Weekend Package": {
                "price": 300,
                "validity": "Three Days",
                "features": "All races during the weekend",
                "discount": False
            },
            "Season Membership": {
                "price": 1200,
                "validity": "Full Season",
                "features": "Access to all season races",
                "discount": False
            },
            "Group Discount Pack": {
                "price": 1000,
                "validity": "One Day",
                "features": "10 tickets at a discounted rate",
                "discount": True
            }
        }

    # ---------- Account Management ----------

    #add a new account to the system
    def add_account(self, username, password):
        if username in self.accounts:  # do not allow duplicate usernames
            return False
        self.accounts[username] = password  # add new user
        save_data(self.accounts_file, self.accounts)  # save the updated accounts
        return True

    #checking if login credentials are valid
    def validate_login(self, username, password):
        return username in self.accounts and self.accounts[username] == password

    #update the password for an existing account
    def edit_account(self, username, new_password):
        if username in self.accounts:
            self.accounts[username] = new_password  # Update password
            save_data(self.accounts_file, self.accounts)
            return True
        return False

    #remove an account from the system
    def delete_account(self, username):
        if username in self.accounts:
            del self.accounts[username]  # Delete user
            save_data(self.accounts_file, self.accounts)
            return True
        return False

    #return a list of all usernames
    def get_all_customers(self):
        return self.accounts.keys()

    # ---------- Orders Management ----------

    #create a new ticket order and save it
    def purchase_ticket(self, username, ticket_type, quantity, payment_method):
        price = self.tickets[ticket_type]["price"]  #get the unit price for the selected ticket
        total_cost = price * quantity  #calculate total cost
        order = {
            "username": username,
            "ticket_type": ticket_type,
            "quantity": quantity,
            "total_cost": total_cost,
            "payment_method": payment_method,
            "date": datetime.now().strftime("%Y-%m-%d")  #save order date as string
        }
        self.orders.append(order)  #add the order to the list
        save_data(self.orders_file, self.orders)  #save updated orders
        return total_cost

    #return all saved orders
    def get_orders(self):
        return self.orders

    #delete an order by its index in the list
    def delete_order(self, index):
        if 0 <= index < len(self.orders):  # make sure that the index is valid
            del self.orders[index]
            save_data(self.orders_file, self.orders)
            return True
        return False

    #count how many orders a specific user has made
    def get_customer_orders_count(self, username):
        return len([order for order in self.orders if order["username"] == username])

    # ---------- Discount Management ----------

    # apply a 50% discount to all ticket prices
    def apply_discount_to_all(self):
        for ticket in self.tickets.values():
            if "original_price" not in ticket:  #store the original price if not already stored
                ticket["original_price"] = ticket["price"]
            ticket["price"] = ticket["price"] // 2  #apply discount (integer division)

    #restore all ticket prices to their original values (without the discount)
    def disable_discount_to_all(self):
        for ticket in self.tickets.values():
            if "original_price" in ticket:
                ticket["price"] = ticket["original_price"]  # Restore price
                del ticket["original_price"]  #remove the temporary key

    # ---------- Ticket Info Getter ----------

    #return the full ticket dictionary
    def get_ticket_info(self):
        return self.tickets