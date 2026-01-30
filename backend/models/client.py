from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))

    cars = relationship("Car", back_populates="client")
