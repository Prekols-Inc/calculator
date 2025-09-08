import os
from http import HTTPStatus
from flask import Flask, jsonify, abort, request, Response
from typing import Any
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config.from_object("config")
db = SQLAlchemy(app)

bad_expression_msg = "Bad expression"
json_error_msg = "Request must be JSON"


def error(code: HTTPStatus, message: str):
    abort(Response(message, int(code)))


class Calculation(db.Model):
    __tablename__ = "calculations"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    expression = db.Column(db.String(512), nullable=False)
    result = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<{self.expression} = {self.result}>"


class HistoryStore:
    def __init__(self, commit_every: int = 1):
        self._buffer = []
        self._n = commit_every if commit_every > 0 else 1

    def add(self, expression: str, result: str):
        self._buffer.append(Calculation(expression=expression, result=result))
        if len(self._buffer) >= self._n:
            db.session.add_all(self._buffer)
            db.session.commit()
            self._buffer.clear()

    def flush(self):
        if self._buffer:
            db.session.add_all(self._buffer)
            db.session.commit()
            self._buffer.clear()

    def all(self):
        return Calculation.query.order_by(Calculation.created_at.desc()).all()


store = HistoryStore(commit_every=1)


def list_history() -> list[dict[str, Any]]:
    rows = store.all()
    payload = [
        {
            "expression": r.expression,
            "result": (r.result or "").replace("\n", ""),
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
    return payload


def add_record(expr: str, res: str) -> bool:
    store.add(expr, res)

    return True


def calculate(expr: str) -> tuple[bool, Any]:
    try:
        answer = eval(expr)
        result = True
        return result, answer
    except BaseException as e:
        print(f"eval error: {e}")
        return False, None


@app.route("/v1/calculate", methods=["POST"])
def calculate_handler():
    if not request.is_json:
        return jsonify({"error": json_error_msg}), 400

    expr = request.get_json().get("expression")
    result, answer = calculate(expr)
    if result:
        add_record(expr, answer)
        return jsonify({"result": str(answer)}), 200
    else:
        return jsonify({"error": bad_expression_msg}), 400


@app.route("/v1/history", methods=["GET"])
def history_handler():
    return jsonify(list_history())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host=app.config.get("FLASK_HOST", "127.0.0.1"),
        port=app.config.get("FLASK_PORT", 5000),
        debug=app.config.get("DEBUG", False),
    )
