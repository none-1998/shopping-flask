from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, jsonify
from config import Config
from flask import request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import os
import json
from flask import flash

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     description = db.Column(db.Text)
#     image_url = db.Column(db.String(200))
#     img_src = db.Column(db.String(200))
#
#     def __repr__(self):
#         return f'<Product {self.name}>'

@app.route("/", methods=["GET"])
def home():
    products = Product.query.order_by(Product.id.desc()).limit(3).all()
    return render_template("home.html", products=products)
    # return render_template("home.html")

# @app.route("/add", methods=["GET", "POST"])
# def add_product():
#     if "user_id" not in session:
#         flash("برای افزودن محصول باید وارد حساب خود شوید", "warning")
#         return redirect(url_for("login"))
#
#     if request.method == "POST":
#         name = request.form["name"]
#         price = float(request.form["price"])
#         description = request.form.get("description")
#         image_url = request.form.get("image_url")
#
#         new_product = Product(name=name, price=price, description=description, image_url=image_url)
#         db.session.add(new_product)
#         db.session.commit()
#
#         return redirect(url_for("add_product"))
#
#     return render_template("add_product.html")
#
# @app.route("/products", methods=["GET"])
# def show_products():
#     query = request.args.get("q")
#     if query:
#         products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
#     else:
#         products = Product.query.all()
#     return render_template("products_1.html", products=products)


# @app.route("/product/<int:product_id>")
# def product_detail(product_id):
#     product = Product.query.get_or_404(product_id)
#
#     # مسیر به فایل json مربوط به هر محصول
#
#
#     json_path = os.path.join("json_files", f"product_{product_id}.json")
#     print("Looking for JSON at:", json_path)
#     print("Exists?", os.path.exists(json_path))
#
#     # بررسی وجود فایل و بارگذاری داده‌ها
#     extra_data = {}
#     if os.path.exists(json_path):
#         with open(json_path, "r", encoding="utf-8") as f:
#             extra_data = json.load(f)
#             print("Loaded JSON:", extra_data)
#
#     else:
#         print("JSON file not found.")
#
#     # ترکیب داده‌ی محصول و داده‌ی JSON
#     product_dict = {
#         "id": product.id,
#         "name": product.name,
#         "price": product.price,
#         "description": product.description,
#         "image_url": product.image_url,
#         "img_src": product.img_src,
#     }
#     product_dict.update(extra_data)
#
#     return render_template("product_detail.html", product=product_dict)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#
#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             # ✅ اینجا اطلاعات کاربر رو در session ذخیره کن
#             session["user_id"] = user.id
#             session["username"] = user.username
#
#             flash("ورود موفقیت‌آمیز بود.", "success")
#             return redirect(url_for("show_products"))
#         else:
#             flash("نام کاربری یا رمز عبور اشتباه است!", "danger")
#             return render_template("login.html")
#
#     return render_template("login.html")


@app.route("/cart")
def view_cart():
    cart_ids = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    return render_template('cart.html', products=products)

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True

    return redirect("/")

@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    if "cart" in session:
        session["cart"] = [pid for pid in session["cart"] if pid != product_id]
        session.modified = True
    return redirect(url_for("view_cart"))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]
#         confirm_password = request.form["confirm_password"]
#
#         if password != confirm_password:
#             flash("رمز عبور و تکرار آن مطابقت ندارد", "danger")
#             return render_template("signup.html")
#
#         existing_user = User.query.filter(
#             (User.username == username) | (User.email == email)
#         ).first()
#
#         if existing_user:
#             flash("نام کاربری یا ایمیل قبلاً ثبت شده‌اند!", "danger")
#             return render_template("signup.html")
#
#         new_user = User(username=username, email=email)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#
#         flash("ثبت نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.", "success")
#         return redirect(url_for("login"))
#
#     return render_template("signup.html")

# @app.route("/logout")
# def logout():
#     session.clear()
#     flash("شما با موفقیت خارج شدید.", "info")
#     return redirect(url_for("login"))

@app.route("/api/products", methods=["GET"])
def api_get_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "image_url": product.image_url,
            "img_src": product.img_src,
        })
    return jsonify(products_list)

@app.route("/api/product/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_dict = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image_url": product.image_url,
        "img_src": product.img_src,
    }
    return jsonify(product_dict)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "درخواست نامعتبر است"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "نام کاربری و رمز عبور الزامی است"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "message": "ورود موفق بود"
        }), 200

    return jsonify({"msg": "نام کاربری یا رمز عبور اشتباه است"}), 401

@app.route("/api/profile", methods=["POST"])
@jwt_required()
def api_get_profile():
    user_id = get_jwt_identity()

    # گرفتن اطلاعات کاربر از دیتابیس
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "کاربر پیدا نشد"}), 404

    # بازگرداندن اطلاعات کاربر
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("database created")
    app.run(debug=True)

