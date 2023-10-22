from rest_framework import serializers
from api.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'token')
        extra_kwargs = {
            'username': {
                'label': 'username',
                'help_text': 'username',
                'required': True,
                'validators': [
                    UniqueValidator(queryset=User.objects.all(), message='This username has been registered.')],
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': 'Allow 6-20 characters of username',
                    'max_length': 'Allow 6-20 characters of username',
                }
            },
            'email': {
                'label': 'Mail',
                'help_text': 'Mail',
                'write_only': True,
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all(), message='This mailbox has been registered.')],
            },
            'password': {
                'label': 'password',
                'help_text': 'password',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': 'Allow 6-20 characters passwords',
                    'max_length': 'Allow 6-20 characters passwords',
                }
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        return user
