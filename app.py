from flask import Flask, render_template, request, jsonify
import config
import translator_nllb as translator
import tts
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Azure OpenAI 설정
api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
api_version = "2025-01-01-preview"

if api_key and endpoint and deployment:
    openai_client = OpenAI(
        api_key=api_key,
        base_url=f"{endpoint}openai/deployments/{deployment}",
        default_query={"api-version": api_version}
    )
    AI_ENABLED = True
else:
    openai_client = None
    AI_ENABLED = False
    print(" Azure OpenAI 설정이 없습니다. AI 챗봇 기능이 비활성화됩니다.")

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

@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    """AI 챗봇 엔드포인트"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': '메시지를 입력해주세요'}), 400
        
        if not AI_ENABLED:
            return jsonify({
                'response': 'AI 챗봇 기능이 비활성화되어 있습니다. .env 파일을 확인해주세요.'
            })
        
        response = generate_ai_response(message)
        return jsonify({'response': response})
    
    except Exception as e:
        import traceback
        print("=" * 60)
        print("CHATBOT ERROR:", str(e))
        print(traceback.format_exc())
        print("=" * 60)
        return jsonify({
            'response': f'죄송합니다. 오류가 발생했습니다: {str(e)}'
        }), 500

def generate_ai_response(message: str) -> str:
    try:
        system_msg = """당신은 번역기 도우미 챗봇입니다. 
        사용자의 번역, 언어 학습, 문법 체크 등에 관한 질문에 친절하게 답변해주세요.
        간단명료하게 답변하되, 도움이 되는 정보를 제공하세요.
        답변은 200자 이내로 작성해주세요."""
        
        response = openai_client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"AI 응답 생성 오류: {e}")
        return "죄송합니다. AI 응답 생성 중 오류가 발생했습니다."

if __name__ == '__main__':
    print(f"Server starting on http://localhost:{config.SERVER_PORT}")
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.DEBUG_MODE
    )
