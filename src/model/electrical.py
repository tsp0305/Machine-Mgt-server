from src.config import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship


class Electrical(Base):
    __tablename__= "electrical"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machine.id"), unique=True)
    installed_power_kw_per_machine = Column(Float)
    installed_power_kw_total = Column(Float)
    fuse_or_mccb = Column(Integer)
    power_cable_size_sqmm = Column(String)
    earth_wire_size_sqmm = Column(String)

    machine = relationship("Machine", back_populates="electrical")