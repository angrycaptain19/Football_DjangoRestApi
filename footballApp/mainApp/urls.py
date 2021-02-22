from django.urls import path
from .views import (
    api_detail_player_view,
    api_update_player_view,
    api_delete_player_view,
    api_create_player_view,
    PlayerListView
)

app_name = 'mainApp'

urlpatterns = [
    path('<player_id>/', api_detail_player_view, name="detail"),
    path('<player_id>/update', api_update_player_view, name="update"),
    path('<player_id>/delete', api_delete_player_view, name="delete"),
    path('create', api_create_player_view, name="create"),
    path('', PlayerListView.as_view(), name="list"),
    #path('', api_list_player_view, name="list"),
]
