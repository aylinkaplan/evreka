### Device Location Tracker 
This project tracks GPS location data from IoT devices. The data is received via a TCP server, queued, and processed before being stored in the database. It uses Django, Django REST framework, Celery, Redis, and GraphQL for its implementation.


### Working in a Virtual Environment

Project uses Python 3.11.

#### Create/activate relevant Python version

```bash
brew install pyenv
pyenv install 3.11
pyenv shell 3.11
python --version
```

#### Prepare virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.dev.txt
```

### Working with Container
```bash
docker-compose build
docker-compose up
```
