# Simple Go Demo Service

## How to run?

```shell
docker compose up
```

or more brutal solution:

```shell
docker compose up --force-recreate --remove-orphans --detach
```

stop:

```shell
docker compose down
```

get rid of odl image:
```shell
docker rmi $(docker images 'godemoservice-godemoserv' -a -q)
```

## How to test?

1. After running the docker compose 
2. Go to Locust Web UI at [localhost:8094](http://localhost:8084/).
3. Input
    * Number of users - peak number of concurrent Locust users.
    * Ram up - rate to spawn users at (users per second).
    * Mocking target (Go Service at [http://godemoservice:8083](http://godemoservice:8083))
4. Press `Start`. Locust will now mock service and agregate statistics
5. Go to http://localhost:16686/. There will be no traces for _godemoservice_ so it won't be available in the dropdown.
   * Select _godemoservice_ with the Service dropdown.
   * Should see the interactive logs in the Jaeger UI

## Documentation

* DEFAULT_URL= [http://godemoservice:8083](http://godemoservice:8083)

### Get an object with limit:

```curl
curl --location 'localhost:8083/demo?limit=1'
```

`limit` is an optional field (default = 10)
* if limit is not positive integer returns `422` UnprocessableEntity status code
* if database is empty returns `404` NotFound status code

### Post an object to the db:

```curl
curl --location 'localhost:8083/demo' \
--header 'Content-Type: application/json' \
--data '{
    "StringField": "jan",
	"IntField": 122,
	"BoolField": false
}'
```

`StringField` is required and cannot be empty
* if not string returns `400` BadRequest
* if empty returns `422` UnprocessableEntity

`IntField` is an optional field (default = 0)
* if not string returns `400` BadRequest

`BoolField` is an optional field (default = false)
* if not string returns `400` BadRequest
