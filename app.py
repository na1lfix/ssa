import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Укажите директорию для хранения загруженных файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создание директории для загрузки файлов, если она не существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "File uploaded successfully!", 200

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '').lower()  # Приводим запрос к нижнему регистру
    matching_files = []
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if query in f.lower():  # Приводим имя файла к нижнему регистру для сравнения
            matching_files.append(os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], f)))  # Абсолютный путь
    return jsonify({'files': matching_files})

if __name__ == '__main__':
    app.run(debug=True)
