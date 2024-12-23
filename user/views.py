from django.contrib.auth import logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .models import User
from online_store_drf.permissions import IsClient


class UserLogoutView(GenericAPIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "logout"},
            status=status.HTTP_200_OK,
        )


class UserLoginView(GenericAPIView):
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.save()
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsletterSubscriptionView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        user = request.user
        user.is_subscribed = True
        user.save()
        return Response({"message": "You have successfully subscribed to the newsletter"}, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user.is_subscribed = False
        user.save()
        return Response({"message": "You have unsubscribed from the mailing list"}, status=status.HTTP_200_OK)