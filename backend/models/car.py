from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=True)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    license_plate: Mapped[str] = mapped_column(String(15), nullable=True)
    color: Mapped[str] = mapped_column(String(30), nullable=True)

    client = relationship("Client", back_populates="cars")
    contracts = relationship("Contract", back_populates="car")