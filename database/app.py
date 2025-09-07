import os
from http import HTTPStatus
from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)


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


@app.route("/history", methods=["GET"])
def list_history():
    rows = store.all()
    payload = [
        {
            "expression": r.expression,
            "result": (r.result or "").replace("\n", ""),
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
    return jsonify({"calculations": payload})


@app.route("/add", methods=["POST"])
def add_record():
    data = request.get_json(silent=True)
    if not data:
        error(HTTPStatus.BAD_REQUEST, "No JSON provided")
    try:
        expr = data["expression"]
        res = data["result"]
    except KeyError as e:
        error(HTTPStatus.BAD_REQUEST, f"Missing field: {e.args[0]}")
    if not isinstance(expr, str) or not isinstance(res, str):
        error(
            HTTPStatus.BAD_REQUEST, "Fields 'expression' and 'result' must be strings"
        )

    store.add(expr, res)
    return "done", HTTPStatus.CREATED


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(
        host=app.config.get("FLASK_HOST", "127.0.0.1"),
        port=app.config.get("FLASK_PORT", 5000),
        debug=app.config.get("DEBUG", False),
    )
