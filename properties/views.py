from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

"""
Set default page cache timeout
"""
@cache_page(60 * 15)
def property_list(request):
    """
    A view to display all the properties
    """
    data = Property.objects.all()
    return JsonResponse({'properties': list(data)})
