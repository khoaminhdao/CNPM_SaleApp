from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from app import app, dao, utils
from functools import wraps


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.url))

        return f(*args, **kwargs)

    return check


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def product_list():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    return render_template("products.html",
                           products=dao.read_products(keyword=kw,
                                                      from_price=from_price,
                                                      to_price=to_price))


@app.route("/api/products", methods=["get", "post"])
def api_product_list():
    if request.method == "POST":
        err = ""
        product_id = request.args.get("product_id")
        product = None
        if product_id:
            product = dao.read_product_by_id(product_id=int(product_id))

        if request.method.lower() == "post":
            if product_id:  # Cap nhat
                data = dict(request.form.copy())
                data["product_id"] = product_id
                if dao.update_product(**data):
                    return redirect(url_for("product_list"))
            else:  # Them

                import json
                product = dao.add_product(**dict(json.loads(request.data)))
                if product:
                    return jsonify(product)

            err = "Something wrong!!! Please back later!"

        return jsonify({"error_message": err})

    kw = request.args.get("keyword")

    return jsonify(dao.read_products(keyword=kw))


@app.route("/products/<int:category_id>")
def products_by_cate_id(category_id):
    return render_template("products.html",
                           products=dao.read_products(category_id=category_id))


@app.route("/products/add", methods=["get", "post"])
@login_required
def add_or_update_product():

    err = ""
    product_id = request.args.get("product_id")
    product = None
    if product_id:
        product = dao.read_product_by_id(product_id=int(product_id))

    if request.method.lower() == "post":
        # name = request.form.get("name")
        # price = request.form.get("price", 0)
        # images = request.form.get("images")
        # description = request.form.get("description")
        # category_id = request.form.get("category_id", 0)
        # import pdb
        # pdb.set_trace()
        if product_id: # Cap nhat
            data = dict(request.form.copy())
            data["product_id"] = product_id
            if dao.update_product(**data):
                return redirect(url_for("product_list"))
        else: # Them
            if dao.add_product(**dict(request.form)):
                return redirect(url_for("product_list"))

        err = "Something wrong!!! Please back later!"

    return render_template("product-add.html",
                           categories=dao.read_categories(),
                           product=product,
                           err=err)


@app.route("/api/products/<int:product_id>", methods=["delete"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": {"product_id": product_id}
        })

    return jsonify({
        "status": 500,
        "message": "Failed"
    })


@app.route("/products/export")
@login_required
def export_product():
    return send_file(utils.export_csv())


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.validate_user(username=username, password=password)
        if user:
            session["user"] = user

            if "next" in request.args:
                return redirect(request.args["next"])
            else:
                return redirect(url_for("index"))
        else:
            err_msg = "DANG NHAP KHONG THANH CONG"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)