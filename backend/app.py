from flask import Flask, request, jsonify
from typing import Any
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bad_expression_msg = "Bad expression"
json_error_msg = "Request must be JSON"


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
        return jsonify({"result": str(answer)}), 200
    else:
        return jsonify({"error": bad_expression_msg}), 400


@app.route("/v1/history", methods=["GET"])
def history_handler():
    pass

@app.route('/health', methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
