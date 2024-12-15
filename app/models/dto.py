import hashlib
from typing import List
from pydantic import BaseModel, field_validator
from shapely import Polygon
from shapely.geometry import shape
from typing import Optional

class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]]

    @property
    def sig_figs(self) -> int:
        all_coordinates = []
        for lat_long in self.coordinates:
            for number in lat_long:
                all_coordinates.extend(number)
        return max(len(str(digit)) for digit in all_coordinates)

    def as_polygon(self) -> Polygon:
        return shape(self.dict())

class FeatureProperties(BaseModel):
    elevation: Optional[float] = None

class Feature(BaseModel):
    type: str
    properties: FeatureProperties
    geometry: Geometry

    @field_validator("geometry")
    @classmethod
    def geometry_is_polygon(cls, value):
        polygon = shape(value.dict())
        if not isinstance(polygon, Polygon):
            raise ValueError
        return value

class FeatureCollection(BaseModel):
    type: str
    features: List[Feature]

class BuildingLimitInput(BaseModel):
    feature: Feature

    def __hash__(self):
        return hashlib.sha256(self.model_dump_json().encode()).hexdigest()[:16]


class HeightPlateauInput(BaseModel):
    feature: Feature

    def __hash__(self):
        return hashlib.sha256(self.model_dump_json().encode()).hexdigest()[:16]

    @field_validator("feature")
    @classmethod
    def must_have_elevation(cls, value):
        if not value.properties.elevation:
            raise ValueError
        return value


class SplitBuildingLimitsInput(BaseModel):
    building_limits: FeatureCollection
    height_plateaus: FeatureCollection

    @field_validator("building_limits")
    @classmethod
    def only_one_building_project(cls, value):
        if len(value.features) > 1:
            raise ValueError("Can only process one building site at a time")
        return value

    def to_building_limit(self) -> BuildingLimitInput:
        return BuildingLimitInput(feature=self.building_limits.features[0])

    def to_height_plateaus(self) -> list[HeightPlateauInput]:
        return [HeightPlateauInput(feature=feature) for feature in self.height_plateaus.features]


class SplitBuildingLimitResult(BaseModel):
    geometry: Geometry
    elevation: float


class SplitBuildingLimitsOutput(BaseModel):
    building_project_id: str
    height_plateau_ids: list[str]
    split_building_limits: list[SplitBuildingLimitResult]
