from rest_framework import generics
from .models import Repository
from .serializers import RepositorySerializer


# Create your views here.
class RepositoryList(generics.ListCreateAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()

class RepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()
    lookup_field = 'name'