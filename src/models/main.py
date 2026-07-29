from .database import SessionLocal
from .plants_model import Plant
from .database import engine, Base
import os
from typing import Any

from sqlalchemy import select

Base.metadata.create_all(bind=engine)

def save_in_database(data: dict[str, Any]) -> None:
    try:
        with open(f"./images/imagem_{data["id"]}.jpg", "rb") as file:
            image = file.read()


        planta = Plant(
            id=data["id"],
            name=data.get("name", None) or None,
            month=data.get("months", None) or None,
            feature=data.get("features", None) or None,
            other_names=data.get("other_names", None),
            pruning=data.get("pruning", None) or None,
            scientific_name=data.get("scientific_name", None) or None,
            seasons=data.get("seasons", None) or None,
            sunlight=data.get("sunlight", None) or None,
            watering=data.get("watering", None) or None,
            image=image,
            alt_image=data.get("alt_img", None) or None,
        )

        session = SessionLocal()
        session.add(planta)
        session.commit()
    finally:
        session.close()

        if os.path.exists(f"./images/imagem_{data["id"]}.jpg"):
            os.remove(f"./images/imagem_{data["id"]}.jpg")

# session = SessionLocal()
# table = select(Plant.id)

# plantas = session.scalars(table).all()

# print(plantas)



# diferentes = []
# contador = 0
# for id in ids:
#     contador += 1
#     if contador != id:
#         diferentes.append(contador)
#         contador += 1

# print(diferentes)
# print(len(diferentes))