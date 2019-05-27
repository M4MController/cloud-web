from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Object(Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    controllers = relationship(
        'Controller',
        uselist=True,
        lazy='noload',
    )


class Controller(Base):
    __tablename__ = 'controllers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    meta = Column(String, default='')
    activation_date = Column(DateTime(timezone=False))
    deactivation_date = Column(DateTime(timezone=False))
    status = Column(Integer, default=None)
    controller_type = Column(Integer, default=None)
    mac = Column(String, nullable=False)
    object_id = Column(Integer, ForeignKey('objects.id'), nullable=False)

    sensors = relationship(
        'Sensor',
        uselist=True,
        lazy='noload',
    )

    object = relationship(
        'Object',
        uselist=False,
        lazy='noload',
    )


class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    activation_date = Column(DateTime(timezone=False))
    deactivation_date = Column(DateTime(timezone=False))
    status = Column(Integer, default=None)
    sensor_type = Column(Integer, default=None)
    controller_id = Column(String, ForeignKey('controllers.id'), nullable=False)

    # one-to-many relation
    controller = relationship(
        'Controller',
        uselist=False,
        lazy='noload',
    )
