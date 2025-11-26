# 🌐 NLLB 번역기

Meta AI의 NLLB-200 모델 기반 다국어 번역기 (TTS 음성 합성 지원)

---

## 📋 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [주요 기능](#주요-기능)
3. [시스템 요구사항](#시스템-요구사항)
4. [설치 방법](#설치-방법)
5. [실행 방법](#실행-방법)
6. [사용 방법](#사용-방법)
7. [지원 언어](#지원-언어)
8. [문제 해결](#문제-해결)
9. [파일 구조](#파일-구조)

---

## 프로젝트 소개

Meta AI의 NLLB-200 (No Language Left Behind) 모델을 사용한 고품질 번역기입니다.
웹 기반 인터페이스로 누구나 쉽게 사용할 수 있으며, Coqui TTS를 통한 음성 합성 기능도 제공합니다.

### 특징
- ✅ **고품질 번역**: Meta AI의 최신 번역 모델 사용
- ✅ **다국어 지원**: 7개 주요 언어 번역
- ✅ **음성 합성**: 4개 언어 TTS 지원
- ✅ **웹 기반**: 브라우저에서 바로 사용
- ✅ **무료**: 오픈소스 기반

---

## 주요 기능

### 1. 번역
- 7개 언어 간 자유로운 번역
- 최대 5,000자 지원
- 실시간 번역 결과

### 2. 음성 합성 (TTS)
- 번역 결과를 음성으로 변환
- 영어, 스페인어, 프랑스어, 독일어 지원
- 고품질 단일 언어 모델 사용

### 3. 편의 기능
- 언어 바꾸기 (⇄ 버튼)
- 결과 복사
- 키보드 단축키
  - `Ctrl + Enter`: 번역
  - `Esc`: 입력 지우기

---

## 시스템 요구사항

### 필수 사항
- **운영체제**: Windows 10/11, macOS, Linux
- **Python**: 3.8 ~ 3.11 (3.10 권장)
- **RAM**: 최소 4GB (8GB 이상 권장)
- **저장공간**: 최소 5GB (모델 다운로드용)
- **인터넷**: 첫 실행 시 모델 다운로드 필요 (~2.5GB)

### 권장 사항
- **RAM**: 8GB 이상
- **저장공간**: 10GB 이상
- **CPU**: 멀티코어 프로세서 (번역 속도 향상)

---

## 설치 방법

### 1. Python 설치 확인

```bash
python --version
```

Python 3.8 ~ 3.11 버전이어야 합니다.

**설치되어 있지 않다면**:
- Windows: https://www.python.org/downloads/
- macOS: `brew install python@3.10`
- Linux: `sudo apt install python3.10`

---

### 2. 프로젝트 다운로드

```bash
# ZIP 파일 압축 해제
unzip translator_clean_updated.zip
cd translator_clean
```

---

### 3. 가상환경 생성 (권장)

#### Windows (CMD)
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

만약 PowerShell에서 에러 발생 시:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

**설치되는 패키지**:
- `flask` - 웹 서버
- `transformers` - NLLB 번역 모델
- `torch` - 딥러닝 프레임워크
- `sentencepiece` - 토크나이저
- `protobuf` - 데이터 직렬화
- `TTS` - Coqui TTS 음성 합성

**소요 시간**: 5-10분 (인터넷 속도에 따라)

---

## 실행 방법

### 1. 서버 시작

```bash
python app.py
```

**첫 실행 시**:
- NLLB 모델 다운로드 (~2.5GB)
- 5-10분 소요
- 이후 실행은 즉시 시작

**실행 성공 시 출력**:
```
Server starting on http://localhost:5000
 * Running on http://0.0.0.0:5000
```

---

### 2. 웹 브라우저에서 접속

```
http://localhost:5000
```

또는

```
http://127.0.0.1:5000
```

---

### 3. 종료

터미널에서 `Ctrl + C` 누르기

---

## 사용 방법

### 기본 번역

1. **원본 언어 선택** (기본값: 한국어)
2. **번역 언어 선택** (기본값: 영어)
3. **텍스트 입력** (최대 5,000자)
4. **번역하기 버튼 클릭** 또는 `Ctrl + Enter`

### 음성 합성 (TTS)

1. **TTS 체크박스 선택**
2. **번역 실행**
3. **번역 결과가 영어/스페인어/프랑스어/독일어면 음성 재생**

**주의**: 한국어, 일본어, 중국어는 TTS 미지원

### 언어 바꾸기

- **⇄ 버튼 클릭**: 원본 언어와 번역 언어 교체

### 결과 복사

- **📋 복사 버튼 클릭**: 번역 결과를 클립보드에 복사

---

## 지원 언어

### 번역 (7개 언어)

| 언어 | 코드 | 번역 | TTS |
|------|------|------|-----|
| 영어 | en | ✅ | ✅ |
| 한국어 | ko | ✅ | ❌ |
| 일본어 | ja | ✅ | ❌ |
| 중국어 | zh | ✅ | ❌ |
| 스페인어 | es | ✅ | ✅ |
| 프랑스어 | fr | ✅ | ✅ |
| 독일어 | de | ✅ | ✅ |

### TTS 지원 언어
- **영어** (최고 품질)
- **스페인어**
- **프랑스어**
- **독일어**

**한국어, 일본어, 중국어는 TTS 미지원**
(Coqui TTS에 고품질 단일 언어 모델이 없음)

---

## 문제 해결

### 1. 모듈을 찾을 수 없습니다 (ModuleNotFoundError)

**원인**: 패키지가 설치되지 않았거나 가상환경이 활성화되지 않음

**해결**:
```bash
# 가상환경 활성화 확인
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

---

### 2. 첫 실행이 너무 느립니다

**원인**: NLLB 모델 다운로드 중 (정상)

**해결**: 
- 5-10분 기다리기
- 이후 실행은 빠름
- 진행 상황 확인: 터미널 출력 확인

---

### 3. 메모리 부족 에러

**원인**: RAM 부족

**해결**:
- 다른 프로그램 종료
- 최소 4GB RAM 필요
- 8GB 이상 권장

---

### 4. TTS 음성이 나오지 않습니다

**원인**: 번역 결과 언어가 TTS 미지원 언어

**확인**:
- TTS는 영어, 스페인어, 프랑스어, 독일어만 지원
- 한국어, 일본어, 중국어는 미지원

**예시**:
- ✅ "Hello" (영어) → TTS 작동
- ❌ "안녕하세요" (한국어) → TTS 미작동

---

### 5. PowerShell 스크립트 실행 에러

**에러 메시지**:
```
이 시스템에서 스크립트를 실행할 수 없으므로...
```

**해결**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 CMD 사용:
```cmd
.venv\Scripts\activate.bat
```

---

### 6. 포트 5000이 이미 사용 중

**원인**: 다른 프로그램이 포트 5000 사용 중

**해결**:
```python
# config.py 수정
SERVER_PORT = 5001  # 다른 포트로 변경
```

---

### 7. CUDA / GPU 관련 에러

**원인**: GPU가 없거나 CUDA 미설치 (무시 가능)

**해결**: 
- CPU로 실행됨 (정상)
- GPU 없어도 작동
- 속도만 약간 느림

---

## 파일 구조

```
translator_clean/
├── app.py                  # Flask 웹 서버
├── translator_nllb.py      # NLLB 번역 엔진
├── tts.py                  # Coqui TTS 음성 합성
├── config.py               # 설정 파일
├── requirements.txt        # 필요 패키지 목록
├── README.md               # 이 파일
├── README.txt              # 텍스트 버전
├── templates/
│   └── index.html         # 웹 UI
└── static/
    └── audio/             # TTS 음성 파일 저장
```

---

## 설정 변경

### config.py

```python
# 기본 설정
MAX_TEXT_LENGTH = 5000      # 최대 텍스트 길이
SERVER_PORT = 5000          # 서버 포트
DEBUG_MODE = False          # 디버그 모드

# TTS 활성화/비활성화
TTS_ENABLED = True          # False로 변경 시 TTS 사용 안함
```

### 언어 추가

**translator_nllb.py**:
```python
LANGUAGE_CODES = {
    'en': 'eng_Latn',
    'ko': 'kor_Hang',
    # ... 기존
    'ru': 'rus_Cyrl',  # 러시아어 추가
}
```

**config.py**:
```python
LANGUAGE_NAMES = {
    'en': 'English (영어)',
    'ko': '한국어',
    # ... 기존
    'ru': 'Русский (러시아어)',  # 추가
}
```

**templates/index.html**:
```html
<option value="ru">🇷🇺 Русский (러시아어)</option>
```

---

## 주의사항

### ⚠️ 첫 실행
- 모델 다운로드로 5-10분 소요
- 약 2.5GB 다운로드
- 인터넷 연결 필수

### ⚠️ TTS 제한
- 한국어, 일본어, 중국어 TTS 미지원
- 영어, 스페인어, 프랑스어, 독일어만 지원

### ⚠️ 시스템 요구사항
- 최소 4GB RAM (8GB 권장)
- 5GB 이상 저장공간
- Python 3.8-3.11

### ⚠️ 번역 품질
- 비영어 쌍 번역 (예: 한국어↔일본어) 품질 변동 가능
- 영어 경유 번역 시 더 정확할 수 있음

---

## 기술 스택

- **번역 모델**: Meta NLLB-200-distilled-600M
- **TTS 엔진**: Coqui TTS
- **웹 프레임워크**: Flask
- **딥러닝**: PyTorch, Transformers
- **언어**: Python 3.8-3.11

---

## 라이선스

오픈소스 라이브러리를 사용하여 제작되었습니다:
- NLLB-200: CC-BY-NC 4.0
- Coqui TTS: MPL 2.0
- Flask: BSD-3-Clause

---

## 문의 및 지원

문제가 발생하면:
1. [문제 해결](#문제-해결) 섹션 확인
2. 터미널 에러 메시지 확인
3. requirements.txt 재설치 시도

---

## 버전 정보

- **버전**: 1.0
- **마지막 업데이트**: 2025-11-26
- **Python**: 3.8-3.11
- **NLLB 모델**: facebook/nllb-200-distilled-600M

---
