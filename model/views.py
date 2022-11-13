from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from .models import Model, Version, Input, Output, CustomFile
from .serializers import ModelSerializer, VersionSerializer, InputSerializer, OutputSerializer, CustomFileSerializer


# Create your views here.
class ModelList(generics.ListCreateAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()

class ModelDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()
    lookup_field = 'name'

class InputList(generics.ListCreateAPIView):
    serializer_class = InputSerializer

    def get_queryset(self):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        return model.inputs
    
    def perform_create(self, serializer):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        if model.inputs.filter(name=serializer.validated_data['name']).count() != 0:
            raise serializers.ValidationError({'name': ['input name already exists.']})
        serializer.validated_data['model'] = model
        serializer.save()

class InputDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InputSerializer

    def get_object(self):
        return get_object_or_404(Input, model__name=self.kwargs['name'], name=self.kwargs['input_name'])

    def perform_update(self, serializer):
        inputs = Input.objects.filter(model=serializer.instance.model, name=serializer.validated_data['name'])
        if inputs.count() == 1 and inputs[0] != serializer.instance:
            raise serializers.ValidationError({'name': ['input name already exists.']})
        serializer.save()

class OutputList(generics.ListCreateAPIView):
    serializer_class = OutputSerializer

    def get_queryset(self):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        return model.outputs
    
    def perform_create(self, serializer):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        if model.outputs.filter(name=serializer.validated_data['name']).count() != 0:
            raise serializers.ValidationError({'name': ['output name already exists.']})
        serializer.validated_data['model'] = model
        serializer.save()

class OutputDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OutputSerializer

    def get_object(self):
        return get_object_or_404(Output, model__name=self.kwargs['name'], name=self.kwargs['output_name'])

    def perform_update(self, serializer):
        outputs = Output.objects.filter(model=serializer.instance.model, name=serializer.validated_data['name'])
        if outputs.count() == 1 and outputs[0] != serializer.instance:
            raise serializers.ValidationError({'name': ['output name already exists.']})
        serializer.save()

class VersionList(generics.ListCreateAPIView):
    serializer_class = VersionSerializer

    def get_queryset(self):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        return model.versions
    
    def perform_create(self, serializer):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        first = model.versions.order_by('-version').first()
        serializer.validated_data['model'] = model
        serializer.validated_data['version'] = 1 if first is None else first.version + 1
        serializer.save()

class VersionDetail(generics.RetrieveUpdateAPIView):
    serializer_class = VersionSerializer

    def get_object(self):
        return get_object_or_404(Version, model__name=self.kwargs['name'], version=self.kwargs['version'])

class CustomFileList(generics.ListCreateAPIView):
    serializer_class = CustomFileSerializer

    def get_queryset(self):
        version = get_object_or_404(Version, model__name=self.kwargs['name'], version=self.kwargs['version'])
        return version.custom_files
    
    def perform_create(self, serializer):
        version = get_object_or_404(Version, model__name=self.kwargs['name'], version=self.kwargs['version'])
        if version.custom_files.filter(path=serializer.validated_data['path']).count() != 0:
            raise serializers.ValidationError({'path': ['file with this path already exists.']})
        serializer.validated_data['version'] = version
        serializer.save()

class CustomFileDetail(generics.RetrieveDestroyAPIView):
    serializer_class = CustomFileSerializer

    def get_object(self):
        return get_object_or_404(CustomFile, version__model__name=self.kwargs['name'], version__version=self.kwargs['version'], id=self.kwargs['id'])