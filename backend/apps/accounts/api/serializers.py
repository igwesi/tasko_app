from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import RefreshToken


User = get_user_model()


class UserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active", "is_staff"]

class UserCurrentErrorSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type":"password"}, write_only=True)
    new_password = serializers.CharField(style={"input_type": "password"})
    new_password_retype = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    
    default_error_messages = {
        "password_mismatch": _("Current password is not matching"),
        "password_invalid": _("Password does not meet all requirements"),
        "password_same": _("Both new and current passwords are same"),
    }

    class Meta:
        model = User
        fields = ["password", "password_new", "password_retype"]

    def validate(self, attrs):
        request = self.context.get('request', None)

        if not request.user.check_password(attrs["password"]):
            raise serializers.ValidationError(
                {'password':self.default_error_messages['password_mismatch']}
            )
        try:
            validate_password(attrs["new_password"])
        except ValidationError as e:
            raise exceptions.ValidationError({"new_password": list(e.messages)}) from e
        
        if attrs["new_password"] != attrs["new_password_retype"]:
            raise serializers.ValidationError(
                {'new_password_retype': self.default_error_messages['password_invalid']}
            )
        
        if attrs["new_password"] == attrs["password"]:
            raise serializers.ValidationError(
                {'new_password': self.default_error_messages['password_same']}
            )
        
        return super().validate(attrs)

class UserChangePasswordErrorSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.ListSerializer(
        child=serializers.CharField(), required=False
    )
    new_password_retype = serializers.ListSerializer(
       child=serializers.CharField(), required=False
    )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})
    password_retype = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "password_mismatch": _("Password are not matching."),
        "password_invalid": _("Password does not meet all requirements."),
    }

    class Meta:
        model = User
        fields = ["email", "password", "password_retype"]

    def validate(self, attrs):
        print(attrs)
        password_retype = attrs.pop("password_retype")
    
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError:
            self.fail("password_invalid")

        if attrs.pop("password") != password_retype:
            return self.fail("password_mismatch")
        return attrs
    
    def create(self, data):
        print(data)
        with transaction.atomic():
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists.')

            user = User.objects.create_user(**data)
            user.is_active = True
            user.save()
            return user
    
class UserCreateErrorSerializer(serializers.Serializer):
    email = serializers.ListSerializer(child=serializers.EmailField(), required=False)
    password = serializers.ListSerializer(child=serializers.CharField(), required=False)
    password_retype = serializers.ListSerializer(
        child=serializers.CharField(), required=False
    )


class LoginSerializer(serializers.Serializer):  # Using Serializer instead of ModelSerializer for flexibility
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')
        data['message']  = ""
        
        if not email or not password:
            data['message'] = "Form Validation Error"
            return data
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        
        if user is None:
            if not User.objects.filter(email=email).exists():
                data['message'] = "User with Email does not exist"                
            else:
                data['message'] = "Incorrect password"                
            return data
        
        # Optionally, add the authenticated user to the serialized output
        data['user'] = user
        return data
