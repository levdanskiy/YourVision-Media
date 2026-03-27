import os

# КОНСОЛИДИРОВАННЫЙ HTML: STANDINGS 2.0 + TITAN UI
final_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YourVision | Vienna 2026 Insider Hub</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0a021a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Inter+Tight:wght@900&display=swap" rel="stylesheet">
    <link rel="icon" href="https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp" type="image/webp">
    <style>
        :root {
            --bg-deep: #0a021a; --accent-pink: #ff007f; --accent-cyan: #00f5ff; --accent-acid: #ccff00;
            --glass-bg: rgba(255, 255, 255, 0.03); --glass-border: rgba(255, 255, 255, 0.08); --text-main: #e0e0e0; --text-dim: #777;
        }
        body { 
            background: var(--bg-deep); color: var(--text-main); font-family: 'Inter', sans-serif; margin: 0; overflow-x: hidden; letter-spacing: -0.02em; 
            background-image: linear-gradient(to bottom, rgba(10, 2, 26, 0.8), rgba(10, 2, 26, 0.95)), url('https://storage.googleapis.com/eurovision-com.appspot.com/renditions/public/cms/newwebsite_70png/NewWebsite_70-fill_size%3D1600x900-fill_size%3D1600x900.png');
            background-attachment: fixed; background-size: cover; background-position: center;
        }
        body::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('https://grainy-gradients.vercel.app/noise.svg'); opacity: 0.05; pointer-events: none; z-index: 9999; }

        .hero-view { min-height: 100vh; display: flex; flex-direction: column; padding: 40px; box-sizing: border-box; }
        nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 60px; }
        .logo-box { display: flex; flex-direction: column; text-decoration: none; line-height: 0.9; }
        .logo, .logo-sub { font-family: 'Inter Tight', sans-serif; font-size: 1.8rem; font-weight: 900; color: #fff; text-transform: uppercase; margin: 0; letter-spacing: -0.02em; }
        .logo span { color: var(--accent-pink); }
        .logo-sub { color: var(--accent-cyan); margin-top: 5px; text-shadow: 0 0 20px var(--accent-cyan); }
        #clock { font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--accent-cyan); font-weight: 900; }

        .timers-hero { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 80px; }
        .timer-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 12px; overflow: hidden; display: flex; backdrop-filter: blur(10px); flex-direction: column; text-decoration: none; transition: 0.3s; }
        .timer-card:hover { transform: translateY(-5px); border-color: var(--accent-pink); box-shadow: 0 10px 30px rgba(255,0,127,0.2); }
        .timer-poster { width: 100%; aspect-ratio: 16/9; background-size: cover; background-position: center; border-bottom: 1px solid var(--glass-border); }
        .timer-info { padding: 15px 20px; background: rgba(0,0,0,0.4); }
        .timer-val { font-family: 'Inter Tight', sans-serif; font-size: 1.5rem; font-weight: 900; color: #fff; }
        .timer-label { font-size: 0.55rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7; color: var(--accent-cyan); }

        .layout { display: grid; grid-template-columns: 380px 1fr 450px; gap: 40px; align-items: start; }
        .column { display: flex; flex-direction: column; gap: 30px; }
        .card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 12px; padding: 25px; backdrop-filter: blur(15px); position: relative; }

        /* HEADER COLORS */
        .section-title { font-family: 'Inter Tight', sans-serif; font-size: 1.2rem; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: 0.1em; border-left: 4px solid var(--accent-pink); padding-left: 15px; margin-bottom: 25px; }
        .header-gradient { background: linear-gradient(90deg, var(--accent-pink), var(--accent-cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; border-left: none; padding-left: 0; }
        
        .grid-sub-header { font-size: 0.7rem; font-weight: 900; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.2em; margin: 30px 0 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px; }
        .sub-qualified { color: var(--accent-acid); text-shadow: 0 0 10px rgba(204, 255, 0, 0.3); }
        .sub-eliminated { color: #ff4d4d; opacity: 0.8; }
        
        .tournament-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
        .bracket-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 30px; }
        
        /* TITAN BRACKET STYLES */
        .battle-box { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; display: flex; flex-direction: column; gap: 15px; transition: 0.4s; position: relative; min-height: 200px; justify-content: center; }
        .battle-box-small { min-height: 120px; opacity: 0.6; padding: 15px; }
        .battle-box:hover { border-color: var(--accent-pink); transform: translateY(-5px); background: rgba(255,255,255,0.05); }
        .battle-n { font-family: 'Inter Tight', sans-serif; font-size: 0.7rem; font-weight: 900; color: var(--accent-pink); text-transform: uppercase; letter-spacing: 0.15em; }
        .battle-qf-label { position: absolute; top: 20px; right: 20px; font-size: 0.6rem; color: var(--accent-cyan); font-weight: 900; opacity: 0.6; }
        
        .battle-team { display: flex; align-items: center; gap: 15px; padding: 10px; border-radius: 10px; transition: 0.3s; }
        .team-info { display: flex; flex-direction: column; gap: 2px; }
        .team-song { font-size: 1.3rem; font-weight: 900; color: #fff; line-height: 1.1; text-shadow: 0 0 15px rgba(255,255,255,0.1); }
        .team-artist { font-size: 0.9rem; color: var(--accent-cyan); font-weight: 400; }
        .team-score { margin-left: auto; font-family: 'Inter Tight', sans-serif; font-weight: 900; font-size: 1.5rem; color: #fff; }
        
        .winner-glow { background: rgba(204, 255, 0, 0.05); border: 1px solid var(--accent-acid); box-shadow: 0 0 30px rgba(204, 255, 0, 0.15); }
        .winner-tag-large { font-size: 1.2rem; color: var(--accent-acid); text-shadow: 0 0 15px var(--accent-acid); margin-left: 10px; }
        
        .score-bar-bg { width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; margin-top: 10px; }
        .score-bar-fill { height: 100%; background: var(--accent-pink); box-shadow: 0 0 15px var(--accent-pink); transition: 1.5s width ease-in-out; }
        
        .team-lose { opacity: 0.25; filter: grayscale(1); }
        .vs-label-large { font-size: 0.8rem; letter-spacing: 0.6em; color: var(--text-dim); text-align: center; margin: 15px 0; font-weight: 900; }
        
        @keyframes live-pulse { 0% { border-color: var(--accent-pink); box-shadow: 0 0 10px var(--accent-pink); } 50% { border-color: #fff; box-shadow: 0 0 30px var(--accent-pink); } 100% { border-color: var(--accent-pink); box-shadow: 0 0 10px var(--accent-pink); } }
        .status-live { animation: live-pulse 2s infinite; border-width: 2px; background: rgba(255,0,127,0.08); }

        /* COUNTRY BUBBLES 2.0 */
        .country-bubble { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 12px; transition: 0.3s; width: 100%; box-sizing: border-box; }
        .country-bubble:hover { background: rgba(255,255,255,0.06); border-color: var(--accent-cyan); transform: scale(1.02); }
        .bubble-info { display: flex; flex-direction: column; gap: 1px; flex-grow: 1; }
        .bubble-country { font-size: 0.55rem; font-weight: 900; color: var(--accent-cyan); text-transform: uppercase; letter-spacing: 0.1em; }
        .bubble-artist { font-size: 0.65rem; color: #fff; font-weight: 700; line-height: 1.1; }
        .bubble-song { font-size: 0.6rem; color: #888; font-weight: 400; }
        .heart-bubble { width: 30px; height: auto; }
        
        .status-q { border-left: 3px solid var(--accent-acid); }
        .status-el { border-left: 3px solid #444; opacity: 0.6; }

        .chart-table { width: 100%; border-collapse: collapse; }
        .chart-row { border-bottom: 1px solid rgba(255,255,255,0.05); transition: 0.3s; }
        .chart-cell { padding: 12px 5px; vertical-align: middle; }
        .rank { font-weight: 900; color: var(--accent-cyan); width: 45px; text-align: center; font-size: 1.1rem; }
        .track-cover { width: 45px; height: 45px; border-radius: 6px; object-fit: cover; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .info-cell { display: flex; flex-direction: column; gap: 2px; }
        .artist { font-weight: 900; text-transform: uppercase; font-size: 0.95rem; color: #fff; line-height: 1.1; }
        .song { font-size: 0.95rem; color: #888; font-weight: 700; line-height: 1.1; }
        .pts { font-weight: 900; color: var(--accent-pink); width: 75px; text-align: right; font-size: 1rem; }

        .feed-title { font-family: 'Inter Tight', sans-serif; font-size: 3rem; font-weight: 900; color: #fff; text-shadow: 0 0 40px var(--accent-pink); margin: 60px 0 40px 0; text-align: center; text-transform: uppercase; letter-spacing: 0.25em; border-bottom: 3px solid var(--accent-pink); display: block; padding-bottom: 20px; }
        .news-grid-main { display: grid; grid-template-columns: 1fr; gap: 30px; }
        
        .post-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; overflow: hidden; display: flex; flex-direction: column; transition: 0.4s; cursor: pointer; text-decoration: none; }
        .post-card:hover { transform: scale(1.01); background: rgba(255,255,255,0.05); border-color: var(--accent-pink); }
        .post-content { padding: 35px; flex-grow: 1; }
        .post-meta { font-size: 0.65rem; color: var(--accent-cyan); font-weight: 900; text-transform: uppercase; margin-bottom: 15px; display: block; letter-spacing: 0.1em; }
        .post-h { font-family: 'Inter Tight', sans-serif; font-size: 1.45rem; font-weight: 900; color: #fff; text-transform: uppercase; display: block; margin-bottom: 20px; }
        .post-b { font-size: 1.05rem; color: #ddd; line-height: 1.8; white-space: pre-wrap; }

        .section-title-pink { font-family: 'Inter Tight', sans-serif; font-size: 1.8rem; font-weight: 900; color: var(--accent-pink); text-shadow: 0 0 25px var(--accent-pink); text-transform: uppercase; border-bottom: 2px solid var(--accent-pink); padding-bottom: 10px; margin-bottom: 25px; display: block; width: 100%; text-align: center; }
        .on-air-live { position: absolute; top: 20px; right: 20px; background: var(--accent-pink); color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 0.6rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; z-index: 10; }
        .player-cover { width: 100%; aspect-ratio: 1; border-radius: 12px; background-size: cover; background-position: center; margin-bottom: 25px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); }
        .player-artist, .player-song { font-weight: 900; font-size: 1.5rem; display: block; text-align: center; text-transform: uppercase; }
        .player-artist { color: var(--accent-pink); }
        .player-song { color: var(--accent-cyan); margin-top: 8px; }
        .timer-container { margin-top: 20px; display: flex; align-items: center; gap: 15px; }
        .progress-bg { flex-grow: 1; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
        .progress-bar { height: 100%; background: var(--accent-pink); width: 0%; }
        .timer-text { font-family: 'Inter', sans-serif; font-size: 0.8rem; font-weight: 900; color: var(--accent-cyan); min-width: 40px; text-align: right; }

        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        footer { background: rgba(0,0,0,0.5); border-top: 1px solid var(--glass-border); padding: 60px 40px; margin-top: 100px; backdrop-filter: blur(20px); }
        .footer-copy { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; font-weight: 900; margin-top: 40px; text-align: center; letter-spacing: 0.2em; }
    </style>
</head>
<body>
    <div class="hero-view">
        <nav>
            <a href="https://t.me/YourEurovision" class="logo-box"><div class="logo">Your<span>Vision</span></div><div class="logo-sub">levdanskiy</div></a>
            <div id="clock">RIGA: 00:00:00</div>
        </nav>

        <div class="timers-hero">
            <a href="https://www.youtube.com/watch?v=Yy510SZZDw4" target="_blank" class="timer-card">
                <div class="timer-poster" style="background-image:url('assets/ESC_2026_SF1.jpg')"></div>
                <div class="timer-info"><div class="timer-label">Semi-Final 1 / 12.05</div><div class="timer-val" id="timer-sf1">--d --h --m</div></div>
            </a>
            <a href="https://www.youtube.com/watch?v=VeLS4psFNqQ" target="_blank" class="timer-card">
                <div class="timer-poster" style="background-image:url('assets/ESC_2026_SF2.jpg')"></div>
                <div class="timer-info"><div class="timer-label">Semi-Final 2 / 14.05</div><div class="timer-val" id="timer-sf2">--d --h --m</div></div>
            </a>
            <a href="https://www.youtube.com/watch?v=wYEIv2qhYAI" target="_blank" class="timer-card">
                <div class="timer-poster" style="background-image:url('assets/ESC_2026_GF.jpg')"></div>
                <div class="timer-info"><div class="timer-label">Grand Final / 16.05</div><div class="timer-val" id="timer-gf">--d --h --m</div></div>
            </a>
        </div>

        <div class="layout">
            <aside class="column">
                <div class="card">
                    <span class="on-air-live" style="animation: pulse 1.5s infinite">On Air LIVE</span>
                    <div id="player-cover" class="player-cover"></div>
                    <span class="player-artist" id="radio-artist">Loading</span>
                    <span class="player-song" id="radio-song">Wait</span>
                    <div class="timer-container"><div class="progress-bg"><div id="progress-bar" class="progress-bar"></div></div><span id="timer-text" class="timer-text">0:00 / 0:00</span></div>
                    <div class="main-controls" style="display:flex; justify-content:center; margin:20px 0;"><button id="toggle-play" style="background:#fff; border:none; width:60px; height:60px; border-radius:50%; cursor:pointer;"><svg id="play-icon" viewBox="0 0 24 24" width="30"><path d="M8 5v14l11-7z"/></svg></button></div>
                    <input type="range" id="volume-slider" style="width:100%; height:4px; appearance:none; background:rgba(255,255,255,0.1); border-radius:2px;" min="0" max="1" step="0.01" value="0.8">
                    <audio id="audio-stream" preload="none" crossorigin="anonymous"></audio>
                </div>
                <div class="card"><div class="section-title-pink">Recently Played [15]</div><table class="chart-table" id="history-list"></table></div>
            </aside>

            <main class="column">
                <div class="card">
                    <div class="section-title header-gradient">YOURVISION CUP / 2026 STANDINGS</div>
                    <div class="grid-sub-header">PLAY-OFF BRACKET [ROUND OF 16]</div>
                    <div id="bracket-body" class="bracket-grid"></div>
                    <div class="grid-sub-header sub-qualified">QUALIFIED COUNTRIES</div>
                    <div id="grid-qualifiers" class="tournament-grid"></div>
                    <div class="grid-sub-header sub-eliminated">ELIMINATED</div>
                    <div id="grid-eliminated" class="tournament-grid"></div>
                </div>
                <div class="feed-title">INSIDER NEWS FEED [20]</div>
                <div id="news-grid" class="news-grid-main"></div>
            </main>

            <aside class="column">
                <div class="card">
                    <div class="section-title-pink">Eurogroove / Full Top 24</div>
                    <table class="chart-table" id="chart-list"></table>
                </div>
            </aside>
        </div>
    </div>

    <footer><div class="footer-copy">© 2026 YOURVISION INSIDER | Vienna Edition | Zemgale, Latvia</div></footer>

    <script src="data.js"></script>
    <script>
        const DATES = { sf1: new Date('2026-05-12T22:00:00+02:00'), sf2: new Date('2026-05-14T22:00:00+02:00'), gf: new Date('2026-05-16T22:00:00+02:00') };

        function getHeartUrl(id) { return id === "70" ? "https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp" : `https://www.eurovision.com/static/images/flags/flag_${id.toLowerCase()}.svg`; }

        function updateTimers() {
            const now = new Date();
            Object.keys(DATES).forEach(k => {
                const diff = DATES[k] - now;
                const el = document.getElementById('timer-'+k);
                if (!el) return;
                if (diff < 0) { el.innerText = "LIVE"; return; }
                const d = Math.floor(diff/86400000), h = Math.floor((diff%86400000)/3600000), m = Math.floor((diff%3600000)/60000), s = Math.floor((diff%60000)/1000);
                el.innerText = `${d}d ${h}h ${m}m ${s}s`;
            });
        }

        var currentSongId = ""; var songStartedAt = 0; var songDuration = 180000;

        async function syncRadio() {
            try {
                const res = await fetch('https://myradio24.com/users/levdanskiy/status.json?apikey=e81720544fe8cf709a784a5cf1e4a89c&v=' + Date.now());
                const data = await res.json();
                const current = data.songs[data.songs.length - 1];
                if (currentSongId !== current.songid) {
                    currentSongId = current.songid; songStartedAt = Date.now(); 
                    document.getElementById('radio-artist').innerText = data.artist || current.song.split(' - ')[0];
                    document.getElementById('radio-song').innerText = data.songtitle || current.song.split(' - ')[1];
                    const img = (data.imgbig && !data.imgbig.includes('nocover')) ? `https://myradio24.com/${data.imgbig}` : `https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp`;
                    document.getElementById('player-cover').style.backgroundImage = `url('${img}')`;
                }
                document.getElementById('history-list').innerHTML = data.songs.slice().reverse().slice(0,15).map(h => `
                    <tr class="chart-row">
                        <td class="chart-cell rank" style="font-size:0.6rem; color:var(--accent-pink);">${h.time}</td>
                        <td class="chart-cell"><img src="https://myradio24.com/${h.img}" class="track-cover" onerror="this.src='https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp'"></td>
                        <td class="chart-cell info-cell">
                            <span class="artist" style="font-size:0.8rem; display:block; color:#fff;">${h.song.split(' - ')[0]}</span>
                            <span class="song" style="font-size:0.7rem; display:block; color:#888;">${h.song.split(' - ')[1] || ''}</span>
                        </td>
                    </tr>
                `).join('');
            } catch(e) {}
        }

        function render() {
            const bubble = (c, st) => `
                <div class="country-bubble ${st}">
                    <img src="${getHeartUrl(c.id)}" class="heart-bubble">
                    <div class="bubble-info">
                        <span class="bubble-country">${c.id.toUpperCase()}</span>
                        <span class="bubble-artist">${c.a}</span>
                        <span class="bubble-song">${c.s}</span>
                    </div>
                </div>`;
            
            document.getElementById('grid-qualifiers').innerHTML = DATA.qualifiers.map(c => bubble(c, 'status-q')).join('');
            document.getElementById('grid-eliminated').innerHTML = DATA.eliminated.map(c => bubble(c, 'status-el')).join('');
            
            document.getElementById('bracket-body').innerHTML = DATA.battles.map(b => {
                const isMajor = b.status === 'FINISHED' || b.status === 'LIVE';
                return `
                <div class="battle-box ${b.status === 'LIVE' ? 'status-live' : ''} ${!isMajor ? 'battle-box-small' : ''}">
                    <div class="battle-n">${b.n}</div>
                    <div class="battle-qf-label">${b.qf}</div>
                    <div class="battle-team ${b.w===1?'winner-glow':(b.w===2?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t1)}" style="width:35px; height:35px; border-radius:50%; border: 2px solid rgba(255,255,255,0.1);">
                        <div class="team-info">
                            <span class="team-song">${b.s1}</span>
                            <span class="team-artist">${b.a1}</span>
                        </div>
                        <span class="team-score">${b.sc1}${b.w===1?' <span class="winner-tag-large">★</span>':''}</span>
                    </div>
                    ${isMajor ? `<div class="score-bar-bg"><div class="score-bar-fill" style="width:${b.sc1}"></div></div>` : ''}
                    <div class="vs-label-large">VS</div>
                    <div class="battle-team ${b.w===2?'winner-glow':(b.w===1?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t2)}" style="width:35px; height:35px; border-radius:50%; border: 2px solid rgba(255,255,255,0.1);">
                        <div class="team-info">
                            <span class="team-song">${b.s2}</span>
                            <span class="team-artist">${b.a2}</span>
                        </div>
                        <span class="team-score">${b.sc2}${b.w===2?' <span class="winner-tag-large">★</span>':''}</span>
                    </div>
                    ${isMajor && b.sc2 ? `<div class="score-bar-bg"><div class="score-bar-fill" style="width:${b.sc2}; background:var(--accent-cyan); box-shadow: 0 0 15px var(--accent-cyan);"></div></div>` : ''}
                </div>`;
            }).join('');

            document.getElementById('chart-list').innerHTML = DATA.chart.map(i => `
                <tr class="chart-row">
                    <td class="chart-cell rank">${i.r}</td>
                    <td class="chart-cell"><img src="${i.img}" class="track-cover" onerror="this.src='https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp'"></td>
                    <td class="chart-cell info-cell">
                        <span class="artist" style="display:block; color:#fff;">${i.a}</span>
                        <span class="song" style="display:block; color:#888;">${i.s}</span>
                    </td>
                    <td class="chart-cell pts">${i.p}</td>
                </tr>`).join('');
            
            document.getElementById('news-grid').innerHTML = DATA.news.map(p => {
                const title = p.t.replace(/\\*/g, '');
                const body = p.b.replace(/\\*/g, '');
                return `
                <a href="${p.u}" target="_blank" class="post-card">
                    <div class="post-content">
                        <span class="post-meta">${p.m}</span>
                        <span class="post-h">${title}</span>
                        <div class="post-b">${body}</div>
                    </div>
                </a>`;
            }).join('');
        }

        var isPlaying = false;
        var audio = document.getElementById('audio-stream'), playBtn = document.getElementById('toggle-play'), progressBar = document.getElementById('progress-bar'), timerText = document.getElementById('timer-text');
        playBtn.onclick = () => {
            if (!isPlaying) {
                audio.src = "https://myradio24.org/levdanskiy?v=" + Date.now();
                audio.play().then(() => {
                    isPlaying = true;
                    playBtn.innerHTML = '<svg viewBox="0 0 24 24" width="30"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>';
                }).catch(e => console.error("Play error:", e));
            } else {
                audio.pause(); audio.src = ""; isPlaying = false;
                playBtn.innerHTML = '<svg viewBox="0 0 24 24" width="30"><path d="M8 5v14l11-7z"/></svg>';
            }
        };

        function update() {
            const clock = document.getElementById('clock');
            if(clock) clock.innerText = "RIGA: " + new Date().toLocaleTimeString('ru-RU');
            updateTimers();
            if (songStartedAt > 0) {
                const elapsed = Date.now() - songStartedAt;
                const m = Math.floor(elapsed / 60000), s = Math.floor((elapsed % 60000) / 1000);
                const tm = Math.floor(songDuration / 60000), ts = Math.floor((songDuration % 60000) / 1000);
                if(timerText) timerText.innerText = `${m}:${s < 10 ? '0' : ''}${s} / ${tm}:${ts < 10 ? '0' : ''}${ts}`;
                if(progressBar) progressBar.style.width = Math.min(100, (elapsed / songDuration) * 100) + "%";
            }
        }
        setInterval(update, 1000); setInterval(syncRadio, 15000); render(); syncRadio();
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print("Standings 2.0 with detailed country bubbles deployed.")
