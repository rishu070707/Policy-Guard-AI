from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from load_docs import save_all_to_vector_db
from query_docs import search_chunks

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    save_all_to_vector_db(filepath)

    return jsonify({'message': f'✅ File {file.filename} uploaded and indexed.'})


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({'error': 'Query cannot be empty'}), 400

    try:
        result = search_chunks(user_query)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
