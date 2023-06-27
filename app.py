from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(120), nullable=False)


@app.route('/', methods=['GET'])
def main_page():
    return jsonify({"body": "Hello, world!"})


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': note.id, 'title': note.title, 'body': note.body} for note in notes])


@app.route('/new_note', methods=['POST'])
def new_note():
    note_data = request.get_json()
    new_note = Note(title=note_data['title'], body=note_data['body'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id, 'title': new_note.title, 'body': new_note.body}), 201


@app.route('/note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)