from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserSearch(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        )

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        receiver_username = self.request.data.get('receiver')
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({'error': 'Receiver does not exist'}, status=404)
        serializer.save(sender=self.request.user, receiver=receiver)

    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        user = request.user
        friends = User.objects.filter(
            Q(sent_requests__receiver=user, sent_requests__status='accepted') |
            Q(received_requests__sender=user, received_requests__status='accepted')
        ).distinct()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def accept(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status': 'Friend request accepted'})
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request does not exist or not authorized'}, status=404)

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': 'Friend request rejected'})
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request does not exist or not authorized'}, status=404)
