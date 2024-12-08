from resources.input import BuildingLimits, HeightPlateaus

class Project:
    def __init__(self, building_limits: BuildingLimits, height_plateaus: HeightPlateaus):
        self.building_limits = building_limits
        self.height_plateaus = height_plateaus
