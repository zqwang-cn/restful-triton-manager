from rest_framework import serializers
from model.models import Model
from .models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    models = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Model.objects.all())

    class Meta:
        model = Repository
        exclude = ['id']