from function import FamilyTreeApp
from menu import Menu

def main():
    app = FamilyTreeApp("neo4j+s://b0fba925.databases.neo4j.io", "neo4j", "MrGNUAzXQenWSbf0WI4BydfRICBYkG7oTqE5SpNQ4TY")
    menu = Menu(app)
    menu.run()

if __name__ == "__main__":
    main()
