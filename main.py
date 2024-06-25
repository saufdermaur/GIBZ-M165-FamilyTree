from neo4j import GraphDatabase

class FamilyTreeApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, first_name, last_name, birthdate, occupation, deathdate=None, description=None):
        with self.driver.session() as session:
            session.execute_write(self._create_person, first_name, last_name, birthdate, occupation, deathdate, description)

    def _create_person(self, tx, first_name, last_name, birthdate, occupation, deathdate, description):
        query = (
            "CREATE (p:Person {first_name: $first_name, last_name: $last_name, birthdate: $birthdate, occupation: $occupation, deathdate: $deathdate, description: $description})"
        )
        tx.run(query, first_name=first_name, last_name=last_name, birthdate=birthdate, occupation=occupation, deathdate=deathdate, description=description)

    def add_married_relationship(self, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
        with self.driver.session() as session:
            session.execute_write(self._add_married_relationship, person1_first_name, person1_last_name, person2_first_name, person2_last_name)

    def _add_married_relationship(self, tx, person1_first_name, person1_last_name, person2_first_name, person2_last_name):
        # Check if either person is already married
        check_query = (
            "MATCH (p:Person)-[:MARRIED]-(spouse:Person) "
            "WHERE (p.first_name = $person1_first_name AND p.last_name = $person1_last_name) "
            "OR (p.first_name = $person2_first_name AND p.last_name = $person2_last_name) "
            "RETURN p.first_name AS first_name, p.last_name AS last_name, collect(spouse.first_name + ' ' + spouse.last_name) AS spouses"
        )
        result = tx.run(check_query, person1_first_name=person1_first_name, person1_last_name=person1_last_name, person2_first_name=person2_first_name, person2_last_name=person2_last_name)
        marriage_status = result.single()

        if marriage_status:
            for person in marriage_status.items():
                if person in [(person1_first_name, person1_last_name), (person2_first_name, person2_last_name)] and marriage_status['spouses']:
                    raise ValueError(f"{person1_first_name} {person1_last_name} or {person2_first_name} {person2_last_name} is already married to {', '.join(marriage_status['spouses'])}")

        # Create the marriage relationship
        query = (
            "MATCH (p1:Person {first_name: $person1_first_name, last_name: $person1_last_name}), (p2:Person {first_name: $person2_first_name, last_name: $person2_last_name}) "
            "CREATE (p1)-[:MARRIED]->(p2), (p2)-[:MARRIED]->(p1)"
        )
        tx.run(query, person1_first_name=person1_first_name, person1_last_name=person1_last_name, person2_first_name=person2_first_name, person2_last_name=person2_last_name)

    def add_child_of_relationship(self, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
        with self.driver.session() as session:
            session.execute_write(self._add_child_of_relationship, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name)

    def _add_child_of_relationship(self, tx, child_first_name, child_last_name, parent1_first_name, parent1_last_name, parent2_first_name, parent2_last_name):
        query = (
            "MATCH (c:Person {first_name: $child_first_name, last_name: $child_last_name}), "
            "(p1:Person {first_name: $parent1_first_name, last_name: $parent1_last_name}), "
            "(p2:Person {first_name: $parent2_first_name, last_name: $parent2_last_name}) "
            "CREATE (c)-[:CHILD_OF]->(p1), (c)-[:CHILD_OF]->(p2)"
        )
        tx.run(query, child_first_name=child_first_name, child_last_name=child_last_name, parent1_first_name=parent1_first_name, parent1_last_name=parent1_last_name, parent2_first_name=parent2_first_name, parent2_last_name=parent2_last_name)

# Example usage
if __name__ == "__main__":
    # Replace 'bolt://localhost:7687', 'neo4j', 'password' with your Neo4j connection details
    app = FamilyTreeApp("neo4j+s://b0fba925.databases.neo4j.io", "neo4j", "MrGNUAzXQenWSbf0WI4BydfRICBYkG7oTqE5SpNQ4TY")

    try:
        app.create_person("John", "Doe", "1970-01-01", "Engineer")
        app.create_person("Jane", "Smith", "1975-02-02", "Doctor")
        app.add_married_relationship("John", "Doe", "Jane", "Smith")
        app.create_person("Jimmy", "Doe", "2000-03-03", "Student")
        app.add_child_of_relationship("Jimmy", "Doe", "John", "Doe", "Jane", "Smith")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        app.close()
