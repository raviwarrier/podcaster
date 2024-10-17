from flask import Flask, request, jsonify
import app
import os

app = Flask(__name__)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    input_type = data.get('input_type')
    text_input = data.get('text_input')
    markdown_input = data.get('markdown_input')
    url_input = data.get('url_input')
    pdf_files = data.get('pdf_files')
    openai_api_key = data.get('openai_api_key')
    text_model = data.get('text_model', 'o1-mini')
    audio_model = data.get('audio_model', 'tts-1')
    speaker_1_voice = data.get('speaker_1_voice', 'alloy')
    speaker_2_voice = data.get('speaker_2_voice', 'echo')
    audio_format = data.get('audio_format', 'mp3')
    file_name = data.get('file_name', '')
    api_base = data.get('api_base', None)
    intro_instructions = data.get('intro_instructions', '')
    text_instructions = data.get('text_instructions', '')
    scratch_pad_instructions = data.get('scratch_pad_instructions', '')
    prelude_dialog = data.get('prelude_dialog', '')
    podcast_dialog_instructions = data.get('podcast_dialog_instructions', '')
    edited_transcript = data.get('edited_transcript', None)
    user_feedback = data.get('user_feedback', None)

    try:
        audio_file, transcript, original_text, error = app.validate_and_generate_audio(
            input_type, pdf_files, text_input, markdown_input, url_input,
            openai_api_key, text_model, audio_model, 
            speaker_1_voice, speaker_2_voice, api_base,
            audio_format, file_name,
            intro_instructions, text_instructions, scratch_pad_instructions, 
            prelude_dialog, podcast_dialog_instructions, 
            edited_transcript, user_feedback
        )
        if error:
            return jsonify({'error': error}), 400
        return jsonify({'audio_file': audio_file, 'transcript': transcript, 'original_text': original_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
