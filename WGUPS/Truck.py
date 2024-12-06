"""
Cole Detrick
Student ID:011447776
"""
# Defining Class object Truck, this enhances my programs usability and scalability in the future.
class Truck:
    def __init__(self,truck_id, capacity, speed, load, packages, mileage, address, depart_time):
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def print_mileage(self):
        print(f"Truck ID: {self.truck_id}, Mileage: {self.mileage} miles")
# returns a string representative of the truck object
    def __str__(self):
        return f"Truck ID: {self.truck_id}Capacity: {self.capacity}, Speed: {self.speed}, Load: {self.load}, Packages: {self.packages}, Mileage: {self.mileage}, Address: {self.address}, Depart Time: {self.depart_time}"