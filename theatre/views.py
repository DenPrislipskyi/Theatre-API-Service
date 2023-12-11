from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from theatre.models import TheatreHall, Reservation, Actor, Genre, Play, Performance
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.serializers import TheatreHallSerializer, ReservationSerializer, ActorSerializer, GenreSerializer, \
    PlaySerializer, PerformanceSerializer, PerformanceListSerializer, \
    PlayDetailSerializer, PerformanceDetailSerializer, PlayListSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


    # N + 1 manytoOne
    def get_queryset(self):
        queryset = self.queryset

        play = self.request.query_params.get("play")
        if play:
            play_ids = [int(x) for x in self.request.query_params.get("play").split(',')]
            queryset = queryset.filter(play__id__in=play_ids)
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related("play", "theatre_hall")
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class GenreViewSet(viewsets.ViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    # N + 1 Manytomany
    def get_queryset(self):
        queryset = self.queryset

        title = self.request.query_params.get("title")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if self.action in ("retrieve", "list"):
            queryset = queryset.prefetch_related("actor", "genre")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


# class TicketViewSet(viewsets.ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(reservation__user=self.request.user)
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
