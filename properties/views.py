from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from .utils import get_all_properties, get_redis_cache_metrics

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/property_list.html", {"properties": properties})

def property_list(request):
    properties = get_all_properties()
    data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": str(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat(),
        }
        for p in properties
    ]

    metrics = get_redis_cache_metrics()

    return JsonResponse({
        "data": data,
        "cache_metrics": metrics
    })
