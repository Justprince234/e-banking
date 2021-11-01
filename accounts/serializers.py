from rest_framework import serializers
from accounts.models import User, InternationalTransfer, LocalTransfer, History, Contact
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from accounts.models import UpdateUser
from rest_framework.fields import CurrentUserDefault

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, max_length=35, min_length=6, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, max_length=35, min_length=6, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'email','first_name', 'middle_name', 'surname', 'phone', 'sex', 'security_question', 'security_answer', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match!."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data.get('account_number'),
            )
        user.first_name = validated_data['first_name']
        user.middle_name = validated_data['middle_name']
        user.surname = validated_data['surname']
        user.phone = validated_data['phone']
        user.sex = validated_data['sex']
        user.security_question = validated_data['security_question']
        user.security_answer = validated_data['security_answer']
        user.set_password(validated_data['password'])
        user.save()

        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'surname', 'email', 'security_question', 'security_answer', 'account_number', 'available_bal', 'status')

# International Transfer Serializer
class InternationalTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalTransfer
        fields = '__all__'

# Local Transfer Serializer
class LocalTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalTransfer
        fields = '__all__'

# History Serializaer
class HistorySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = History
        fields = '__all__'

    def save(self, **kwargs):
        """Include default for read_only `account` field"""
        kwargs["owner"] = self.fields["owner"].get_default()
        return super().save(**kwargs)

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UpdateUserSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())  
    class Meta:
        model = UpdateUser
        fields = '__all__'

    def save(self, **kwargs):
        """Include default for read_only `account` field"""
        kwargs["owner"] = self.fields["owner"].get_default()
        return super().save(**kwargs)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

# class RequestPasswordResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)

#     class Meta:
#         fields = ['email']

# class SetNewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(min_length=6, max_length=65, write_only=True)
#     token = serializers.CharField(min_length=1, write_only=True)
#     uidb64 = serializers.CharField(min_length=1, write_only=True)

#     class Meta:
#         fields = ['password', 'token', 'uidb64']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uidb64 = attrs.get('uidb64')

#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed('The reset link is invalid', status=401)

#             user.set_password(password)
#             user.save()
#             return (user)
#         except Exception as e:

#             raise AuthenticationFailed('The reset link is invalid', status=401)
#         return super().validate(attrs)