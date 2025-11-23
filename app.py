# app.py
# 메인 Flask 애플리케이션
# 라우팅만 담당, 실제 로직은 각 모듈에서 처리

from flask import Flask, render_template, request, jsonify
import config
import translator
import tts

app = Flask(__name__)

# ============================================
# 페이지 라우트
# ============================================

@app.route('/')
def home():
    """메인 페이지"""
    return render_template('index.html')


# ============================================
# API 엔드포인트
# ============================================

@app.route('/translate', methods=['POST'])
def translate_api():
    """
    번역 API
    
    Request Body:
        - text: 번역할 텍스트
        - source_lang: 원본 언어 코드 (기본값: 'en')
        - target_lang: 대상 언어 코드 (기본값: 'ko')
        - use_tts: TTS 사용 여부 (기본값: False)
    """
    data = request.json
    
    # 파라미터 추출
    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'ko')
    use_tts = data.get('use_tts', False)
    
    # 빈 텍스트 체크
    if not text:
        return jsonify({'error': '텍스트를 입력해주세요!'}), 400
    
    # 글자 수 제한 체크
    if len(text) > config.MAX_TEXT_LENGTH:
        return jsonify({
            'error': f'텍스트가 너무 깁니다. (최대 {config.MAX_TEXT_LENGTH}자)'
        }), 400
    
    # 언어 쌍 유효성 체크
    lang_pair = f"{source_lang}-{target_lang}"
    if lang_pair not in config.SUPPORTED_LANGUAGE_PAIRS:
        return jsonify({
            'error': f'지원하지 않는 언어 쌍입니다: {lang_pair}',
            'supported': list(config.SUPPORTED_LANGUAGE_PAIRS.keys())
        }), 400
    
    # ========== 번역 수행 (translator 모듈 사용) ==========
    translate_result = translator.translate(text, source_lang, target_lang)
    
    if not translate_result['success']:
        return jsonify({'error': translate_result['error']}), 500
    
    # 응답 구성
    response = {
        'original': text,
        'translated': translate_result['translated'],
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    
    # ========== TTS 처리 (tts 모듈 사용) ==========
    if use_tts:
        tts_result = tts.synthesize(translate_result['translated'], target_lang)
        
        if tts_result['success']:
            response['audio_url'] = tts_result['audio_url']
        else:
            # TTS 실패해도 번역 결과는 반환
            response['tts_error'] = tts_result['error']
    
    return jsonify(response)


@app.route('/tts', methods=['POST'])
def tts_api():
    """
    TTS 전용 API (번역 없이 TTS만 사용할 때)
    
    Request Body:
        - text: 음성으로 변환할 텍스트
        - language: 언어 코드 (기본값: 'en')
    """
    data = request.json
    
    text = data.get('text', '').strip()
    language = data.get('language', 'en')
    
    if not text:
        return jsonify({'error': '텍스트를 입력해주세요!'}), 400
    
    # TTS 수행
    result = tts.synthesize(text, language)
    
    if result['success']:
        return jsonify({
            'audio_url': result['audio_url'],
            'text': text,
            'language': language
        })
    else:
        return jsonify({'error': result['error']}), 500


@app.route('/languages', methods=['GET'])
def get_languages():
    """사용 가능한 언어 목록"""
    return jsonify({
        'languages': config.LANGUAGE_NAMES,
        'pairs': config.SUPPORTED_LANGUAGE_PAIRS,
        'tts_languages': tts.get_supported_languages()
    })


@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 체크"""
    return jsonify({
        'status': 'ok',
        'version': '0.2-modular',
        'tts_enabled': tts.is_available(),
        'cached_translation_models': translator.get_cached_models(),
        'cached_tts_models': tts.get_cached_models()
    })


# ============================================
# 서버 실행
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🌐 번역기 v0.2 - 모듈화 버전")
    print("=" * 50)
    print(f"📋 지원 언어 쌍: {len(config.SUPPORTED_LANGUAGE_PAIRS)}개")
    print(f"🔊 TTS 활성화: {tts.is_available()}")
    print("=" * 50)
    print("\n📁 모듈 구조:")
    print("   ├── app.py        (라우팅)")
    print("   ├── translator.py (번역)")
    print("   ├── tts.py        (음성 합성)")
    print("   └── config.py     (설정)")
    print("=" * 50)
    print("\n🚀 서버를 시작합니다!")
    print(f"👉 http://localhost:{config.SERVER_PORT}")
    print("")
    
    app.run(
        debug=config.DEBUG_MODE,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT
    )
