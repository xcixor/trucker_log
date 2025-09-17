from rest_framework import serializers
from .models import Trip, Stop, LogSheet, DutyStatusChange


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'


class LogSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSheet
        fields = '__all__'


class DutyStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DutyStatusChange
        fields = '__all__'
