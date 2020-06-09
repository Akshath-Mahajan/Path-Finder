from .models import Nodes
from .models import DestinationNodes
from .models import Edges
def get_nodes(filename):
    fh = open(filename, 'r', encoding='utf-8')
    ID_TO_COORDS = {}
    for line in fh:
        line = line.strip()
        if line.startswith('<node'):
            ID = line[line.index('=')+2:line.index('lat')-2]
            LAT = line[line.index('lat="')+5:line.index('" lon=')]
            LON = line[line.index('lon="')+5:line.index('" ve')]
            ID_TO_COORDS[int(ID)] = (float(LAT), float(LON))
            node = Nodes(name=int(ID), latitude=float(LAT), longitude=float(LON), isRoadNode=False)
            node.save()
    fh.close()
    return ID_TO_COORDS
def get_edges(filename, ID_TO_COORDS):
    fh = open(filename, 'r', encoding='utf-8')
    alldata = fh.read().split('\n')
    fh.close()
    for i in range(len(alldata)):
        alldata[i] = alldata[i].strip()
    i = 0
    edges = set()
    prevNode = None
    currentNode = None
    inWayElement = False
    isRoute = False

    while i < len(alldata):
        if alldata[i].startswith('<way'):
            prevNode = None
            currentNode = None
            isRoute = False
            edges_this_way = []
            inWayElement = True
        if alldata[i].startswith('</way'):
            if isRoute:
                for j in edges_this_way[1:]:    #To exclude (none, node1)
                    edges.add(j)
            inWayElement = False
        if inWayElement:
            if alldata[i].startswith('<nd'):
                prevNode = currentNode
                currentNode = int(alldata[i][alldata[i].index('"')+1:alldata[i].index("/")-1])
                edges_this_way.append((prevNode, currentNode))
            if alldata[i].startswith('<tag k="highway"'):
                isRoute = True
        i+=1
    roadNodes = set()
    for i in edges:
        coord1 = ID_TO_COORDS[i[0]]
        coord2 = ID_TO_COORDS[i[1]]
        n1 = Nodes.objects.filter(name=i[0])[0]
        n1.isRoadNode = True
        n1.save()
        n2 = Nodes.objects.filter(name=i[1])[0]
        n2.isRoadNode = True
        n2.save()
        #Mark i[0] node and i[1] node as roadnodes
        roadNodes.add(coord1)
        roadNodes.add(coord2)
        dist = ((coord1[0]-coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5
        edge = Edges(node1 = i[0], node2 = i[1], cost=dist)
        edge.save()
    return roadNodes

def get_destination_nodes(filename, ID_TO_COORDS, roadNodes):
    fh = open(filename, encoding='utf-8')
    data = fh.read().split('\n')
    fh.close()
    for i in range(len(data)):
        data[i] = data[i].strip()
    inNodeElement = False
    isToBeAdded = False
    dests = []
    i = 0
    j = 0
    boo = False
    while i < len(data):
        if data[i].startswith('<node'):
            if not data[i].endswith('/>'):
                line = data[i]
                dest_node_id = int(line[line.index('="')+2:line.index('" lat')])
                inNodeElement = True
        if data[i].startswith('</node'):
            inNodeElement = False
            if isToBeAdded:
                j+=1
                dests.append(dest_node_id)
                isToBeAdded = False
        if inNodeElement:
            if data[i].startswith('<tag k="amenity"') or data[i].startswith('<tag k="shop"') or data[i].startswith('<tag k="sport"'):
                isToBeAdded = True
        i+=1
    
    for i in dests:
        coord1 = ID_TO_COORDS[i]
        nearestNeighbour = -1
        mindist = float('inf')
        for j in roadNodes:
            coord2 = ID_TO_COORDS[j]
            dist = ((coord1[0]-coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5
            if dist<mindist:
                mindist = dist
                nearestNeighbour = j
        dn = DestinationNodes(name=i, nearest_neighbour=nearestNeighbour)
        dn.save()

filename = 'raw_data/MAP_Borivali-Kandivali.txt'
id_to_coords = get_nodes(filename)
roadNodes = get_edges(filename, id_to_coords)
get_destination_nodes(filename, id_to_coords, roadNodes)
