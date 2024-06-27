import os
from datetime import datetime
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
        print("10: Search people")
        print("11: Get people over age")
        print("12: Get person with most children")
        print("13: Get siblings of a person")
        print("14: Count total number of people")
        print("0: Exit")

    def validate_input(self, prompt, data_type=str, required=True):
        """Validates user input."""
        while True:
            user_input = input(prompt)
            if required and not user_input.strip():
                print("Input cannot be empty. Please try again.")
            elif user_input.strip() == "" and not required:
                return None
            else:
                try:
                    if data_type == int:
                        user_input = int(user_input)
                    elif data_type == float:
                        user_input = float(user_input)
                    elif data_type == datetime:
                        user_input = datetime.strptime(user_input, '%Y-%m-%d').date()
                    elif data_type == str:
                        user_input = user_input.strip()
                    return user_input
                except ValueError:
                    print(f"Invalid input format. Please enter a valid {data_type.__name__}.")

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
                first_name = self.validate_input("Enter first name: ")
                last_name = self.validate_input("Enter last name: ")
                birthdate = self.validate_input("Enter birthdate (YYYY-MM-DD): ", data_type=datetime)
                occupation = self.validate_input("Enter occupation: ")
                deathdate = self.validate_input("Enter deathdate (YYYY-MM-DD) (Optional): ", data_type=datetime, required=False)
                description = self.validate_input("Enter description (Optional): ", required=False)
                self.app.create_person(first_name, last_name, birthdate, occupation, deathdate, description)
                print(f"\n{first_name} {last_name} created successfully.")
            elif choice == '4':
                self.clear_screen()
                print("Updating a person...\n")
                first_name = self.validate_input("Enter first name: ")
                last_name = self.validate_input("Enter last name: ")
                birthdate = self.validate_input("Enter new birthdate (YYYY-MM-DD) (leave blank to keep current): ", data_type=datetime, required=False)
                occupation = self.validate_input("Enter new occupation (leave blank to keep current): ", required=False)
                deathdate = self.validate_input("Enter new deathdate (YYYY-MM-DD) (leave blank to keep current): ", data_type=datetime, required=False)
                description = self.validate_input("Enter new description (leave blank to keep current): ", required=False)
                self.app.update_person(first_name, last_name, birthdate or None, occupation, deathdate, description)
                print(f"\n{first_name} {last_name} updated successfully.")
            elif choice == '5':
                self.clear_screen()
                print("Deleting a person...\n")
                first_name = self.validate_input("Enter first name: ")
                last_name = self.validate_input("Enter last name: ")
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
                person1_first_name = self.validate_input("Enter first name of first person: ")
                person1_last_name = self.validate_input("Enter last name of first person: ")
                person2_first_name = self.validate_input("Enter first name of second person: ")
                person2_last_name = self.validate_input("Enter last name of second person: ")
                self.app.add_married_relationship(person1_first_name, person1_last_name, person2_first_name, person2_last_name)
                print(f"\nMarried relationship added between {person1_first_name} {person1_last_name} and {person2_first_name} {person2_last_name}.")
            elif choice == '8':
                self.clear_screen()
                print("Adding a child relationship...\n")
                child_first_name = self.validate_input("Enter first name of child: ")
                child_last_name = self.validate_input("Enter last name of child: ")
                parent1_first_name = self.validate_input("Enter first name of first parent: ")
                parent1_last_name = self.validate_input("Enter last name of first parent: ")
                parent2_first_name = self.validate_input("Enter first name of second parent: ")
                parent2_last_name = self.validate_input("Enter last name of second parent: ")
                self.app.add_child_of_relationship(child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name)
                print(f"\nChild relationship added for {child_first_name} {child_last_name}.")
            elif choice == '9':
                self.clear_screen()
                print("Displaying family tree...\n")
                tree_data = self.app.get_family_tree()
                visualize_family_tree(tree_data)
            elif choice == '10':
                self.clear_screen()
                search_term = self.validate_input("Enter search term: ")
                result = self.app.search_people(search_term)
                for record in result:
                    print(f"{record['first_name']} {record['last_name']} - "
                          f"{record['birthdate']} - {record['occupation']} - "
                          f"{record['deathdate']} - {record['description']}")
            elif choice == '11':
                self.clear_screen()
                age = self.validate_input("Enter age: ", data_type=int)
                count, people = self.app.list_and_count_people_over_age(age)
                print(f"Number of people over {age} years old: {count}")
                for person in people:
                    print(person)
            elif choice == '12':
                self.clear_screen()
                persons_with_most_children = self.app.get_persons_with_most_children()
                if persons_with_most_children:
                    print("Persons with the most children:")
                    for person, num_children in persons_with_most_children:
                        print(f"{person} has {num_children} children")
                else:
                    print("No persons found with children.")
            elif choice == '13':
                self.clear_screen()
                first_name = self.validate_input("Enter first name: ")
                last_name = self.validate_input("Enter last name: ")
                siblings = self.app.get_siblings(first_name, last_name)
                if siblings:
                    print(f"Siblings of {first_name} {last_name}:")
                    for sibling in siblings:
                        print(sibling)
                else:
                    print(f"No siblings found for {first_name} {last_name}.")
            elif choice == '14':
                self.clear_screen()
                count = self.app.count_people()
                print(f"Total number of people: {count}")
            elif choice == '0':
                self.clear_screen()
                print("Exiting application. Goodbye!")
                self.app.close()
                break
            else:
                self.clear_screen()
                print("Invalid choice. Please try again.")
