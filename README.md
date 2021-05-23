# Bitstamp API client
This is Bitstamp API client written in a form of a Python module.
It includes a REST API client as well as Websocket API client.

## Documentation

### Rest API
Library implements V2 Bitstamp REST API Client, its original documentation can be found using following link:
https://www.bitstamp.net/api/

### Websocket API
Library also implements V2 Bitstamp Websocket API, which is used in order to subscribe to market data.
Original documentation can be found using following link: https://www.bitstamp.net/websocket/v2/


## Development

### Local
In order to develop and run the project locally, python 3.8 needs to be installed on your machine.
your python interpreter needs dependencies defined in `requirements.txt`. You can install them via:
```
pip install -r requirements.txt
``` 
### Docker
In order to sandbox the project and make development easier, library provides an option to develop in docker container
(which encapsulates a perfect environment).
Run:
```
docker-compose up -d
```
Then:
```
docker-compose exec bitstamp bash
```
is going to provide you a shell with your environment (and build a docker image if it doesn't yet exist on your machine).
We suggest using docker for development.

## Usage
Examples for how to use clients defined in the projects can be found inside: `examples.py`
