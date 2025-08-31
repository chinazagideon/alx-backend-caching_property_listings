from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties

"""
Set default page cache timeout
"""
@cache_page(60 * 15)
def property_list(request):
    """
    A view to display all the properties
    """
    data = get_all_properties()
    return JsonResponse({'properties': list(data)})
