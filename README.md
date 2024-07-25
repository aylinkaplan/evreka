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

### List Device
```bash
query {
  devices {
    id
    name
  }
}
```

### Create Device
```bash
mutation{
    createDevice(name: "Device 1"){
    	device{
        id
        name
      }
  }
}
```


### Update Device
```bash
mutation {
  updateDevice(deviceId: 1, name: "Updated Device") {
    ok
    device {
      id
      name
    }
  }
}
```

### Delete Device
```bash
mutation {
  deleteDevice(deviceId: 1) {
    ok
  }
}
```


### Generate location data via TCP server
```bash
echo '{"device_id": 1, "latitude": 42.7128, "longitude": -73.0060}' | nc localhost 65432
```


### List location history by device
```bash
query {
  deviceLocationHistory(deviceId: 1) {
    id
    latitude
    longitude
    createdAt
  }
}
```


### Get last location for all devices
```bash
query {
  devicesWithLastLocations {
    id
    lastLocation {
      id
      latitude
      longitude
      createdAt
    }
  }
}
```

### Running tests
```bash
python manage.py test
```