from app import dao, app
from datetime import datetime
import csv
import os


def export_csv():
    products = dao.read_products()
    p = os.path.join(app.root_path, "data/products-%s.csv" % str(datetime.now()))
    with open(p, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "description",
                                               "price", "images", "category_id"])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

    return p