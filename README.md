# NIDIE, National ID Information Extractor

Egyptian ID information extractor API, this is a simple single endpoint API that will validate and extract the information found in a a valid national id according to this [resource](https://ar.wikipedia.org/wiki/%D8%A8%D8%B7%D8%A7%D9%82%D8%A9_%D8%A7%D9%84%D8%B1%D9%82%D9%85_%D8%A7%D9%84%D9%82%D9%88%D9%85%D9%8A_%D8%A7%D9%84%D9%85%D8%B5%D8%B1%D9%8A%D8%A9#%D9%88%D8%B5%D9%81_%D8%A7%D9%84%D8%B1%D9%82%D9%85_%D8%A7%D9%84%D9%82%D9%88%D9%85%D9%8A).

##### Project layout and implementation choices:
The choice to use FastAPI to build this was out of mere convince of taking advantage of it's small size, auto docs feature and the use of pydantic to describe and validate the shape of our Data Model (NationalID).

The code has the following basic layout:
- `api` module, this contains our api implementation.
  - `api/__init__.py` contains the FastAPI app instance and it's config.
  - `api/model.py` contains our Pydantic data model `NationalID` responsible of validating and extracting the needed information.
  - `api/utils.py` contains simple utility functions and mapping constants.
  - `api/endpoints` contains our single endpoint implementation and router declaration.

- `tests` module, contains our API unittests.

The API consists of a single endpoint `/nid/extract` that accepts a payload validate it's value and only return the extracted information if the value is a valid National ID, otherwise it will return the validation errors with a `422` status_code response.

##### Docker build and run:
To build the docker image of this project:
```
$ docker build -t nidie:latest .
```

To run a docker container of the image just built:
```
$ docker run -d --name nidie_api -p 8000:8000 nidie
```

##### Running the tests
To run the project test suite using our docker image.
```
$ docker run --rm nidie pytest
```

##### API Docs:
After building and running the project locally you can access the auto generated API docs either with:
- Swagger's UI at `http://localhost:8000/docs`
- or with Redoc's UI at `http://localhost:8000/redoc`

##### Usage example:
Make sure the docker container is running first then send the following request from `curl` or any other http client.

```
$ curl -X POST "http://localhost:8000/nid/extract" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"nid\":\"29001011234567\"}"
```
