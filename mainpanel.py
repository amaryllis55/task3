from neo4j import GraphDatabase
from test import populateGraph
from getpass import getpass


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
        self.dbm=DBManager()

    def openConnection(self):
        self.dbm.openConnection()

    def closeConnection(self):
        self.dbm.closeConnection()

    def getSession(self):
        return self.dbm.getSession()


    def create_hotel(self, name, nation="nat", city="rr"):
        ses = self.getSession()
        ses.run("CREATE (a:Hotel {name: $name, city: $city,  nation: $nation}) ",
                name=name, nation=nation, city=city)

    def create_reviewer(self, nameReviewer):
        ses = self.getSession()
        ses.run("CREATE (a:Reviewer {name: $nameReviewer}) ",
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
        if ses==None:
            print("prob")
        nat=[]
        for record in ses.run("MATCH (n:Hotel) RETURN distinct n.nation"):
            print(record["n.nation"]+ "\n")
            nat.append(record["n.nation"])
        return(nat)


    def printCities(self):
        ses = self.getSession()
        for record in ses.run("MATCH (n:Hotel) RETURN distinct n.city"):
            print(record["n.city"] + "\n")

    def printReviewers(self):
        ses = self.getSession()
        for record in ses.run("MATCH (n:Reviewer) RETURN n.name as nameRev"):
            print(record["nameRev"])
    def deleteNationHotels(self):
        while(True):
            nat=graph_mg.printNations()
            choice = input("Select nation to be deleted or enter 'exit' to return to administrator menu: ")
            if choice in nat:
                ses = self.getSession()
                ses.run("MATCH (n { nation: $nation }) DETACH DELETE n ", nation=choice)
                break
            elif choice=="exit":
                break
            else:
                print("Choice not valid.\n")


    def manageLogin(self):
        print("ADMIN MENU")
        print("Insert admin password or 'exit' to return to main menu. \n")
        pw = getpass()
        while(True):

            if pw=="admin":
                option = ["logout", "delete nation", "delete city", "delete hotel", "delete reviewer",
                          "delete review", "find user"]

                while (True):
                    chosen = input("Select option or enter 'help' to see command list: ")
                    if chosen == option[0]:  # logout
                        break
                    if chosen == option[1]:  # delete nation
                       graph_mg.deleteNationHotels()
                    if chosen == option[2]:  # delete city
                        print("TODO")
                    if chosen == option[3]:  # delete hotel
                       print(option[3])
                    if chosen == option[4]:  # delete reviewer
                        print(option[4])
                    if chosen == option[5]:  # delete review
                        print(option[5])
                    if chosen == option[6]:  # find user
                        print(option[6])

                    if chosen == options[1]:  # analitycs
                        print(options[1])
                    if chosen == options[2]:  # statistics
                        print(options[2])
                    if chosen == options[3]:  # "find hotel"
                        print(options[3])
                    if chosen == options[4]:  # "find reviewer"
                        print(options[4])
                    if chosen == options[5]:  # "list Nations"
                        graph_mg.printNations()
                    if chosen == "help":
                        for item in option:
                            print(item)
                        for item in options:
                            print(item)
                    if chosen == "exit":
                        pw="exit"
                        break
            elif pw=="exit":
                break
            else:
                print("Input not valid.\n")
                print("Insert admin password or 'exit' to return to main menu. \n")
                pw = getpass()




if __name__ == '__main__':
    options = ["login", "read analytics", "read statistics", "find hotel", "find reviewer", "list nations"]
    print("Options:\n")
    for item in options:
        print(item + "\n")
    print("Select an option or enter exit to quit the application (enter 'help' for command explanation).\n")
    graph_mg = GraphManager()
    graph_mg.openConnection()
    #populateGraph(graph_mg)   uncomment just once to populate graph
    while (True):

        chosen = input("Choice: ")

        if chosen == options[0]:  # login
            graph_mg.getSession()
            graph_mg.manageLogin()
            print("MAIN MENU\n")
        if chosen == options[1]:  # analitycs
            graph_mg.getSession()
        if chosen == options[2]:  # statistics
            graph_mg.getSession()
        if chosen == options[3]:  # "find hotel"
            graph_mg.getSession()
            graph_mg.printHotelNames()
        if chosen == options[4]:  # "find reviewer"
            graph_mg.getSession()
            graph_mg.printReviewers()
        if chosen == options[5]:  # "list Nations"
            graph_mg.getSession()
            graph_mg.printNations()
        if chosen == "help":
            print(options[0] + " - log in the application\n")
            print(options[1] + " - show available analytics about hotels in specific city or nation\n")
            print(options[2] + " - show available statistics about hotels in a specific city or nation\n")
            print(options[3] + " - find hotel in the system\n")
            print(options[4] + " - find all the reviews by a specific reviewer\n")
            print(options[5] + " - print all nations in the system\n")

        if chosen == "exit":
            break
        print("Select an option or enter exit to quit the application (enter 'help' for command explanation).\n")
    if graph_mg != None:
        graph_mg.closeConnection()
