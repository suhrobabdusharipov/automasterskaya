from sqlalchemy import Date, ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)

    client = relationship("Client", back_populates="contracts")
    car = relationship("Car", back_populates="contracts")
    orders = relationship("Order", back_populates="contract")
