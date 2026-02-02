from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class SparePart(Base):
    __tablename__ = "spare_parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
