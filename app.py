import json
from datetime import datetime

DATA_FILE = "customers.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_offer_valid(booking_time, ticket_count):
    offer_start_time = "2025-05-12T09:30:00"
    booking_dt = datetime.fromisoformat(booking_time)
    offer_start_dt = datetime.fromisoformat(offer_start_time)
    time_diff = (booking_dt - offer_start_dt).total_seconds()

    if ticket_count >= 4 and 0 <= time_diff <= 3600:
        return True
    else:
        return False

def add_customer():
    
    data = load_data()

    name = input("Enter your name: ").strip()
    if name in data:
        print("Customer already exists.")
        return

    count = int(input("Enter number of tickets: "))
    booking_time = datetime.now().isoformat()
    offer_applied = is_offer_valid(booking_time, count)

    # Get age and is_adult
    age = int(input(f"Enter age for {name}: "))
    is_adult = age >= 18

    members = [{
        "name": name,
        "age": age,
        "is_adult": is_adult
    }]

    data[name] = {
        "ticket_count": count,
        "members": members,
        "booking_time": booking_time,
        "offer_applied": offer_applied
    }

    save_data(data)

    print(f"{name} added with {count} tickets")
    if offer_applied:
        print("25% OFF applied!")
    else:
        print("No offer applied")

def add_member():
    data = load_data()
    name = input("Enter customer name: ").strip()
    customer = data.get(name)

    if not customer:
        print("Customer not found.")
        return

    while True:
        if len(customer["members"]) >= customer["ticket_count"]:
            print("Ticket limit reached. Cannot add more members.")
            break

        member_name = input("Enter member name (or 'done' to finish): ").strip()
        if member_name.lower() == "done":
            break

        age = int(input(f"Enter age for {member_name}: "))
        is_adult = age >= 18

        customer["members"].append({
            "name": member_name,
            "age": age,
            "is_adult": is_adult
        })

        print(f"{member_name} added successfully!")

    data[name] = customer
    save_data(data)

def gate_check():
    data = load_data()
    name = input("Enter customer name: ").strip()
    customer = data.get(name)

    if not customer:
        print("Customer not found.")
        return

    total_adults = 0
    total_kids = 0

    while True:
        visitor = input("Enter visitor name: ").strip()
        found = False

        for member in customer["members"]:
            if member["name"].lower() == visitor.lower():
                found = True
                if member['is_adult']:
                    adult = "Adult"
                else:
                    adult = "Kid"
                print(f"{visitor} allowed entry! (Age: {member['age']}, Adult / Kid: {adult})")
                if member["is_adult"]:
                    total_adults += 1
                else:
                    total_kids += 1
                break

        if not found:
            print(f"{visitor} not in the member list")

        again = input("Check another visitor? (yes/no): ").strip().lower()
        if again in ["yes", "y"]:
            continue
        elif again in ["no", "n"]:
            print("\n--- Ticket Summary ---")
            print(f"Adults Checked-in : {total_adults}")
            print(f"Kids Checked-in   : {total_kids}")

            adult_price = 1200
            kid_price = 900

            total_price = (total_adults * adult_price) + (total_kids * kid_price)

            if customer["offer_applied"]:
                print("Offer Applied: 25% Discount!")
                discount = total_price * 0.25
                total_price -= discount
            else:
                print("No Offer Applied")

            print(f"Final Ticket Amount: ₹{int(total_price)}")
            print("Gate Check Complete. Enjoy your time!")
            break
        else:
            print("Please type 'yes' or 'no'.")



def main():
    while True:
        print("\n--- Black Thunder Theme Park ---")
        print("1. Add a new customer")
        print("2. Add a member")
        print("3. Gate check")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            add_member()
        elif choice == "3":
            gate_check()
        elif choice == "4":
            print("Thank you! Come again to Black Thunder!")
            break
        else:
            print("Invalid choice. Try again.")

main()