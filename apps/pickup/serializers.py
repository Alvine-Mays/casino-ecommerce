from rest_framework import serializers


class ValidateCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
