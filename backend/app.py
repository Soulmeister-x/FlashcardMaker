from flask import Flask, request, jsonify
from pdf_processor import process_file


app = Flask(__name__)

@app.route('/process_pdf', methods=['POST'])
def handle_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    flashcards = process_file(file)
    return jsonify(flashcards), 200
    #return jsonify({"error": "Invalid file type"}), 400


if '__main__' == __name__:
    app.run(host='0.0.0.0', port=5000)
