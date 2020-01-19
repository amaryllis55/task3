from neo4j import GraphDatabase


class Connection:
    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "amalia"))

    def getSession(self):
        return self._driver.session()

    def close(self):
        self._driver.close()


class GraphManager:
    def __init__(self):
        self.conn = None
        self.session = None

    def openConnection(self):
        if self.conn == None:
            self.conn = Connection()

    def closeConnection(self):
        self.conn.close()

    def getSession(self):
        if self.session == None:
            self.session = self.conn.getSession()

    def create_hotel(self, name, nation, city):
        ses = self.conn.getSession()
        ses.run("CREATE (a:Hotel {name: $name, city: $city,  nation: $nation}) ",
                name=name, nation=nation, city=city)

    def create_reviewer(self, nameReviewer):
        ses = self.conn.getSession()
        ses.run("CREATE (a:Reviewer {name: $nameReviewer}) ",
                nameReviewer=nameReviewer)

    def add_review(self, nameHotel, nameReviewer, vote):
        ses = self.conn.getSession()
        ses.run(
            "MATCH (a:Reviewer), (b:Hotel) WHERE a.name = $nameReviewer AND b.name = $nameHotel   MERGE (a)-[r:REVIEW]->(b) SET r.vote=$vote",
            nameHotel=nameHotel, nameReviewer=nameReviewer,            vote=vote)

    def delete_hotel(self, nameHotel):
        ses = self.conn.getSession()
        ses.run(" MATCH (n { name: $nameHotel })", "DETACH DELETE n", nameHotel=nameHotel)

    def delete_reviewer(self, nameReviewer):
        ses = self.conn.getSession()
        ses.run(" MATCH (n { name: $nameReviewer })", "DETACH DELETE n", nameHotel=nameReviewer)

    def seeGraph(self):
        ses = self.conn.getSession()
        pg=ses.run("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
        print(pg.single()["n"]["name"])

    def dropEverything(self):
        ses = self.conn.getSession()
        ses.run("MATCH (n) DETACH DELETE n")
    def printRelationshipHotel(self, nameHotel):
        ses=self.conn.getSession()
        rec=ses.run("MATCH ()-[r:REVIEW]->(b:Hotel) WHERE b.name = $nameHotel RETURN r.vote", nameHotel=nameHotel)
        for record in rec:
            print(record)





if __name__ == '__main__':
    graph_mg=GraphManager()
    graph_mg.openConnection()
    graph_mg.getSession()

    graph_mg.create_hotel("Hotel", "J", "hf")
    graph_mg.create_reviewer("Rev")
    graph_mg.create_reviewer("Pinco")
    graph_mg.add_review("Hotel", "Rev", 7)
    graph_mg.add_review("Hotel", "Pinco", 6)

    graph_mg.printRelationshipHotel("Hotel")


    graph_mg.dropEverything()
    graph_mg.closeConnection()