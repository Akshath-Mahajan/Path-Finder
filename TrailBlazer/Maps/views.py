from django.shortcuts import render
from django.http import HttpResponse
import folium
from .models import DestinationNodes
from .models import Nodes
from .algorithms import Dijkstra_4

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
        
        all_nodes = Nodes.objects.all()
        s_coords = all_nodes.filter(name=s)[0].latitude, all_nodes.filter(name=s)[0].longitude
        d_coords = all_nodes.filter(name=d)[0].latitude, all_nodes.filter(name=d)[0].longitude
        print(s,d)
        path = Dijkstra_4(s,d)
        coords = []
        for i in path:
            ob = all_nodes.filter(name=i)[0]
            coords.append([ob.latitude, ob.longitude])
        folium.PolyLine(coords, color='red', weight = 4.5).add_to(map1)
        folium.Marker(s_coords).add_to(map1)
        folium.Marker(d_coords).add_to(map1)
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