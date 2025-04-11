from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

class OwnerDetails(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        all_users = CustomUser.objects.all()
        serializer = UserSerializer(all_users ,many=True)
        return Response({"message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": " success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message":serializer.errors})
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data.get('user')
                return Response({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class ShopAPIView(APIView):
    def get(self, request, user_id):
        data = ChaiShop.objects.all()
        serializer = ShopSerializer(data, many=True)
        return Response({"status": 200, "message" :serializer.data}, status = status.HTTP_200_OK)



    def post(self, request, user_id):
        try:
            
            data = request.data.copy()
            if user_id:
                data['owner'] = user_id
            else:
                data['owner'] = NULL
            serializer = ShopSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"success","data":serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({"message": "failed", "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductAPIView(APIView):
    def get(self, request, user_id, shop_id):
        try:
            data = ChaiCategory.objects.all()
            serializer = ProductSerializer(data, many=True)
            return Response({"message":serializer.data})
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, user_id, shop_id):
        try:
            data = request.data.copy()
            if shop_id:
                data['chai_shop'] = shop_id
            else:
                data['chai_shop'] = NULL
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors})
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)