#code for admin user and there function
from User import User

class Admin(User):

    def __init__(self, userId, password, email):
        super().__init__(userId, password, email)

    def viewAllUsers(self):
        """
        Returns a list of all User objects.
        """
        users_data = User.loadUsers()  # load the JSON dictionaries
        users_list = []

        for user_dict in users_data:
            # create a User instance for each entry
            user = User(
                userId=user_dict["userId"],
                password=user_dict["password"],
                email=user_dict["email"],
                bookings=user_dict.get("bookings", [])
            )
            users_list.append(user)

        return users_list