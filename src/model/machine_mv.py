from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MachineFullView(Base):
    __tablename__ = "machine_full_view"

    # REQUIRED for SQLAlchemy (must have a primary key)
    machine_id = Column(Integer, primary_key=True)

    # =====================
    # MACHINE
    # =====================
    model_name = Column(String)
    description = Column(Text)
    model = Column(String)
    waste_collection_split = Column(String)
    can_changer_type = Column(String)
    feed_type = Column(String)
    wcs_type = Column(String)
    webdoff_type = Column(String)
    product_code = Column(String)
    quantity = Column(Integer)
    weight_kg = Column(Float)
    dept_id = Column(Integer)

    # =====================
    # DEPARTMENT
    # =====================
    department_id = Column(Integer)
    department_name = Column(String)

    # =====================
    # ELECTRICAL
    # =====================
    electrical_id = Column(Integer)
    installed_power_kw_per_machine = Column(Float)
    installed_power_kw_total = Column(Float)
    fuse_or_mccb = Column(String)
    power_cable_size_sqmm = Column(Float)
    earth_wire_size_sqmm = Column(Float)

    # =====================
    # COMPRESSED AIR
    # =====================
    compressed_air_id = Column(Integer)
    nm3_per_hr_per_machine = Column(Float)
    nm3_per_hr_total = Column(Float)
    pressure_bar = Column(Float)
    incoming_hose_size_mm = Column(Float)

    # =====================
    # EXHAUST AIR
    # =====================
    exhaust_air_id = Column(Integer)
    air_m3_sec_per_machine = Column(Float)
    air_m3_sec_total = Column(Float)
    air_to_trench_per_machine = Column(Float)
    air_to_trench_total = Column(Float)
    air_to_filter_per_machine = Column(Float)
    air_to_filter_total = Column(Float)
    pressure_pascal = Column(Float)
    remarks = Column(Text)
