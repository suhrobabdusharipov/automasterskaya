from datetime import date
from sqlalchemy import Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    services_description: Mapped[str] = mapped_column(Text)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=0)

    contract = relationship("Contract", back_populates="orders")