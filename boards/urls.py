from django.urls import path
from .views      import BoardListView, MyBoardsView, PinListView

urlpatterns = [
    path("", BoardListView.as_view()),
    path("/pin", PinListView.as_view()),
    path("/board/me", MyBoardsView.as_view()),
]