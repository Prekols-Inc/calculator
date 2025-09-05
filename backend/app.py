from flask import Flask, jsonify, request
from calculate import calculate

app = Flask(__name__)

@app.route('/v1/calculate', methods=['POST'])

def calculate():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    expr = request.get_json().get('expression')
    result, answer = calculate(expr)
    if result:
        return jsonify({"result": str(answer)})
    
    return None, 400


@app.route("/history")
def get_history():
    pass

if __name__ == "__main__":
    app.run(debug=True)
