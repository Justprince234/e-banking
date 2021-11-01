from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from .serializers import UserSerializer, RegisterSerializer, UpdateUserSerializer, LoginSerializer, ChangePasswordSerializer, InternationalTransferSerializer, LocalTransferSerializer,HistorySerializer, ContactSerializer
from rest_framework.permissions import IsAuthenticated
from .models import UpdateUser, User, InternationalTransfer, LocalTransfer, Contact, History
from rest_framework import permissions
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers

from django.shortcuts import render,HttpResponseRedirect,Http404
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

# Change Password
from .models import User
from .serializers import ChangePasswordSerializer
# Create your views here.

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Confirmation Email Configuration
        # current_site = get_current_site(request)
        # message = render_to_string('email_confirmation.html', {
        #         'user':user, 
        #         'domain':current_site.domain,
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #         'token': account_activation_token.make_token(user),
        #     })
        # mail_subject = 'Activate your Steplight Bank Account.'
        # to_email = user.email
        # email = EmailMessage(mail_subject, message, to=[to_email])
        # email.send()

        # Account Details
        # message = render_to_string('account_detail.html', {
        #         'user':user, 
        #     })
        # mail_subject = 'Welcome to Steplight Bank.'
        # to_email = user.email
        # email = EmailMessage(mail_subject, message, to=[to_email])
        # email.send()

        # Account Details Twilio
        # client = Client(account_sid, auth_token)
        # message = client.messages \
        #         .create(
        #             body="Welcome to Steplight Bank\n\nHello, "+ user.first_name + " "+ user.surname+",\n\nYour account number is "+ user.account_number + "\n\nThank you for choosing Steplight Bank!",
        #             from_='+15863152155',
        #             to=user.phone
        #         )

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# Login API
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
        
# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class InternaltionalTransferAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InternationalTransferSerializer

    def get(self, request, *args, **kwargs):
        items = InternationalTransfer.objects.filter(owner=self.request.user,)
        serializer = InternationalTransferSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)

    def post(self, request, *args, **kwargs):
        serializer = InternationalTransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # user.to_account.available_bal += serializer.validated_data['transfer_amount']
            # user.to_account.save()
            # # Account Details
            # message = render_to_string('notification.html', {
            #         'user':user,
            #         'serializer':serializer,
            #     })
            # mail_subject = 'Steplight Bank Notification!'
            # to_email = self.request.user.email
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()

        return Response({
            "status": "Transaction successful",
            "user": InternationalTransferSerializer(serializer.validated_data).data
            })


class LocalTransferAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = LocalTransferSerializer

    def get(self, request, *args, **kwargs):
        items = LocalTransfer.objects.filter(owner=self.request.user,)
        serializer = LocalTransferSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)

    def post(self, request, *args, **kwargs):
        serializer = LocalTransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # user.to_account.available_bal += serializer.validated_data['transfer_amount']
            # user.to_account.save()
            # # Account Details
            # message = render_to_string('notification.html', {
            #         'user':user,
            #         'serializer':serializer,
            #     })
            # mail_subject = 'Steplight Bank Notification!'
            # to_email = self.request.user.email
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()

        return Response({
            "status": "Transaction successful",
            "user": LocalTransferSerializer(serializer.validated_data).data
            })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def transfer_api_view(request):
    
#     if request.method == 'GET':
#         items = Transfer.objects.filter(owner=request.user,)
#         serializer = TransferSerializer(items, many=True)
#         return JsonResponse(serializer.data, safe =False)
 

# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def profiles_api_view(request):
    
    if request.method == 'GET':
        items = UpdateUser.objects.filter(owner=request.user,)
        serializer = UpdateUserSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)
    
    elif request.method == 'POST':
        owner = request.user
        data = JSONParser().parse(request)
        serializer =UpdateUserSerializer(data = data)
 
        if serializer.is_valid():
            serializer.save(owner)
            return JsonResponse(serializer.data,status = 201)
        return JsonResponse(serializer.errors,status = 400)
 

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def histories_api_view(request):
    
    if request.method == 'GET':
        items = History.objects.filter(owner=request.user,)
        serializer = HistorySerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)
    
    elif request.method == 'POST':
        owner = request.user
        data = JSONParser().parse(request)
        serializer =HistorySerializer(data = data)
 
        if serializer.is_valid():
            serializer.save(owner)
            return JsonResponse(serializer.data,status =201)
        return JsonResponse(serializer.errors,status = 400)

@api_view(['GET'])
def all_user_view(request):
    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe =False)

 