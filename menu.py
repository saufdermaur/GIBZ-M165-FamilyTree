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
        print("10: Search people")
        print("11: Get people over age")
        print("12: Get person with most children")
        print("13: Get siblings of a person")
        print("14: Count total number of people")
        print("0: Exit")

    def run(self):
        """Runs the main menu loop."""
        while True:
            self.print_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.clear_screen()
                print("Inserting example data...")
                try:
                    self.app.insert_example_data()
                    print("Example data inserted successfully.")
                except Exception as e:
                    print(f"Failed to insert example data: {str(e)}")

            elif choice == '2':
                self.clear_screen()
                print("Fetching all people...\n")
                try:
                    people = self.app.get_all_people()
                    if people:
                        for person in people:
                            print(f"{person['first_name']} {person['last_name']}")
                    else:
                        print("No people found in the database.")
                except Exception as e:
                    print(f"Failed to fetch all people: {str(e)}")

            elif choice == '3':
                self.clear_screen()
                print("Creating a new person...\n")
                try:
                    first_name = input("Enter first name: ").strip()
                    last_name = input("Enter last name: ").strip()
                    birthdate = input("Enter birthdate (YYYY-MM-DD): ").strip()
                    occupation = input("Enter occupation: ").strip()
                    deathdate = input("Enter deathdate (YYYY-MM-DD) (Optional): ").strip()
                    description = input("Enter description (Optional): ").strip()
                    
                    if not first_name or not last_name or not birthdate or not occupation:
                        print("Error: Please provide all required information.")
                        continue  
                    
                    self.app.create_person(first_name, last_name, birthdate, occupation, deathdate or None, description or None)
                    print(f"\n{first_name} {last_name} created successfully.")
                except Exception as e:
                    print(f"Failed to create person: {str(e)}")

            elif choice == '4':
                self.clear_screen()
                print("Updating a person...\n")
                try:
                    first_name = input("Enter first name: ").strip()
                    last_name = input("Enter last name: ").strip()
                    
                    if not first_name or not last_name:
                        print("Error: Please provide both first name and last name.")
                        continue 
                    
                    birthdate = input("Enter new birthdate (YYYY-MM-DD) (leave blank to keep current): ").strip()
                    occupation = input("Enter new occupation (leave blank to keep current): ").strip()
                    deathdate = input("Enter new deathdate (YYYY-MM-DD) (leave blank to keep current): ").strip()
                    description = input("Enter new description (leave blank to keep current): ").strip()
                    
                    self.app.update_person(first_name, last_name, birthdate or None, occupation or None, deathdate or None, description or None)
                    print(f"\n{first_name} {last_name} updated successfully.")
                except Exception as e:
                    print(f"Failed to update person: {str(e)}")

            elif choice == '5':
                self.clear_screen()
                print("Deleting a person...\n")
                try:
                    first_name = input("Enter first name: ").strip()
                    last_name = input("Enter last name: ").strip()
                    
                    if not first_name or not last_name:
                        print("Error: Please provide both first name and last name.")
                        continue  
                    
                    self.app.delete_person(first_name, last_name)
                    print(f"\n{first_name} {last_name} deleted successfully.")
                except Exception as e:
                    print(f"Failed to delete person: {str(e)}")

            elif choice == '6':
                self.clear_screen()
                confirmation = input("Are you sure you want to delete everything? (y/n): ").strip().lower()
                if confirmation == 'y':
                    try:
                        print("\nDeleting everything...")
                        self.app.delete_everything()
                        print("All data deleted.")
                    except Exception as e:
                        print(f"Failed to delete everything: {str(e)}")
                else:
                    print("\nDeletion canceled.")

            elif choice == '7':
                self.clear_screen()
                print("Adding a married relationship...\n")
                try:
                    person1_first_name = input("Enter first name of first person: ").strip()
                    person1_last_name = input("Enter last name of first person: ").strip()
                    person2_first_name = input("Enter first name of second person: ").strip()
                    person2_last_name = input("Enter last name of second person: ").strip()
                    
                    if not person1_first_name or not person1_last_name or not person2_first_name or not person2_last_name:
                        print("Error: Please provide all names.")
                        continue  
                    
                    self.app.add_married_relationship(person1_first_name, person1_last_name, person2_first_name, person2_last_name)
                    print(f"\nMarried relationship added between {person1_first_name} {person1_last_name} and {person2_first_name} {person2_last_name}.")
                except Exception as e:
                    print(f"Failed to add married relationship: {str(e)}")

            elif choice == '8':
                self.clear_screen()
                print("Adding a child relationship...\n")
                try:
                    child_first_name = input("Enter first name of child: ").strip()
                    child_last_name = input("Enter last name of child: ").strip()
                    parent1_first_name = input("Enter first name of first parent: ").strip()
                    parent1_last_name = input("Enter last name of first parent: ").strip()
                    parent2_first_name = input("Enter first name of second parent: ").strip()
                    parent2_last_name = input("Enter last name of second parent: ").strip()
                    
                    if not child_first_name or not child_last_name or not parent1_first_name or not parent1_last_name or not parent2_first_name or not parent2_last_name:
                        print("Error: Please provide all names.")
                        continue 
                    
                    self.app.add_child_of_relationship(child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name)
                    print(f"\nChild relationship added for {child_first_name} {child_last_name}.")
                except Exception as e:
                    print(f"Failed to add child relationship: {str(e)}")

            elif choice == '9':
                self.clear_screen()
                print("Displaying family tree...\n")
                try:
                    tree_data = self.app.get_family_tree()
                    visualize_family_tree(tree_data)
                except Exception as e:
                    print(f"Failed to display family tree: {str(e)}")

            elif choice == '10':
                self.clear_screen()
                search_term = input("Enter search term: ").strip()
                try:
                    if not search_term:
                        print("Error: Please provide a search term.")
                        continue  
                    
                    result = self.app.search_people(search_term)
                    for record in result:
                        print(f"{record['first_name']} {record['last_name']} - "
                              f"{record['birthdate']} - {record['occupation']} - "
                              f"{record['deathdate']} - {record['description']}")
                except Exception as e:
                    print(f"Failed to search people: {str(e)}")

            elif choice == '11':
                self.clear_screen()
                age = input("Enter age: ").strip()
                try:
                    if not age.isdigit():
                        print("Error: Please enter a valid age.")
                        continue  
                    
                    count, people = self.app.list_and_count_people_over_age(age)
                    print(f"Number of people over {age} years old: {count}")
                    for person in people:
                        print(person)
                except Exception as e:
                    print(f"Failed to list people over age: {str(e)}")

            elif choice == '12':
                self.clear_screen()
                try:
                    persons_with_most_children = self.app.get_persons_with_most_children()
                    if persons_with_most_children:
                        print("Persons with the most children:")
                        for person, num_children in persons_with_most_children:
                            print(f"{person} has {num_children} children")
                    else:
                        print("No persons found with children.")
                except Exception as e:
                    print(f"Failed to get persons with most children: {str(e)}")

            elif choice == '13':
                self.clear_screen()
                try:
                    first_name = input("Enter first name: ").strip()
                    last_name = input("Enter last name: ").strip()
                    
                    if not first_name or not last_name:
                        print("Error: Please provide both first name and last name.")
                        continue 
                    
                    siblings = self.app.get_siblings(first_name, last_name)
                    if siblings:
                        print(f"Siblings of {first_name} {last_name}:")
                        for sibling in siblings:
                            print(sibling)
                    else:
                        print(f"No siblings found for {first_name} {last_name}.")
                except Exception as e:
                    print(f"Failed to get siblings: {str(e)}")

            elif choice == '14':
                self.clear_screen()
                try:
                    count = self.app.count_people()
                    print(f"Total number of people: {count}")
                except Exception as e:
                    print(f"Failed to count people: {str(e)}")

            elif choice == '0':
                self.clear_screen()
                print("Exiting application. Goodbye!")
                try:
                    self.app.close()
                except Exception as e:
                    print(f"Failed to close application: {str(e)}")
                break

            else:
                self.clear_screen()
                print("Invalid choice. Please try again.")