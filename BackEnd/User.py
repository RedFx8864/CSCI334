#main User class and functions for them
class User:
    nextId = 1
    
    def __init__(self, userId, password, email, bookings = []):
        self.userId = userId
        self.password = password
        self.email = email
        self.bookings = bookings if bookings is not None else []     

    @classmethod
    def createUser(cls, email, password):
        userId = f"user{cls.nextId}"
        cls.nextId += 1
        return cls(userId, password, email)
    

user1 = User.createUser("jojo@gmail.com", "password123")
user2 = User.createUser("janedoe@gmail.com", "password456")

print(user1.userId + " " + user1.email)
print(user2.userId + " " + user2.email)