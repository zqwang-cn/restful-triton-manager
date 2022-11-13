from rest_framework import serializers
from repository.models import Repository


OPERATION_CHOICES = [
    'create',
    'remove',
    'start',
    'stop',
]

class OperationSerializer(serializers.Serializer):
    repo = serializers.SlugRelatedField('name', queryset=Repository.objects.all())
    op = serializers.ChoiceField(OPERATION_CHOICES)