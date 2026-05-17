import json, re, os

HUB_DIR = "/home/levdanskiy/.gemini/01_YOURVISION/08_HUB"

# Читаем текущие данные один раз для генерации хэша кэша
with open(os.path.join(HUB_DIR, "data.js"), "r", encoding="utf-8") as f:
    content = f.read()
    data_json = re.search(r"var DATA = ({.*});", content, re.DOTALL).group(1)
    data_obj = json.loads(data_json, strict=False)

html = r"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>YourVision | Vienna 2026 Insider Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Inter+Tight:ital,wght@0,900;1,900&family=Forum&display=swap" rel="stylesheet">
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.1.0/uicons-regular-rounded/css/uicons-regular-rounded.css'>
    <style>
        :root {
            --bg: #05010d; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08);
            --pink: #ff007f; --cyan: #00f5ff; --acid: #ccff00; --text: #e0e0e0;
        }
        body { 
            background: var(--bg); color: var(--text); font-family: "Inter", sans-serif; margin: 0; padding: 40px; 
            background-image: radial-gradient(circle at 50% 0%, #1a052e 0%, var(--bg) 70%);
            background-attachment: fixed; letter-spacing: -0.02em;
        }
        .logo-box { margin-bottom: 40px; }
        .logo { font-family: "Inter Tight", sans-serif; font-size: 2.2rem; text-transform: uppercase; color: #fff; font-weight: 900; line-height: 0.9; font-style: italic; }
        .logo span { color: var(--pink); text-shadow: 0 0 20px var(--pink); }
        
        .timers-hero { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 60px; }
        .timer-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; overflow: hidden; display: flex; backdrop-filter: blur(25px); flex-direction: column; transition: 0.5s; }
        .timer-card:hover { border-color: var(--pink); transform: translateY(-10px); }
        .timer-poster { width: 100%; aspect-ratio: 16/9; background-size: cover; background-position: center; border-bottom: 1px solid var(--border); filter: brightness(0.6); }
        .timer-info { padding: 25px; background: rgba(0,0,0,0.5); }
        .timer-val { font-family: "Inter Tight", sans-serif; font-size: 2.8rem; font-weight: 900; color: var(--pink); text-shadow: 0 0 30px rgba(255,0,127,0.6); line-height: 1; font-style: italic; }
        .timer-label { font-size: 0.9rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.2em; color: var(--cyan); opacity: 0.9; margin-bottom: 5px; display: block; font-style: italic; }

        .layout { display: grid; grid-template-columns: 380px 1fr 420px; gap: 40px; align-items: start; }
        .column { display: flex; flex-direction: column; gap: 30px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 25px; padding: 30px; backdrop-filter: blur(20px); position: relative; }
        
        .section-title-base { font-family: "Inter Tight", sans-serif; font-weight: 900; font-style: italic; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 30px; display: block; width: 100%; }
        .title-pink { color: var(--pink); text-shadow: 0 0 20px rgba(255,0,127,0.4); border-bottom: 2px solid var(--pink); padding-bottom: 10px; text-align: center; font-size: 1.6rem; }
        .title-cyan { color: var(--cyan); text-shadow: 0 0 20px rgba(0,245,255,0.4); border-bottom: 2px solid var(--cyan); padding-bottom: 10px; text-align: center; font-size: 1.6rem; }
        .title-acid { color: var(--acid); text-shadow: 0 0 20px rgba(204,255,0,0.4); border-bottom: 2px solid var(--acid); padding-bottom: 10px; text-align: center; font-size: 1.6rem; }
        
        .side-label { font-family: "Inter Tight", sans-serif; font-weight: 900; font-style: italic; font-size: 1rem; letter-spacing: 0.15em; margin-bottom: 20px; display: block; }
        .heart-shape { clip-path: url(#official-h-mask) !important; -webkit-clip-path: url(#official-h-mask) !important; width: 45px; height: 45px; object-fit: cover; background: #fff; display: inline-block; vertical-align: middle; }
        .winner-glow { border: 2px solid var(--pink) !important; box-shadow: 0 0 25px var(--pink) !important; background: rgba(255,0,127,0.1) !important; border-radius: 15px !important; padding: 12px !important; margin: -2px 0 !important; }
        .artist-rich { font-family: "Inter Tight", sans-serif; font-weight: 900; text-transform: uppercase; color: #fff; font-size: 1rem; display: block; line-height: 1.1; }
        .song-rich { font-family: "Inter", sans-serif; color: var(--cyan); font-size: 0.8rem; opacity: 0.8; text-transform: uppercase; font-weight: 900; }
        
        .post-card { padding: 65px; margin-bottom: 60px; border-radius: 50px; border: 1px solid var(--border); background: rgba(255,255,255,0.015); backdrop-filter: blur(30px); overflow: hidden; transition: 0.6s; position: relative; }
        .post-h { font-family: "Inter Tight", sans-serif; font-size: 3.2rem; font-weight: 900; line-height: 0.9; text-transform: uppercase; margin-bottom: 35px; background: linear-gradient(to bottom, #fff 40%, var(--pink) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; }
        .post-media { width: 340px; float: left; margin: 0 45px 25px 0; border-radius: 25px; box-shadow: 0 40px 80px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1); }
        .post-b { font-size: 1.25rem; line-height: 1.9; color: #bbb; }
        .post-b strong { color: var(--pink); font-weight: 900; text-shadow: 0 0 10px rgba(255,0,127,0.3); }
        .post-meta { font-size: 0.8rem; color: var(--pink); font-weight: 900; text-transform: uppercase; margin-bottom: 20px; display: flex; align-items: center; gap: 15px; letter-spacing: 0.2em; font-style: italic; }
        .post-meta::after { content: ""; height: 2px; flex-grow: 1; background: linear-gradient(to right, var(--pink), transparent); opacity: 0.3; }
        .post-sub-h { font-family: "Inter Tight", sans-serif; font-weight: 900; display: block; color: var(--cyan); font-size: 1.8rem; margin: 45px 0 20px 0; text-transform: uppercase; border-left: 10px solid var(--cyan); padding-left: 20px; font-style: italic; }
        
        .poll-box { margin-top: 45px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; clear: both; }
        .poll-option { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 15px; padding: 20px 30px; font-family: "Inter Tight", sans-serif; font-weight: 900; text-transform: uppercase; font-size: 0.95rem; color: #fff; display: flex; align-items: center; justify-content: space-between; transition: 0.4s; cursor: pointer; position: relative; overflow: hidden; font-style: italic; }
        .poll-option:hover { background: rgba(255,0,127,0.08); border-color: var(--pink); transform: translateY(-3px); }
        .poll-option.voted { border-color: var(--pink); background: rgba(255,0,127,0.1); }
        .poll-option.voted::before { content: ""; position: absolute; left: 0; top: 0; height: 100%; width: var(--p-width, 0%); background: rgba(255,0,127,0.15); z-index: -1; transition: 1s ease-out; }
        .poll-percent { color: var(--cyan); font-size: 1.1rem; text-shadow: 0 0 10px var(--cyan); display: none; }
        .poll-option.voted .poll-percent { display: block; }
        
        .num-highlight { color: var(--cyan); font-weight: 900; font-family: "Inter Tight", sans-serif; text-shadow: 0 0 15px rgba(0,245,255,0.4); }
        .bubble { display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.03); padding: 12px 18px; border-radius: 40px; margin-bottom: 10px; border: 1px solid var(--border); }
    </style>
</head>
<body>
    <svg width="0" height="0" style="position:absolute;"><defs><clipPath id="official-h-mask" clipPathUnits="objectBoundingBox"><path transform="scale(0.0042, 0.004)" d="M180.938 1c-25.317 0-55.258 18.698-73.381 49.771-4.89-11.222-22.313-23.451-43.024-23.451-16.689 0-63.533 20.858-63.533 88.178 0 86.88 87.901 104.725 105.671 131.729 1.221 1.857 5.154 3.26 6.655-1.177 14.179-41.845 124.125-89.125 124.125-174.279-0.001-47.756-31.197-70.771-56.513-70.771z"></path></clipPath></defs></svg>
    <div class="logo-box"><div class="logo">Your<span>Vision</span></div><div id="clock" style="font-weight:900; color:var(--cyan); font-size:0.9rem; font-family:Inter Tight; font-style:italic;">RIGA: 00:00:00</div></div>
    
    <div class="timers-hero">
        <div class="timer-card"><div class="timer-poster" style="background-image:url('assets/ESC_2026_SF1.jpg')"></div><div class="timer-info"><span class="timer-label"><i class="fi fi-rr-calendar"></i> Semi-Final 1 / 12.05</span><div id="timer-sf1" class="timer-val">--d --h --m --s</div></div></div>
        <div class="timer-card"><div class="timer-poster" style="background-image:url('assets/ESC_2026_SF2.jpg')"></div><div class="timer-info"><span class="timer-label"><i class="fi fi-rr-calendar"></i> Semi-Final 2 / 14.05</span><div id="timer-sf2" class="timer-val">--d --h --m --s</div></div></div>
        <div class="timer-card"><div class="timer-poster" style="background-image:url('assets/ESC_2026_GF.jpg')"></div><div class="timer-info"><span class="timer-label"><i class="fi fi-rr-calendar"></i> Grand Final / 16.05</span><div id="timer-gf" class="timer-val">--d --h --m --s</div></div></div>
    </div>

    <div class="layout">
        <aside class="column">
            <div class="card">
                <div class="section-title-base title-cyan"><i class="fi fi-rr-broadcast-tower"></i> ON AIR LIVE</div>
                <div id="player-cover" style="width:100%; aspect-ratio:1; border-radius:20px; background-size:cover; background-position:center; margin-bottom:25px; box-shadow: 0 20px 50px rgba(0,0,0,0.7);"></div>
                <div id="radio-artist" class="artist-rich" style="color:var(--pink); font-size:1.4rem; text-align:center; font-style:italic;">Loading...</div>
                <div id="radio-song" class="song-rich" style="text-align:center; font-size:1rem; margin-top:5px; font-style:italic;">Wait...</div>
                <div style="display:flex; justify-content:center; margin-top:25px;">
                    <button id="toggle-play" style="background:#fff; border:none; width:60px; height:60px; border-radius:50%; cursor:pointer;"><i class="fi fi-rr-play" style="font-size:1.5rem;"></i></button>
                </div>
                <audio id="audio-stream" preload="none" crossorigin="anonymous"></audio>
            </div>
            <div class="card">
                <div class="section-title-base title-acid"><i class="fi fi-rr-history"></i> RECENTLY PLAYED</div>
                <div id="hist-list"></div>
            </div>
        </aside>
        
        <main class="column">
            <div class="card">
                <div class="section-title-base title-pink" style="font-size:2rem;"><i class="fi fi-rr-trophy"></i> YOURVISION CUP / 2026 STANDINGS</div>
                <div id="bracket" style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:40px;"></div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:30px;">
                    <div><span class="side-label" style="color:var(--acid);"><i class="fi fi-rr-check"></i> QUALIFIED</span><div id="q-list"></div></div>
                    <div><span class="side-label" style="color:var(--pink);"><i class="fi fi-rr-cross"></i> ELIMINATED</span><div id="e-list"></div></div>
                </div>
            </div>
            <div id="news-grid"></div>
        </main>
        
        <aside class="column">
            <div class="card">
                <div class="section-title-base title-cyan"><i class="fi fi-rr-stats"></i> EUROGROOVE TOP 24</div>
                <div id="chart-list"></div>
            </div>
        </aside>
    </div>

    <!-- LOAD EXTERNAL DATA.JS -->
    <script src="data.js?v=""" + str(hash(json.dumps(data_obj))) + r""""></script>
    <script>
        const DATES = { sf1: new Date('2026-05-12T22:00:00+02:00'), sf2: new Date('2026-05-14T22:00:00+02:00'), gf: new Date('2026-05-16T22:00:00+02:00') };
        const countryMap = {"al":"Albania","am":"Armenia","au":"Australia","at":"Austria","az":"Azerbaijan","be":"Belgium","bg":"Bulgaria","hr":"Croatia","cy":"Cyprus","cz":"Czechia","dk":"Denmark","ee":"Estonia","fi":"Finland","fr":"France","ge":"Georgia","de":"Germany","gr":"Greece","il":"Israel","it":"Italy","lv":"Latvia","lt":"Lithuania","lu":"Luxembourg","mt":"Malta","md":"Moldova","me":"Montenegro","no":"Norway","pl":"Poland","pt":"Portugal","ro":"Romania","sm":"San Marino","rs":"Serbia","se":"Sweden","ch":"Switzerland","ua":"Ukraine","gb":"United Kingdom","nl":"Netherlands","kh":"Cambodia","vn":"Vietnam","th":"Thailand","my":"Malaysia","ph":"Philippines","np":"Nepal","bd":"Bangladesh","la":"Laos","bt":"Bhutan"};
        const getH = (id) => {
            if (id === "70") return "assets/heart_white_2026.svg";
            const asia = ["kh","vn","th","my","ph","np","bd","la","bt"];
            if (asia.includes(id.toLowerCase())) return `https://flagcdn.com/w160/${id.toLowerCase()}.png`;
            return `https://www.eurovision.com/static/images/flags/flag_${id.toLowerCase()}.svg`;
        };
        const decodeS = (s) => { try { return JSON.parse('"' + s.replace(/"/g, '\\"') + '"'); } catch(e) { return s; } };
        const emojiMap = {"📊": '<i class="fi fi-rr-stats"></i>',"🔗": '<i class="fi fi-rr-link"></i>',"🎧": '<i class="fi fi-rr-headphones"></i>',"⏱": '<i class="fi fi-rr-clock"></i>',"🚨": '<i class="fi fi-rr-alarm-exclamation"></i>',"🏆": '<i class="fi fi-rr-trophy"></i>',"⚡": '<i class="fi fi-rr-bolt"></i>',"🏛": '<i class="fi fi-rr-bank"></i>',"📅": '<i class="fi fi-rr-calendar"></i>',"🗳": '<i class="fi fi-rr-box-ballot"></i>'};
        const flagMap = {"🇦🇱":"al","🇦🇲":"am","🇦🇺":"au","🇦🇹":"at","🇦🇿":"az","🇧🇪":"be","🇧🇬":"bg","🇭🇷":"hr","🇨🇾":"cy","🇨🇿":"cz","🇩🇰":"dk","🇪🇪":"ee","🇫🇮":"fi","🇫🇷":"fr","🇬🇪":"ge","🇩🇪":"de","🇬🇷":"gr","🇮🇱":"il","🇮🇹":"it","🇱🇻":"lv","🇱🇹":"lt","🇱🇺":"lu","🇲🇹":"mt","🇲🇩":"md","🇲🇪":"me","🇳🇴":"no","🇵🇱":"pl","🇵🇹":"pt","🇷🇴":"ro","🇸🇲":"sm","🇷🇸":"rs","🇸🇪":"se","🇨🇭":"ch","🇺🇦":"ua","🇬🇧":"gb","🇰🇭":"kh","🇻🇳":"vn","🇹🇭":"th","🇲🇾":"my","🇵🇭":"ph","🇳🇵":"np","🇧🇩":"bd","🇱🇦":"la","🇧🇹":"bt"};

        function update() {
            const cl = document.getElementById('clock'); if(cl) cl.innerText = "RIGA: " + new Date().toLocaleTimeString("ru-RU");
            const now = new Date();
            Object.keys(DATES).forEach(k => {
                const el = document.getElementById('timer-'+k); if (!el) return;
                const diff = DATES[k] - now;
                if (diff < 0) { el.innerText = "LIVE"; return; }
                const d = Math.floor(diff/86400000), h = Math.floor((diff%86400000)/3600000), m = Math.floor((diff%3600000)/60000), s = Math.floor((diff%60000)/1000);
                el.innerText = `${d}d ${h}h ${m}m ${s}s`;
            });
        }

        function replaceFlags(text) {
            if (!text) return "";
            let res = text.replace(/❤️|\u2764\ufe0f|\u2764/g, `<img src="assets/heart_white_2026.svg" class="heart-icon" style="width:40px; height:40px; vertical-align:middle; margin-right:15px; filter:drop-shadow(0 0 10px rgba(255,255,255,0.5));">`);
            res = res.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
            res = res.replace(/(?<![="])\b(\d+%?)\b(?![="])/g, "<span class='num-highlight'>$1</span>");
            res = res.replace(/^([A-ZА-ЯЁ\s\(\):-]{5,}:?)$/gm, "<span class='post-sub-h'>$1</span>");
            for (const e in emojiMap) { res = res.split(e).join(emojiMap[e]); }
            for (const f in flagMap) { if (res.includes(f)) res = res.split(f).join(`<img src="${getH(flagMap[f])}" class="heart-shape" style="width:30px; height:30px; vertical-align:middle; margin-right:8px;">`); }
            return res;
        }

        function handleVote(postId, optIdx) { localStorage.setItem('yv_vote_'+postId, optIdx); render(); }

        function render() {
            if(!window.DATA) return;
            document.getElementById("q-list").innerHTML = DATA.qualifiers.map(c => `<div class="bubble"><img src="${getH(c.id)}" class="heart-shape" style="width:28px; height:28px;"><span class="artist-rich" style="font-size:0.85rem; color:#fff;">${decodeS(c.a)}</span></div>`).join("");
            document.getElementById("e-list").innerHTML = DATA.eliminated.map(c => `<div class="bubble" style="opacity:0.5;"><img src="${getH(c.id)}" class="heart-shape" style="width:28px; height:28px;"><span class="artist-rich" style="font-size:0.85rem; color:#888;">${decodeS(c.a)}</span></div>`).join("");
            document.getElementById("bracket").innerHTML = DATA.battles.map(b => `<div class="card ${b.status==='LIVE'?'status-live-box':''}" style="padding:20px; background:rgba(255,255,255,0.01);"><div style="font-size:0.6rem; color:#777; font-weight:900; letter-spacing:0.1em; margin-bottom:12px;">${b.n}</div><div class="battle-team ${b.w===1?'winner-glow':''}" style="display:flex; align-items:center; gap:12px;"><img src="${getH(b.t1)}" class="heart-shape"><div><span class="artist-rich" style="font-size:1.1rem;">${decodeS(b.a1)}</span><span class="song-rich">${decodeS(b.s1||'')}</span></div><span style="margin-left:auto; font-weight:900; color:var(--cyan); font-size:1.3rem; font-style:italic;">${b.sc1}</span></div><div class="battle-team ${b.w===2?'winner-glow':''}" style="display:flex; align-items:center; gap:12px; margin-top:15px;"><img src="${getH(b.t2)}" class="heart-shape"><div><span class="artist-rich" style="font-size:1.1rem;">${decodeS(b.a2)}</span><span class="song-rich">${decodeS(b.s2||'')}</span></div><span style="margin-left:auto; font-weight:900; color:var(--cyan); font-size:1.3rem; font-style:italic;">${b.sc2}</span></div></div>`).join("");
            document.getElementById("chart-list").innerHTML = DATA.chart.map(i => `<div class="bubble"><span style="color:var(--pink); font-weight:900; width:35px; font-family:'Inter Tight'; font-size:1.2rem; font-style:italic;">${i.r}</span><img src="${i.img}" style="width:45px; height:45px; border-radius:8px;"><div><div class="artist-rich" style="font-size:0.95rem; color:var(--pink); font-style:italic;">${decodeS(i.a)}</div><div class="song-rich" style="font-size:0.85rem;">${decodeS(i.s)}</div></div><span style="margin-left:auto; font-weight:900; color:var(--pink); font-family:'Inter Tight'; font-size:1.1rem; font-style:italic;">${i.p}</span></div>`).join("");
            document.getElementById("news-grid").innerHTML = DATA.news.map((p, pIdx) => {
                const votedIdx = localStorage.getItem('yv_vote_'+pIdx);
                let pollHtml = "";
                if (p.poll && p.poll.options) {
                    pollHtml = `<div class="poll-box">${p.poll.options.map((opt, oIdx) => {
                        const isVoted = votedIdx !== null;
                        const isSelected = votedIdx == oIdx;
                        const mockPct = Math.floor(100 / p.poll.options.length) + (oIdx % 3);
                        return `<div class="poll-option ${isSelected?'voted':''} ${isVoted?'voted':''}" onclick="handleVote(${pIdx}, ${oIdx})" style="--p-width: ${isVoted ? mockPct : 0}%"><span>${replaceFlags(opt)}</span><span class="poll-percent">${mockPct}%</span></div>`;
                    }).join("")}</div>`;
                }
                return `<div class="post-card"><span class="post-meta">${p.m} | YOURVISION INSIDER</span><div class="post-h">${replaceFlags(p.t.replace(/\*/g, ""))}</div><div style="overflow:hidden;">${p.isVideo ? `<video src="${p.vid}" autoplay loop muted playsinline controls class="post-media"></video>` : (p.img ? `<img src="${p.img}" class="post-media">` : "")}<div class="post-b">${replaceFlags(p.b.replace(/\n/g, "<br>"))}</div></div>${pollHtml}</div>`;
            }).join("");
        }

        async function syncRadio() {
            try {
                const r = await fetch("https://myradio24.com/users/levdanskiy/status.json?apikey=e81720544fe8cf709a784a5cf1e4a89c&v=" + Date.now());
                const d = await r.json();
                const cur = d.songs[d.songs.length - 1];
                document.getElementById("radio-artist").innerText = decodeS(d.artist || cur.song.split(" - ")[0]);
                document.getElementById("radio-song").innerText = decodeS(d.songtitle || cur.song.split(" - ")[1]);
                document.getElementById("player-cover").style.backgroundImage = `url("https://myradio24.com/${d.imgbig && !d.imgbig.includes('nocover') ? d.imgbig : 'assets/heart_white_2026.svg'}")`;
                document.getElementById("hist-list").innerHTML = d.songs.slice().reverse().slice(0,10).map(h => {
                    const pts = decodeS(h.song).split(" - ");
                    return `<div class="bubble"><span style="color:var(--cyan); font-size:0.75rem; font-weight:900; width:55px; font-family:'Inter Tight'; font-style:italic;">${h.time.substring(0,5)}</span><img src="${h.img ? "https://myradio24.com/" + h.img : "assets/heart_white_2026.svg"}" style="width:40px; height:40px; border-radius:8px;"><div><div class="artist-rich" style="font-size:0.95rem; color:var(--pink); font-style:italic;">${pts[0]}</div><div class="song-rich" style="font-size:0.8rem;">${pts[1]||'...'}</div></div></div>`;
                }).join("");
            } catch(e) {}
        }

        setInterval(update, 1000); setInterval(syncRadio, 15000);
        window.onload = () => { update(); render(); syncRadio(); };

        var isPlaying = false;
        var audio = document.getElementById("audio-stream"), playBtn = document.getElementById("toggle-play");
        playBtn.onclick = () => {
            if (!isPlaying) { 
                audio.src = "https://myradio24.org/levdanskiy?v=" + Date.now(); 
                audio.play(); isPlaying = true; 
                playBtn.style.background = "var(--pink)";
                playBtn.innerHTML = '<i class="fi fi-rr-stop" style="font-size:1.5rem; color:white;"></i>';
            } else { 
                audio.pause(); audio.src = ""; isPlaying = false; 
                playBtn.style.background = "white";
                playBtn.innerHTML = '<i class="fi fi-rr-play" style="font-size:1.5rem; color:black;"></i>';
            }
        };
    </script>
</body>
</html>"""

with open(os.path.join(HUB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
