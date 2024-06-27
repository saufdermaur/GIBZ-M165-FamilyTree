import os
from function import visualize_family_tree

class Menu:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def clear_screen():
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
        """Prints the menu options."""
        print("\n===== Family Tree Application Menu =====")
        print("1: Insert example data")
        print("2: Get all people")
        print("3: Create a person")
        print("4: Update a person")
        print("5: Delete a person")
        print("6: Delete everything")
        print("7: Add married relationship")
        print("8: Add child relationship")
        print("9: Show family tree")
        print("0: Exit")

    def run(self):
        """Runs the main menu loop."""
        while True:
            self.print_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.clear_screen()
                print("Inserting example data...")
                self.app.insert_example_data()
                print("Example data inserted successfully.")
            elif choice == '2':
                self.clear_screen()
                print("Fetching all people...\n")
                self.app.get_all_people()
            elif choice == '3':
                self.clear_screen()
                print("Creating a new person...\n")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                birthdate = input("Enter birthdate (YYYY-MM-DD): ")
                occupation = input("Enter occupation: ")
                deathdate = input("Enter deathdate (YYYY-MM-DD) (Optional): ")
                description = input("Enter description (Optional): ")
                self.app.create_person(first_name, last_name, birthdate, occupation, deathdate, description)
                print(f"\n{first_name} {last_name} created successfully.")
            elif choice == '4':
                self.clear_screen()
                print("Updating a person...\n")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                birthdate = input("Enter new birthdate (YYYY-MM-DD) (leave blank to keep current): ")
                occupation = input("Enter new occupation (leave blank to keep current): ")
                deathdate = input("Enter new deathdate (YYYY-MM-DD) (leave blank to keep current): ")
                description = input("Enter new description (leave blank to keep current): ")
                self.app.update_person(first_name, last_name, birthdate or None, occupation or None, deathdate or None, description or None)
                print(f"\n{first_name} {last_name} updated successfully.")
            elif choice == '5':
                self.clear_screen()
                print("Deleting a person...\n")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                self.app.delete_person(first_name, last_name)
                print(f"\n{first_name} {last_name} deleted successfully.")
            elif choice == '6':
                self.clear_screen()
                confirmation = input("Are you sure you want to delete everything? (y/n): ").strip().lower()
                if confirmation == 'y':
                    print("\nDeleting everything...")
                    self.app.deleteEverything()
                    print("All data deleted.")
                else:
                    print("\nDeletion canceled.")
            elif choice == '7':
                self.clear_screen()
                print("Adding a married relationship...\n")
                person1_first_name = input("Enter first name of first person: ")
                person1_last_name = input("Enter last name of first person: ")
                person2_first_name = input("Enter first name of second person: ")
                person2_last_name = input("Enter last name of second person: ")
                self.app.add_married_relationship(person1_first_name, person1_last_name, person2_first_name, person2_last_name)
                print(f"\nMarried relationship added between {person1_first_name} {person1_last_name} and {person2_first_name} {person2_last_name}.")
            elif choice == '8':
                self.clear_screen()
                print("Adding a child relationship...\n")
                child_first_name = input("Enter first name of child: ")
                child_last_name = input("Enter last name of child: ")
                parent1_first_name = input("Enter first name of first parent: ")
                parent1_last_name = input("Enter last name of first parent: ")
                parent2_first_name = input("Enter first name of second parent: ")
                parent2_last_name = input("Enter last name of second parent: ")
                self.app.add_child_of_relationship(child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name)
                print(f"\nChild relationship added for {child_first_name} {child_last_name}.")
            elif choice == '9':
                self.clear_screen()
                print("Displaying family tree...\n")
                tree_data = self.app.get_family_tree()
                visualize_family_tree(tree_data)
            elif choice == '0':
                self.clear_screen()
                print("Exiting application. Goodbye!")
                self.app.close()
                break
            else:
                self.clear_screen()
                print("Invalid choice. Please try again.")
