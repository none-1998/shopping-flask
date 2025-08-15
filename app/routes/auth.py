from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User  # اگر مدل‌ها رو جدا کردی
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length




auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("ورود موفقیت‌آمیز بود.", "success")
            return redirect(url_for("products.show_products"))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است!", "danger")

    return render_template("login.html")

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('رمز عبور و تکرار آن مطابقت ندارد.', 'danger')
            return render_template('signup.html')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('نام کاربری یا ایمیل قبلاً ثبت شده‌اند!', 'danger')
            return render_template('signup.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('ثبت نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("شما با موفقیت خارج شدید.", "info")
    return redirect(url_for("auth.login"))
# مشابه همین کار برای signup, logout
