import json
from typing import Optional
from shapely import from_geojson
from shapely.errors import GeometryTypeError
from shapely.geometry import Polygon, shape

from pydantic import BaseModel, ConfigDict


class GeoJson(BaseModel):
    coordinates: list[list[float]]
    elevation: Optional[float] = None

class BuildingLimits(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    building_area: Polygon

    @classmethod
    def from_request(cls, raw_input: dict) -> "BuildingLimits":
        try:
            geometry_collection = from_geojson(json.dumps(raw_input))
        except GeometryTypeError:
            raise Exception("Input is not a valid GeometryJson")

        if len(geometry_collection.geoms) > 1:
            raise Exception("Input can only have one Polygon")

        geom = geometry_collection.geoms[0]
        if isinstance(geom, Polygon):
            return cls(building_area=geom)


class HeightPlateaus(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    plateaus: list[Polygon]

    @classmethod
    def from_request(cls, raw_input: dict) -> "BuildingLimits":
        try:
            geometry_collection = from_geojson(json.dumps(raw_input))
        except GeometryTypeError:
            raise Exception("Input is not a valid GeometryJson")

        for polygon in raw_input["features"]:
            elevation = polygon["properties"]["elevation"]
            polygon_coords = polygon["geometry"]["coordinates"][0]
            new_polygon_coords = [[*coords, elevation] for coords in polygon_coords]
            polygon["geometry"]["coordinates"][0] = new_polygon_coords

        return cls(plateaus=[shape(polygon["geometry"]) for polygon in raw_input["features"]])
