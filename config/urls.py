from django.urls import path, include

urlpatterns = [
    path('boards', include("boards.urls")),
]
