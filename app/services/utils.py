from shapely.geometry import mapping
from shapely.wkt import loads
from shapely import Polygon, to_wkt
from typing import Tuple

from app.models.db import BuildingLimit, HeightPlateau
from app.services.database import get_db
from sqlalchemy import text
from sqlalchemy.engine.row import Row


def shapely_to_wkt(geometry: Polygon, rounding_precision: int) -> str:
    return to_wkt(geometry, rounding_precision)


def wkt_to_shapely(wkt: str) -> Polygon:
    return loads(wkt)

def shapely_to_geojson(geometry: Polygon):
    return mapping(geometry)


def query_building_resources(building_project_id: str,
                            height_plateaus_ids: list[str]) -> Tuple[list[Row], list[Row]]:
    db_session =get_db()

    height_plateaus_as_string = ", ".join(f"'{id}'" for id in height_plateaus_ids)
    _query_template: str = """SELECT * FROM {table_name} WHERE {column_name} in ({targets})"""
    existing_building_project: list[Row] = []
    existing_height_plateaus: list[Row] = []

    with db_session as db:
        existing_building_project = db.query(BuildingLimit).filter(BuildingLimit.unique_hash == building_project_id).all()
        existing_height_plateaus = db.execute(text(_query_template.format(table_name=HeightPlateau.__tablename__,
                                                                          column_name="unique_hash",
                                                                          targets=height_plateaus_as_string))).all()

    return existing_building_project, existing_height_plateaus

def assess_if_resources_exist(building_project_id: str,
                              height_plateaus_ids: list[str]) -> bool:

    existing_building_project, existing_height_plateaus = query_building_resources(building_project_id,
                                                                                   height_plateaus_ids)
    return (any(existing_building_project) and any(existing_height_plateaus))
