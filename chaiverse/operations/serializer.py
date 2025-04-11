from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_admin', 'is_staff']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            is_admin = validated_data.get('is_admin', False),
            is_staff = validated_data.get('is_staff', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChaiShop
        fields = ['id', 'shop_name', 'adress', 'owner']


    def create(self, validated_data):
        shop = ChaiShop.objects.create(**validated_data)
        return shop

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChaiCategory
        fields = ['id', 'product_name', 'chai_shop']

    def create(self, validated_data):
        product = ChaiCategory.objects.create(**validated_data)
        return product






class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data['user'] = user
        return data





