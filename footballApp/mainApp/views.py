from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
import datetime
from dateutil.parser import parse as dateparser

from .serializers import PlayerSerializer, PlayerUpdateSerializer, PlayerCreateSerializer
from .models import Player

DELETE_SUCCESS = 'Deleted: '
UPDATE_SUCCESS = 'Updated'
CREATE_SUCCESS = 'Created'


class PlayerListView(ListAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('last_name', 'best_position')

    def head(self, *args, **kwargs):
        latest = self.get_queryset().latest('last_modified').last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
        mod_date = self.request.headers["If-Modified-Since"]
        response = HttpResponse()
        response['Last-Modified'] = latest

        if mod_date == "" or dateparser(latest) > dateparser(mod_date):
            response.status_code = status.HTTP_302_FOUND
        else:
            response.status_code = status.HTTP_304_NOT_MODIFIED
        return response


@api_view(['GET', 'HEAD', ])
def api_detail_player_view(request, player_id):

    try:
        player = Player.objects.get(player_id=player_id)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'HEAD':
        mod_date = request.headers["If-Modified-Since"]
        response = HttpResponse()
        response['Last-Modified'] = player.last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT')

        if mod_date == "" or dateparser(response['Last-Modified']) > dateparser(mod_date):
            response.status_code = status.HTTP_302_FOUND
        else:
            response.status_code = status.HTTP_304_NOT_MODIFIED
        return response


@api_view(['PUT', ])
def api_update_player_view(request, player_id):

    try:
        player = Player.objects.get(player_id=player_id)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PlayerUpdateSerializer(player, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            data['first_name'] = player.first_name
            data['last_name'] = player.last_name
            data['birth_date'] = player.birth_date
            data['best_position'] = player.best_position.__str__()
            data['manager'] = player.manager_id.__str__()
            data['club'] = player.club_id.__str__()
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def api_create_player_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = PlayerCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            player = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['player_id'] = player.player_id
            data['first_name'] = player.first_name
            data['last_name'] = player.last_name
            data['birth_date'] = player.birth_date
            data['best_position'] = player.best_position.__str__()
            data['manager'] = player.manager_id.__str__()
            data['club'] = player.club_id.__str__()
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_delete_player_view(request, player_id):
    try:
        player = Player.objects.get(player_id=player_id)
        player_name = player.__str__()
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = player.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS + player_name
        else:
            data['response'] = "Delete failed"
        return Response(data=data, status=status.HTTP_202_ACCEPTED)
