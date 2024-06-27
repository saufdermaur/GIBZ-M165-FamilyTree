from function import FamilyTreeApp
from menu import Menu
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    connection_string = os.getenv("CONNECTION_STRING_DB")
    username = os.getenv("USERNAME_DB")
    password = os.getenv("PASSWORD_DB")

    if not connection_string or not username or not password:
        print("Environment variables are not set correctly.")
        return

    app = FamilyTreeApp(connection_string, username, password)
    menu = Menu(app)
    menu.run()

if __name__ == "__main__":
    main()
