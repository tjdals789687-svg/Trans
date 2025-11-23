# 🌐 다국어 번역기 v0.2 (모듈화 버전)

번역과 TTS 기능을 **별도 파일로 분리**한 모듈화 버전입니다.

## 📁 프로젝트 구조

```
translator-v0_2_modular/
├── app.py              # 🎯 메인 Flask 앱 (라우팅만)
├── translator.py       # 🌍 번역 모듈 (번역 담당자)
├── tts.py              # 🔊 TTS 모듈 (TTS 담당자)
├── config.py           # ⚙️ 공통 설정
├── requirements.txt    # 📦 의존성
├── README.md          # 📖 이 문서
├── run.sh             # 🐧 Linux/Mac 실행
├── run.bat            # 🪟 Windows 실행
├── templates/
│   └── index.html     # 🎨 프론트엔드 UI
└── static/
    └── audio/         # 🔊 TTS 오디오 저장
```

## 👥 팀 작업 분담

| 파일 | 담당 | 설명 |
|------|------|------|
| `translator.py` | 번역 담당 | 번역 로직 |
| `tts.py` | TTS 담당 | 음성 합성 로직 |
| `app.py` | 공통 | 라우팅 (수정 거의 불필요) |
| `config.py` | 공통 | 설정값 |

## 🚀 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python app.py
```

### 3. 브라우저 접속
```
http://localhost:5000
```

---

## 📦 모듈별 사용법

### translator.py (번역)

```python
import translator

# 번역 실행
result = translator.translate("Hello!", "en", "ko")

if result['success']:
    print(result['translated'])  # "안녕!"
else:
    print(result['error'])

# 캐시된 모델 확인
print(translator.get_cached_models())  # ['en-ko']
```

### tts.py (음성 합성)

```python
import tts

# TTS 사용 가능 여부 확인
if tts.is_available():
    result = tts.synthesize("Hello!", "en")
    
    if result['success']:
        print(result['audio_url'])  # '/static/audio/tts_xxx.wav'
```

---

## 🔊 TTS 팀원 작업 가이드

### 1단계: config.py 수정
```python
# config.py
TTS_ENABLED = True  # False → True로 변경
```

### 2단계: tts.py의 synthesize() 함수 구현

```python
def synthesize(text: str, language: str = 'en') -> dict:
    # 1. TTS 임포트
    from TTS.api import TTS
    
    # 2. 모델 선택
    model_name = TTS_MODELS.get(language, TTS_MODELS['en'])
    
    # 3. 모델 로드 (캐싱)
    if language not in _tts_cache:
        _tts_cache[language] = TTS(model_name=model_name, progress_bar=False)
    tts_model = _tts_cache[language]
    
    # 4. 파일 경로 생성
    filename = generate_audio_filename(text, language)
    audio_path = os.path.join(AUDIO_DIR, filename)
    
    # 5. 음성 생성
    tts_model.tts_to_file(text=text, file_path=audio_path)
    
    # 6. 결과 반환
    return {
        'success': True,
        'audio_path': f'static/audio/{filename}',
        'audio_url': f'/static/audio/{filename}',
        'error': None
    }
```

### 3단계: requirements.txt 수정
```
# TTS 주석 해제
TTS>=0.22.0
```

### 4단계: 테스트
```bash
python tts.py  # 모듈 단독 테스트
python app.py  # 전체 앱 테스트
```

---

## 🔌 API 엔드포인트

### POST /translate
번역 요청 (TTS 포함 가능)

```json
// Request
{
    "text": "Hello, world!",
    "source_lang": "en",
    "target_lang": "ko",
    "use_tts": true
}

// Response
{
    "original": "Hello, world!",
    "translated": "안녕, 세상아!",
    "source_lang": "en",
    "target_lang": "ko",
    "audio_url": "/static/audio/tts_xxx.wav"
}
```

### POST /tts
TTS 전용 요청 (번역 없이)

```json
// Request
{
    "text": "안녕하세요",
    "language": "ko"
}

// Response
{
    "audio_url": "/static/audio/tts_xxx.wav",
    "text": "안녕하세요",
    "language": "ko"
}
```

### GET /languages
지원 언어 목록

### GET /health
서버 상태

---

## ⌨️ 키보드 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl + Enter` | 번역 실행 |
| `Esc` | 전체 지우기 |

---

## 🔄 Git 협업 팁

### 충돌 방지
- 각자 담당 파일만 수정
- `app.py`는 가급적 수정 X

### 브랜치 전략
```
main
├── feature/translator  (번역 담당)
└── feature/tts         (TTS 담당)
```

### 병합 순서
1. translator 브랜치 먼저 병합
2. tts 브랜치 병합
3. 통합 테스트

---

Made with ❤️ using Hugging Face Transformers + Coqui TTS
