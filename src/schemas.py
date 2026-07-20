from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime

# ========================
# PLAYERS
# ========================
class PlayerBase(BaseModel):
    name: str
    jerseyNumber: Optional[int] = None
    battingStyle: str
    bowlingStyle: str
    role: str
    photoUri: Optional[str] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    jerseyNumber: Optional[int] = None
    battingStyle: Optional[str] = None
    bowlingStyle: Optional[str] = None
    role: Optional[str] = None
    photoUri: Optional[str] = None

class Player(PlayerBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ========================
# TEAMS
# ========================
class TeamBase(BaseModel):
    name: str
    logoUri: Optional[str] = None
    color: str
    captainId: Optional[str] = None
    viceCaptainId: Optional[str] = None

class TeamCreate(TeamBase):
    playerIds: Optional[List[str]] = []

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    logoUri: Optional[str] = None
    color: Optional[str] = None
    captainId: Optional[str] = None
    viceCaptainId: Optional[str] = None
    playerIds: Optional[List[str]] = None

class Team(TeamBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    players: List[Player] = []
    playerIds: List[str] = []
    
    model_config = ConfigDict(from_attributes=True)

# ========================
# TOURNAMENTS
# ========================
class TournamentBase(BaseModel):
    name: str
    venue: str
    season: str
    organizer: str
    logoUri: Optional[str] = None

class TournamentCreate(TournamentBase):
    teamIds: Optional[List[str]] = []

class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    venue: Optional[str] = None
    season: Optional[str] = None
    organizer: Optional[str] = None
    logoUri: Optional[str] = None
    teamIds: Optional[List[str]] = None

class Tournament(TournamentBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    teams: List[Team] = []
    teamIds: List[str] = []
    
    model_config = ConfigDict(from_attributes=True)

# ========================
# MATCHES
# ========================
class MatchBase(BaseModel):
    type: str
    tournamentId: Optional[str] = None
    teamAId: str
    teamBId: str
    totalOvers: int
    status: str
    toss: Dict[str, Any]
    innings: Optional[List[Dict[str, Any]]] = []
    playingXIA: Optional[List[str]] = []
    playingXIB: Optional[List[str]] = []
    currentStrikerId: Optional[str] = None
    currentNonStrikerId: Optional[str] = None
    currentBowlerId: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    type: Optional[str] = None
    tournamentId: Optional[str] = None
    teamAId: Optional[str] = None
    teamBId: Optional[str] = None
    totalOvers: Optional[int] = None
    status: Optional[str] = None
    toss: Optional[Dict[str, Any]] = None
    innings: Optional[List[Dict[str, Any]]] = None
    playingXIA: Optional[List[str]] = None
    playingXIB: Optional[List[str]] = None
    currentStrikerId: Optional[str] = None
    currentNonStrikerId: Optional[str] = None
    currentBowlerId: Optional[str] = None

class Match(MatchBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    model_config = ConfigDict(from_attributes=True)
