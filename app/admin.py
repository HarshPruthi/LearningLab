from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

admin_bp = Blueprint("admin", __name__, template_folder="templates")

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped

@admin_bp.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        password = request.form.get("password")
        config = current_app.config_store.load()
        admin_hash = config.get("admin", {}).get("password_hash")
        if admin_hash and check_password_hash(admin_hash, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Invalid credentials", "error")
    return render_template("admin_login.html")

@admin_bp.get("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("admin.login"))

@admin_bp.route("/", methods=["GET", "POST"]) 
@login_required
def dashboard():
    config = current_app.config_store.load()
    message = None
    if request.method == "POST":
        if request.form.get("form_type") == "db":
            # DB settings are managed via environment/Secrets; ignore saves
            message = "Database settings are managed by AWS Secrets and cannot be changed here."
        elif request.form.get("form_type") == "queries":
            queries = {}
            for key, value in request.form.items():
                if key.startswith("q_"):
                    queries[key[2:].replace("__", ":")] = value
            config["queries"] = queries
            current_app.config_store.save(config)
            message = "Queries updated."
        elif request.form.get("form_type") == "password":
            new_password = request.form.get("new_password")
            if new_password:
                config.setdefault("admin", {})["password_hash"] = generate_password_hash(new_password)
                current_app.config_store.save(config)
                message = "Admin password updated."

    # Provide DB env values to template for read-only display
    db_env = {
        "driver": os.environ.get("DB_DRIVER", "postgresql"),
        "host": os.environ.get("DB_HOST", ""),
        "port": os.environ.get("DB_PORT", ""),
        "database": os.environ.get("DB_NAME", ""),
        "username": os.environ.get("DB_USERNAME", ""),
        "password": "********" if os.environ.get("DB_PASSWORD") else "",
    }
    return render_template("admin_dashboard.html", config=config, message=message, db_env=db_env)