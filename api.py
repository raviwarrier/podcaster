from flask import Flask, request, jsonify, render_template_string
import app
import os

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Podcaster</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        h1 { color: #333; }
        form { margin-bottom: 20px; }
        input, textarea, select { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h1>Podcaster</h1>
    <form id="audioForm">
        <input type="text" name="url_input" placeholder="Enter URL" required>
        <textarea name="text_input" placeholder="Or enter text here"></textarea>
        <input type="text" name="openai_api_key" placeholder="OpenAI API Key" required>
        <select name="text_model">
            <option value="o1-mini">o1-mini</option>
            <option value="gpt-4-turbo">gpt-4-turbo</option>
        </select>
        <button type="submit">Generate Audio</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('audioForm').onsubmit = function(e) {
            e.preventDefault();
            var formData = new FormData(this);
            var jsonData = {};
            formData.forEach((value, key) => {jsonData[key] = value});
            
            fetch('/generate-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('result').innerHTML = 'Error: ' + data.error;
                } else {
                    document.getElementById('result').innerHTML = 'Audio generated successfully. Transcript: ' + data.transcript;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('result').innerHTML = 'An error occurred.';
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    input_type = data.get('url_input') and 'URL' or 'Text'
    text_input = data.get('text_input')
    url_input = data.get('url_input')
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
            input_type, None, text_input, None, url_input,
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
