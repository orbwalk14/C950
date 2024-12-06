"""
Cole Detrick
Student ID:011447776
"""
import datetime

class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        # Store address for package 9
        if ID == 9:
            self.correct_address = "410 S State St"
            self.correct_city = "Salt Lake City"
            self.correct_state = "UT"
            self.correct_zip = "84111"

    def __str__(self):
        # Format delivery time if it exists
        if self.delivery_time:
            total_seconds = int(self.delivery_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            delivery_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            delivery_time_str = "Not yet delivered"

        return (f"ID: {self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, "
                f"Zipcode: {self.zipcode}, Deadline: {self.deadline_time}, Weight: {self.weight}, "
                f"Delivery Time: {delivery_time_str}, Status: {self.status}")

    def update_status(self, current_time):
        # handling for Package 9
        if self.ID == 9:
            address_update_time = datetime.timedelta(hours=10, minutes=20)
            if current_time < address_update_time:
                self.address = "300 State St"
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84103"
                self.status = "Address incorrect - waiting for update"
                return
            else:
                self.address = self.correct_address
                self.city = self.correct_city
                self.state = self.correct_state
                self.zipcode = self.correct_zip

        # Normal status update logic for all packages
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and current_time >= self.departure_time:
            self.status = "En route"
        else:
            self.status = "At Hub"
