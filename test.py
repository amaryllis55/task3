import random
from neo4j import GraphDatabase
from getpass import getpass


def manageLogin(graph_mg, options):
    # print("ADMIN MENU")
    print("Insert admin password or 'exit' to return to main menu. \n")
    pw = getpass()
    while (True):
        if pw == "admin":
            option = ["logout", "fake reviewers"]

            while (True):
                chosen = input("Select option or enter 'help' to see command list: \n")
                if chosen == option[0]:  # logout
                    pw = "exit"
                    break
                if chosen == option[1]:  # show possible fake reviewers
                    print(option[1])
                if chosen == options[1]:
                    graph_mg.popular_hotels()
                if chosen == options[2]:
                    graph_mg.reccomandRev()
                if chosen == "help":
                    print(option[0] + " - logout and return to main menu")
                    print(option[1] + " - show possible fake reviewers")
                    print(options[1] + " - show most popular hotels")
                    print(options[2] + " - find all the reviews by a specific reviewer\n")
                if chosen == "exit":
                    pw = "exit"
                    break
        elif pw == "exit":
            break
        else:
            print("Input not valid.\n")
            print("Insert admin password or 'exit' to return to main menu. \n")
            pw = getpass()


class Connection:
    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "amalia"))

    def getSession(self):
        return self._driver.session()

    def close(self):
        self._driver.close()


class DBManager:
    def __init__(self):
        self.conn = None
        self.session = None

    def openConnection(self):
        if self.conn == None:
            self.conn = Connection()

    def closeConnection(self):
        if self.conn != None:
            self.conn.close()

    def getSession(self):
        if self.session == None:
            self.session = self.conn.getSession()
        return self.session


class GraphManager:
    def __init__(self):
        self.dbm = DBManager()

    def openConnection(self):
        self.dbm.openConnection()

    def closeConnection(self):
        self.dbm.closeConnection()

    def getSession(self):
        return self.dbm.getSession()

    def getReviewerNames(self):
        self.getSession()
        return self.getSession().run("MATCH (n:Reviewer) return distinct n.name")

    def create_hotel(self, name, nation, city):
        ses = self.getSession()
        ses.run("MERGE (n:Hotel {name: $nameHotel,  city:$city, nation: $nation}) ", nameHotel=name,
                city=city, nation=nation)

    def create_reviewer(self, nameReviewer):
        ses = self.getSession()
        ses.run("MERGE (a:Reviewer {name: $nameReviewer}) ",
                nameReviewer=nameReviewer)

    def add_review(self, nameHotel, nameReviewer, vote):
        ses = self.getSession()
        ses.run(
            "MATCH (a:Reviewer), (b:Hotel) WHERE a.name = $nameReviewer AND b.name = $nameHotel   MERGE (a)-[r:REVIEW]->(b) SET r.vote=$vote",
            nameHotel=nameHotel, nameReviewer=nameReviewer, vote=vote)

    def delete_hotel(self, nameHotel):
        ses = self.getSession()
        ses.run(" MATCH (n { name: $nameHotel }) DETACH DELETE n", nameHotel=nameHotel)

    def delete_reviewer(self, nameReviewer):
        ses = self.getSession()
        ses.run(" MATCH (n { name: $nameReviewer }) DETACH DELETE n", nameReviewer=nameReviewer)

    def delete_review(self, nameHotel, nameReviewer):
        ses = self.getSession()
        ses.run("MATCH (b:Reviewer)-[r]->(a:Hotel) where a.name=$nameHotel and b.name=$nameReviewer DETACH DELETE r",
                nameReviewer=nameReviewer, nameHotel=nameHotel)

    def seeGraph(self):
        ses = self.getSession()
        pg = ses.run("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
        print(pg.single()["n"]["name"])

    def dropEverything(self):
        ses = self.getSession()
        ses.run("MATCH (n) DETACH DELETE n")

    def printRelationshipHotel(self, nameHotel):
        ses = self.getSession()
        rec = ses.run("MATCH ()-[r:REVIEW]->(b:Hotel) WHERE b.name = $nameHotel RETURN r.vote", nameHotel=nameHotel)
        for record in rec:
            print(record)

    def printHotelNames(self):
        ses = self.getSession()
        for record in ses.run("MATCH (n:Hotel) RETURN n.name"):
            print(record["n.name"])

    def printNations(self):
        ses = self.getSession()
        if ses == None:
            print("prob")
        nat = []
        for record in ses.run("MATCH (n:Hotel) RETURN distinct n.nation"):
            print(record["n.nation"] + "\n")
            nat.append(record["n.nation"])
        return (nat)

    def printCities(self):
        ses = self.getSession()
        for record in ses.run("MATCH (n:Hotel) RETURN distinct n.city"):
            print(record["n.city"] + "\n")

    def printReviewers(self):
        ses = self.getSession()
        result = []
        for item in ses.run("MATCH (n:Reviewer) RETURN n.name as nameRev"):
            result.append(item["nameRev"])
        return result

    def deleteNationHotels(self):
        while (True):
            nat = graph_mg.printNations()
            choice = input("Select nation to be deleted or enter 'exit' to return to administrator menu: ")
            if choice in nat:
                ses = self.getSession()
                ses.run("MATCH (n { nation: $nation }) DETACH DELETE n ", nation=choice)
                break
            elif choice == "exit":
                break
            else:
                print("Choice not valid.\n")

    def reccomandRev(self):
        ses = self.getSession()
        choice = input(
            "Enter reviewer's name, 'list reviewers' to see all the reviewers in the system or exit to return to administrator menu: ")
        lista = self.printReviewers()
        while (True):
            if choice in list:
                print(
                    ses.run(
                        "MATCH (me:Reviewer)-[myReview:REVIEW]->(h:Hotel)<-[sameHotelReview:REVIEW]-otherPerson:Reviewer)-[otherReview:Review]->(otherHotel:Hotel) "
                        "WHERE me.name = $nameRev AND myReview.vote > 7 AND sameHotelReview.vote > 7   AND otherReview.vote > 7 AND me != otherReview AND otherHotel != h RETURN otherHotel",
                        nameRev=choice))

                break
            elif choice == "list reviewers":
                for item in lista:
                    print(item)
            elif choice == "exit":
                break
            else:
                print("Input not valid.\n")
                choice = input(
                    "Enter reviewer's name, 'list reviewers' to see all the reviewers in the system or exit to return to administrator menu: ")

        # print(ses.run("CALL algo.degree.stream(Hotel, REVIEW, {direction: incoming}) YIELD nodeId, score RETURN algo.asNode(nodeId).id AS name, score AS followers ORDER BY followers DESC"))

    def popular_hotels(self):
        ses = self.getSession()
        print(ses.run(
            "CALL algo.degree.stream(Hotel, REVIEW, {direction: incoming}) YIELD nodeId, score RETURN algo.asNode(nodeId).id AS name, score AS followers ORDER BY followers DESC"))

def populateGraph(graph_mg):
    graph_mg.openConnection()
    graph_mg.getSession()
    hotels=[]
    cities=["Naples", "Cincinnati", "Tucson"]
    nations=["USA", "Italy"]
    for i in range(5):
        hotels.append("H"+str(i))
    for hotel in hotels:
        graph_mg.create_hotel(hotel, random.choice(nations), random.choice(cities))
    reviewers=[]
    for i in range(4):
        reviewers.append("Nome"+str(i))
    for reviewer in reviewers:
        graph_mg.create_reviewer(reviewer)
    ses=graph_mg.getSession()
    for record in ses.run("MATCH (n:Reviewer) RETURN n.name"):
        print(record["n.name"])
    graph_mg.add_review("H3", "Nome2", 8)
    graph_mg.add_review("H3", "Nome3", 9)
    graph_mg.add_review("H2", "Nome3", 8)
    graph_mg.add_review("H1", "Nome3", 7)
    graph_mg.add_review("H4", "Nome3", 9)

    result=ses.run(
        "MATCH (me:Reviewer)-[myReview:REVIEW]->(h:Hotel)<-[sameHotelReview:REVIEW]-(otherPerson:Reviewer)-[otherReview:REVIEW]->(otherHotel:Hotel) "
        "WHERE me.name = $nameRev AND myReview.vote > 7 AND sameHotelReview.vote > 7   AND otherReview.vote > 7 AND me <> otherReview AND otherHotel <> h RETURN otherHotel",
        nameRev="Nome2")
    for item in result:
        print(item)
    graph_mg.dropEverything()
    graph_mg.closeConnection()

if __name__ == '__main__':

    populateGraph(GraphManager())