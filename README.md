이 프로젝트는 Markdown 파일을 PDF 형식의 보고서로 변환하는 Flask 웹 애플리케이션입니다. 주요 특징으로는 Eisvogel LaTeX 템플릿을 활용한 고품질의 보고서 스타일링과 한국어 문서 변환을 위한 특화된 설정이 포함됩니다. 이를 통해 사용자는 한국어로 작성된 Markdown 문서를 쉽게 PDF 보고서로 변환할 수 있으며, 변환 과정에서 한국어 텍스트의 정확한 렌더링을 보장합니다.

---

# Markdown to PDF Converter with Eisvogel Template for Korean Reports
이 프로젝트는 사용자가 Markdown 문서를 PDF 보고서로 변환할 수 있게 해주는 Flask 기반 웹 서비스입니다. 특히, [Eisvogel LaTeX](https://github.com/Wandmalfarbe/pandoc-latex-template) 템플릿을 사용하여 보고서의 스타일링을 강화하고, 한국어로 된 문서의 변환을 개선하기 위한 추가 설정을 제공합니다. 이 서비스는 특히 한국어로 작성된 마크다운 파일을 높은 품질의 PDF로 변환하는 데 최적화되어 있습니다.

## 주요 특징

- **Eisvogel 템플릿 스타일링**: PDF 출력물에 고품질, 프로페셔널한 디자인을 적용합니다.
- **한국어 문서 변환 최적화**: 한국어로 된 Markdown 파일을 원활하게 PDF로 변환합니다. 이는 나눔고딕 폰트를 포함한 한국어 지원 설정 덕분에 가능합니다.
- **웹 기반 파일 업로드**: 사용자는 웹 인터페이스를 통해 파일을 쉽게 업로드하고 변환할 수 있습니다.
- **Docker를 이용한 간편한 배포와 실행**: 모든 필요한 종속성을 포함한 Dockerfile을 제공하여 어디서나 쉽게 서비스를 배포하고 실행할 수 있습니다.

## 시작하기

이 프로젝트를 로컬 머신 또는 서버에서 실행하기 위한 단계별 가이드입니다. Docker가 설치되어 있어야 합니다. 설치되어 있지 않다면, [Docker 공식 문서](https://docs.docker.com/get-docker/)를 참고하여 설치하세요.

### 프로젝트 클론

첫 단계로, GitHub 리포지토리를 클론합니다:

```bash
git clone https://github.com/your-username/Markdown-KR-PDF-Eisvogel.git
cd Markdown-KR-PDF-Eisvogel
```

### Docker 이미지 빌드

다음으로, Docker 이미지를 빌드합니다. 이 과정에서 필요한 모든 종속성이 설치됩니다:

```bash
docker build -t markdown-pdf-converter .
```

### Docker 컨테이너 실행

이미지 빌드가 완료되면, 아래 명령어로 Docker 컨테이너를 실행합니다:

```bash
docker run -d -p 8080:8080 markdown-pdf-converter
```

이제 서비스가 `8080` 포트에서 실행되고 있습니다. 웹 브라우저를 통해 `http://localhost:8080` 에 접속하면 서비스를 사용할 수 있습니다.

## 사용 방법

서비스를 사용하기 위해 웹 인터페이스를 이용하는 단계는 다음과 같습니다:

1. 웹 브라우저를 열고 `http://localhost:8080` 주소로 이동합니다.
2. 화면에 표시된 "파일 선택" 버튼을 클릭하여 변환하고자 하는 Markdown 파일을 선택합니다.
3. "업로드" 버튼을 클릭하여 파일을 서버에 전송합니다.
4. 파일이 성공적으로 변환되면, 변환된 PDF 파일을 다운로드하는 링크가 화면에 표시됩니다. 링크를 클릭하여 PDF 파일을 다운로드하세요.

이 과정을 통해 사용자는 간단하게 Markdown 파일을 고품질의 PDF로 변환할 수 있습니다. 변환된 PDF는 바로 다운로드할 수 있어, 효율적으로 문서 작업을 진행할 수 있습니다.
