from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "phone_number",]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "user_avatar", "is_seller"] 

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "user_avatar",]        
        extra_kwargs = {

            "email": {"required": False, "allow_null": True},
            "phone_number": {"required": False, "allow_null": True},
            "user_avatar": {"required": False, "allow_null": True},
        }

        
              


