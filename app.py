from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML = """
<h2 style="text-align:center;font-family:sans-serif">Saymon Downloader</h2>
<form method="post" action="/download" style="text-align:center">
<input name="url" placeholder="Video link paste koro" style="width:80%;padding:10px">
<br><br>
<button style="padding:10px 20px">Download</button>
</form>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "Link dao nai!"
    name = str(uuid.uuid4())[:8]
    out = f"/tmp/{name}.%(ext)s"
    opts = {"outtmpl": out, "format": "best", "quiet": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
