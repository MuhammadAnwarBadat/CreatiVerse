from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file


app = Flask(__name__)


# Set your OpenAI API key here
# api_key = "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"
# api_key = "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"
api_key = os.environ.get('OPENAI_API_KEY')
# Initialize the OpenAI API

openai.api_key = api_key

# Function to generate a poem with emotions using ChatGPT API
def generate_poem(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poet."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,
    )

    poem = response['choices'][0]['message']['content']
    return poem.strip()

# @app.route("/", methods=["GET"])
# def home():
#     return render_template("landingpage.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        poem = generate_poem(prompt)


        # Save the poem as an audio file using gTTS
        tts = gTTS(text=poem, lang="en")
        # audio_file = "poem_audio.mp3"
        audio_file = os.path.join("static", "poem_audio.mp3")
        tts.save(audio_file)
        response = openai.Image.create(prompt=prompt, n=3, size="256x256")
        image_urls = [img['url'] for img in response['data']]

        return render_template("app.html", poem=poem, audio_file=audio_file, images=image_urls)

    return render_template("app.html", poem=None, audio_file=None, images=None)

@app.route("/static/<path:filename>")
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, "static"), filename)

if __name__ == "__main__":
    app.run(debug=True)
