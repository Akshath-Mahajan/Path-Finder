from django.shortcuts import render
from django.http import HttpResponse
import folium
def home(req):
    return render(req, 'Maps/maps_home.html')
def map(request):
    map1 = folium.Map(location=[19.0760, 72.8777], zoom_start=15) #Replace location with avg of bounds in database
    #68.26% Height fits perfectly in the container and prevents a lot of css-overflow issues which are currently managed by overflow:auto
    #REPLACE LOCATION AND FILL DATABASE
    m = map1._repr_html_()
    
    if request.method == 'POST':
        #Add path to map before returning
        #opt1 - remove all nodes except start and end and display map [will need to add reset button too as people cant remember all node ids]
        #opt2 - Keep all destination nodes and just add path [no need to add reset map button]
        #set location of  returning map to be average of node1coords and node2coords
        return render(request, 'Maps/maps_map.html', {'map':m})
    if request.method == 'GET':
        #Add destination nodes to map before returning
        return render(request, 'Maps/maps_map.html', {'map':m})