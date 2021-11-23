from django.urls import path

from .views      import BoardListView,PinListView


urlpatterns = [
    path("", BoardListView.as_view()),
    path("/pinlist", PinListView.as_view()),
]