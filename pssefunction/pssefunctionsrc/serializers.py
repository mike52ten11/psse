from rest_framework import serializers
from .models import (   PowerUser,
                        DeviceData,
                        DeviceElectricNumberMapping
                    )

class PowerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerUser
        fields = ['electricnumber', 'account', 'registered', 'regdate']



class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = ['deviceuuid', 'name', 'value','datatime', 'createtime']    

class DeviceUserMappingSerializer(serializers.ModelSerializer):
    account = serializers.CharField(max_length=10)
    class Meta:
        model = DeviceElectricNumberMapping
        fields = ['electricnumber', 'deviceuuid', 'registered', 'createtime','account']    
    

class UserInfoSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=10)


class ChangeUserSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=10)    
    newaccount = serializers.CharField(max_length=10)

class DeleteUserSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=10)


class SubscribeStatusSerializer(serializers.Serializer):
    electricnumber = serializers.CharField(max_length=11)
    account = serializers.CharField(max_length=10)
    


class GetDataSerializer(serializers.Serializer):
    electricnumber = serializers.CharField(max_length=11)
    account = serializers.CharField(max_length=10)
    start = serializers.IntegerField()       