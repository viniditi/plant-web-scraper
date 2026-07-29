from sqlalchemy import Integer, String, JSON, Text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Plant(Base):

    __tablename__ = "Plant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    other_names: Mapped[list] = mapped_column(JSON, nullable=True)
    scientific_name: Mapped[str] = mapped_column(String(100), nullable=True)
    month: Mapped[dict] = mapped_column(JSON, nullable=True)
    feature: Mapped[dict] = mapped_column(JSON, nullable=True)
    pruning: Mapped[str] = mapped_column(Text, nullable=True)
    seasons: Mapped[dict] = mapped_column(JSON, nullable=True)
    sunlight: Mapped[str] = mapped_column(Text, nullable=True)
    watering: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    alt_image: Mapped[str] = mapped_column(String(100), nullable=True)