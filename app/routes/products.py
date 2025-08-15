from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Product
from app.extensions import db
import os
import json

products_bp = Blueprint("products", __name__)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if "user_id" not in session:
        flash("برای افزودن محصول باید وارد حساب خود شوید", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form.get("description")
        image_url = request.form.get("image_url")

        new_product = Product(name=name, price=price, description=description, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for("products.add_product"))

    return render_template("add_product.html")

@products_bp.route("/products", methods=["GET"])
def show_products():
    query = request.args.get("q")
    if query:
        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        products = Product.query.all()
    return render_template("products_1.html", products=products)


@products_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    # مسیر به فایل json مربوط به هر محصول


    json_path = os.path.join("json_files", f"product_{product_id}.json")
    print("Looking for JSON at:", json_path)
    print("Exists?", os.path.exists(json_path))

    # بررسی وجود فایل و بارگذاری داده‌ها
    extra_data = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            extra_data = json.load(f)
            print("Loaded JSON:", extra_data)

    else:
        print("JSON file not found.")

    # ترکیب داده‌ی محصول و داده‌ی JSON
    product_dict = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image_url": product.image_url,
        "img_src": product.img_src,
    }
    product_dict.update(extra_data)

    return render_template("product_detail.html", product=product_dict)
