import os
import json
from app import app, db, Product

JSON_DIR = os.path.join(os.getcwd(), "json_files")

with app.app_context():
    for filename in os.listdir(JSON_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(JSON_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

                title = data.get("title") or data.get("name") or filename.replace(".json", '')

                product = Product(title=title, data=data)
                db.session.add(product)

    db.session.commit()
    print("all json files have been imported.")