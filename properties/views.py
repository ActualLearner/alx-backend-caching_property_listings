from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Property


# This decorator will cache the entire response of this view for 15 minutes.
@cache_page(60 * 15)
def property_list(request):
    """
    A view that retrieves all properties from the database
    and returns them as a JSON list. The response is cached.
    """
    # Get all property objects from the database
    properties = Property.objects.all()

    # Convert the queryset into a list of dictionaries to be serialized into JSON.
    # .values() is efficient as it only selects the fields we need.
    data = list(properties.values("title", "description", "price", "location"))

    # Return the data as a JSON response.
    # safe=False is required to allow a list to be the top-level object.
    return JsonResponse({"properties": data})```
