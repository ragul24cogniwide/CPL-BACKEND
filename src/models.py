import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, JSON, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

team_players = Table(
    'team_players',
    Base.metadata,
    Column('team_id', String, ForeignKey('teams.id', ondelete="CASCADE"), primary_key=True),
    Column('player_id', String, ForeignKey('players.id', ondelete="CASCADE"), primary_key=True)
)

tournament_teams = Table(
    'tournament_teams',
    Base.metadata,
    Column('tournament_id', String, ForeignKey('tournaments.id', ondelete="CASCADE"), primary_key=True),
    Column('team_id', String, ForeignKey('teams.id', ondelete="CASCADE"), primary_key=True)
)

class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    jerseyNumber = Column(Integer, nullable=True)
    battingStyle = Column(String, nullable=False)
    bowlingStyle = Column(String, nullable=False)
    role = Column(String, nullable=False)
    photoUri = Column(String, nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    teams = relationship("Team", secondary=team_players, back_populates="players")
    captainOf = relationship("Team", foreign_keys="[Team.captainId]", back_populates="captain")
    viceCaptainOf = relationship("Team", foreign_keys="[Team.viceCaptainId]", back_populates="viceCaptain")


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    logoUri = Column(String, nullable=True)
    color = Column(String, nullable=False)
    captainId = Column(String, ForeignKey("players.id", ondelete="SET NULL"), nullable=True)
    viceCaptainId = Column(String, ForeignKey("players.id", ondelete="SET NULL"), nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    players = relationship("Player", secondary=team_players, back_populates="teams")
    captain = relationship("Player", foreign_keys=[captainId], back_populates="captainOf")
    viceCaptain = relationship("Player", foreign_keys=[viceCaptainId], back_populates="viceCaptainOf")
    tournaments = relationship("Tournament", secondary=tournament_teams, back_populates="teams")


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    season = Column(String, nullable=False)
    organizer = Column(String, nullable=False)
    logoUri = Column(String, nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    teams = relationship("Team", secondary=tournament_teams, back_populates="tournaments")
    matches = relationship("Match", back_populates="tournament")


class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    tournamentId = Column(String, ForeignKey("tournaments.id", ondelete="SET NULL"), nullable=True)
    teamAId = Column(String, nullable=False)
    teamBId = Column(String, nullable=False)
    totalOvers = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    toss = Column(JSON, nullable=False)
    innings = Column(JSON, nullable=False, default=list)
    playingXIA = Column(ARRAY(String), nullable=True, default=list)
    playingXIB = Column(ARRAY(String), nullable=True, default=list)
    currentStrikerId = Column(String, nullable=True)
    currentNonStrikerId = Column(String, nullable=True)
    currentBowlerId = Column(String, nullable=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    tournament = relationship("Tournament", back_populates="matches")
