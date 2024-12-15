from app.services.database import Base
from sqlalchemy import Column, Integer, Float, Text, String


class BuildingLimit(Base):
    __tablename__ = "building_limit"
    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(Text)  # Store as WKT
    unique_hash = Column(String(16), unique=True, nullable=False)


class HeightPlateau(Base):
    __tablename__ = "height_plateau"
    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(Text)  # Store as WKT
    elevation = Column(Float)
    unique_hash = Column(String(16), unique=True, nullable=False)


class SplitBuildingLimit(Base):
    __tablename__ = "split_building_limit"
    id = Column(Integer, primary_key=True, index=True)
    geometry = Column(Text)  # Store as WKT
    elevation = Column(Float)
