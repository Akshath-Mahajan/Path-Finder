from django.shortcuts import render
from django.http import HttpResponse
import folium
from .models import DestinationNodes
from .models import Nodes
from .algorithms import Dijkstra, Dijkstra_2, Dijkstra_3

def home(req):
    return render(req, 'Maps/maps_home.html')
def map(request):
     #Replace location with avg of bounds in database
    #68.26% Height fits perfectly in the container and prevents a lot of css-overflow issues which are currently managed by overflow:auto
    #REPLACE LOCATION AND FILL DATABASE
    if request.method == 'POST':
        map1 = folium.Map(location=[19.2120, 72.8567], zoom_start=14)#LOCATION = s.coords+d.coords/2
        s = request.POST['source']
        d = request.POST['destination']
        path = Dijkstra_3(s,d)
        for i in path:
            ob = Nodes.objects.filter(name=i)[0]
            coord = [ob.latitude, ob.longitude]
            folium.Marker(location=coord, popup=i).add_to(map1)
        m = map1._repr_html_()
        return render(request, 'Maps/maps_map.html', {'map':m})

    if request.method == 'GET':
        map1 = folium.Map(location=[19.2120, 72.8567], zoom_start=14)
        destnodes = DestinationNodes.objects.all()  #Destination nodes qs
        for destnode in destnodes:
            n = Nodes.objects.filter(name=destnode.name)[0]
            coord = (n.latitude, n.longitude)
            folium.Marker(location=coord, popup="NODE ID: "+str(n.name)).add_to(map1)
        m = map1._repr_html_()
        return render(request, 'Maps/maps_map.html', {'map':m})
# s,v = 7553183710,7553183709
# Dijkstra_2(s,v)
# print("HERE")
# Dijkstra_3(s,v)

#7048041081,1939199158