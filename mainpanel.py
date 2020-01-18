from neo4j import GraphDatabase


def create_hotel(tx, name, nation, city):
    tx.run("CREATE (a:Hotel {name: $name, city: $city,  nation: $nation}) ",
           name=name, nation=nation, city=city)


def create_reviewer(tx, nameReviewer):
    tx.run("CREATE (a:Reviewer {name: $nameReviewer}) ",
           nameReviewer=nameReviewer)


def add_review(tx, nameHotel, nameReviewer, vote):
    tx.run("MATCH (a:Hotel { name:$nameHotel }),(b:Reviewer { name: $nameReviewer })",
           "MERGE (b)-[r:REVIEW { vote: $vote }]->(a)", nameHotel=nameHotel, nameReviewer=nameReviewer,
           vote=vote)

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    with driver.session() as tx:
        tx.write_transaction(create_hotel, "Residenza K", "Italy", "Rome")
        tx.write_transaction(create_reviewer, "Arthur")
        tx.add_review(add_review, "ResidenzaK", "Merlin", 4.8)

    driver.close()
