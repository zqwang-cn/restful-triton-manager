import os
import shutil
import subprocess
import jinja2
import zipfile
import tarfile

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from repository.models import Repository
from .serializers import OperationSerializer, OPERATION_CHOICES

TRITON_START_COMMAND = 'tritonserver --model-repository {}'
TEMPLATE_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.BASE_DIR / 'templates'))

triton_process = None
current_repository = None

def create_model(repo_dir, model):
    model_dir = os.path.join(repo_dir, model.name)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    template = TEMPLATE_ENV.get_template('config.pbtxt')
    s = template.render(model=model)
    with open(os.path.join(model_dir, 'config.pbtxt'), 'w') as f:
        f.write(s)

    for version in model.versions.all():
        version_dir = os.path.join(model_dir, str(version.version))
        if not os.path.exists(version_dir):
            os.mkdir(version_dir)
        
        if version.model_file:
            file_path = version.model_file.path
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path) as f:
                    extract_dir = os.path.join(version_dir, 'model')
                    if not os.path.exists(extract_dir):
                        os.mkdir(extract_dir)
                    f.extractall(extract_dir)
            elif file_path.endswith(('.tar', '.tar.gz')):
                with tarfile.open(file_path) as f:
                    extract_dir = os.path.join(version_dir, 'model')
                    if not os.path.exists(extract_dir):
                        os.mkdir(extract_dir)
                    f.extractall(extract_dir)
            else:
                ext = os.path.splitext(file_path)[-1]
                os.symlink(file_path, os.path.join(version_dir, 'model' + ext))

        for custom_file in version.custom_files.all():
            src = custom_file.file.path
            dst = os.path.join(version_dir, custom_file.path)
            dst_dir = os.path.split(dst)[0]
            if dst_dir:
                os.makedirs(dst_dir, exist_ok=True)
            os.symlink(src, dst)

def create(repository):
    repo_dir = os.path.join(settings.REPOSITORY_ROOT_DIR, repository.name)
    if os.path.exists(repo_dir):
        return 'repository dir already exists.'

    os.makedirs(repo_dir)
    for model in repository.models.all():
        create_model(repo_dir, model)

def remove(repository):
    if triton_process is not None and triton_process.poll() is None:
        return 'triton still running.'

    repo_dir = os.path.join(settings.REPOSITORY_ROOT_DIR, repository.name)
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

def start(repository):
    global triton_process
    global current_repository
    if triton_process is not None and triton_process.poll() is None:
        return 'triton already running.'

    repo_dir = os.path.join(settings.REPOSITORY_ROOT_DIR, repository.name)
    if not os.path.exists(repo_dir):
        return 'repository dir not exists.'

    cmd = TRITON_START_COMMAND.format(repo_dir)
    triton_process = subprocess.Popen(cmd, shell=True)
    current_repository = repository

def stop():
    if triton_process is None or triton_process.poll() is not None:
        return 'triton not running.'

    triton_process.kill()
    try:
        triton_process.wait(10)
    except subprocess.TimeoutExpired:
        return 'wait timeout.'

# Create your views here.
class OperationList(APIView):
    serializer_class = OperationSerializer
    
    def get(self, request):
        if triton_process is not None and triton_process.poll() is None:
            msg = {
                'triton status': 'running',
                'current repository': current_repository.name,
                'operation list': OPERATION_CHOICES
            }
        else:
            msg = {
                'triton status': 'stopped',
                'operation list': OPERATION_CHOICES
            }
        return Response(msg)
    
    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': 'input not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        repository = get_object_or_404(Repository, name=serializer.data['repo'])
        op = serializer.data['op']
        if op == 'create':
            msg = create(repository)
        elif op == 'remove':
            msg = remove(repository)
        elif op == 'start':
            msg = start(repository)
        elif op == 'stop':
            msg = stop()
        else:
            return Response({'msg': 'operation not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        if msg is not None:
            return Response({'msg': msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': 'success.'})
    