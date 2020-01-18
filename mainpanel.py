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
        ses.run("MATCH (b:Reviewer { name: $nameReviewer }) MATCH ((a:Hotel { name:$nameHotel })) MERGE (b)-[r:REVIEW ]->(a) SET r.vote = $vote", nameHotel=nameHotel, nameReviewer=nameReviewer,
                vote=vote)

    def delete_hotel(self, nameHotel):
        ses = self.conn.getSession()
        ses.run(" MATCH (n { name: $nameHotel })", "DETACH DELETE n", nameHotel=nameHotel)

    def delete_reviewer(self, nameReviewer):
        ses = self.conn.getSession()
        ses.run(" MATCH (n { name: $nameReviewer })", "DETACH DELETE n", nameHotel=nameReviewer)

    def getReviewers(self, hotelName):
        print("TODO") #restituisce gli id dei reviewers



