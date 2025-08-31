from django.urls import path
from . import views

urlpatterns = [
    # The empty path '' corresponds to the root of the path defined in the project's urls.py
    # So this will handle requests to /properties/
    path("", views.property_list, name="property-list"),
]
