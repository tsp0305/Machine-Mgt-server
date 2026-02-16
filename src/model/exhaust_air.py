from src.config import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship


class ExhaustAir(Base):
    __tablename__ = "exhaust_air"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machine.id"), nullable=False)
    air_m3_sec_per_machine = Column(Float)
    air_m3_sec_total = Column(Float)
    air_to_trench_per_machine = Column(Float)
    air_to_trench_total = Column(Float)
    air_to_filter_per_machine = Column(Float)
    air_to_filter_total = Column(Float)
    pressure_pascal = Column(Float)
    remarks = Column(String)

    machine = relationship("Machine", back_populates="exhaust_air")
