import pandas as pd
from app_4 import app, Product, db

df = pd.read_excel("totalads.xlsx")

with app.app_context():
    for index, row in df.iterrows():
        product = Product(
            name=row["name"],
            price=row["price"],
            description=row.get("description", ""),
            image_url=row.get("image_url", ""),
            img_src=row.get("img_src", ""),
        )
        db.session.add(product)

    db.session.commit()

