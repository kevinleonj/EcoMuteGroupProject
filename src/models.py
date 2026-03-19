# SQLAlchemy ORM Models – Lab 5 (Full Bidirectional Relationships)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey


class Base(DeclarativeBase):
    pass


class Bike(Base):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    battery: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")
    battery_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Standard Commuter (400-600 Wh)")  # ADD THIS

    #fix testpy ORM model with Pydantic schema
    station_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # FULL bidirectional relationship
    rentals: Mapped[list["Rental"]] = relationship(
        back_populates="bike",
        cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)

    # ADD THESE TWO LINES
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    rentals: Mapped[list["Rental"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)

    bike_id: Mapped[int] = mapped_column(
        ForeignKey("bikes.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Bidirectional relationships
    bike: Mapped["Bike"] = relationship(
        back_populates="rentals"
    )

    user: Mapped["User"] = relationship(
        back_populates="rentals"
    )