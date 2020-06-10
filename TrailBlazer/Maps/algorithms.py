from .models import Nodes
from .models import DestinationNodes
from .models import Edges
import time
from django.db.models import Q
def Dijkstra(source, destination):
    starttime = time.time()
    s = Nodes.objects.filter(name=source)[0]    #Marked on map
    d = Nodes.objects.filter(name=destination)[0]   #Marked on map
    
    #Road nodes v
    nearest_s_ID = DestinationNodes.objects.filter(name=source)[0].nearest_neighbour
    nearest_d_ID = DestinationNodes.objects.filter(name=destination)[0].nearest_neighbour
    all_edges = Edges.objects.all()
    X = [nearest_s_ID]  #Processed Node IDS
    A = {}
    A[nearest_s_ID] = 0
    path = {}
    print(time.time()-starttime)
    while X[-1] != nearest_d_ID:
        mincost = float('inf')
        for v in X: #v is ID
            edges_with_v = Edges.objects.filter(Q(node1=v)|Q(node2=v))
            for edge in edges_with_v:
                if edge.node1 in X and edge.node2 in X:
                    continue
                dijkstra_greedy = A[v] + edge.cost
                if dijkstra_greedy < mincost:
                    mincost = dijkstra_greedy
                    if edge.node1 == v:
                        w_star = edge.node2
                        v_star = v
                    else:
                        w_star = edge.node1
                        v_star = v
        A[w_star] = mincost
        X.append(w_star)
        path[w_star] = v_star
    print(time.time()-starttime)
    t = nearest_d_ID
    res = []
    while(t != nearest_s_ID):
        res.append(t)
        t = path[t]
    print(time.time()-starttime)
    return res