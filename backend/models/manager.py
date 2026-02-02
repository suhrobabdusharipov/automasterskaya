from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Manager(Base):
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contacts: Mapped[str] = mapped_column(String(255))
