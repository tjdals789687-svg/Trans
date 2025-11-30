# 기본 설정
MAX_TEXT_LENGTH = 5000

# 서버 설정
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG_MODE = False

# 언어 설정 (18개 언어)
LANGUAGE_NAMES = {
    'en': 'English (영어)',
    'ko': '한국어',
    'ja': '日本語 (일본어)',
    'zh': '中文 (중국어)',
    'es': 'Español (스페인어)',
    'fr': 'Français (프랑스어)',
    'de': 'Deutsch (독일어)',
    'ru': 'Русский (러시아어)',
    'ar': 'العربية (아랍어)',
    'hi': 'हिन्दी (힌디어)',
    'pt': 'Português (포르투갈어)',
    'it': 'Italiano (이탈리아어)',
    'nl': 'Nederlands (네덜란드어)',
    'pl': 'Polski (폴란드어)',
    'tr': 'Türkçe (터키어)',
    'vi': 'Tiếng Việt (베트남어)',
    'th': 'ไทย (태국어)',
    'id': 'Indonesia (인도네시아어)',
}

# TTS 설정
TTS_ENABLED = True
AUDIO_DIR = 'static/audio'

# TTS 모델 (단일 언어 모델만)
TTS_MODELS = {
    'en': 'tts_models/en/ljspeech/tacotron2-DDC',
    'es': 'tts_models/es/css10/vits',
    'fr': 'tts_models/fr/css10/vits',
    'de': 'tts_models/de/thorsten/tacotron2-DDC',
}
