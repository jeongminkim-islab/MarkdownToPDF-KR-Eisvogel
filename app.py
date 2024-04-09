from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for
import subprocess
import os
import uuid
import yaml

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
BACKGROUND_FOLDER = 'backgrounds'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BACKGROUND_FOLDER'] = BACKGROUND_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Markdown to PDF Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            max-width: 400px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: inline-block;
            margin-right: 10px;
        }
        .form-group input[type="checkbox"] {
            vertical-align: middle;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #666;
        }
        input[type="file"], select, input[type="text"], input[type="date"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            margin-bottom: 20px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Markdown 파일을 PDF로 변환</h1>
    <form action="/convert" method="post" enctype="multipart/form-data">
        <label for="markdown">Markdown 파일:</label>
        <input type="file" name="markdown" id="markdown"><br>
        
        <label for="background">제목 페이지 배경 PDF 파일 (선택 사항):</label>
        <input type="file" name="background" id="background"><br>
        
        <label for="font">글꼴 (선택 사항):</label>
        <select name="font" id="font">
            <option value="NanumGothic">나눔고딕</option>
            <option value="NanumGothicCoding">나눔고딕코딩</option>
            <option value="NanumMyeongjo">나눔명조</option>
            <option value="NanumBarunGothic">나눔바른고딕</option>
            <option value="NanumSquare">나눔스퀘어</option>
            <option value="NanumSquareBold">나눔스퀘어 Bold</option>
            <option value="NanumSquareRound">나눔스퀘어라운드</option>
            <option value="NanumSquareRoundBold">나눔스퀘어라운드 Bold</option>
            <option value="NanumSquareRoundRegular">나눔 스퀘어라운드 Regular</option>
        </select><br>
        
        <label for="title">제목:</label>
        <input type="text" name="title" id="title"><br>
        
        <label for="author">작성자:</label>
        <input type="text" name="author" id="author"><br>
        
        <label for="date">날짜:</label>
        <input type="date" name="date" id="date"><br>
        
        <div class="form-group">
            <label for="titlepage" style="display: inline;">제목 페이지 생성:</label>
            <input type="checkbox" name="titlepage" id="titlepage" style="display: inline; width: auto; margin-left: 10px;">
        </div>

        <div class="form-group">
            <label for="titlepage-rule-height" style="display: block;">제목 페이지 줄 높이 (0은 줄 없음):</label>
            <input type="text" name="titlepage-rule-height" id="titlepage-rule-height" value="4" style="display: block; width: auto;">
        </div>      
        
        <div class="form-group">
            <label for="toc" style="display: inline;">목차 생성:</label>
            <input type="checkbox" name="toc" id="toc" style="display: inline; width: auto; margin-left: 10px;">
        </div>
        
        <div class="form-group">
            <label for="toc-own-page" style="display: inline;">목차 개별 페이지:</label>
            <input type="checkbox" name="toc-own-page" id="toc-own-page" style="display: inline; width: auto; margin-left: 10px;">
        </div>

        <input type="submit" value="변환">
    </form>
</body>
</html>
''')


def read_yaml_header(markdown_filename):
    with open(markdown_filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        yaml_header = content.split('---', 2)[1].strip()
        try:
            return yaml.safe_load(yaml_header)
        except yaml.YAMLError:
            return None
    else:
        return None


@app.route('/convert', methods=['POST'])
def convert():
    markdown_file = request.files.get('markdown')
    background_file = request.files.get('background')
    font = request.form.get('font')
    title = request.form.get('title')
    author = request.form.get('author')
    date = request.form.get('date')
    titlepage_rule_height = request.form.get('titlepage-rule-height', '4')  # 기본값은 4, 없애려면 0

    # 사용자 입력을 boolean 값으로 변환
    titlepage = request.form.get('titlepage') == 'on'
    toc = request.form.get('toc') == 'on'
    toc_own_page = request.form.get('toc-own-page') == 'on'

    if markdown_file:
        markdown_filename = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()) + '.md')
        markdown_file.save(markdown_filename)

        yaml_header = {
            'title': title or '',
            'author': author or '',
            'date': date or '',
            'titlepage': titlepage,
            'toc': toc,
            'toc-own-page': toc_own_page,
            'titlepage-rule-height': titlepage_rule_height
        }

        # 배경 PDF 파일이 제공된 경우
        if background_file:
            background_filename = os.path.join(BACKGROUND_FOLDER, str(uuid.uuid4()) + '.pdf')
            background_file.save(background_filename)
            # 배경 이미지 설정을 YAML 헤더에 추가
            yaml_header['titlepage-background'] = os.path.abspath(background_filename)

        with open(markdown_filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 기존 YAML 헤더가 있다면 제거
        if content.startswith('---'):
            content = content.split('---', 2)[-1].strip()
            if content.endswith('...'):
                content = content[:-3].strip()

        # 업데이트된 YAML 헤더와 기존 내용을 Markdown 파일에 쓰기
        with open(markdown_filename, 'w', encoding='utf-8') as f:
            f.write('---\n' + yaml.dump(yaml_header, allow_unicode=True) + '---\n\n' + content)

        # Pandoc 명령어 준비
        output_filename = os.path.join(OUTPUT_FOLDER, markdown_filename.split('/')[-1].replace('.md', '.pdf'))
        pandoc_command = [
            'pandoc', markdown_filename,
            '-o', output_filename,
            '--from', 'markdown',
            '--template', 'eisvogel',
            '--listings',
            '--pdf-engine=xelatex'
        ]

        # 글꼴 설정 추가
        if font:
            pandoc_command.extend(['-V', f'CJKmainfont={font}'])

        # Pandoc을 사용하여 Markdown을 PDF로 변환
        try:
            subprocess.run(pandoc_command, check=True)
        except subprocess.CalledProcessError as e:
            return f"Error producing PDF: {e}", 400

        return send_from_directory(directory=OUTPUT_FOLDER, path=os.path.basename(output_filename), as_attachment=True)

    return redirect(url_for('index'))


if __name__ == '__main__':
    for path in [UPLOAD_FOLDER, OUTPUT_FOLDER, BACKGROUND_FOLDER]:
        os.makedirs(path, exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
