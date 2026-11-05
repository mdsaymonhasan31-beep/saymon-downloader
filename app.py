from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML = """
<h1 style="text-align:center">Saymon Downloader</h1>
<form method="POST" action="/download" style="text-align:center">
<input type="text" name="url" placeholder="Paste YouTube / TikTok / FB link" style="width:80%;padding:12px" required>
<br><br>
<button type="submit" style="padding:12px 25px">Download</button>
</form>
<p style="text-align:center">YouTube / TikTok / Facebook / Instagram</p>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL! <a href='/'>Back</a>"
    filename = str(uuid.uuid4()) + ".mp4"
    filepath = f"/tmp/{filename}"
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': filepath,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'impersonate': 'chrome',
        'extractor_args': {'youtube': {'player_client': ['android', 'ios', 'web']}},
        'http_headers': {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filepath, as_attachment=True, download_name="saymon-video.mp4")
    except Exception as e:
        return f"Ei link ta download hocche na!<br><br>Error: {e}<br><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
