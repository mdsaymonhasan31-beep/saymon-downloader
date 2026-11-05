import os, random
from flask import Flask, request, jsonify, render_template_string
import yt_dlp
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Saymon Video Downloader Server - Best & Free</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',sans-serif}
body{background:linear-gradient(135deg,#4a00ff,#ff00a8,#0066ff,#00e5ff,#ff00a8);background-size:400% 400%;animation:g 8s ease infinite;min-height:100vh;color:white}
@keyframes g{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.top{display:flex;justify-content:space-between;align-items:center;padding:13px 16px;background:white;box-shadow:0 4px 20px rgba(0,0,0,.2)}
.logo{font-size:26px;font-weight:900;color:#4a00ff;letter-spacing:.5px}.logo span{color:#ff00a8}
.install{background:linear-gradient(90deg,#b44bff,#ff00a8);color:white;padding:10px 18px;border-radius:12px;font-weight:800;border:none;box-shadow:0 4px 15px rgba(255,0,168,.4)}
.live{background:#ff0033;color:white;font-size:12px;padding:6px 14px;border-radius:20px;font-weight:800;display:inline-block;margin-top:12px;animation:blink 1.2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.6}}
.hero{text-align:center;padding:22px 16px 5px}.hero h1{font-size:39px;line-height:1.05;font-weight:900;text-shadow:0 5px 25px rgba(0,0,0,.35)}
.hero p{margin-top:10px;font-size:14px;opacity:.95}
.card{background:rgba(255,255,255,.97);border-radius:24px;padding:18px;margin:16px 14px;box-shadow:0 25px 50px rgba(0,0,0,.35);border:2px solid rgba(255,255,255,.8)}
.plat{display:inline-block;background:#f1f1ff;color:#4a00ff;padding:7px 13px;border-radius:20px;font-size:13px;font-weight:700;margin:3px;border:1px solid #ddd}
.plat.active{background:#4a00ff;color:white}
.input-box{display:flex;background:#e8e8f5;border-radius:14px;padding:6px;margin-top:10px}
.input-box input{flex:1;border:none;background:transparent;padding:13px;font-size:16px;outline:none;color:#333}
.paste{background:white;color:#4a00ff;border:none;padding:8px 14px;border-radius:10px;font-weight:800}
.download-btn{width:100%;margin-top:13px;background:linear-gradient(90deg,#ff00a8,#4a00ff,#0066ff);background-size:200% 100%;color:white;border:none;padding:17px;border-radius:14px;font-size:20px;font-weight:900;box-shadow:0 10px 25px rgba(255,0,168,.45)}
.download-btn:active{transform:scale(.98)}
.result{margin-top:14px;color:#222;text-align:left}.result img{width:100%;border-radius:14px}
.result a{display:block;background:linear-gradient(90deg,#111,#333);color:white;text-align:center;padding:13px;border-radius:11px;margin-top:8px;text-decoration:none;font-weight:700}
.features{display:grid;grid-template-columns
