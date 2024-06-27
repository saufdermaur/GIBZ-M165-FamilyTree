from neo4j import GraphDatabase
from datetime import date, datetime
import networkx as nx
import matplotlib.pyplot as plt

class FamilyTreeApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.setup_schema()
 
    def close(self):
        self.driver.close()

    def setup_schema(self):
        with self.driver.session() as session:
            # Combination of first name and last name: unique
            session.run("CREATE CONSTRAINT constraint_unique_person_name IF NOT EXISTS FOR (p:Person) REQUIRE (p.first_name, p.last_name) IS NODE KEY")
            # First name: not null, string format
            session.run("CREATE CONSTRAINT constraint_for_person_first_name IF NOT EXISTS FOR (p:Person) REQUIRE p.first_name IS :: STRING")
            # Last name: not null, string format
            session.run("CREATE CONSTRAINT constraint_for_person_last_name IF NOT EXISTS FOR (p:Person) REQUIRE p.last_name IS :: STRING")
            # Birthdate: not null, date format
            session.run("CREATE CONSTRAINT constraint_for_person_birthdate IF NOT EXISTS FOR (p:Person) REQUIRE p.birthdate IS :: DATE")
            # Occupation: string format
            session.run("CREATE CONSTRAINT constraint_for_person_occupation IF NOT EXISTS FOR (p:Person) REQUIRE p.occupation IS :: STRING")
            # Deathdate: date format
            session.run("CREATE CONSTRAINT constraint_for_person_deathdate IF NOT EXISTS FOR (p:Person) REQUIRE p.deathdate IS :: DATE")

            # Create Index on properties
            session.run("CREATE INDEX index_for_person_first_name IF NOT EXISTS FOR (p:Person) ON (p.first_name)")
            session.run("CREATE INDEX index_for_person_last_name IF NOT EXISTS FOR (p:Person) ON (p.last_name)")
            session.run("CREATE INDEX index_for_person_birthdate IF NOT EXISTS FOR (p:Person) ON (p.birthdate)")
            session.run("CREATE INDEX index_for_person_occupation IF NOT EXISTS FOR (p:Person) ON (p.occupation)")
            session.run("CREATE INDEX index_for_person_deathdate IF NOT EXISTS FOR (p:Person) ON (p.deathdate)")
            session.run("CREATE INDEX index_for_person_description IF NOT EXISTS FOR (p:Person) ON (p.description)") 
        
    def _insert_example_data(self, tx):
        # Create people
        self._create_person(tx, "John", "Doe", "1950-07-15", "Retired Engineer", description="Patriarch of the Doe family")
        self._create_person(tx, "Jane", "Doe", "1955-09-20", "Homemaker", description="Matriarch of the Doe family")
        self._create_person(tx, "Mike", "Doe", "1975-03-10", "Doctor", description="Eldest son of John and Jane Doe")
        self._create_person(tx, "Sarah", "Doe", "1978-06-25", "Lawyer", description="Daughter of John and Jane Doe")
        self._create_person(tx, "Emily", "Doe", "1980-11-05", "Teacher", description="Youngest daughter of John and Jane Doe")
        self._create_person(tx, "Mark", "Smith", "1988-04-12", "Architect", description="Son of Robert and Mary Smith")
        self._create_person(tx, "Mary", "Smith", "1990-06-20", "Nurse", description="Wife of Mark Smith")
        self._create_person(tx, "Jacob", "Brown", "1992-09-15", "Software Developer", description="Son of William and Emma Brown")
        self._create_person(tx, "Emma", "Brown", "1994-11-30", "Accountant", description="Wife of Jacob Brown")
        self._create_person(tx, "Sophia", "Jones", "1985-03-22", "Professor", description="Daughter of Peter and Susan Jones")
        self._create_person(tx, "Peter", "Jones", "1960-08-10", "Lawyer", description="Patriarch of the Jones family")
        self._create_person(tx, "Susan", "Jones", "1965-11-25", "Artist", description="Matriarch of the Jones family")
        self._create_person(tx, "Olivia", "Williams", "1993-07-18", "Veterinarian", description="Wife of Mike Doe")
        self._create_person(tx, "Thomas", "Miller", "1995-12-20", "Engineer", description="Husband of Sarah Doe")
        self._create_person(tx, "Karl", "Washington", "1888-04-12", "Entrepreneur", deathdate="1980-05-22", description="Root of the Washington family")
        self._create_person(tx, "Linda", "Washington", "1890-06-20", "Philanthropist", deathdate="1975-04-02", description="Root of the Washington family")

        # Establish relationships
        self._create_marriage_relationship(tx, "John", "Doe", "Jane", "Doe")
        self._create_marriage_relationship(tx, "Mike", "Doe", "Olivia", "Williams")
        self._create_marriage_relationship(tx, "Thomas", "Miller", "Sarah", "Doe")
        self._create_marriage_relationship(tx, "Mark", "Smith", "Mary", "Smith")
        self._create_marriage_relationship(tx, "Jacob", "Brown", "Emma", "Brown")
        self._create_marriage_relationship(tx, "Peter", "Jones", "Susan", "Jones")
        self._create_marriage_relationship(tx, "Karl", "Washington", "Linda", "Washington")

        self._create_child_relationship(tx, "Mike", "Doe", "John", "Doe", "Jane", "Doe")
        self._create_child_relationship(tx, "Sarah", "Doe", "John", "Doe", "Jane", "Doe")
        self._create_child_relationship(tx, "Emily", "Doe", "John", "Doe", "Jane", "Doe")
        self._create_child_relationship(tx, "Mark", "Smith", "John", "Smith", "Susan", "Smith")
        self._create_child_relationship(tx, "Mary", "Smith", "Peter", "Jones", "Susan", "Jones")
        self._create_child_relationship(tx, "Jacob", "Brown", "Peter", "Jones", "Susan", "Jones")
        self._create_child_relationship(tx, "Sophia", "Jones", "Peter", "Jones", "Susan", "Jones")
        self._create_child_relationship(tx, "Susan", "Jones", "Karl", "Washington", "Linda", "Washington")
        self._create_child_relationship(tx, "John", "Doe", "Karl", "Washington", "Linda", "Washington")

    def get_all_people(self):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._get_all_people)
                people = [record for record in result]
                return people

        except Exception as e:
            raise RuntimeError(f"Failed to get all people: {str(e)}")


    def create_person(self, first_name, last_name, birthdate, occupation, deathdate=None, description=None):
        try:
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            if deathdate:
                deathdate = datetime.strptime(deathdate, "%Y-%m-%d").date()
            else:
                deathdate = datetime(1, 1, 1).date()

            with self.driver.session() as session:
                session.write_transaction(self._create_person, first_name, last_name, birthdate, occupation, deathdate, description)
        
        except Exception as e:
            raise RuntimeError(f"Failed to create person: {str(e)}")

    def update_person(self, first_name, last_name, birthdate=None, occupation=None, deathdate=None, description=None):
        try:
            with self.driver.session() as session:
                if birthdate and isinstance(birthdate, str):
                    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

                if deathdate:
                    if isinstance(deathdate, str):
                        deathdate = datetime.strptime(deathdate, "%Y-%m-%d").date()
                    elif isinstance(deathdate, date):
                        deathdate = deathdate  # Already a date object
                    else:
                        deathdate = datetime(1, 1, 1).date()  # Default date if None or invalid type

                session.write_transaction(self._update_person, first_name, last_name, birthdate, occupation, deathdate, description)
        
        except Exception as e:
            raise RuntimeError(f"Failed to update person: {str(e)}")

    def delete_person(self, first_name, last_name):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._delete_person, first_name, last_name)
        
        except Exception as e:
            raise RuntimeError(f"Failed to delete person: {str(e)}")

    def delete_everything(self):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._delete_everything)
        
        except Exception as e:
            raise RuntimeError(f"Failed to delete everything: {str(e)}")

    def add_married_relationship(self, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._create_marriage_relationship, person1_first_name, person1_last_name, person2_first_name, person2_last_name)
        
        except Exception as e:
            raise RuntimeError(f"Failed to add married relationship: {str(e)}")

    def add_child_of_relationship(self, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._create_child_relationship, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name)
        
        except Exception as e:
            raise RuntimeError(f"Failed to add child-of relationship: {str(e)}")

    def get_family_tree(self):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._get_family_tree)
                return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get family tree: {str(e)}")
    
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

    def search_people(self, search_term):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._search_people, search_term)
                return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to search people: {str(e)}")

    def list_and_count_people_over_age(self, age):
        try:
            with self.driver.session() as session:
                count, people = session.read_transaction(self._list_and_count_people_over_age, age)
                return count, people
            
        except Exception as e:
            raise RuntimeError(f"Failed to list and count people over age: {str(e)}")

    def get_persons_with_most_children(self):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._get_persons_with_most_children)
                return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get persons with most children: {str(e)}")

    def get_siblings(self, first_name, last_name):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._get_siblings, first_name, last_name)
                return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get siblings: {str(e)}")

    def count_people(self):
        try:
            with self.driver.session() as session:
                result = session.read_transaction(self._count_people)
                return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to count people: {str(e)}")
        
    # Neo4j Transaktionsfunktionen
    @staticmethod
    def _create_person(tx, first_name, last_name, birthdate, occupation, deathdate=None, description=None):
        query = (
            "CREATE (p:Person {first_name: $first_name, last_name: $last_name, birthdate: $birthdate, "
            "occupation: $occupation, deathdate: $deathdate, description: $description})"
        )
        tx.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
               occupation=occupation, deathdate=deathdate, description=description)

    @staticmethod
    def _update_person(tx, first_name, last_name, birthdate=None, occupation=None, deathdate=None, description=None):
        query = (
            "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) "
            "SET p.birthdate = $birthdate, p.occupation = $occupation, "
            "p.deathdate = $deathdate, p.description = $description"
        )
        tx.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate,
               occupation=occupation, deathdate=deathdate, description=description)

    @staticmethod
    def _delete_person(tx, first_name, last_name):
        query = (
            "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) "
            "DETACH DELETE p"
        )
        tx.run(query, first_name=first_name, last_name=last_name)

    @staticmethod
    def _delete_everything(tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)

    @staticmethod
    def _create_marriage_relationship(tx, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
        query = (
            "MATCH (p1:Person {first_name: $person1_first_name, last_name: $person1_last_name}), "
            "(p2:Person {first_name: $person2_first_name, last_name: $person2_last_name}) "
            "CREATE (p1)-[:MARRIED_TO]->(p2)"
        )
        tx.run(query, person1_first_name=person1_first_name, person1_last_name=person1_last_name,
               person2_first_name=person2_first_name, person2_last_name=person2_last_name)

    @staticmethod
    def _create_child_relationship(tx, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
        query = (
            "MATCH (child:Person {first_name: $child_first_name, last_name: $child_last_name}), "
            "(parent1:Person {first_name: $parent1_first_name, last_name: $parent1_last_name}), "
            "(parent2:Person {first_name: $parent2_first_name, last_name: $parent2_last_name}) "
            "CREATE (child)-[:CHILD_OF]->(parent1), (child)-[:CHILD_OF]->(parent2)"
        )
        tx.run(query, child_first_name=child_first_name, child_last_name=child_last_name,
               parent1_first_name=parent1_first_name, parent1_last_name=parent1_last_name,
               parent2_first_name=parent2_first_name, parent2_last_name=parent2_last_name)

    @staticmethod
    def _get_all_people(tx):
        query = "MATCH (p:Person) RETURN p.first_name, p.last_name"
        result = tx.run(query)
        return [{"first_name": record['p.first_name'], "last_name": record['p.last_name']} for record in result]

    @staticmethod
    def _get_family_tree(tx):
        query = (
            "MATCH path=(p:Person)-[:CHILD_OF*]->(ancestor:Person) "
            "RETURN path"
        )
        result = tx.run(query)
        return result

    @staticmethod
    def _search_people(tx, search_term):
        query = (
            "MATCH (p:Person) "
            "WHERE p.first_name CONTAINS $search_term OR p.last_name CONTAINS $search_term "
            "RETURN p.first_name, p.last_name"
        )
        result = tx.run(query, search_term=search_term)
        return [{"first_name": record['p.first_name'], "last_name": record['p.last_name']} for record in result]

    @staticmethod
    def _list_and_count_people_over_age(tx, age):
        current_year = datetime.now().year
        birth_year = current_year - age
        query = (
            "MATCH (p:Person) "
            "WHERE p.birthdate.year <= $birth_year "
            "RETURN count(p) as count, collect({first_name: p.first_name, last_name: p.last_name}) as people"
        )
        result = tx.run(query, birth_year=birth_year)
        record = result.single()
        return record['count'], record['people']

    @staticmethod
    def _get_persons_with_most_children(tx):
        query = (
            "MATCH (parent:Person)-[:CHILD_OF]->(:Person) "
            "RETURN parent.first_name, parent.last_name, count(*) as children_count "
            "ORDER BY children_count DESC"
        )
        result = tx.run(query)
        return [{"first_name": record['parent.first_name'], "last_name": record['parent.last_name'],
                 "children_count": record['children_count']} for record in result]

    @staticmethod
    def _get_siblings(tx, first_name, last_name):
        query = (
            "MATCH (:Person {first_name: $first_name, last_name: $last_name})-[:CHILD_OF]->(parent:Person)<-[:CHILD_OF]-(sibling:Person) "
            "WHERE NOT (sibling {first_name: $first_name, last_name: $last_name}) "
            "RETURN sibling.first_name, sibling.last_name"
        )
        result = tx.run(query, first_name=first_name, last_name=last_name)
        return [{"first_name": record['sibling.first_name'], "last_name": record['sibling.last_name']} for record in result]

    @staticmethod
    def _count_people(tx):
        query = "MATCH (p:Person) RETURN count(p) as count"
        result = tx.run(query)
        return result.single()['count']
    
def test_connection(uri, user, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()['count']
            print(f"Successfully connected to the database. Found {count} nodes.")
            return True
    except Exception as e:
        print(f"Failed to connect to the database: {str(e)}")
        return False
    
def visualize_family_tree(tree_data):
    G = nx.Graph()

    for record in tree_data:
        G.add_edge(record['person1'], record['person2'], relationship=record['relationship'])

    pos = nx.spring_layout(G, k=0.9)
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()    