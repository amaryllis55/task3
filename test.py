import random
def populateGraph(graph_mg):
    graph_mg.openConnection()
    graph_mg.getSession()
    hotels=[]
    cities=["Naples", "Cincinnati", "Tucson"]
    nations=["USA", "Italy"]
    for i in range(20):
        hotels.append("H"+str(i))
    for hotel in hotels:
        graph_mg.create_hotel(hotel, random.choice(nations), random.choice(cities))
    graph_mg.printHotelNames()
