from flask import Flask, request, render_template_string, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML = """
<h1 style="text-align:center">Saymon Downloader</h1>
<form method="POST" action="/download" style="text-align:center">
<input type="text" name="url" placeholder="Paste link here" style="width:80%;padding:12px" required>
<br><br>
<button type="submit" style="padding:12px 30px">Download</button>
</form>
<p style="text-align:center">YouTube | TikTok | Facebook | Instagram</p>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Link dao nai!"
    
    file_id = str(uuid.uuid4())[:8]
    out_path = f"/tmp/{file_id}.mp4"

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': out_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        if not os.path.exists(out_path):
            return "Download hoyni, onno link diye try koro!"

        return send_file(out_path, as_attachment=True, download_name=f"saymon_{file_id}.mp4")
    except Exception as e:
        print("ERROR:", str(e))
        return f"<h2>Ei link ta download hocche na!</h2><p>Onno link diye try koro. TikTok diye try koro.</p><p>Error: {str(e)[:200]}</p><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
