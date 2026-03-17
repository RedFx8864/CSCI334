#the back end code for the live analytics system

from User import User
from Booking import Booking
from Admin import Admin

admin = Admin("admin", "password", "admin@example.com")
all_users = admin.viewAllUsers()
for user in all_users:
    print(user.userId, user.email, user.bookings)