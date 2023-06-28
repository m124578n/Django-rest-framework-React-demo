from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save(force_insert=True)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError('require username and password')
        if not user:
            raise serializers.ValidationError('unable to login')
        if not user.is_active:
            raise serializers.ValidationError('user is disabled')
        return data
