from __future__ import annotations
from datetime import date
from typing import List
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# @dataclass
# class Event(Base):
#     __tablename__ = 'llhk_event'
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: str = Column(String)
#     date: date = Column(DateTime, default=func.now())
#     users: List[User] = relationship('User', secondary='llhk_user_event')
#     location: str = Column(String)
#     sponsors: List[Company] = relationship('Company', secondary='sponsor')
#     archived: bool = Column(Integer, default=0)
#     description: str = Column(String)
#     status: int = Column(Integer, default=0)

class Company(Base):
    __tablename__ = 'company'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    address: str = Column(String)
    telephone: str = Column(String)
    website: str = Column(String)
    logo: str = Column(String)
    users: List[User] = relationship('User', secondary='company_user')
    # events: List[Event] = relationship('Event', secondary='sponsor')

    
class User(Base):
    __tablename__ = 'llhk_user'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    nickname: str = Column(String)
    password: str = Column(String)
    birthdate: date = Column(DateTime)
    food_restrictions: str = Column(String)
    email: str = Column(String)
    telephone: str = Column(String)
    address: str = Column(String)
    shirt_size: str = Column(String)
    type: str = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "llhk_user",
        "polymorphic_on": type,
    }


class LleidaHacker(User):
    __tablename__ = 'lleida_hacker'
    user_id = Column(Integer, ForeignKey('llhk_user.id'), primary_key=True)
    role: str = Column(String)
    nif: str = Column(String)
    student: bool = Column(Integer, default=0)
    active: bool = Column(Integer, default=0)
    image: str = Column(String)
    github: str = Column(String)
    groups: List[LleidaHackerGroup] = relationship('LleidaHackerGroupUser', secondary='lleida_hacker_group', backref='lleida_hacker')

    __mapper_args__ = {
        "polymorphic_identity": "lleida_hacker",
    }

class CompanyUser(User):
    __tablename__ = 'company_user'
    user_id = Column(Integer, ForeignKey('llhk_user.id'), primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'), primary_key=True)
    role: str = Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "company",
    }

class Hacker(User):
    __tablename__ = 'hacker'
    user_id = Column(Integer, ForeignKey('llhk_user.id'), primary_key=True)
    banned: bool = Column(Integer, default=0)
    github: str = Column(String)
    linkedin: str = Column(String)
    groups: List[HackerGroup] = relationship('HackerGroupUser', secondary='hacker_group', backref='hacker')
    # is_leader: bool = Column(Integer, default=0)
    # events: List[Event] = relationship('Event', secondary='hacker_event')
    __mapper_args__ = {
        "polymorphic_identity": "hacker",
    }

class HackerGroup(Base):
    __tablename__ = 'hacker_group'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    leader_id: int = Column(Integer, ForeignKey('hacker.user_id'), nullable=False)
    users: List[Hacker] = relationship('Hacker', secondary='hacker_group_user', backref='hacker_group')

class HackerGroupUser(Base):
    __tablename__ = 'hacker_group_user'
    hacker_id = Column(Integer, ForeignKey('hacker.user_id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('hacker_group.id'), primary_key=True)

class LleidaHackerGroupUser(Base):
    __tablename__ = 'group_lleida_hacker_user'
    group_id = Column(Integer, ForeignKey('lleida_hacker_group.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('lleida_hacker.user_id'), primary_key=True)

class LleidaHackerGroup(Base):
    __tablename__ = 'lleida_hacker_group'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    leader_id: int = Column(Integer, ForeignKey('lleida_hacker.user_id'), nullable=False)
    members: List[LleidaHacker] = relationship('LleidaHacker', secondary='group_lleida_hacker_user', backref='lleida_hacker_group')

