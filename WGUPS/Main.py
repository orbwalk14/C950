"""
Cole Detrick
Student ID:011447776
"""

import csv
import datetime
from Hash import CreateHashMap
from Package import Package
from Truck import Truck

# function for loading CSV Data => 0(n)
def load_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

CSV_Distance = load_csv("CSV/distances_file.csv")
CSV_Address = load_csv("CSV/addresses_file.csv")
CSV_Package = load_csv("CSV/packages_file.csv")

# Load Package Data into Hash Table => O(n)
def load_package_data(package_hash_table, filename="CSV/packages_file.csv"):
    package_data = load_csv(filename)
    for package in package_data:
        pack_id = int(package[0])
        # Initial address for all packages (Package 9's address will be handled in its class now)
        pack_addr = package[1]
        pack_city = package[2]
        pack_state = package[3]
        pack_zip = package[4]
        pack_deadline = package[5]
        pack_weight = package[6]
        pack_status = "At Hub"
        pack_obj = Package(pack_id, pack_addr, pack_city, pack_state, pack_zip, pack_deadline, pack_weight, pack_status)
        package_hash_table.insert(pack_id, pack_obj)

# Function to change the address of a package
def change_package_address(package_hash_table, package_id, new_address, new_city, new_state, new_zip):
    package = package_hash_table.lookup(package_id)
    if package:
        package.address = new_address
        package.city = new_city
        package.state = new_state
        package.zipcode = new_zip

# Find Distance Between Addresses => O(1)
def distance_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value] or CSV_Distance[y_value][x_value]
    return float(distance)

def print_truck_mileage(trucks):
    for truck in trucks:
        truck.print_mileage()

# Get Address Number from Address String => O(n)
def get_address_number(address):
    return next(int(row[0]) for row in CSV_Address if address in row[2])

# Truck assignments - Package 9 will be handled separately
trucks = [
    Truck(1, 16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
          datetime.timedelta(hours=8)),  # Starts at 8:00 AM
    Truck(2, 16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East",
          datetime.timedelta(hours=9, minutes=5)),  # Starts at 9:05 AM
    Truck(3, 16, 18, None, [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
          datetime.timedelta(hours=10, minutes=20))  # Starts at 10:20 AM
]

# Load packages into hash table
pack_hash_table = CreateHashMap()
load_package_data(pack_hash_table)

def deliver_packages(truck):
    not_delivered = [pack_hash_table.lookup(packageID) for packageID in truck.packages]
    truck.packages.clear()

    while not_delivered:
        next_package = min(not_delivered, key=lambda package: distance_between(get_address_number(truck.address),
                                                                               get_address_number(package.address)))

        # Skip package 9 if current time is before 10:20 AM
        if next_package.ID == 9 and truck.time < datetime.timedelta(hours=10, minutes=20):
            not_delivered.remove(next_package)
            continue

        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)

        distance = distance_between(get_address_number(truck.address), get_address_number(next_package.address))
        travel_time = datetime.timedelta(hours=distance / 18.0)

        truck.mileage += distance
        truck.time += travel_time

        next_package.departure_time = truck.depart_time
        next_package.delivery_time = truck.time

        truck.address = next_package.address


# Function to handle package 9's delayed delivery
def handle_package_nine(trucks):
    # Package 9 is updated at 10:20
    change_package_address(pack_hash_table, 9, "410 S State St", "Salt Lake City", "UT", "84111")

    # Find the truck with the earliest available time after 10:20
    available_truck = min(trucks, key=lambda t: t.time if t.time >= datetime.timedelta(hours=10,
                                                                                       minutes=20) else datetime.timedelta(
        hours=24))

    # Add package 9 to the selected truck's route
    available_truck.packages.append(9)

    # Deliver the package
    package = pack_hash_table.lookup(9)
    distance = distance_between(get_address_number(available_truck.address), get_address_number(package.address))

    # Update delivery information
    available_truck.mileage += distance
    delivery_time = available_truck.time + datetime.timedelta(hours=distance / 18)
    package.departure_time = datetime.timedelta(hours=10, minutes=20)
    package.delivery_time = delivery_time
    available_truck.time = delivery_time
    available_truck.address = package.address


def find_package_truck(package_id, trucks):
    for truck in trucks:
        if package_id in truck.packages:
            return truck.truck_id
    return None


# Delivery process
for truck in trucks[:2]:
    deliver_packages(truck)
trucks[2].depart_time = min(trucks[0].time, trucks[1].time)
deliver_packages(trucks[2])

# Handle package 9 after all initial deliveries
handle_package_nine(trucks)


class Main:
    while True:

        print("                       _____________________________________________________   ")
        print("                      |                                                     |  ")
        print("              _______ |                                                     |  ")
        print("             / _____ || Total mileage for all routes: {:.2f}".format(sum(truck.mileage for truck in trucks)))
        print("            / /(__) |||                                                     |  ")
        print("  ________/ / |OO| || |                                                     |  ")
        print(" |         |-------|| |                                                     |  ")
        print("(|         |     -.|| |_______________________                              |  ")
        print(" |  ____   \       ||_________||____________  |             ____      ____  |  ")
        print("/| / __ \   |______||     / __ \   / __ \   | |            / __ \    / __ \ |\ ")
        print("\|| /  \ |_______________| /  \ |_| /  \ |__| |___________| /  \ |__| /  \|_|/ ")
        print("   | () |                 | () |   | () |                  | () |    | () |    ")
        print("    \__/                   \__/     \__/                    \__/      \__/     ")

        first_input = input("To begin tracking, please type the word 'START' : ")
        if first_input.upper() ==  "EXIT":
            break
        if first_input.upper() == "START":
            try:
                status_time = input("Please enter a time to check status of package(s) (HH:MM:SS): ")
                h, m, s = map(int, status_time.split(":"))
                convert_timedelta = datetime.timedelta(hours=h, minutes=m, seconds=s)

                second_input = input("To track all related packages type 'ALL', for a single parcel type 'SINGLE': ")

                if second_input.upper() == "SINGLE":
                    try:
                        pack_input = int(input("Provide the package ID: "))
                        package = pack_hash_table.lookup(pack_input)
                        package.update_status(convert_timedelta)
                        truck_id = find_package_truck(pack_input, trucks)
                        print(f"\nDelivered by Truck {truck_id}")
                        print(f"Package ID: {package.ID}")
                        print(f"Delivery Address: {package.address}")
                        print(f"City: {package.city}")
                        print(f"State: {package.state}")
                        print(f"Zip: {package.zipcode}")
                        print(f"Deadline: {package.deadline_time}")
                        print(f"Weight: {package.weight}")
                        print(f"Status: {package.status}")

                        # Delivery time display
                        if package.delivery_time and package.status == "Delivered":
                            total_seconds = int(package.delivery_time.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            seconds = total_seconds % 60
                            print(f"Delivery Time: {hours:02d}:{minutes:02d}:{seconds:02d}")

                    except ValueError:
                        print("Invalid entry. Closing program.")
                        exit()
                elif second_input.upper() == "ALL":
                    try:
                        for packageID in range(1, 41):
                            package = pack_hash_table.lookup(packageID)
                            package.update_status(convert_timedelta)
                            truck_id = find_package_truck(packageID, trucks)
                            print(f"\nDelivered by Truck {truck_id}")
                            print(f"Package ID: {package.ID}")
                            print(f"Delivery Address: {package.address}")
                            print(f"City: {package.city}")
                            print(f"State: {package.state}")
                            print(f"Zip: {package.zipcode}")
                            print(f"Deadline: {package.deadline_time}")
                            print(f"Weight: {package.weight}")
                            print(f"Status: {package.status}")

                            # Delivery time display
                            if package.delivery_time and package.status == "Delivered":
                                total_seconds = int(package.delivery_time.total_seconds())
                                hours = total_seconds // 3600
                                minutes = (total_seconds % 3600) // 60
                                seconds = total_seconds % 60
                                print(f"Delivery Time: {hours:02d}:{minutes:02d}:{seconds:02d}")

                        print("\nTruck Mileage Summary:")
                        print_truck_mileage(trucks)
                    except ValueError:
                        print("Invalid entry. Closing program.")
                        exit()
                else:
                    exit()
            except ValueError:
                print("Invalid entry. Closing program.")
                exit()
        else:
            print("Invalid entry. Closing program.")
            exit()
