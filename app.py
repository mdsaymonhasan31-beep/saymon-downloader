import os
from flask import Flask, request, jsonify
import yt_dlp
app = Flask(__name__)

@app.route("/")
def home():
 return """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>SAYMON DOWNLOADER</title><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:linear-gradient(180deg,#7b00ff,#ff00c8 45%,#2a00ff);min-height:100vh;color:white}
.top{display:flex;justify-content:space-between;align-items:center;padding:15px}
.logo{font-weight:900;font-size:22px;letter-spacing:1px} .logo span{color:#ffe600}
.menu{font-size:28px}
.hero{text-align:center;padding:20px 15px 10px}
.hero h1{font-size:38px;line-height:1.1;text-shadow:0 5px 20px rgba(0,0,0,.3)}
.hero p{margin-top:10px;opacity:.9;font-size:14px}
.box{background:rgba(255,255,255,.92);border-radius:18px;padding:8px;display:flex;margin:20px 15px 0;box-shadow:0 15px 40px rgba(0,0,0,.3)}
.box input{flex:1;border:none;outline:none;padding:15px;font-size:16px;background:transparent;color:#333}
.box button{background:white;border:1px solid #ddd;border-radius:10px;padding:0 14px;font-weight:700;color:#4a00ff}
.btn{margin:15px;background:linear-gradient(90deg,#ff00b3,#4a00ff);border:2px solid rgba(255,255,255,.7);color:white;width:calc(100% - 30px);padding:18px;font-size:20px;font-weight:800;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.3)}
.card{background:white;color:#222;margin:15px;border-radius:18px;padding:15px}
.card img{width:100%;border-radius:12px}
.dl{display:block;background:#111;color:white;text-align:center;padding:13px;border-radius:10px;margin-top:10px;text-decoration:none;font-weight:700}
.badge{display:flex;gap:8px;justify-content:center;margin:20px 15px}
.badge div{background:rgba(255,255,255,.2);padding:8px 12px;border-radius:20px;font-size:12px}
</style></head><body>
<div class="top"><div class="logo">SAYMON<span> ⚡</span></div><div class="menu">☰</div></div>
<div class="hero"><h1>SAYMON<br>Video Downloader</h1><p>TikTok • YouTube • Facebook • Instagram - No Watermark</p></div>
<div class="box"><input id="u" placeholder="Insert a link here"><button onclick="paste()">📋 Paste</button></div>
<button class="btn" onclick="go()">⬇ DOWNLOAD</button>
<div class="badge"><div>⚡ Super Fast</div><div>💎 HD Quality</div><div>🔓 100% Free</div></div>
<div id="r"></div>
<script>
async function paste(){try{let t=await navigator.clipboard.readText();document.getElementById('u').value=t;}catch(e){}}
async function go(){let url=document.getElementById('u').value;if(!url){alert('Link dao age!');return;}
document.getElementById('r').innerHTML='<div class="card">⏳ Loading... Gorgeous Video Antechhi...</div>';
let res=await fetch('/info?url='+encodeURIComponent(url));let d=await res.json();
if(d.error){document.getElementById('r').innerHTML='<div class="card">❌ '+d.error+'</div>';return;}
let h='<div class="card"><img src="'+(d.thumb||'')+'"><h3 style="margin:10px 0">'+d.title+'</h3>';
d.formats.forEach(f=>{h+='<a class="dl" href="'+f.url+'" target="_blank">⬇ '+f.label+'</a>'});h+='</div>';
document.getElementById('r').innerHTML=h;}
</script></body></html>"""

@app.route("/info")
def info():
 url=request.args.get("url","")
 if not url: return jsonify({"error":"Link dao"})
 try:
  o={"quiet":True,"noplaylist":True,"skip_download":True}
  with yt_dlp.YoutubeDL(o) as y:
   d=y.extract_info(url,download=False)
  f2=[]
  for f in d.get("formats",[]):
   if f.get("url") and f.get("height"):
    f2.append({"label":str(f.get("height"))+"p HD - Download","url":f["url"]})
  return jsonify({"title":d.get("title","Video"),"thumb":d.get("thumbnail",""),"formats":f2[-4:]})
 except Exception as e:
  return jsonify({"error":str(e)})

if __name__=="__main__":
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
