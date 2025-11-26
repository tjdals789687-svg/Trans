from flask import Flask, render_template, request, jsonify
import config
import translator_nllb as translator
import tts

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_api():
    try:
        data = request.json
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'ko')
        use_tts = data.get('use_tts', False)
        
        if not text:
            return jsonify({'error': '텍스트를 입력해주세요'}), 400
        
        if len(text) > config.MAX_TEXT_LENGTH:
            return jsonify({'error': f'텍스트가 너무 깁니다 (최대 {config.MAX_TEXT_LENGTH}자)'}), 400
        
        if source_lang == target_lang:
            return jsonify({'error': '원본 언어와 번역 언어가 같습니다'}), 400
        
        supported_langs = translator.get_supported_languages()
        if source_lang not in supported_langs or target_lang not in supported_langs:
            return jsonify({'error': '지원하지 않는 언어입니다'}), 400
        
        translate_result = translator.translate(text, source_lang, target_lang)
        
        if not translate_result['success']:
            return jsonify({'error': translate_result['error']}), 500
        
        response = {
            'original': text,
            'translated': translate_result['translated'],
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        
        if use_tts:
            tts_result = tts.synthesize(translate_result['translated'], target_lang)
            if tts_result['success']:
                response['audio_url'] = tts_result['audio_url']
            else:
                response['tts_error'] = tts_result['error']
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        print("=" * 60)
        print("ERROR:", str(e))
        print(traceback.format_exc())
        print("=" * 60)
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
    return jsonify({
        'languages': config.LANGUAGE_NAMES,
        'tts_available': tts.is_available()
    })

if __name__ == '__main__':
    print(f"Server starting on http://localhost:{config.SERVER_PORT}")
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.DEBUG_MODE
    )
