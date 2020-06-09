from django.contrib import admin
from .models import Nodes, DestinationNodes, Edges

admin.site.register(Nodes)
admin.site.register(DestinationNodes)
admin.site.register(Edges)
