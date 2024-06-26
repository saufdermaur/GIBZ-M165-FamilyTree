from neo4j import GraphDatabase

class FamilyTreeApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

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
        
if __name__ == "__main__":
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
