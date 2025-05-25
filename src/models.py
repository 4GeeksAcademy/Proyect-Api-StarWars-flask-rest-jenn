from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

    def __repr__(self):
        return f"<User {self.email}>"

class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
        }

    def __repr__(self):
        return f"<People {self.name}>"

class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[str] = mapped_column(String(50))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }

    def __repr__(self):
        return f"<Planet {self.name}>"

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)

    user = relationship('User')
    people = relationship('People')
    planet = relationship('Planet')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} people_id={self.people_id} planet_id={self.planet_id}>"
