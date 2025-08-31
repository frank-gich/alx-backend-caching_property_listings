from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/property_list.html", {"properties": properties})

def property_list(request):
    properties = get_all_properties()
    return render(request, "properties/property_list.html", {"properties": properties})