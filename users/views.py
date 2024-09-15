from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    EmailVerificationSerializer
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: UserProfileSerializer()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        send_mail(
            'Verify your email',
            f'Your verification code is: {user.email_verification_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response({
            "user": UserProfileSerializer(user).data,
            "message": "User registered successfully. Please check your email for the verification code."
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login user",
        request_body=UserLoginSerializer,
        responses={200: openapi.Response('Successful login', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
            }
        ))}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user and user.email_verified:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        elif user and not user.email_verified:
            return Response({"error": "Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EmailVerificationView(APIView):
    @swagger_auto_schema(
        operation_description="Verify user email",
        request_body=EmailVerificationSerializer,
        responses={200: openapi.Response('Email verified successfully'),
                   400: openapi.Response('Invalid email or verification code')}
    )
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.validated_data['email'],
                email_verification_code=serializer.validated_data['code']
            )
            if not user.email_verified:
                user.email_verified = True
                user.is_active = True
                user.email_verification_code = None
                user.save()
                return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Email already verified"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or verification code"}, status=status.HTTP_400_BAD_REQUEST)