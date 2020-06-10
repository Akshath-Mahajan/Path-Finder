from django.shortcuts import render
from django.http import HttpResponse
import folium
from .models import DestinationNodes
from .models import Nodes
from .algorithms import Dijkstra

def home(req):
    return render(req, 'Maps/maps_home.html')
def map(request):
     #Replace location with avg of bounds in database
    #68.26% Height fits perfectly in the container and prevents a lot of css-overflow issues which are currently managed by overflow:auto
    #REPLACE LOCATION AND FILL DATABASE
    if request.method == 'POST':
        map1 = folium.Map(location=[19.2120, 72.8567], zoom_start=14)
        path = Dijkstra(7553183710,7553183709)
        for i in path:
            print(i)
            ob = Nodes.objects.filter(name=i)[0]
            coord = [ob.latitude, ob.longitude]
            folium.Marker(location=coord).add_to(map1)
        m = map1._repr_html_()
        #Add path to map before returning
        #opt1 - remove all nodes except start and end and display map [will need to add reset button too as people cant remember all node ids]
        #opt2 - Keep all destination nodes and just add path [no need to add reset map button]
        #set location of  returning map to be average of node1coords and node2coords
        return render(request, 'Maps/maps_map.html', {'map':m})
    if request.method == 'GET':
        map1 = folium.Map(location=[19.2120, 72.8567], zoom_start=14)
        destnodes = DestinationNodes.objects.all()  #Destination nodes qs
        for destnode in destnodes:
            n = Nodes.objects.filter(name=destnode.name)[0]
            coord = (n.latitude, n.longitude)
            folium.Marker(location=coord, popup="NODE ID: "+str(n.name)).add_to(map1)
        m = map1._repr_html_()
        #Add destination nodes to map before returning
        return render(request, 'Maps/maps_map.html', {'map':m})