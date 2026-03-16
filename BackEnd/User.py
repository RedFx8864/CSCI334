from Booking import Booking
import json
import os

class User:

    def __init__(self, userId, password, email, bookings=None):
        self.userId = userId
        self.password = password
        self.email = email
        self.bookings = bookings if bookings is not None else []


    @classmethod
    def createUser(cls, email, password):

        users = cls.loadUsers()

        userId = f"user{len(users) + 1}"

        user = cls(userId, password, email)

        users.append({
            "userId": user.userId,
            "email": user.email,
            "password": user.password,
            "bookings": []
        })

        cls.saveAllUsers(users)

        return user

    @staticmethod
    def loadUsers():

        if not os.path.exists("users.json"):
            return []

        with open("users.json", "r") as file:
            return json.load(file)


    @staticmethod
    def saveAllUsers(users):

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

    def makeBooking(self, duration, date, startTime):

        booking = Booking.createBooking(duration, date, startTime)

        self.bookings.append({
            "bookingId": booking.bookingId,
            "duration": booking.duration,
            "date": booking.date,
            "startTime": booking.startTime
        })

        users = self.loadUsers()

        for user in users:
            if user["userId"] == self.userId:
                user["bookings"] = self.bookings

        self.saveAllUsers(users)

        return booking

    def showBookings(self):

        if not self.bookings:
            print("No bookings found")
            return

        for booking in self.bookings:
            print(
                f"Booking ID: {booking['bookingId']}, "
                f"Duration: {booking['duration']}, "
                f"Date: {booking['date']}, "
                f"Start Time: {booking['startTime']}"
            )