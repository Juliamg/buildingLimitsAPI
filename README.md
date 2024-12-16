# Split Building Limits API
## To run locally:

1. Install dependencies (poetry must be installed): `poetry install` and activate with `poetry shell`
2. Have a local database set up that you can connect to. In this project, MySQL was used for all DB tables.
2. Create an `.env` file with an env variable `DB_CONNECTION_STRING` where you put your local DB connection string.
2. Run the app from the command line with `uvicorn app.main:app --env-file .env`

## Build the Docker image
This project uses Buildpacks to build a Docker image with a Procfile as the application entrypoint.
Run the Docker image with the env variable `DB_CONNECTION_STRING` and `PORT` set.
If building from a Github workflow, the connection string should be fetched from a key vault and set as an env variable
before executing the build script from a GitHub action.

To build the Docker image, run the build.sh script in your terminal; `./build.sh`

## Endpoints
### `POST /building_limit`
Create a building limit project from a GeoJSON input. See `app.models.dto.BuildingLimitInput` to see the pydantic
schema for this request.

Example request body:
```
{
  "feature": {
    "type": "string",
    "properties": {},
    "geometry": {
      "type": "string",
      "coordinates": [
        [
          [
            0
          ]
        ]
      ]
    }
  }
}
```

### `POST /height_plateau`
Create a height plateau from a GeoJSON input. See `app.models.dto.HeightPlateauInput` to see the pydantic
schema for this request.

Example request body:
```
{
  "feature": {
    "type": "string",
    "properties": {
      "elevation": 0
    },
    "geometry": {
      "type": "string",
      "coordinates": [
        [
          [
            0
          ]
        ]
      ]
    }
  }
}
```

### `POST /create_split_building_limits`
The core functionality of this API. This takes in a building limit GeoJSON, and a list of height plateaus
and splits the building limits with corresponding elevation levels. The input schema for this request is
`app.models.dto.SplitBuildingLimitsInput` and the response model is `app.models.dto.SplitBuildingLimitsOutput`.

Before this request can be performed, the height plateaus and building limits for the project must be created
first. If the request is successful, the resulting split building limits will be created in a separate table.


Example request body:
````
{
  "building_limits": {
    "type": "string",
    "features": [
      {
        "type": "string",
        "properties": {
          "elevation": 0
        },
        "geometry": {
          "type": "string",
          "coordinates": [
            [
              [
                0
              ]
            ]
          ]
        }
      }
    ]
  },
  "height_plateaus": {
    "type": "string",
    "features": [
      {
        "type": "string",
        "properties": {
          "elevation": 0
        },
        "geometry": {
          "type": "string",
          "coordinates": [
            [
              [
                0
              ]
            ]
          ]
        }
      }
    ]
  }
}
````

## Frameworks used
- FastAPI as the API framework
- Shapely for handling GeoJSON objects and for performing geometric operations on Polygon objects
- Pydantic for schemas and data validation