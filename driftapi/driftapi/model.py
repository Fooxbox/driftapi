
"""
Module defining the driftapi core and enum classes.
Note: for a complete server implementation, you probably want to also define some additional classes.

"""
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ValidationError, Field

class game_mode(str, Enum):
    RACE = "RACE"
    GYMKHANA = "GYMKHANA"

class track_condition(str, Enum):
    drift_asphalt = "drift_asphalt"
    drift_asphalt_wet = "drift_asphalt_wet"
    drift_dirt = "drift_dirt"
    drift_ice = "drift_ice"
    drift_sand = "drift_sand"

class track_bundle(str, Enum):
    none = "none"
    rally = "rally"
    rally_cross = "rally_cross"

class wheels(str, Enum):
    normal = "normal"
    spikes = "spikes"
    gravel_tires = "gravel_tires"

class setup_mode(str, Enum):
    RACE = "RACE"
    DRIFT = "DRIFT"

class target_code(str, Enum):
    start_finish = "0" #Gymkhana, Race, Rally, Rally Cross
    speed_drift = "4" #Gymkhana
    drift_asphalt = "4" #Rally, Rally Cross
    angle_drift = "5" #Gymkhana
    drift_asphalt_wet = "5" #Rally, Rally Cross
    oneeighty = "6" #Gymkhana
    drift_dirt = "6" # Rally, Rally Cross
    threesixty = "7" #Gymkhana
    drift_ice = "7" # Rally
    drift_sand = "7" # Rally Cross

class EnterData(BaseModel):
    game_mode: game_mode
    start_time: datetime
    time_limit: float = Field(None, title="the time limit for the run, in seconds")
    lap_count: int = Field(None, title="number of rounds (for the race mode)")
    track_condition: track_condition
    track_bundle: track_bundle
    wheels: wheels
    setup_mode: setup_mode
    engine_type: str = Field(None, title="The id of the motor type. No ENUM for the above reason. Example: 'DTM', 'V8' etc.") 
    tuning_type: str = Field(None, title="The id of the motor setup. No ENUM for the above reason. Example: 'DTM', 'V8' etc.")  #according to the app-internal id for the different motor setups. No ENUM for the above reason.
    steering_angle: float = Field(None, title="the choosen steering angle as set in the settings menue of the app")
    driftassist:bool = Field(None, title="if driftassist is enabled in the settings menue of the app.")
    softsteering:bool = Field(None, title="if softsteering is enabled in the settings menue of the app.")

class StartData(BaseModel):
    signal_time:datetime

class TargetData(BaseModel):
    crossing_time: datetime
    data: target_code
    false_start: bool
    driven_distance:float
    driven_time:float
    score:int

class EndData(BaseModel):
    finished_time: datetime
    total_score: int
    false_start: bool
    driven_distance: float
    driven_time: float


class RaceEvent(BaseModel):
    app_version:str
    game_id: str
    user_id: UUID = Field(None, title="unique user id", description="unique identifier (for the duration of the current race), can and should be different from the Sturmkind user name for legal and security reasons, for example a hash of the username or a hash of the devices ip address.")
    user_name: str = Field(None, title="the name choosen by the user to be displayed on the scoreboard", description="Can be different from the Sturmkind user name (for legal reasons)")
    time: datetime = Field(None, title="the exact timestamp down to the precision the sturmkind app uses, so fractions of a second")


class EnterEvent(RaceEvent):
    data:EnterData

class StartEvent(RaceEvent):
    data:StartData

class TargetEvent(RaceEvent):
    data: TargetData


# This event is triggered whenever the user leaves a run (shutting down the motor)
class EndEvent(RaceEvent):
    data:EndData