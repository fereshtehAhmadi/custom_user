from rest_framework import serializers
from accounts.models import User


class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Register serializer
    and need username, email, firstname, lastname, phone and password
    validate checked password and confirm password was matched...
    """
    
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only': True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2 :
            raise serializers.ValidationError("password and confirm password dosen't match!!")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        return user
