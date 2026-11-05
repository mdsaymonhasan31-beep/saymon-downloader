import os, re
from flask import Flask, request, jsonify, redirect
import yt_dlp

app = Flask(__name__)

HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>SAYMON DOWNLOADER</title><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:linear-gradient(180deg,#7b00ff,#ff00c8 45%,#2a00ff);min-height:100vh;color:white}
.top{display:flex;justify-content:space-between;align-items:center;padding:15px}
.logo{font-weight:900;font-size:22px} .logo span{color:#ffe600}
.hero{text-align:center;padding:20px 15px 10px}
.hero h1{font-size:38px;line-height:1.1}
.hero p{margin-top:10px;opacity:.9;font-size:14px}
.box{background:rgba(255,255,255,.95);border-radius:18px;padding:8px;display:flex;margin:20px 15px 0}
.box input{flex:1;border:none;outline:none;padding:15px;font-size:15px;background:transparent;color:#333;min-width:0}
.box button{background:white;border:1px solid #ddd;border-radius:10px;padding:0 14px;font-weight:700;color:#4a00ff;white-space:nowrap}
.btn{margin:15px;background:linear-gradient(90deg,#ff00b3,#4a00ff);border:2px solid rgba(255,255,255,.7);color:white;width:calc(100% - 30px);padding:18px;font-size:20px;font-weight:800;border-radius:14px;cursor:pointer}
.card{background:white;color:#222;margin:15px;border-radius:18px;padding:15px}
.card img{width:100%;border-radius:12px;max-height:320px;object-fit:cover}
.dl{display:block;background:#111;color:white;text-align:center;padding:15px;border-radius:10px;margin-top:10px;text-decoration:none;font-weight:700;font-size:17px}
.tip{background:#fff3cd;color:#333;margin:0 15px 15px;padding:12px;border-radius:10px;font-size:13px;text-align:center;line-height:1.5}
.apps{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:12px}
.apps span{background:rgba(255,255,255,.2);padding:6px 12px;border-radius:20px;font-size:12px}
</style></head><body>
<div class="top"><div class="logo">SAYMON<span> ⚡</span></div></div>
<div class="hero"><h1>SAYMON<br>Video Downloader</h1><p>All App Video Downloader - With Sound 🔊</p><div class="apps"><span>TikTok</span><span>YouTube</span><span>Facebook</span><span>Instagram</span><span>Twitter/X</span><span>Likee</span></div></div>
<div class="box"><input id="u" placeholder="Video link ekhane paste koro"><button onclick="paste()">📋 Paste</button></div>
<button class="btn" onclick="go()">⬇ DOWNLOAD</button>
<div id="r"></div>
<script>
async function paste(){try{let t=await navigator.clipboard.readText();document.getElementById('u').value=t;}catch(e){alert('Box er vitore chap diye dhore rakho, tarpor Paste dao');}}
async function go(){let url=document.getElementById('u').value.trim();if(!url){alert('Age link dao!');return;}
document.getElementById('r').innerHTML='<div class="card">⏳ Loading... Video khujtesi, ektu wait koro...</div>';
try{
let res=await fetch('/info?url='+encodeURIComponent(url));let d=await res.json();
if(d.error){document.getElementById('r').innerHTML='<div class="card">❌ '+d.error+'</div>';return;}
let h='<div class="card"><img src="'+(d.thumb||'')+'"><h3 style="margin:10px 0">'+d.title+'</h3><p style="font-size:13px;color:#666">'+d.uploader+'</p>';
d.formats.forEach(f=>{h+='<a class="dl" href="/dl?url='+encodeURIComponent(f.url)+'" download target="_blank">⬇ '+f.label+' 🔊</a>'});h+='</div>';
h+='<div class="tip">✅ Download na hole: Button e <b>chap diye dhore rakho</b> -> <b>Download link</b> e chap dao.<br>Facebook er Private / Login kora video nambe na.</div>';
document.getElementById('r').innerHTML=h;
}catch(e){document.getElementById('r').innerHTML='<div class="card">❌ Net e problem, abar try koro</div>';}}
</script></body></html>"""

@app.route("/")
def home():
    return HTML

@app.route("/info")
def info():
    url = request.args.get("url","").strip()
    if not url:
        return jsonify({"error":"Age link dao!"})

    # vm.tiktok.com er moto choto link holeo cholbe
    if not url.startswith("http"):
        url = "https://" + url

    opts = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        "no_warnings": True,
        "socket_timeout": 30,
        "retries": 3,
        "fragment_retries": 3,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
        "extractor_args": {
            "tiktok": {"api_hostname": "api16-normal-c-useast1a.tiktokv.com"},
            "youtube": {"player_client": ["android", "web"]},
            "facebook": {"api_hostname": "graph.facebook.com"},
        },
        # Shudhu Sound + Video eksathe thaka format
        "format": "best[acodec!=none][vcodec!=none]/best",
    }

    try:
        with yt_dlp.YoutubeDL(opts) as y:
            d = y.extract_info(url, download=False)

        if not d:
            return jsonify({"error":"Video pawa jay nai, link ta thik ache kina dekho"})

        formats = []
        for f in d.get("formats", []) or []:
            if not f.get("url"):
                continue
            if f.get("acodec") in (None, "none"):
                continue
            if f.get("vcodec") in (None, "none"):
                continue
            h = f.get("height") or 0
            if h == 0:
                continue
            ext = f.get("ext","mp4")
            formats.append({"label": f"{h}p HD - {ext.upper()}","url": f["url"],"h": h})

        # Jodi alada alada format na pai, main url tai dao
        if not formats and d.get("url"):
            formats = [{"label":"Best Quality","url": d.get("url"), "h": 720}]

        if not formats:
            return jsonify({"error":"Ei video ta Protected / Private. Onno ekta Public video diye try koro."})

        # Duplicate sorano + sort
        seen = set()
        clean = []
        for x in sorted(formats, key=lambda x: x["h"]):
            if x["h"] not in seen:
                seen.add(x["h"])
                clean.append({"label": x["label"], "url": x["url"]})
        # Sesher 3 ta sera quality
        clean = clean[-3:]

        return jsonify({
            "title": d.get("title","Video")[:80],
            "thumb": d.get("thumbnail",""),
            "uploader": d.get("uploader") or d.get("channel") or "",
            "formats": clean
        })
    except Exception as e:
        msg = str(e)
        # User friendly error
        if "Private" in msg or "Login" in msg or "login" in msg:
            return jsonify({"error":"Ei video ta Private / Login lage. Public video diye try koro."})
        if "Unsupported" in msg:
            return jsonify({"error":"Ei App er link support kore na. TikTok / YouTube / FB / Instagram link dao."})
        return jsonify({"error":"Server ektu busy, 30 sec por abar DOWNLOAD e chap dao."})

@app.route("/dl")
def dl():
    return redirect(request.args.get("url",""))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
