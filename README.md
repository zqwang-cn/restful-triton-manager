# RESTful API Server For Managing Triton Inference Server

## Preparations

```bash
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

## Run API Server

```bash
python3 manage.py runserver
```


## Usage

### Create Models

1. Fill basic configurations
   Link: http://127.0.0.1:8000/models/

2. Add input and output configurations
   Link:
   - http://127.0.0.1:8000/models/{model_name}/inputs/
   - http://127.0.0.1:8000/models/{model_name}/outputs/

3. Create new version and add model file
   Link: http://127.0.0.1:8000/models/{model_name}/versions/

4. (optional) Add custom files to each version
   Link: http://127.0.0.1:8000/models/{model_name}/versions/{version_id}/custom-files/

### Create Repositories

Fill name and select models
Link: http://127.0.0.1:8000/repositories/

### Manage Triton Server

Execute managing operations
Link: http://127.0.0.1:8000/operations/

Possible operations:
- create: create directory and all triton models for selected repository
- remove: remove all contents of selected repository
- start: start triton server using selected repository
- stop: stop current triton server