from fastapi.responses import UJSONResponse

from app.models.dto import (
    SplitBuildingLimitsInput,
    SplitBuildingLimitsOutput,
    HeightPlateauInput,
    BuildingLimitInput,
)
from fastapi import APIRouter, Depends, HTTPException
from app.services.database import get_db, SessionLocal
from app.services.calculation import calculate_split_building_limits

from app.models.db import BuildingLimit, HeightPlateau, SplitBuildingLimit
from app.services.utils import shapely_to_wkt, query_building_resources
from app.exceptions import BuildingResourceMissing

router = APIRouter()

@router.post("/building_limit")
async def create_building_limit(building_limit: BuildingLimitInput, db: SessionLocal = Depends(get_db)):
    """Upload a building limit (GeoJSON format)."""

    unique_identifier = building_limit.__hash__()
    db_building_limit = BuildingLimit(unique_hash=unique_identifier,
                                      geometry=shapely_to_wkt(building_limit.feature.geometry.as_polygon(),
                                                              building_limit.feature.geometry.sig_figs))
    try:
        db.begin()
        if db.query(BuildingLimit).filter_by(unique_hash=unique_identifier).first():
            return UJSONResponse(status_code=409,
                                 content="Building project already exists")

        db.add(db_building_limit)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    else:
        db.commit()
        return UJSONResponse(status_code=201, content=f"Building project with id {db_building_limit.id} created")
    finally:
        db.close()


@router.post("/height_plateau")
async def create_height_plateau(height_plateau: HeightPlateauInput, db: SessionLocal = Depends(get_db)):
    """Upload height plateaus (GeoJSON format)."""
    unique_identifier = height_plateau.__hash__()
    db_height_plateau = HeightPlateau(unique_hash=unique_identifier,
                                      geometry=shapely_to_wkt(height_plateau.feature.geometry.as_polygon(),
                                                              height_plateau.feature.geometry.sig_figs))
    try:
        db.begin()
        if db.query(HeightPlateau).filter_by(unique_hash=unique_identifier).first():
            return UJSONResponse(status_code=409,
                                 content="Height plateau already exists")
        db.add(db_height_plateau)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    else:
        db.commit()
        return UJSONResponse(status_code=201, content=f"Height Plateau with id {db_height_plateau.id} created")
    finally:
        db.close()


@router.post("/create_split_building_limits", response_model=SplitBuildingLimitsOutput, status_code=201)
async def create_split_building_limits(project: SplitBuildingLimitsInput, db: SessionLocal = Depends(get_db)):
    """Split building limits by height plateaus and assign elevations."""
    building_project = project.to_building_limit()
    height_plateaus = [hp for hp in project.to_height_plateaus()]

    building_project_id = building_project.__hash__()
    height_plateau_ids = [hp.__hash__() for hp in height_plateaus]

    try:
        db.begin()
        existing_building_project, existing_height_plateaus = query_building_resources(building_project_id,
                                                                                       height_plateau_ids, db)

        if not (any(existing_building_project) and any(existing_height_plateaus)):
            raise BuildingResourceMissing("Height plateaus or Building project are missing. Please create them first.")

        split_limits = calculate_split_building_limits(building_project, height_plateaus)

        for split_limit_result in split_limits:
            db.add(SplitBuildingLimit(
                    geometry=shapely_to_wkt(split_limit_result.geometry.as_polygon(),
                                            split_limit_result.geometry.sig_figs),
                    elevation=split_limit_result.elevation)
                )
    except Exception as e:
        db.rollback()
        if isinstance(e, BuildingResourceMissing):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        db.commit()
        return SplitBuildingLimitsOutput(split_building_limits=split_limits,
                                         building_project_id=building_project_id,
                                         height_plateau_ids=height_plateau_ids)
    finally:
        db.close()
