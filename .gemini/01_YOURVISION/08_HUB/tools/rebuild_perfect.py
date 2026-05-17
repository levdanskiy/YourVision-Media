import json
import re
import os

HUB_DIR = "/home/levdanskiy/.gemini/01_YOURVISION/08_HUB"

# 1. LOAD DATA
with open(os.path.join(HUB_DIR, "data.js"), "r", encoding="utf-8") as f:
    data_content = f.read()
    data_match = re.search(r"var DATA = ({.*});", data_content, re.DOTALL)
    data_obj = json.loads(data_match.group(1), strict=False)

# 2. DEFINE THE PERFECT TITAN PLATINUM TEMPLATE (NO F-STRINGS)
html = r"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>YourVision | Vienna 2026 Insider Hub</title>
    <style>
        /* LOCAL FONTS FACE */
        @font-face { font-family: "Uni Sans Heavy"; src: url("assets/fonts/UniSansHeavy.woff2") format("woff2"); font-weight: 900; }
        @font-face { font-family: "Avenir Next"; src: url("assets/fonts/AvenirNext-Regular.ttf") format("truetype"); font-weight: 400; }
        @font-face { font-family: "Forum Local"; src: url("assets/fonts/Forum-Regular.ttf") format("truetype"); font-weight: 400; }

        :root {
            --bg: #05010d; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08);
            --pink: #ff007f; --cyan: #00f5ff; --acid: #ccff00; --text: #e0e0e0;
        }
        body { 
            background: var(--bg); color: var(--text); font-family: "Avenir Next", sans-serif; margin: 0; padding: 40px; 
            background-image: radial-gradient(circle at 50% 0%, #1a052e 0%, var(--bg) 70%);
            background-attachment: fixed; letter-spacing: -0.01em;
        }
        .logo { font-family: "Uni Sans Heavy", sans-serif; font-size: 2.5rem; text-transform: uppercase; color: #fff; margin-bottom: 60px; line-height: 1; }
        .logo span { color: var(--pink); text-shadow: 0 0 30px var(--pink); }
        
        .layout { display: grid; grid-template-columns: 380px 1fr 420px; gap: 40px; align-items: start; }
        .column { display: flex; flex-direction: column; gap: 30px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 30px; padding: 30px; backdrop-filter: blur(20px); position: relative; }
        
        /* MAGAZINE NEWS STYLE */
        .post-card { padding: 50px; margin-bottom: 50px; border-radius: 40px; border: 1px solid var(--border); transition: 0.5s; overflow: hidden; background: rgba(255,255,255,0.01); }
        .post-card:hover { border-color: var(--pink); background: rgba(255,255,255,0.03); transform: scale(1.01); }
        .post-h { font-family: "Uni Sans Heavy", sans-serif; font-size: 2.8rem; font-weight: 900; line-height: 0.95; margin-bottom: 30px; text-transform: uppercase; letter-spacing: -0.04em; color: #fff; }
        .post-media { width: 320px; float: left; margin: 0 40px 20px 0; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1); }
        .post-b { font-size: 1.15rem; line-height: 1.8; color: #ccc; }
        .post-b strong { color: var(--pink); font-weight: 900; }
        .post-meta { font-size: 0.75rem; color: var(--cyan); font-weight: 900; text-transform: uppercase; margin-bottom: 15px; display: block; letter-spacing: 0.1em; }
        .post-sub-h { font-family: "Forum Local", serif; display: block; color: var(--acid); font-size: 1.3rem; margin: 30px 0 15px 0; }

        /* HEARTS & BUBBLES */
        .heart-shape { clip-path: url(#h-mask); -webkit-clip-path: url(#h-mask); width: 40px; height: 40px; object-fit: cover; background: #fff; display: inline-block; vertical-align: middle; }
        .bubble { display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.03); padding: 12px 20px; border-radius: 50px; border: 1px solid var(--border); margin-bottom: 12px; }
        .artist-label { font-family: "Uni Sans Heavy", sans-serif; font-weight: 900; text-transform: uppercase; background: linear-gradient(to bottom, #fff 30%, var(--pink) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.1rem; display: block; line-height: 1.1; }
        .song-label { font-family: "Avenir Next", sans-serif; color: var(--cyan); font-size: 0.85rem; opacity: 0.8; font-style: italic; }
        
        .winner-glow { border: 2px solid var(--pink) !important; box-shadow: 0 0 25px var(--pink) !important; background: rgba(255,0,127,0.08) !important; border-radius: 15px !important; }
        .status-live { border: 2px solid var(--pink) !important; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; border-color: var(--pink); } 50% { opacity: 0.7; border-color: #fff; } }
        
        .chart-table { width: 100%; border-collapse: collapse; }
        .chart-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
        .chart-cell { padding: 15px 0; }
        .rank { color: var(--pink); font-family: "Uni Sans Heavy", sans-serif; font-weight: 900; width: 40px; font-size: 1.2rem; }
    </style>
</head>
<body>
    <svg width="0" height="0" style="position:absolute;"><defs><clipPath id="h-mask" clipPathUnits="objectBoundingBox"><path d="M0.5,0.16 C0.41,-0.05,0.1,-0.05,0.02,0.21 C-0.08,0.55,0.18,0.85,0.5,1 C0.82,0.85,1.08,0.55,0.98,0.21 C0.9,-0.05,0.59,-0.05,0.5,0.16"></path></clipPath></defs></svg>
    
    <div class="logo">Your<span>Vision</span><br><small style="font-size:0.7rem; color:var(--cyan); letter-spacing:0.5em;">Insider Hub</small></div>
    
    <div class="layout">
        <aside class="column">
            <div class="card">
                <div style="color:var(--pink); font-family:Uni Sans Heavy; font-weight:900; margin-bottom:25px; font-size:1.2rem; border-left:4px solid var(--pink); padding-left:15px;">QUALIFIED</div>
                <div id="q-list"></div>
                <div style="color:#ff4d4d; font-family:Uni Sans Heavy; font-weight:900; margin:40px 0 20px 0; font-size:1.2rem; border-left:4px solid #ff4d4d; padding-left:15px;">ELIMINATED</div>
                <div id="e-list"></div>
            </div>
            <div class="card">
                <div style="color:var(--cyan); font-family:Uni Sans Heavy; font-weight:900; margin-bottom:20px; border-left:4px solid var(--cyan); padding-left:15px;">RECENTLY PLAYED</div>
                <div id="hist-list"></div>
            </div>
        </aside>
        
        <main id="news-grid"></main>
        
        <aside class="column">
            <div class="card">
                <div style="color:var(--cyan); font-family:Uni Sans Heavy; font-weight:900; text-align:center; margin-bottom:30px; font-size:1.2rem; border-bottom:2px solid var(--cyan); padding-bottom:10px;">PLAY-OFF BRACKET</div>
                <div id="bracket"></div>
            </div>
            <div class="card">
                <div style="color:var(--pink); font-family:Uni Sans Heavy; font-weight:900; text-align:center; margin-bottom:25px; border-bottom:2px solid var(--pink); padding-bottom:10px;">EUROGROOVE TOP 24</div>
                <table class="chart-table" id="chart-list"></table>
            </div>
        </aside>
    </div>

    <script>
        const DATA = __DATA__;
        const getH = (id) => id === "70" ? "https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp" : `https://www.eurovision.com/static/images/flags/flag_${id.toLowerCase()}.svg`;
        const decodeS = (s) => { try { return JSON.parse('"' + s.replace(/"/g, '\\"') + '"'); } catch(e) { return s; } };
        const flagMap = {"🇦🇱":"al","🇦🇲":"am","🇦🇺":"au","🇦🇹":"at","🇦🇿":"az","🇧🇪":"be","🇧🇬":"bg","🇭🇷":"hr","🇨🇾":"cy","🇨🇿":"cz","🇩🇰":"dk","🇪🇪":"ee","🇫🇮":"fi","🇫🇷":"fr","🇬🇪":"ge","🇩🇪":"de","🇬🇷":"gr","🇮🇱":"il","🇮🇹":"it","🇱🇻":"lv","🇱🇹":"lt","🇱🇺":"lu","🇲🇹":"mt","🇲🇩":"md","🇲🇪":"me","🇳🇴":"no","🇵🇱":"pl","🇵🇹":"pt","🇷🇴":"ro","🇸🇲":"sm","🇷🇸":"rs","🇸🇪":"se","🇨🇭":"ch","🇺🇦":"ua","🇬🇧":"gb","🇰🇭":"kh","🇻🇳":"vn","🇹🇭":"th","🇲🇾":"my","🇵🇭":"ph","🇳🇵":"np","🇧🇩":"bd","🇱🇦":"la","🇧🇹":"bt"};

        function replaceFlags(text) {
            if (!text) return "";
            let res = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
            res = res.replace(/^([A-ZА-ЯЁ\s\(\)]{5,})$/gm, "<span class='post-sub-h'>$1</span>");
            for (const f in flagMap) {
                if (res.includes(f)) {
                    res = res.split(f).join(`<img src="${getH(flagMap[f])}" class="heart-shape" style="width:30px; height:30px; vertical-align:middle; margin-right:10px;">`);
                }
            }
            return res;
        }

        function render() {
            document.getElementById("q-list").innerHTML = DATA.qualifiers.map(c => `
                <div class="bubble">
                    <img src="${getH(c.id)}" class="heart-shape" style="width:25px; height:25px;">
                    <div><span class="artist-label" style="font-size:0.85rem;">${decodeS(c.a)}</span></div>
                </div>`).join("");

            document.getElementById("e-list").innerHTML = DATA.eliminated.map(c => `
                <div class="bubble" style="opacity:0.5;">
                    <img src="${getH(c.id)}" class="heart-shape" style="width:25px; height:25px;">
                    <div><span class="artist-label" style="font-size:0.85rem; background:none; -webkit-text-fill-color:#888;">${decodeS(c.a)}</span></div>
                </div>`).join("");

            document.getElementById("bracket").innerHTML = DATA.battles.map(b => `
                <div class="card ${b.status==='LIVE'?'status-live':''}" style="margin-bottom:20px; padding:20px; background:rgba(255,255,255,0.01);">
                    <div style="font-size:0.55rem; color:#777; margin-bottom:12px; font-weight:900; text-transform:uppercase;">${b.n}</div>
                    <div class="battle-team ${b.w===1?'winner-glow':''}" style="display:flex; align-items:center; gap:12px; padding:8px;">
                        <img src="${getH(b.t1)}" class="heart-shape" style="width:35px; height:35px;">
                        <div><span class="artist-label" style="font-size:0.95rem;">${decodeS(b.a1)}</span><span class="song-label">${decodeS(b.s1||'')}</span></div>
                        <span style="margin-left:auto; font-weight:900; color:var(--pink); font-family:'Uni Sans Heavy';">${b.sc1}</span>
                    </div>
                    <div class="battle-team ${b.w===2?'winner-glow':''}" style="display:flex; align-items:center; gap:12px; padding:8px; margin-top:8px;">
                        <img src="${getH(b.t2)}" class="heart-shape" style="width:35px; height:35px;">
                        <div><span class="artist-label" style="font-size:0.95rem;">${decodeS(b.a2)}</span><span class="song-label">${decodeS(b.s2||'')}</span></div>
                        <span style="margin-left:auto; font-weight:900; color:var(--pink); font-family:'Uni Sans Heavy';">${b.sc2}</span>
                    </div>
                </div>`).join("");

            document.getElementById("chart-list").innerHTML = DATA.chart.map(i => `
                <tr class="chart-row">
                    <td class="rank">${i.r}</td>
                    <td class="chart-cell"><img src="${i.img}" class="heart-shape" style="width:40px; height:40px;"></td>
                    <td class="chart-cell">
                        <span class="artist-label" style="font-size:0.9rem;">${decodeS(i.a)}</span>
                        <span class="song-label">${decodeS(i.s)}</span>
                    </td>
                </tr>`).join("");

            document.getElementById("news-grid").innerHTML = DATA.news.map(p => {
                let media = p.isVideo ? `<video src="${p.vid}" autoplay loop muted playsinline controls class="post-media"></video>` : (p.img ? `<img src="${p.img}" class="post-media">` : "");
                return `<div class="post-card">
                    <span class="post-meta">${p.m} | YOURVISION</span>
                    <div class="post-h">${replaceFlags(p.t.replace(/\*/g, ""))}</div>
                    <div style="overflow:hidden;">${media}<div class="post-b">${replaceFlags(p.b.replace(/\n/g, "<br>"))}</div></div>
                </div>`;
            }).join("");
        }

        async function syncRadio() {
            try {
                const r = await fetch("https://myradio24.com/users/levdanskiy/status.json?apikey=e81720544fe8cf709a784a5cf1e4a89c&v=" + Date.now());
                const d = await r.json();
                document.getElementById("hist-list").innerHTML = d.songs.slice().reverse().slice(0,10).map(h => {
                    const parts = decodeS(h.song).split(" - ");
                    return `<div style="display:flex; align-items:center; gap:12px; margin-bottom:15px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.05);">
                        <span style="color:var(--cyan); font-size:0.65rem; font-weight:900; font-family:'Uni Sans Heavy';">${h.time}</span>
                        <img src="${h.img ? "https://myradio24.com/" + h.img : "https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp"}" class="heart-shape" style="width:32px; height:32px;">
                        <div><span class="artist-label" style="font-size:0.85rem;">${parts[0]}</span><span class="song-label" style="font-size:0.75rem;">${parts[1]||'...'}</span></div>
                    </div>`;
                }).join("");
            } catch(e) {}
        }

        window.onload = () => { render(); syncRadio(); };
        setInterval(syncRadio, 15000);
    </script>
</body>
</html>"""

# 3. GENERATE FINAL FILE (SAFE REPLACE)
final_html = html.replace("__DATA__", json.dumps(data_obj, ensure_ascii=False))

with open(os.path.join(HUB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(final_html)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
