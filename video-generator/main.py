from flask import Flask, request, send_file
import subprocess
import uuid

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    audio = request.files['audio']
    image = request.files['image']

    uid = str(uuid.uuid4())
    audio_path = f"{uid}_audio.mp3"
    image_path = f"{uid}_image.jpg"
    video_path = f"{uid}_video.mp4"

    audio.save(audio_path)
    image.save(image_path)

    subprocess.call([
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-pix_fmt', 'yuv420p',
        video_path
    ])

    return send_file(video_path, mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)