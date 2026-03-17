from User import User
from Booking import Booking
while True:
        print("Welcome to the Booking System!")
        email =input("Email: ")
        password = input("Password:")
        
        select1 = input("1. Create Account\n2. Login\nSelect an option: ")
        
        if select1 == "1": 
            user = User.createUser(email, password)
            print(f"Account created successfully! Your user ID is {user.userId}")
        
        elif select1 == "2":
            users = User.loadUsers()
            user = next((u for u in users if u["email"] == email and u["password"] == password), None)
            if user:
                print(f"Login successful! Welcome, {user['userId']}!")
                select1 = input("1. Make a booking\n2. View bookings\n3. Logout\nSelect an option: ")
                if select1 == "1":
                    duration = input("Duration: ")
                    date = input("Date (YYYY-MM-DD): ")
                    startTime = input("Start Time (HH:MM): ")
                    user_obj = User(user["userId"], user["password"], user["email"], user["bookings"])
                    user_obj.makeBooking(duration, date, startTime)
                    print("Booking made successfully!")
                elif select1 == "2":
                    user_obj = User(user["userId"], user["password"], user["email"], user["bookings"])
                    user_obj.showBookings()
                elif select1 == "3":
                    print("Logging out...")
            else:
                print("Invalid email or password. Please try again.")