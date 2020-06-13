from .models import Nodes
from .models import DestinationNodes
from .models import Edges
import time
from django.db.models import Q
from .heaps import minHeap

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
    print(res)
    return res

def Dijkstra_2(source, destination):
    print("DIJKSTRA_2")
    nearest_s_ID = DestinationNodes.objects.filter(name=source)[0].nearest_neighbour
    nearest_d_ID = DestinationNodes.objects.filter(name=destination)[0].nearest_neighbour
    starttime = time.time()
    #Load Graph into ram:
    all_road_nodes = Nodes.objects.filter(isRoadNode=True)
    all_edges = Edges.objects.all()
    edges_in = {}
    for v in all_road_nodes:
        edges_in[v.name] = Edges.objects.filter(Q(node1=v.name)|Q(node2=v.name))

    X = [nearest_s_ID]  #Processed Node IDS
    A = {nearest_s_ID:0}
    path = {}
    
    print(time.time()-starttime)
    while X[-1] != nearest_d_ID:
        mincost = float('inf')
        for v in X: #v is ID
            for edge in edges_in[v]:
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
    print(res)
    return res

def Dijkstra_3(source, destination):
    nearest_s_ID = DestinationNodes.objects.filter(name=source)[0].nearest_neighbour
    nearest_d_ID = DestinationNodes.objects.filter(name=destination)[0].nearest_neighbour
    starttime = time.time()
    #Load Graph into ram:
    all_road_nodes = Nodes.objects.filter(isRoadNode=True)
    all_edges = Edges.objects.all()
    edges_in = {}
    for v in all_road_nodes:
        edges_in[v.name] = Edges.objects.filter(Q(node1=v.name)|Q(node2=v.name))

    X = {roadnode.name:False for roadnode in all_road_nodes}  #Processed Node IDS
    X[nearest_s_ID] = True
    A = {nearest_s_ID:0}
    path = {}
    X_SET = [nearest_s_ID]
    #print(time.time()-starttime)
    while X_SET[-1] != nearest_d_ID:
        mincost = float('inf')
        for v in X_SET: #v is ID
            for edge in edges_in[v]:
                if X[edge.node1] and X[edge.node2]:
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
        X[w_star] = True
        X_SET.append(w_star)
        path[w_star] = v_star
    #print(time.time()-starttime)
    t = nearest_d_ID
    res = []
    while(t != nearest_s_ID):
        res.append(t)
        t = path[t]
    res.append(nearest_s_ID)
    print(time.time()-starttime)
    print(res)
    return res

def Dijkstra_4(source, destination):
    nearest_s_ID = DestinationNodes.objects.filter(name=source)[0].nearest_neighbour
    nearest_d_ID = DestinationNodes.objects.filter(name=destination)[0].nearest_neighbour
    starttime = time.time()
    #Load Graph into ram:
    all_road_nodes = Nodes.objects.filter(isRoadNode=True)
    all_edges = Edges.objects.all()
    edges_in = {}
    for v in all_road_nodes:
        edges_in[v.name] = Edges.objects.filter(Q(node1=v.name)|Q(node2=v.name))
    isInHeap = {roadnode.name:False for roadnode in all_road_nodes}  #Processed Node IDS
    isInHeap[nearest_s_ID] = True
    A = {nearest_s_ID:0}
    path = {}
    X_SET = [nearest_s_ID]

    '''Initialize Heap'''

    edges_of_source = Edges.objects.filter(Q(node1=nearest_s_ID)|Q(node2=nearest_s_ID)).order_by('cost')
    heap = minHeap()
    for edge_ in edges_of_source:
        if edge_.node1 == nearest_s_ID:
            adding_node = edge_.node2
        else:
            adding_node = edge_.node1
        if not isInHeap[adding_node]:            
            heap.insert((edge_.cost, adding_node))
            isInHeap[adding_node] = True
    for roadnode in all_road_nodes:
        if not isInHeap[roadnode.name]:
            heap.insert((float('inf'), roadnode.name))
            isInHeap[roadnode.name] = True
    isInHeap[nearest_s_ID] = False
    #print(time.time()-starttime)
    while X_SET[-1] != nearest_d_ID:
        root = heap.extract_min()
        cost_to_add_in_path = root[0]
        w_star = root[1]
        A[w_star] = cost_to_add_in_path
        X_SET.append(w_star)
        isInHeap[w_star] = False
        for edge in edges_in[w_star]:
            if edge.node1 == w_star:
                v = edge.node2
            else:
                v = edge.node1
            if not isInHeap[v]: #has been processed
                if A[v]+edge.cost == cost_to_add_in_path:
                    v_star = v
            else:
                index = heap.ID_TO_INDEX[v]
                heap.arr[index] = min(heap.arr[index], (cost_to_add_in_path+edge.cost, v))
                ParentIndex = heap.get_parent_index(index)
                while heap.arr[ParentIndex] > heap.arr[index]:
                    heap.swap(ParentIndex, index)
                    index = ParentIndex
                    ParentIndex = heap.get_parent_index(index)
                    if ParentIndex == -1:
                        break
        path[w_star] = v_star
    #print(time.time()-starttime)
    t = nearest_d_ID
    res = []
    while(t != nearest_s_ID):
        res.append(t)
        t = path[t]
    res.append(nearest_s_ID)
    print(time.time()-starttime)
    #print(res)
    return res      