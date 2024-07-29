from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate 
from rest_framework.decorators import authentication_classes,permission_classes 
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        token = Token.objects.create(user=user)
        
        data = {
            "user": serializer.data,
            "token": token.key
        }
        
        return Response(data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
# @authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
def login(request):
 
  data  = request.data
  authenticate_user = authenticate(username=data['username'],password=data['password'])
#checks if  the provided username and password  are correct

  if authenticate_user is not None:
    user  = User.objects.get(username=data['username'])
    serializer = UserSerializer(user)
    #serializes user data
    response_data ={
       'user':serializer.data,
    }
    token, created_token = Token.objects.get_or_create(user=user)
    #fetch existing token or create a new one if it does not exis
    if token:
        response_data['token'] = token.key
    elif created_token:
        response_data['token'] = created_token.key

    return Response(response_data,status=status.HTTP_200_OK)
  return Response({'detail':'not found'}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def TestView(request):
    return Response({'message':'authenticated well'})   


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()  # Assuming you want to delete the token
    return Response({"message": "Logged out successfully"}, status=204)







