from flask import Blueprint, render_template, request, jsonify, current_app
from .db import get_engine
from sqlalchemy import text

main_bp = Blueprint("main", __name__)

COURSES = ["Minimum Standards", "Science Extension", "Sofware Engineering", "Enterprise Computing"]

@main_bp.get("/")
def index():
    return render_template("index.html", courses=COURSES)

@main_bp.post("/query")
def run_query():
    payload = request.get_json(force=True)
    course = payload.get("course")
    action = payload.get("action")
    student_number = payload.get("studentNumber")

    config = current_app.config_store.load()
    queries = config.get("queries", {})
    key = f"{course}:{action}"
    sql = queries.get(key)
    if not sql:
        return jsonify({"error": "Query not configured for this selection"}), 400

    params = {}
    if student_number is not None:
        params["student_number"] = student_number

    engine = get_engine(config.get("database", {}))

    rows = []
    columns = []
    with engine.connect() as conn:
        result = conn.execute(text(sql), params) if params else conn.execute(text(sql))
        columns = list(result.keys())
        rows = [list(r) for r in result.fetchall()]

    return jsonify({"columns": columns, "rows": rows})
