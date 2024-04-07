from flask import Flask, request, send_from_directory, render_template_string
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Upload the file to be converted to PDF</title>
</head>
<body>
    <h1>Upload the file to be converted to PDF</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type="submit" value="Upload" />
    </form>
</body>
</html>
''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Convert the file using Pandoc
        output_filename = os.path.join(OUTPUT_FOLDER, file.filename.rsplit('.', 1)[0] + '.pdf')
        subprocess.run(['pandoc', filename, '-o', output_filename, '--template', 'eisvogel', '--from', 'markdown', '--listings', '-V', 'CJKmainfont="NanumGothic"', '--pdf-engine=xelatex'])
        
        return send_from_directory(directory=OUTPUT_FOLDER, path=os.path.basename(output_filename), as_attachment=True)

if __name__ == '__main__':

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    app.run(host='0.0.0.0', port=8080)
