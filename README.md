# Path-Finder

This is a django-based web application that uses folium to render a world map, and applies Dijkstra's Path finding algorithm (in sublinear time per iteration of the for loop, O(nlogn) time total) on map data downloaded from openstreetmaps


I used Bootstrap 4 to quickly implement the front-end of the project.

The different implementations of Dijkstra's algorithm basically built it up from being slow to decently fast.

The point of the project was to implement a speedy implementation of path finding algorithm on an actual map

It started off at data-collection and data-cleaning, and ended up at marking the shortest path on the map.


## Future updates:

May possibly add A* algorithm in algorithms.py and provide the user with an option to either use A* or Dijkstra's for path finding.
