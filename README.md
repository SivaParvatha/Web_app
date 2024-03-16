# Web_app


Flask User Management System Documentation
Overview
This Flask application serves as a user management system, allowing users to register, login, edit their profile, and delete their account. It provides a simple interface for managing user data stored in an SQLite database.

Installation
Clone the repository or download the source code.
Install the required dependencies by running pip install -r requirements.txt.
Run the Flask application by executing python app.py.
Features
1. User Registration
Users can register by providing a username, password, name, email, age, and date of birth. The application ensures that usernames are unique.

2. User Login
Registered users can log in using their username and password.

3. User Profile Management
Logged-in users can edit their profile details, including username, password, name, email, age, and date of birth.

4. User Deletion
Users have the option to delete their account, which permanently removes their data from the system.

5. Forgot Password
A feature for resetting passwords is provided, although it is not implemented in the current version.

Routes
1. /login
Method: GET, POST
Description: Renders the login form and handles user authentication.
2. /logout
Method: GET
Description: Logs out the current user and redirects to the login page.
3. /users
Method: GET
Description: Displays a list of all registered users.
4. /create_user
Method: GET, POST
Description: Allows users to create a new account or edit their existing profile.if user is alredy there in db then it will not create new user with the same user id.I have added validation of all the fileds.
6. /forgot_password
Method: GET, POST
Description: Provides functionality for resetting passwords (not implemented in current version).
7. /edit_user/<int:id>
Method: GET, POST
Description: Allows users to edit their profile details. we can pass the user values to create user form then the values are auto populated in create user form then we can update the values.
8. /delete_user/<int:id>
Method: POST
Description: Deletes a user account based on the provided user ID.
Templates
login.html: Renders the login form.
users.html: Displays a list of all registered users.
createuser.html: Allows users to create a new account or edit their profile.
forgotpassword.html: Provides functionality for resetting passwords (not implemented).
Database
The application uses an SQLite database named your.db to store user data. The database schema includes fields for username, password, name, email, age, and date of birth.


# test user details:
user name: test
password : test
