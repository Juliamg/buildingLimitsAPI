from shapely import Polygon, MultiPolygon
from app.models.dto import SplitBuildingLimitResult, BuildingLimitInput, HeightPlateauInput
from app.services.utils import shapely_to_geojson


def calculate_split_building_limits(building_project: BuildingLimitInput,
                                    height_plateaus: list[HeightPlateauInput]) -> list[SplitBuildingLimitResult]:
    # Process splits
    split_building_limits_result: list[SplitBuildingLimitResult] = []

    bl_geometry = building_project.feature.geometry.as_polygon()
    for hp in height_plateaus:
        hp_geometry = hp.feature.geometry.as_polygon()
        split_result = bl_geometry.intersection(hp_geometry)
        if split_result.is_empty:
            continue

        if isinstance(split_result, (Polygon, MultiPolygon)):
            split_polygons = split_result if isinstance(split_result, MultiPolygon) else [split_result]
            for sp in split_polygons:
                split_limit = SplitBuildingLimitResult(
                    geometry=shapely_to_geojson(sp), elevation=hp.feature.properties.elevation
                )
                split_building_limits_result.append(split_limit)

    return split_building_limits_result
