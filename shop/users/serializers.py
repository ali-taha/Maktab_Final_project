from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
        ]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_avatar",
            "is_seller",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "user_avatar",
        ]
        extra_kwargs = {
            "email": {"required": False, "allow_null": True},
            "phone_number": {"required": False, "allow_null": True},
            "user_avatar": {"required": False, "allow_null": True},
        }

class OtpRequestSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^0?9\d{9}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = serializers.CharField(validators=[phone_regex], max_length=15, )        
    otp_code = serializers.CharField(max_length=4)