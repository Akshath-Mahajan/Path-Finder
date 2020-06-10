from django.db import models

# Create your models here.
class Nodes(models.Model):
    name = models.IntegerField()    #ID
    latitude = models.FloatField()
    longitude = models.FloatField()
    isRoadNode = models.BooleanField()
    def __str__(self):
        return "< "+str(self.name)+", ("+str(self.latitude)+","+str(self.longitude)+") >"
class DestinationNodes(models.Model):
    name = models.IntegerField()                #DestNode1 Name
    nearest_neighbour = models.IntegerField()   #RoadNode1 Name
    #location_name = models.CharField(max_length=100)
    def __str__(self):
        return "("+str(self.name)+","+str(self.nearest_neighbour)+")"

class Edges(models.Model):
    node1 = models.IntegerField()       #Node1 Name [Must be road node]
    node2 = models.IntegerField()       #Node2 Name [Must be road node]
    cost = models.FloatField()
    def __str__(self):
        return "< ("+str(self.node1)+","+str(self.node2)+") , "+str(self.cost)+" >"


# class Bounds(models.Model):
#     minlat = models.IntegerField()
#     maxlat = models.IntegerField()
#     minlon = models.IntegerField()
#     maxlon = models.IntegerField()