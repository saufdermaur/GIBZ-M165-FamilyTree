from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

class FamilyTreeApp:

    def __init__(self, uri, user, password):
        if test_connection(uri, user, password) is False:
            raise ValueError("Connection failed.")
        else:
            print("Connection successful.")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
 
    def close(self):
        self.driver.close()

    def insert_example_data(app):
        # Create people
        app.create_person("John", "Doe", "1950-07-15", "Retired Engineer", description="Patriarch of the Doe family")
        app.create_person("Jane", "Doe", "1955-09-20", "Homemaker", description="Matriarch of the Doe family")
        app.create_person("Mike", "Doe", "1975-03-10", "Doctor", description="Eldest son of John and Jane Doe")
        app.create_person("Sarah", "Doe", "1978-06-25", "Lawyer", description="Daughter of John and Jane Doe")
        app.create_person("Emily", "Doe", "1980-11-05", "Teacher", description="Youngest daughter of John and Jane Doe")
        app.create_person("Mark", "Smith", "1988-04-12", "Architect", description="Son of Robert and Mary Smith")
        app.create_person("Mary", "Smith", "1990-06-20", "Nurse", description="Wife of Mark Smith")
        app.create_person("Jacob", "Brown", "1992-09-15", "Software Developer", description="Son of William and Emma Brown")
        app.create_person("Emma", "Brown", "1994-11-30", "Accountant", description="Wife of Jacob Brown")
        app.create_person("Sophia", "Jones", "1985-03-22", "Professor", description="Daughter of Peter and Susan Jones")
        app.create_person("Peter", "Jones", "1960-08-10", "Lawyer", description="Patriarch of the Jones family")
        app.create_person("Susan", "Jones", "1965-11-25", "Artist", description="Matriarch of the Jones family")
        app.create_person("Olivia", "Williams", "1993-07-18", "Veterinarian", description="Wife of Mike Doe")
        app.create_person("Thomas", "Miller", "1995-12-20", "Engineer", description="Husband of Sarah Doe")

        # Establish relationships
        app.add_married_relationship("John", "Doe", "Jane", "Doe")
        app.add_married_relationship("Mike", "Doe", "Olivia", "Williams")
        app.add_married_relationship("Thomas", "Miller", "Sarah", "Doe")
        app.add_married_relationship("Mark", "Smith", "Mary", "Smith")
        app.add_married_relationship("Jacob", "Brown", "Emma", "Brown")
        app.add_married_relationship("Peter", "Jones", "Susan", "Jones")

        app.add_child_of_relationship("Mike", "Doe", "John", "Doe", "Jane", "Doe")
        app.add_child_of_relationship("Sarah", "Doe", "John", "Doe", "Jane", "Doe")
        app.add_child_of_relationship("Emily", "Doe", "John", "Doe", "Jane", "Doe")
        app.add_child_of_relationship("Mark", "Smith", "John", "Smith", "Susan", "Smith")
        app.add_child_of_relationship("Mary", "Smith", "Peter", "Jones", "Susan", "Jones")
        app.add_child_of_relationship("Jacob", "Brown", "Peter", "Jones", "Susan", "Jones")
        app.add_child_of_relationship("Sophia", "Jones", "Peter", "Jones", "Susan", "Jones")

    def get_all_people(self):
            with self.driver.session() as session:
                query = "MATCH (p:Person) RETURN p"
                result = session.run(query)
                for record in result:
                    print(f"{record['p']['first_name']} {record['p']['last_name']} - "
                        f"{record['p']['birthdate']} - {record['p']['occupation']} - "
                        f"{record['p']['deathdate']} - {record['p']['description']}")

    def create_person(self, first_name, last_name, birthdate, occupation, deathdate=None, description=None):
        with self.driver.session() as session:
            query = (
                "CREATE (p:Person {first_name: $first_name, last_name: $last_name, birthdate: $birthdate, "
                "occupation: $occupation, deathdate: $deathdate, description: $description})"
            )
            session.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
                        occupation=occupation, deathdate=deathdate, description=description)

    def update_person(self, first_name, last_name, birthdate=None, occupation=None, deathdate=None, description=None):
        with self.driver.session() as session:
            query = (
                "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) "
                "SET p.birthdate = $birthdate, p.occupation = $occupation, "
                "p.deathdate = $deathdate, p.description = $description"
            )
            session.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
                        occupation=occupation, deathdate=deathdate, description=description)

    def delete_person(self, first_name, last_name):
        with self.driver.session() as session:
            query = "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) DETACH DELETE p"
            session.run(query, first_name=first_name, last_name=last_name)

    def deleteEverything(self):
        with self.driver.session() as session:
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)

    def add_married_relationship(self, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
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

    def add_child_of_relationship(self, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
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

    def get_family_tree(self):
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
        
def visualize_family_tree(tree_data):
    G = nx.Graph()

    for record in tree_data:
        G.add_edge(record['person1'], record['person2'], relationship=record['relationship'])

    pos = nx.spring_layout(G, k=0.7)
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()    
    
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