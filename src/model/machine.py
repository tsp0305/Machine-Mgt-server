from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.config import Base


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(Integer,primary_key = True)
    model_name = Column(String(255))
    description = Column(JSONB, default=dict)
    model = Column(String(255))
    waste_collection_split = Column(String)
    can_changer_type = Column(String)
    feed_type = Column(String)
    wcs_type = Column(String)
    webdoff_type = Column(String)
    product_code = Column(Integer)
    quantity = Column(Integer)  
    weight_kg = Column(Float)

    dept_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department = relationship(
        "Department",
        back_populates="machines"
    )

    electrical = relationship("Electrical", uselist=False, back_populates="machine",
        cascade="all, delete-orphan")
    compressed_air = relationship("CompressedAir", uselist=False, back_populates="machine",
        cascade="all, delete-orphan")
    exhaust_air = relationship("ExhaustAir", uselist=False, back_populates="machine",
        cascade="all, delete-orphan")
