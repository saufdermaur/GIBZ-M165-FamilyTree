from neo4j import GraphDatabase
import networkx as nx
from datetime import date, datetime
import matplotlib.pyplot as plt

from neo4j import GraphDatabase, exceptions

class FamilyTreeApp:

    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.setup_schema()
        except exceptions.AuthError as e:
            print(f"Authentication failed: {e}")
        except exceptions.ServiceUnavailable as e:
            print(f"Unable to connect to database: {e}")
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            print(f"Failed to close the database connection: {e}")

    def setup_schema(self):
        try:
            with self.driver.session() as session:
                # Constraints
                session.run("CREATE CONSTRAINT constraint_unique_person_name IF NOT EXISTS FOR (p:Person) REQUIRE (p.first_name, p.last_name) IS NODE KEY")
                session.run("CREATE CONSTRAINT constraint_for_person_first_name IF NOT EXISTS FOR (p:Person) REQUIRE p.first_name IS :: STRING")
                session.run("CREATE CONSTRAINT constraint_for_person_last_name IF NOT EXISTS FOR (p:Person) REQUIRE p.last_name IS :: STRING")
                session.run("CREATE CONSTRAINT constraint_for_person_birthdate IF NOT EXISTS FOR (p:Person) REQUIRE p.birthdate IS :: DATE")
                session.run("CREATE CONSTRAINT constraint_for_person_occupation IF NOT EXISTS FOR (p:Person) REQUIRE p.occupation IS :: STRING")
                session.run("CREATE CONSTRAINT constraint_for_person_deathdate IF NOT EXISTS FOR (p:Person) REQUIRE p.deathdate IS :: DATE")

                # Indexes
                session.run("CREATE INDEX index_for_person_first_name IF NOT EXISTS FOR (p:Person) ON (p.first_name)")
                session.run("CREATE INDEX index_for_person_last_name IF NOT EXISTS FOR (p:Person) ON (p.last_name)")
                session.run("CREATE INDEX index_for_person_birthdate IF NOT EXISTS FOR (p:Person) ON (p.birthdate)")
                session.run("CREATE INDEX index_for_person_occupation IF NOT EXISTS FOR (p:Person) ON (p.occupation)")
                session.run("CREATE INDEX index_for_person_deathdate IF NOT EXISTS FOR (p:Person) ON (p.deathdate)")
                session.run("CREATE INDEX index_for_person_description IF NOT EXISTS FOR (p:Person) ON (p.description)")
        except Exception as e:
            print(f"Error setting up schema: {e}")

    def insert_example_data(self):
        try:
            # Create people with example data                                                                                           
            self.create_person("John", "Doe", "1950-07-15", "Retired Engineer", description="Patriarch of the Doe family")
            self.create_person("Jane", "Doe", "1955-09-20", "Homemaker", description="Matriarch of the Doe family")
            self.create_person("Mike", "Doe", "1975-03-10", "Doctor", description="Eldest son of John and Jane Doe")
            self.create_person("Sarah", "Doe", "1978-06-25", "Lawyer", description="Daughter of John and Jane Doe")
            self.create_person("Emily", "Doe", "1980-11-05", "Teacher", description="Youngest daughter of John and Jane Doe")
            self.create_person("Mark", "Smith", "1988-04-12", "Architect", description="Son of Robert and Mary Smith")
            self.create_person("Mary", "Smith", "1990-06-20", "Nurse", description="Wife of Mark Smith")
            self.create_person("Jacob", "Brown", "1992-09-15", "Software Developer", description="Son of William and Emma Brown")
            self.create_person("Emma", "Brown", "1994-11-30", "Accountant", description="Wife of Jacob Brown")
            self.create_person("Sophia", "Jones", "1985-03-22", "Professor", description="Daughter of Peter and Susan Jones")
            self.create_person("Peter", "Jones", "1960-08-10", "Lawyer", description="Patriarch of the Jones family")
            self.create_person("Susan", "Jones", "1965-11-25", "Artist", description="Matriarch of the Jones family")
            self.create_person("Olivia", "Williams", "1993-07-18", "Veterinarian", description="Wife of Mike Doe")
            self.create_person("Thomas", "Miller", "1995-12-20", "Engineer", description="Husband of Sarah Doe")
            self.create_person("Karl", "Washington", "1888-04-12", "Entrepreneur", deathdate="1980-05-22", description="Root of the Washington family")
            self.create_person("Linda", "Washington", "1890-06-20", "Philanthropist", deathdate="1975-04-02" , description="Root of the Washington family")

            # Establish relationships
            self.add_married_relationship("John", "Doe", "Jane", "Doe")
            self.add_married_relationship("Mike", "Doe", "Olivia", "Williams")
            self.add_married_relationship("Thomas", "Miller", "Sarah", "Doe")
            self.add_married_relationship("Mark", "Smith", "Mary", "Smith")
            self.add_married_relationship("Jacob", "Brown", "Emma", "Brown")
            self.add_married_relationship("Peter", "Jones", "Susan", "Jones")
            self.add_married_relationship("Karl", "Washington", "Linda", "Washington")

            self.add_child_of_relationship("Mike", "Doe", "John", "Doe", "Jane", "Doe")
            self.add_child_of_relationship("Sarah", "Doe", "John", "Doe", "Jane", "Doe")
            self.add_child_of_relationship("Emily", "Doe", "John", "Doe", "Jane", "Doe")
            self.add_child_of_relationship("Mark", "Smith", "John", "Smith", "Susan", "Smith")
            self.add_child_of_relationship("Mary", "Smith", "Peter", "Jones", "Susan", "Jones")
            self.add_child_of_relationship("Jacob", "Brown", "Peter", "Jones", "Susan", "Jones")
            self.add_child_of_relationship("Sophia", "Jones", "Peter", "Jones", "Susan", "Jones")
            self.add_child_of_relationship("Susan", "Jones", "Karl", "Washington", "Linda", "Washington")
            self.add_child_of_relationship("John", "Doe", "Karl", "Washington", "Linda", "Washington")
            pass
        except Exception as e:
            print(f"Failed to insert example data: {e}")

    def get_all_people(self):
        try:
            with self.driver.session() as session:
                query = "MATCH (p:Person) RETURN p"
                result = session.run(query)
                for record in result:
                    print(f"{record['p']['first_name']} {record['p']['last_name']} - "
                          f"{record['p']['birthdate']} - {record['p']['occupation']} - "
                          f"{record['p']['deathdate']} - {record['p']['description']}")
        except Exception as e:
            print(f"Error retrieving people: {e}")


    def create_person(self, first_name, last_name, birthdate, occupation, deathdate=None, description=None):
        try:
            if not deathdate:
                deathdate = datetime(1, 1, 1).date()

            with self.driver.session() as session:
                query = (
                    "CREATE (p:Person {first_name: $first_name, last_name: $last_name, birthdate: $birthdate, "
                    "occupation: $occupation, deathdate: $deathdate, description: $description})"
                )
                session.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
                            occupation=occupation, deathdate=deathdate, description=description)
        
        except Exception as e:
            print(f"Error creating person {first_name} {last_name}: {e}")

    def update_person(self, first_name, last_name, birthdate=None, occupation=None, deathdate=None, description=None):
        try:
            if not deathdate:
                deathdate = datetime(1, 1, 1).date()

            with self.driver.session() as session:
                query = (
                    "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) "
                    "SET p.birthdate = $birthdate, p.occupation = $occupation, "
                    "p.deathdate = $deathdate, p.description = $description"
                )
                session.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
                            occupation=occupation, deathdate=deathdate, description=description)
        
        except Exception as e:
            print(f"Error updating person {first_name} {last_name}: {e}")

    def delete_person(self, first_name, last_name):
        try:
            with self.driver.session() as session:
                query = "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) DETACH DELETE p"
                session.run(query, first_name=first_name, last_name=last_name)
        
        except Exception as e:
            print(f"Error deleting person {first_name} {last_name}: {e}")

    def deleteEverything(self):
        try:
            with self.driver.session() as session:
                query = "MATCH (n) DETACH DELETE n"
                session.run(query)
        
        except Exception as e:
            print(f"Error deleting everything: {e}")

    def add_married_relationship(self, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
        try:
            with self.driver.session() as session:
                check_query = (
                    "MATCH (p:Person)-[:MARRIED]-(spouse:Person) "
                    "WHERE (p.first_name = $person1_first_name AND p.last_name = $person1_last_name) "
                    "OR (p.first_name = $person2_first_name AND p.last_name = $person2_last_name) "
                    "RETURN p.first_name AS first_name, p.last_name AS last_name, "
                    "collect(spouse.first_name + ' ' + spouse.last_name) AS spouses"
                )
                result = session.run(check_query, person1_first_name=person1_first_name,
                                    person1_last_name=person1_last_name, person2_first_name=person2_first_name,
                                    person2_last_name=person2_last_name)
                marriage_status = result.single()

                if marriage_status:
                    for person in marriage_status.items():
                        if person in [(person1_first_name, person1_last_name), (person2_first_name, person2_last_name)] and marriage_status['spouses']:
                            raise ValueError(f"{person1_first_name} {person1_last_name} or {person2_first_name} {person2_last_name} is already married to {', '.join(marriage_status['spouses'])}")

                query = (
                    "MATCH (p1:Person {first_name: $person1_first_name, last_name: $person1_last_name}), "
                    "(p2:Person {first_name: $person2_first_name, last_name: $person2_last_name}) "
                    "CREATE (p1)-[:MARRIED]->(p2), (p2)-[:MARRIED]->(p1)"
                )
                session.run(query, person1_first_name=person1_first_name, person1_last_name=person1_last_name,
                            person2_first_name=person2_first_name, person2_last_name=person2_last_name)

        except ValueError as ve:
            print(f"Error adding married relationship: {ve}")
        except Exception as e:
            print(f"Error adding married relationship: {e}")


    def add_child_of_relationship(self, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
        try:
            with self.driver.session() as session:
                query = (
                    "MATCH (c:Person {first_name: $child_first_name, last_name: $child_last_name}), "
                    "(p1:Person {first_name: $parent1_first_name, last_name: $parent1_last_name}), "
                    "(p2:Person {first_name: $parent2_first_name, last_name: $parent2_last_name}) "
                    "CREATE (c)-[:CHILD_OF]->(p1), (c)-[:CHILD_OF]->(p2)"
                )
                session.run(query, child_first_name=child_first_name, child_last_name=child_last_name,
                            parent1_first_name=parent1_first_name, parent1_last_name=parent1_last_name,
                            parent2_first_name=parent2_first_name, parent2_last_name=parent2_last_name)

        except Exception as e:
            print(f"Error adding child-of relationship: {e}")


    def get_family_tree(self):
        try:
            with self.driver.session() as session:
                query = (
                    "MATCH (p:Person)-[:CHILD_OF]->(parent:Person) "
                    "RETURN p.first_name + ' ' + p.last_name AS person1, parent.first_name + ' ' + parent.last_name AS person2, 'child' AS relationship "
                    "UNION "
                    "MATCH (p1:Person)-[:MARRIED]-(p2:Person) "
                    "RETURN p1.first_name + ' ' + p1.last_name AS person1, p2.first_name + ' ' + p2.last_name AS person2, 'married' AS relationship"
                )
                result = session.run(query)
                return list(result)
        
        except Exception as e:
            print(f"Error fetching family tree: {e}")
            return []
        
    def search_people(self, query_string):
        try:
            with self.driver.session() as session:
                query = (
                    "MATCH (p:Person) WHERE p.description CONTAINS $query_string "
                    "OR p.first_name CONTAINS $query_string "
                    "OR p.last_name CONTAINS $query_string "
                    "OR p.birthdate CONTAINS $query_string "
                    "OR p.occupation CONTAINS $query_string "
                    "OR p.deathdate CONTAINS $query_string "
                    "RETURN p.first_name AS first_name, p.last_name AS last_name, "
                    "p.birthdate AS birthdate, p.occupation AS occupation, "
                    "p.deathdate AS deathdate, p.description AS description"
                )
                result = session.run(query, query_string=query_string)
                return list(result)
        
        except Exception as e:
            print(f"Error searching people: {e}")
            return []

    def list_and_count_people_over_age(self, age):
        try:
            age = int(age)  # Convert age input to integer
            
            today = date.today()
            with self.driver.session() as session:
                query = "MATCH (p:Person) RETURN p.first_name AS first_name, p.last_name AS last_name, p.birthdate AS birthdate, p.deathdate AS deathdate"
                result = session.run(query)
                
                people_over_age = []
                for record in result:
                    birthdate = record['birthdate']
                    if birthdate:
                        birthdate = date(birthdate.year, birthdate.month, birthdate.day) 
                    else:
                        continue 
                    
                    deathdate = record['deathdate']
                    if deathdate and deathdate != date(1, 1, 1):
                        deathdate = date(deathdate.year, deathdate.month, deathdate.day)
                    else:
                        deathdate = today
                    
                    age_at_death_or_today = (deathdate - birthdate).days // 365
                    if age_at_death_or_today > age:
                        people_over_age.append(f"{record['first_name']} {record['last_name']} {age_at_death_or_today} years old")
                
                return len(people_over_age), people_over_age
        
        except Exception as e:
            print(f"Error listing and counting people over age {age}: {e}")
            return 0, []

    def get_persons_with_most_children(self):
        try:
            with self.driver.session() as session:
                query = (
                    "MATCH (child:Person)-[:CHILD_OF]->(parent:Person) "
                    "WITH parent, count(child) AS num_children "
                    "ORDER BY num_children DESC "
                    "RETURN parent.first_name + ' ' + parent.last_name AS person, num_children "
                )
                result = session.run(query)
                
                persons_with_most_children = []
                max_children = 0
                for record in result:
                    person = record['person']
                    num_children = record['num_children']
                    
                    if num_children > max_children:
                        max_children = num_children
                        persons_with_most_children = [(person, num_children)]
                    elif num_children == max_children:
                        persons_with_most_children.append((person, num_children))
                
                return persons_with_most_children
        
        except Exception as e:
            print(f"Error getting persons with most children: {e}")
            return []

    def get_siblings(self, first_name, last_name):
        try:
            with self.driver.session() as session:
                query = (
                    "MATCH (person:Person {first_name: $first_name, last_name: $last_name})-[:CHILD_OF]->(parent:Person)<-[:CHILD_OF]-(sibling:Person) "
                    "WHERE (person.first_name <> sibling.first_name OR person.last_name <> sibling.last_name) "
                    "RETURN DISTINCT sibling.first_name + ' ' + sibling.last_name AS sibling_name"
                )
                result = session.run(query, first_name=first_name, last_name=last_name)
                
                siblings = []
                for record in result:
                    siblings.append(record['sibling_name'])
                
                return siblings
        
        except Exception as e:
            print(f"Error getting siblings for {first_name} {last_name}: {e}")
            return []

    def count_people(self):
        try:
            with self.driver.session() as session:
                query = "MATCH (p:Person) RETURN count(p) AS num_people"
                result = session.run(query)
                record = result.single()
                if record:
                    return record['num_people']
                else:
                    return 0
        
        except Exception as e:
            print(f"Error counting people: {e}")
            return 0


def visualize_family_tree(tree_data):
    try:
        G = nx.Graph()

        for record in tree_data:
            G.add_edge(record['person1'], record['person2'], relationship=record['relationship'])

        pos = nx.spring_layout(G, k=0.9)
        edge_labels = nx.get_edge_attributes(G, 'relationship')
        
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
    
    except Exception as e:
        print(f"Error visualizing family tree: {e}")

def test_connection(connection_string, username, password):
    if not connection_string or not username or not password:
        raise ValueError("One or more environment variables are missing.")

    driver = GraphDatabase.driver(connection_string, auth=(username, password))
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            print("Connection successful: ", result.single()[0])
    except Exception as e:
        print("Connection failed: ", e)
    finally:
        driver.close()
