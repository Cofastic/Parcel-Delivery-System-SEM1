#provides methods for encoding and decoding JSON (JavaScript Object Notation) data
import json
#commonly used in function annotations or variable type hints.
from typing import List
#used for formatting and displaying data in a tabular way and
# in a visually appealing way, especially in the console or terminal.
from tabulate import tabulate
# used for date times
from datetime import datetime

# File names for data storing
CUSTOMERS_FILE = 'customers.json'
PARCELS_FILE = 'parcels.json'
BILLS_FILE = 'bills.json'
def reset_system(system):
    confirmation = input("Are you sure you want to reset all parcels and bills? (yes/no): ")

    if confirmation.lower() == 'yes':
        # Clear parcels and bills data
        system["parcels"] = []
        system["bills"] = []

        # Reset current parcel and consignment numbers to default
        system["current_consignment_number"] = 10000000
        system["current_parcel_number"] = 10000000

        # Reset current bill number to default
        system["current_bill_id"] = 10000000

        # Save changes to files
        save_parcels_to_file(system)
        save_bills_to_file(system)

        print("Parcels, bills, and counters reset successfully!")
    else:
        print("Reset operation canceled.")
def initialize_system():
#creates and returns a dictionary representing the initial state of a system.
    return {
        "users": [],                  # List to store user information
        "current_user": None,         # Variable to store information about the currently logged-in user
        "customers": [],              # List to store customer information
        "current_customer_id": 1,     # Variable to keep track of the current customer ID
        "parcels": [],                # List to store information about parcels
        "current_consignment_number": 10000000,  # Default Variable to keep track of the current consignment number
        "current_parcel_number": 10000000,       # Default Variable to keep track of the current parcel number
        "bills": [],                  # List to store information about bills
        "current_bill_id": 1,         # Variable to keep track of the current bill ID
    }

def login(system, username, password):
# the login function searches for a user with the provided username and password inputted by the user
# in the list of users (system["users"]).
#If a match is found, it sets the "current_user" in the system and returns True; otherwise, it returns False
    for user in system["users"]:
        if user["username"] == username and user["password"] == password:
            system["current_user"] = user
            return True
    return False

def add_user(system, username, password, role="operator"):
#the function add_user provides a way to add a new user to the system by providing a username, password,
# and an optional role  (default is operator). The new user details are then added to the "users" list in the system dictionary
    system["users"].append({"username": username, "password": password, "role": role})
def assign_admin_role(system, index):
    #the function assign_admin_role is used to assigning the administrator role to a user in the system,
    #provided that the index is valid and the user does not already have the administrator role.
    if 0 <= index < len(system["users"]):
        #Check if the provided index is valid (within the range of the "users" list)
        user = system["users"][index]
        if user["role"] != "administrator":
            # If the user does not already have the administrator role, assign it
            user["role"] = "administrator"
            print("Administrator role assigned successfully!")
        else:
        # If the user already has the administrator role, notify the user
            print("User already has administrator role.")
    else:
#If the provided index is invalid, notify the user
        print("Invalid user index!")

def remove_admin_role(system, index):
#the function remove_admin_role works pretty much the same as the assign_admin_role
#difference is that this function would be used to removing the administrator role from a user in the system,
#provided that the index is valid and the user currently has the administrator role.
    if 0 <= index < len(system["users"]):
        user = system["users"][index]
        if user["role"] == "administrator":
            user["role"] = "operator"
            print("Administrator role removed successfully!")
        else:
            print("User does not have administrator role.")
    else:
        print("Invalid user index!")

def delete_user(system, index):
#Delete_user function allows for the deletion of a user from the system,
# provided that the index is valid. If the index is not valid, it will notify the user that the index is invalid
    if 0 <= index < len(system["users"]):
        # Check if the provided index is valid (within the range of the "users" list)
        del system["users"][index]
        # Delete the user at the specified index from the "users" list
        print("User deleted successfully!")
    else:
        # If the provided index is invalid, notify the user
        print("Invalid user index!")

def get_users_by_role(system, role):
#this function is used to filter users by roles. When calling this function, we would have to provide
#the correct role. Eg 'get_users_by_role(system, 'administrator'), this will return a list of users
#that are assigned as administrators
    filtered_users = [user for user in system["users"] if user["role"] == role]
    return filtered_users

def get_all_users(system):
#this function is used to show all users combined
    return system["users"]

def save_users_to_file(system):
#The function save_users_to_file saves the information of users in a computer system to a file named 'users.json'.
#It takes the user data from the system, opens the file, and writes the data in a format that can be easily read and loaded later.
# Extract the list of users from the system dictionary
    data = system["users"]
# Open 'users.json' file in write mode ('w') and create a context using 'with' to ensure the proper file handling
    with open('users.json', 'w') as file:
    # Serialize the user data (a list of dictionaries) and write it to the file in JSON format
        json.dump(data, file)

def load_users_from_file(system):
# this function would attempt to load user data from a file, afterwards
# assigns it to the 'users' key in the system dictionary, and ignores the error FileNotFoundError if the file is not present.
#This prevents the program to crash if the file does not exist when trying to load users.
    try:
        # Attempt to open the 'users.json' file for reading
        with open('users.json', 'r') as file:
            # Load the data from the file using JSON parsing
            data = json.load(file)
            # Assign the loaded user data to the "users" key in the system dictionary
            system["users"] = data
    except FileNotFoundError:
        # If the file is not found, ignore the error (FileNotFoundError)
        pass

# Pricing functions
table_price = [
    ['Zone A', 'RM8.00', 'RM16.00', 'RM18.00'],
    ['Zone B', 'RM9.00', 'RM18.00', 'RM20.00'],
    ['Zone C', 'RM10.00', 'RM20.00', 'RM22.00'],
    ['Zone D', 'RM11.00', 'RM22.00', 'RM24.00'],
    ['Zone E', 'RM12.00', 'RM24.00', 'RM26.00']
]

def modify_price(zone, new_above_3kg_price):
# This function modifies the price for parcels in a specific zone, specifically the price above 3kg.
# When it finds the row (zone) that matches the provided 'zone' by the user, it updates the price above 3kg with the new value.
    for row in table_price:
        # Iterate through each row (zone) in the 'table_price' list.
        if row[0] == zone:
            # Check if the current row (zone) matches the provided 'zone' that the user has input.
            row[-1] = new_above_3kg_price
            # Update the last element of the row (price above 3kg), with the new price.
def delete_price(zone):
    # This function is designed to delete the pricing information for a specific zone, particularly the price above 3kg.
    for row in table_price:
        # Iterate through each row (zone) in the 'table_price' list.
        if row[0] == zone:
            # Check if the current row (zone) matches the provided 'zone' that the user inputted.
            row[-1] = ''
            # Set the last element of the row (price above 3kg) to an empty string, deleting it.


def check_price(zone, weight):
    # This function is designed to check the pricing for a specific zone based on the weight of a parcel.
    #Depending on the given weight by the user it will return the correspoding price. If the provided 'Zone' is not
    #found in the list, system will return 'None'.
    for row in table_price:
        # Iterates through each row (zone) in the 'table_price' list.
        if row[0] == zone:
            # Check if the current row (zone) matches the provided 'zone' that the user has inputted.
            if weight < 1:
                #if weight < 1kg
                return row[1]
            elif 1 <= weight <= 3:
                #if weight 1kg - 3kg
                return row[2]
            else:
                #if weight above 3kg
                return row[3]
    return None


def save_pricing_to_file():
    # This function is designed to save the pricing information (table_price) to a JSON file.
    data = table_price
    # Store the pricing information (table_price) in the 'data' variable.
    with open('pricing.json', 'w') as file:
        # Open a file named 'pricing.json' for writing ('w' mode).
        json.dump(data, file)
        # Use the json.dump() function to write the 'data' (table_price) to the opened file in JSON format.


def load_pricing_from_file():
    # This function is designed to load pricing information from a JSON file into the 'table_price' list.
    try:
        with open('pricing.json', 'r') as file:
            #Try to open a file named 'pricing.json' for reading ('r' mode).
            data = json.load(file)
            #Use json.load() to load the data from the file and store it in the 'data' variable.
            table_price.clear()
            #Clear the existing content of the 'table_price' list.
            table_price.extend(data)
            #Extend the 'table_price' list with the loaded data from the file.
    except FileNotFoundError:
        # If the specified file is not found, catch the FileNotFoundError error
        pass
        # Do nothing if the file is not found, just continue with the program execution.


# Customer management functions
def initialize_customers():
#this function will initialize a data structure to manage customer information,
#starting with an empty list of customers and an starting customer ID of 1.
    return {"customers": [], "current_customer_id": 1}

def add_customer(system, name, address, telephone):
    # Find the highest customer ID
    highest_customer_id = max(customer["id"] for customer in system["customers"]) if system["customers"] else 0
    # Assign the next available customer ID
    customer_id = highest_customer_id + 1
    # Create a dictionary representing the new customer
    customer = {"id": customer_id, "name": name, "address": address, "telephone": telephone}
    # Append/Add the new customer to the list of customers in the system
    system["customers"].append(customer)
    return customer_id

def modify_customer(system, customer_id, address, telephone):
    # Iterate through the list of customers in the system
    for customer in system["customers"]:
        # Check if the current customer's ID matches the specified customer_id
        if customer["id"] == customer_id:
            # Modify the address and telephone of the matched customer
            customer["address"] = address
            customer["telephone"] = telephone
            # Notifies the user
            print("Customer details modified successfully!")
            # Exit the function after modifying the customer
            return
    # If no customer with the specified ID is found, it will notify the user by printing
    print("Customer not found.")

def view_customers(system):
    #check if the list of customers is empty
    if not system["customers"]:
        #Print a message if there are no customers
        print("No customers available.")
    else:
        #headers for the tabulated output
        headers = ["Customer ID", "Name", "Address", "Telephone"]
        #Creates a list of lists containing customer data for tabulation
        customer_data = [
            [customer["id"], customer["name"], customer["address"], customer["telephone"]]
            for customer in system["customers"]
        ]
        # Print the tabulated customer data with headers
        print(tabulate(customer_data, headers=headers, tablefmt="grid"))

def load_customers_from_file(system):
    try:
        # Attempt to open a file named CUSTOMERS_FILE in read mode
        with open(CUSTOMERS_FILE, 'r') as file:
            # Load JSON data from the file
            data = json.load(file)
            # Update the system's customers list with the loaded data
            system["customers"] = data["customers"]
            # Update the system's current_customer_id with the loaded data
            system["current_customer_id"] = data["current_customer_id"]
    except FileNotFoundError:
        # If the specified file is not found, do nothing (pass)
        pass

def save_customers_to_file(system):
    # Create a dictionary containing customers and current_customer_id
    data = {"customers": system["customers"], "current_customer_id": system["current_customer_id"]}
    # Open the CUSTOMERS_FILE in write mode and write the that will be saved as .JSON format
    with open(CUSTOMERS_FILE, 'w') as file:
        json.dump(data, file)

def initialize_parcels():
    return {"parcels": [], "current_consignment_number": 10000000, "current_parcel_number": 10000000}

def add_parcel(system, customer_id, zone, weight, sender_name, sender_address, sender_telephone):
    # Generates unique consignment and parcel numbers
    consignment_number = generate_unique_consignment_number(system)
    parcel_number = generate_unique_parcel_number(system)
    # Checks the price based on the zone and weight
    price = check_price(zone, weight)
    if price is not None:
        parcel = {
            "consignment_number": consignment_number,
            "parcel_number": parcel_number,
            "customer_id": customer_id,
            "zone": zone,
            "weight": weight,
            "sender_name": sender_name,
            "sender_address": sender_address,
            "sender_telephone": sender_telephone,
            "price": price,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        system["parcels"].append(parcel)

        # Generate bill for the consignment
        generate_bill(system, consignment_number)

        return consignment_number, parcel_number
    else:
        print("Invalid zone or weight for pricing. Cannot add parcel.")
        return None

def modify_parcel(system, consignment_number, parcel_number):
    # Iterates over the parcels in the system
    for i, parcel in enumerate(system["parcels"]):
        # Checks if the consignment and parcel numbers match
        if parcel["consignment_number"] == consignment_number and parcel["parcel_number"] == parcel_number:
            # Displays current parcel details and asks for modification option
            print("Current Parcel Details:")
            print(f"1. Sender's Name: {parcel['sender_name']}")
            print(f"2. Sender's Address: {parcel['sender_address']}")
            print(f"3. Sender's Telephone: {parcel['sender_telephone']}")
            print(f"4. zone: {parcel['zone']}")
            print(f"5. Weight: {parcel['weight']} kg")

            modification_option = input("Enter the number of the detail to modify (or '0' to cancel): ")

            if modification_option == '0':
                print("Modification canceled.")
                return

            if modification_option == '1':
                new_sender_name = input("Enter the new sender's name: ")
                parcel["sender_name"] = new_sender_name
            elif modification_option == '2':
                new_sender_address = input("Enter the new sender's address: ")
                parcel["sender_address"] = new_sender_address
            elif modification_option == '3':
                new_sender_telephone = input("Enter the new sender's telephone: ")
                parcel["sender_telephone"] = new_sender_telephone
            elif modification_option == '4':
                new_zone = input("Enter the new zone: ")
                parcel["zone"] = new_zone
                # Update the price after changing the zone
                parcel["price"] = check_price(new_zone, parcel["weight"])
            elif modification_option == '5':
                new_weight = float(input("Enter the new weight: "))
                parcel["weight"] = new_weight
                # Update the price after changing the weight
                parcel["price"] = check_price(parcel["zone"], new_weight)

            # Save changes to files
            save_parcels_to_file(system)
            generate_bill(system, consignment_number)  # Update the bill with modified details
            print("Parcel details modified successfully!")
            return
    # If no matching parcel is found, prints an error message
    print(f"Parcel with Consignment Number {consignment_number} and Parcel Number {parcel_number} not found.")

def view_parcels(system):
    if not system["parcels"]:
        print("No parcels available.")
    else:
        # Defines headers for the parcel data
        headers = ["Consignment Number", "Parcel Number", "Customer ID", "zone", "Weight", "Sender Name", "Sender Address", "Sender Telephone", "Price", "Date"]
        # Creates a list of lists containing parcel data
        parcel_data = [[
            parcel["consignment_number"],
            parcel["parcel_number"],
            parcel["customer_id"],
            parcel["zone"],
            parcel["weight"],
            parcel["sender_name"],
            parcel["sender_address"],
            parcel["sender_telephone"],
            parcel["price"],
            parcel["date"]
        ] for parcel in system["parcels"]]
        # Prints the parcel data in a tabulated format
        print(tabulate(parcel_data, headers=headers, tablefmt="grid"))


def load_parcels_from_file(system):
    try:
        with open(PARCELS_FILE, 'r') as file:
            # Loads parcel data from a file and updates the system
            data = json.load(file)
            system["parcels"] = data["parcels"]
            system["current_consignment_number"] = data["current_consignment_number"]
            system["current_parcel_number"] = data["current_parcel_number"]
    except FileNotFoundError:
    #if the file is not found, do nothing
        pass


def save_parcels_to_file(system):
    # Prepares parcel data and current consignment & parcel number for saving
    data = {
        "parcels": system["parcels"],
        "current_consignment_number": system["current_consignment_number"],
        "current_parcel_number": system["current_parcel_number"]
    }
    with open(PARCELS_FILE, 'w') as file:
        # Saves parcel data to a file .json format
        json.dump(data, file)

def generate_unique_parcel_number(system):
    system["current_parcel_number"] = 10000000  # Set the initial value
    while True:
        # Generates a new parcel number based on the current value
        parcel_number = system["current_parcel_number"]
        system["current_parcel_number"] += 1
        new_parcel_number = f'P{parcel_number}'
        # Checks if the generated parcel number is already in use
        if not any(parcel["parcel_number"] == new_parcel_number for parcel in system["parcels"]):
            return new_parcel_number
def create_consignment(system):
    view_customers(system)
    try:
        # Asks for customer ID input
        customer_id = int(input("Enter the customer ID on where the consignment will be made in: "))
        # Finds the customer with the specified ID
        customer = next((c for c in system["customers"] if c["id"] == customer_id), None)
        if customer:
            # Asks for details to create a parcel
            zone = input("Enter zone: ")
            weight = float(input("Enter weight of the parcel: "))
            sender_name = input("Enter sender's name: ")
            sender_address = input("Enter sender's address: ")
            sender_telephone = input("Enter sender's telephone: ")

            # Adds the parcel and obtains consignment and parcel numbers
            consignment_number, parcel_number = add_parcel(system, customer_id, zone, weight, sender_name, sender_address, sender_telephone)
            if consignment_number:
                print(f"Consignment created successfully! Number: {consignment_number}, Parcel Number: {parcel_number}")
            else:
                print("Failed to create consignment.")
        else:
            print("Customer not found.")
    except ValueError:
        print("Invalid input. Please enter a valid customer ID.")


def generate_unique_consignment_number(system):
    system["current_consignment_number"] = 10000000  # Set the initial value
    while True:
        consignment_number = system["current_consignment_number"]
        system["current_consignment_number"] += 1
        new_consignment_number = f'{consignment_number}'  # Use f-string for correct formatting

        # Check if the generated consignment number is already in use
        if not any(consignment["consignment_number"] == new_consignment_number for consignment in system["parcels"]):
            return new_consignment_number

def delete_parcel_within_consignment(system, consignment_number):
    # Displays the bill for the specified consignment
    view_bill(system, consignment_number)
    # Asks the user to input the parcel number to delete
    parcel_number_to_delete = input("Enter the parcel number to delete within this consignment: ")

    for i, parcel in enumerate(system["parcels"]):
        # Checks if the parcel is in the specified consignment and has the specified parcel number
        if parcel["consignment_number"] == consignment_number and parcel["parcel_number"] == parcel_number_to_delete:
            # Deletes the parcel from the system
            del system["parcels"][i]
            print(f"Parcel {parcel_number_to_delete} deleted successfully from the consignment {consignment_number}!")

            # Save changes to files
            save_parcels_to_file(system)
            generate_bill(system, consignment_number)  # Update the bill after deleting the parcel
            return
    print(f"Parcel {parcel_number_to_delete} not found in the consignment {consignment_number}.")

def delete_parcel_from_bill(system, consignment_number, parcel_number):
    for i, parcel in enumerate(system["parcels"]):
        # Checks if the parcel is in the specified consignment and has the specified parcel number
        if parcel["consignment_number"] == consignment_number and parcel["parcel_number"] == parcel_number:
            # Deletes the parcel from the system
            del system["parcels"][i]
            print("Parcel deleted successfully from the bill!")

            # Save changes to files
            generate_bill(system, consignment_number)  # Update the bill after deleting the parcel
            return
    print("Parcel not found in the bill.")


def generate_bill(system, consignment_number):
    # Initialize a bill with default values
    bill = {
        "consignment_number": consignment_number,
        "date": datetime.now().strftime("%d/%m/%Y"),
        "customer_name": None,
        "customer_address": None,
        "customer_telephone": None,
        "items": []
    }

    # Initialize variables to calculate total amount
    total_amount = 0

    # Iterate over parcels in the system
    for parcel in system["parcels"]:
        # Check if the parcel belongs to the specified consignment
        if parcel["consignment_number"] == consignment_number:
            # Assign customer details once (assuming all parcels in a consignment belong to the same customer)
            if bill["customer_name"] is None:
                # Find the customer associated with the parcel
                customer = next((c for c in system["customers"] if c["id"] == parcel["customer_id"]), None)
                if customer:
                    # Assign customer details to the bill
                    bill["customer_name"] = customer["name"]
                    bill["customer_address"] = customer["address"]
                    bill["customer_telephone"] = customer["telephone"]

            # Create an item for the bill based on parcel details
            item = {
                "parcel_number": parcel["parcel_number"],
                "receiver_name": parcel["sender_name"],  # Assuming sender_name is the receiver's name
                "receiver_address": parcel["sender_address"],  # Assuming sender_address is the receiver's address
                "receiver_telephone": parcel["sender_telephone"],  # Assuming sender_telephone is the receiver's telephone
                "zone": parcel["zone"],
                "weight": parcel["weight"],
                "price": float(parcel["price"].replace('RM', ''))  # Extract the numeric value from the price string
            }

            # Add the item to the bill's items list
            bill["items"].append(item)
            # Update the total amount with the item's price
            total_amount += item["price"]

    # Calculate 8% service tax
    service_tax = total_amount * 0.08
    # Calculate the total amount with tax
    total_amount_with_tax = total_amount + service_tax

    # Update the bill with total amount, service tax, and total amount with tax
    bill["total_amount"] = total_amount
    bill["service_tax"] = service_tax
    bill["total_amount_with_tax"] = total_amount_with_tax

    # Add the generated bill to the system's bills
    system["bills"].append(bill)
    # Print a success message
    print("Bill generated successfully!")


def print_pricing_table():
    # Define the headers for the pricing table
    headers = ["zone", "Below 1kg", "1-3kg", "Above 3kg"]
    # Print the pricing table using the tabulate function
    print(tabulate(table_price, headers=headers, tablefmt="grid"))

# Bill management functions
def view_bill(system, consignment_number):
    total_amount = 0  # Initialize the total amount for the bill
    headers = ["Parcel Number", "Receiver Name", "Receiver Address", "Receiver Telephone", "zone", "Weight", "Price"]
    bill_data = []  # Initialize an empty list to store bill items

    # Iterate through parcels in the system
    for parcel in system["parcels"]:
        if parcel["consignment_number"] == consignment_number:
            # Create an item for the bill with relevant parcel information
            item = [
                parcel["parcel_number"],
                parcel["sender_name"],  # Assuming sender_name is the receiver's name
                parcel["sender_address"],  # Assuming sender_address is the receiver's address
                parcel["sender_telephone"],  # Assuming sender_telephone is the receiver's telephone
                parcel["zone"],
                parcel["weight"],
                parcel["price"]
            ]
            bill_data.append(item)  # Add the item to the list of bill items
            total_amount += float(parcel["price"].replace('RM', ''))  # Update the total amount

    # Display the bill items in a tabular format
    print(f"Bill for Consignment Number: {consignment_number}")
    print(tabulate(bill_data, headers=headers, tablefmt="grid"))
    # Display total amount, service tax, and total amount with tax
    service_tax = total_amount * 0.08
    total_amount_with_tax = total_amount + service_tax
    print(f"Total Amount: RM {total_amount:.2f}")
    print(f"Service Tax (8%): RM {service_tax:.2f}")
    print(f"Total Amount with Tax: RM {total_amount_with_tax:.2f}")


def view_bills_by_customer(system, customer_id):
    total_amount = 0  # Initialize the total amount for the bills
    headers = ["Consignment Number", "Parcel Number", "Receiver Name", "Receiver Address", "Receiver Telephone", "zone",
               "Weight (KG)", "Price (RM)"]
    bill_data = []  # Initialize an empty list to store bill items

    # Iterate through parcels in the system
    for parcel in system["parcels"]:
        if parcel["customer_id"] == customer_id:
            # Convert the price to float for calculations
            price = float(parcel["price"].replace('RM', ''))

            # Add parcel details to the bill_data list
            bill_data.append([
                parcel["consignment_number"],
                parcel["parcel_number"],
                parcel["sender_name"],
                parcel["sender_address"],
                parcel["sender_telephone"],
                parcel["zone"],
                parcel["weight"],
                price  # Use the converted price in calculations
            ])

            total_amount += price  # Update the total amount

    # Calculate 8% service tax
    service_tax = total_amount * 0.08
    total_amount_with_tax = total_amount + service_tax

    # Display the bill items in a tabular format
    print(tabulate(bill_data, headers=headers, tablefmt="grid"))

    # Display total amount, service tax, and total amount with tax
    print(f"Total Amount: RM{total_amount:.2f}")
    print(f"Service Tax (8%): RM{service_tax:.2f}")
    print(f"Total Amount with Tax: RM{total_amount_with_tax:.2f}")


def view_bills_by_date(system, start_date, end_date):
    total_amount = 0  # Initialize the total amount for the bills
    headers = ["Consignment Number", "Parcel Number", "zone", "Weight", "Price"]
    bill_data = []  # Initialize an empty list to store bill items

    # Convert start_date and end_date strings to datetime objects
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    # Iterate through parcels in the system
    for parcel in system["parcels"]:
        parcel_date = datetime.strptime(parcel["date"], "%Y-%m-%d")

        # Check if the parcel date is within the specified range
        if start_datetime <= parcel_date <= end_datetime:
            # Add parcel details to the bill_data list
            bill_data.append([
                parcel["consignment_number"],
                parcel["parcel_number"],
                parcel["zone"],
                parcel["weight"],
                parcel["price"]
            ])
            total_amount += parcel["price"]  # Update the total amount

    # Display the bill items in a tabular format
    print(tabulate(bill_data, headers=headers, tablefmt="grid"))
    print(f"Total Amount: {total_amount}")

def load_bills_from_file(system):
# Load bills data from a file into the system
    try:
        # Attempt to open the specified file for reading
        with open(BILLS_FILE, 'r') as file:
            # Load JSON data from the file into a Python dictionary
            data = json.load(file)
            # Update the system's bills with the loaded data
            system["bills"] = data["bills"]
    except FileNotFoundError:
        # If the file is not found, do nothing (no bills data to load)
        pass

def save_bills_to_file(system):
# Save bills data from the system to a file
    # Create a dictionary containing the system's bills data
    data = {"bills": system["bills"]}
    # Open the specified file for writing
    with open(BILLS_FILE, 'w') as file:
        # Write the JSON representation of the data to the file
        json.dump(data, file)


# Main program
#this part of the code initializes a system and loads existing user, customer,
#parcel, bill, and pricing data from files to set up the initial state of the program.
system = initialize_system()
#creates a dictionary representing the initial state of the system.x
load_users_from_file(system)
#loads user data from 'users.json' into the system.
load_customers_from_file(system)
#loads customer data from 'customers.json' into the system.
load_parcels_from_file(system)
#loads parcel data from 'parcels.json' into the system.
load_bills_from_file(system)
#loads bill data from 'bills.json' into the system.
load_pricing_from_file()
#loads pricing data from 'pricing.json'.
while True:
    username = input("Enter your username (or type 'exit' to quit): ")
    if username.lower() == 'exit':
        # Save customers before exiting
        save_customers_to_file(system)
        break

    password = input("Enter your password: ")

    if login(system, username, password):
        if system["current_user"]["role"] == 'administrator':
            print("Welcome, Administrator:", system["current_user"]["username"])
        else:
            print("Welcome, Operator:", system["current_user"]["username"])

        while True:
            if system["current_user"]["role"] == 'operator':
                print("What would you like to do?")
                print("1. Add customer details")
                print("2. Modify customer address and telephone number")
                print("3. View list of customers")
                print("4. Check price of a parcel")
                print("5. Generate list of parcels received")
                print("6. View bills by customer")
                print("7. View bills by date range")
                print("8. Delete a parcel")
                print("9. Create Consignment")
                print("10. Modify Parcel")
                print("11. Logout")

                operator_choice = input("Enter the option number: ")

                if operator_choice == '1':
                    # Option 1: Add a new customer
                    name = input("Enter customer name: ")
                    address = input("Enter customer address: ")
                    telephone = input("Enter customer telephone: ")
                    add_customer(system, name, address, telephone)

                elif operator_choice == '2':
                    # Option 2: Modify an existing customer
                    view_customers(system)
                    customer_id = int(input("Enter the customer ID to modify: "))
                    if customer_id not in (customer["id"] for customer in system["customers"]):
                        print("Customer not found.")
                    else:
                        address = input("Enter new address: ")
                        telephone = input("Enter new telephone number: ")
                        modify_customer(system, customer_id, address, telephone)

                elif operator_choice == '3':
                    # Option 3: View the list of customers
                    view_customers(system)

                elif operator_choice == '4':
                    # Option 4: Calculate and display the price for a parcel
                    zone = input("Enter zone: ")
                    weight = float(input("Enter weight of the parcel: "))
                    price = check_price(zone, weight)
                    if price is not None:
                        print(f"The price for the parcel is: {price}")
                    else:
                        print("Invalid zone or weight for pricing. Cannot calculate price.")

                elif operator_choice == '5':
                    # Option 5: View the list of parcels
                    view_parcels(system)

                elif operator_choice == '6':
                    # Option 6: View bills for a specific customer
                    customer_id = int(input("Enter customer ID: "))
                    if customer_id not in (customer["id"] for customer in system["customers"]):
                        print("Customer not found.")
                    else:
                        view_bills_by_customer(system, customer_id)

                elif operator_choice == '7':
                    # Option 7: View bills within a date range
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    if start_date > end_date:
                        print("Invalid date range.")
                    elif start_date and end_date not in (parcel["date"] for parcel in system["parcels"]):
                        print("No bills found within the date range.")
                    else:
                        view_bills_by_date(system, start_date, end_date)

                elif operator_choice == '8':
                    # Option 8: Delete a parcel within a consignment
                    consignment_number = int(input("Enter consignment number: "))
                    if consignment_number in (parcel["consignment_number"] for parcel in system["parcels"]):
                        delete_parcel_within_consignment(system, consignment_number)
                    else:
                        print("Consignment number not found.")

                elif operator_choice == '9':
                    # Option 9: Create a new consignment
                    create_consignment(system)
                    save_parcels_to_file(system)
                    save_bills_to_file(system)

                elif operator_choice == '10':
                    # Option 10: Modify details of a parcel within a consignment
                    consignment_number = input("Enter the consignment number: ")
                    parcel_number = input("Enter the parcel number: ")
                    modify_parcel(system, consignment_number, parcel_number)

                elif operator_choice == '11':
                    # Option 11: Save data and exit
                    # Save data before logging out
                    save_customers_to_file(system)
                    save_parcels_to_file(system)
                    save_bills_to_file(system)
                    break

                else:
                    print("Invalid choice")

            elif system["current_user"]["role"] == 'administrator':
                print("What would you like to do?")
                print("1. Add user")
                print("2. Assign administrator role")
                print("3. Remove administrator role")
                print("4. Delete user")
                print("5. List of users")
                print("6. Show Pricing Table")
                print("7. Modify Pricing")
                print("8. Delete Pricing")
                print("9. Check Pricing")
                print("10. Logout")
                option = input("Enter the option number: ")

                if option == '1':
                    # Option 1: Add a new user
                    new_username = input("Enter the username for the new user: ")
                    new_password = input("Enter the password for the new user: ")
                    new_role = input("Enter the role for the new user (default: operator): ")
                    add_user(system, new_username, new_password, new_role)
                    print("User added successfully!")
                    save_users_to_file(system)

                elif option == '2':
                    # Option 2: Assign administrator role to an existing user
                    users = get_all_users(system)
                    if len(users) == 0:
                        print("No operators available to assign as administrators.")
                    else:
                        print("Choose a user to assign as an administrator:")
                        for i, user in enumerate(users):
                            print(f"{i + 1}. {user['username']} (Role: {user['role']})")
                        user_index = int(input("Enter the user number: ")) - 1
                        assign_admin_role(system, user_index)
                        save_users_to_file(system)

                elif option == '3':
                    # Option 3: Remove administrator role from an existing administrator
                    users = get_all_users(system)
                    if len(users) == 0:
                        print("No administrators available to remove the role.")
                    else:
                        print("Choose a user to remove administrator role:")
                        for i, user in enumerate(users):
                            print(f"{i + 1}. {user['username']} (Role: {user['role']})")
                        user_index = int(input("Enter the user number: ")) - 1
                        remove_admin_role(system, user_index)
                        save_users_to_file(system)

                elif option == '4':
                    # Option 4: Delete an existing user
                    if len(system["users"]) == 0:
                        print("No users available to delete.")
                    else:
                        print("Choose a user to delete:")
                        for i, user in enumerate(system["users"]):
                            print(f"{i + 1}. {user['username']}")
                        user_index = int(input("Enter the user number: ")) - 1
                        delete_user(system, user_index)
                        save_users_to_file(system)

                elif option == '5':
                    # Option 5: Filter and display users based on role
                    filter_option = input("Filter users by role (admin/operator/all): ")
                    if filter_option.lower() == 'admin':
                        users = get_users_by_role(system, 'administrator')
                        print("List of administrators:")
                        for i, user in enumerate(users):
                            print(f"{i + 1}. {user['username']} (Role: {user['role']})")
                    elif filter_option.lower() == 'operator':
                        users = get_users_by_role(system, 'operator')
                        print("List of operators:")
                        for i, user in enumerate(users):
                            print(f"{i + 1}. {user['username']} (Role: {user['role']})")
                    elif filter_option.lower() == 'all':
                        if len(system["users"]) == 0:
                            print("No users available.")
                        else:
                            print("List of all users:")
                            for i, user in enumerate(system["users"]):
                                print(f"{i + 1}. {user['username']} (Role: {user['role']})")
                    else:
                        print("Invalid filter option!")

                elif option == '6':
                    # Option 6: Display the current pricing table
                    print("Current Pricing Table:")
                    headers = ['zone', 'Weight below 1kg', 'Weight in between 1kg to 3kg', 'Weight above 3kg']
                    print(tabulate(table_price, headers=headers, tablefmt="grid"))

                elif option == '7':
                    # Option 7: Modify the price for parcels above 3kg
                    modify_zone = input("\nEnter the zone to modify the price for parcels above 3kg: ")
                    new_price = input(f"Enter the new price for {modify_zone} (above 3kg): ")
                    modify_price(modify_zone, new_price)
                    save_pricing_to_file()

                elif option == '8':
                    # Option 8: Delete the price for parcels above 3kg
                    price_to_remove = input("\nEnter the zone to delete the price for parcels above 3kg: ")
                    delete_price(price_to_remove)
                    save_pricing_to_file()

                elif option == '9':
                    # Option 9: Check the price for a given zone and weight
                    zone_to_check = input("\nEnter the zone to check the price: ")
                    weight_to_check = float(input("Enter the weight of the parcel: "))
                    price = check_price(zone_to_check, weight_to_check)
                    if price:
                        print(f"The price for the parcel to {zone_to_check} weighing {weight_to_check}kg is: {price}")
                    else:
                        print("Invalid zone or weight for pricing.")

                elif option == '10':
                    # Option 10: Logout
                    print("Logging out...")
                    break
        else:
                print("Invalid username or password. Please try again.")

