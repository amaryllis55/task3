from neo4j import GraphDatabase


def create_hotel(tx, name, nation, city):
    tx.run("CREATE (a:Hotel {name: $name, city: $city,  nation: $nation}) ",
           "CREATE CONSTRAINT ON (a:Hotel) ASSERT a.name IS UNIQUE",
           name=name, nation=nation, city=city)


def create_reviewer(tx, name):
    tx.run("CREATE (a:Reviewer {name: $name}) ",
           "CREATE CONSTRAINT ON (a:Hotel) ASSERT a.name IS UNIQUE",
           name=name)


def add_review(tx, nameHotel, nameReviewer, vote):
    tx.run("MATCH (a:Hotel),(b:Reviewer) WHERE a.name = $nameHotel AND b.name = $nameReviewer",
           "CREATE (a)-[r:REVIEW { vote: $vote }]->(b)",
           "RETURN type(r), r.name", nameHotel=nameHotel, nameReviewer=nameReviewer, vote=vote)



if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    with driver.session() as tx:
        tx.write_transaction(create_hotel, "Residenza K", "Italy", "Rome")
        tx.write_transaction(create_reviewer, "Arthur")
        tx.add_review(add_review, "ResidenzaK", "Merlin", 4.8)

    driver.close()
