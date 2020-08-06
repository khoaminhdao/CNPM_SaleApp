from app import app
import json
import os


def read_categories():
    with open(os.path.join(app.root_path, "data/categories.json"),
              encoding="utf-8") as f:
        return json.load(f)


def read_product_by_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p

    return None


def read_products(category_id=0, keyword=None, from_price=None, to_price=None):
    with open(os.path.join(app.root_path, "data/products.json"),
              encoding="utf-8") as f:
        products = json.load(f)

        if category_id > 0:
            products = [p for p in products if p["category_id"] == category_id]

        if keyword:
            products = [p for p in products if p["name"].lower().find(keyword.lower()) >= 0]

        if from_price and to_price:
            products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]

        return products


def update_product(product_id, name, description, price, images, category_id):
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            products[idx]["name"] = name
            products[idx]["description"] = description
            products[idx]["price"] = float(price)
            products[idx]["images"] = images
            products[idx]["category_id"] = int(category_id)

            break

    try:
        with open(os.path.join(app.root_path, "data/products.json"),
                  "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

            return True
    except Exception as ex:
        print(ex)
        return False

def add_product(name, description, price, images, category_id):
    products = read_products()
    product = {
         "id": len(products) + 1,
         "name": name,
         "description": description,
         "price": float(price),
         "images": images,
         "category_id": int(category_id)
    }
    products.append(product)

    try:
        with open(os.path.join(app.root_path, "data/products.json"),
                  "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

            return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == "__main__":
    print(read_products())