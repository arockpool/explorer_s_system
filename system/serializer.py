from rest_framework import serializers

from system.models import Admin, ChoiceModel, Appinfo


class AdminSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Admin
        # fields = "__all__"
        exclude = ("is_super", 'permissions')


class ChoiceSerializer(serializers.ModelSerializer):
    # create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ChoiceModel
        fields = "__all__"


class AppinfoSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Appinfo
        fields = "__all__"

