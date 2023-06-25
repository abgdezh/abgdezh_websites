from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_page():
    return jsonify({"body": "Hello, world!"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(
        [
            {"id": 1, "body": "Note 1"},
            {"id": 2, "body": "Note 2"}
        ]
    )

if __name__ == '__main__':
    app.run(port=8080)