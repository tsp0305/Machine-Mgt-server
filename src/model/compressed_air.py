from src.config import Base
from sqlalchemy import Column,Integer,Float,ForeignKey
from sqlalchemy.orm import relationship


class CompressedAir(Base):
    __tablename__ = "compressed_air"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machine.id"), nullable=False)
    nm3_per_hr_per_machine = Column(Float)
    nm3_per_hr_total = Column(Float)
    pressure_bar = Column(Float)
    incoming_hose_size_mm = Column(Float)

    machine = relationship("Machine", back_populates="compressed_air")

