import os

# Стили для интерактивной сетки
extra_styles = """
        .battle-box { transition: transform 0.3s, border-color 0.3s; cursor: pointer; position: relative; overflow: hidden; }
        .battle-box:hover { transform: scale(1.02); border-color: var(--accent-pink); background: rgba(255,255,255,0.05); }
        .battle-qf { font-size: 0.45rem; font-weight: 900; color: var(--accent-cyan); position: absolute; top: 5px; right: 10px; opacity: 0.6; }
        .team-info-mini { display: flex; flex-direction: column; gap: 1px; }
        .artist-mini { font-size: 0.55rem; color: #888; text-transform: none; font-weight: 400; line-height: 1; }
        .song-mini { font-size: 0.65rem; color: #fff; font-weight: 700; line-height: 1.1; }
        
        @keyframes live-glow { 0% { box-shadow: 0 0 5px var(--accent-pink); } 50% { box-shadow: 0 0 20px var(--accent-pink); } 100% { box-shadow: 0 0 5px var(--accent-pink); } }
        .status-live { border-color: var(--accent-pink) !important; animation: live-glow 2s infinite; }
        .winner-crown { color: var(--accent-acid); font-size: 0.7rem; margin-left: 5px; }
"""

# Новая функция рендеринга сетки
new_render_logic = """
        function render() {
            const bubble = (c, st) => `<div class="country-bubble ${st}"><img src="${getHeartUrl(c.id)}" class="heart-bubble"><span class="country-name">${c.id.toUpperCase()}</span></div>`;
            document.getElementById('grid-qualifiers').innerHTML = DATA.qualifiers.map(c => bubble(c, 'status-q')).join('');
            document.getElementById('grid-eliminated').innerHTML = DATA.eliminated.map(c => bubble(c, 'status-el')).join('');
            
            document.getElementById('bracket-body').innerHTML = DATA.battles.map(b => `
                <div class="battle-box ${b.status === 'LIVE' ? 'status-live' : ''}">
                    <div class="battle-n">${b.n}</div>
                    <div class="battle-qf">${b.qf}</div>
                    
                    <div class="battle-team ${b.w===1?'team-win':(b.w===2?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t1)}" style="width:20px; height:20px; border-radius:50%;">
                        <div class="team-info-mini">
                            <span class="song-mini">${b.s1}</span>
                            <span class="artist-mini">${b.a1}</span>
                        </div>
                        <span style="margin-left:auto">${b.sc1}${b.w===1?' <span class="winner-crown">★</span>':''}</span>
                    </div>
                    
                    <div class="vs-label">VS</div>
                    
                    <div class="battle-team ${b.w===2?'team-win':(b.w===1?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t2)}" style="width:20px; height:20px; border-radius:50%;">
                        <div class="team-info-mini">
                            <span class="song-mini">${b.s2}</span>
                            <span class="artist-mini">${b.a2}</span>
                        </div>
                        <span style="margin-left:auto">${b.sc2}${b.w===2?' <span class="winner-crown">★</span>':''}</span>
                    </div>
                </div>
            `).join('');

            document.getElementById('chart-list').innerHTML = DATA.chart.map(i => `
                <tr class="chart-row">
                    <td class="chart-cell rank">${i.r}</td>
                    <td class="chart-cell"><img src="${i.img}" class="track-cover" onerror="this.src='https://www.eurovision.com/static/images/70-heart-sm.ff9bba532601.webp'"></td>
                    <td class="chart-cell info-cell">
                        <span class="artist" style="display:block; color:#fff;">${i.a}</span>
                        <span class="song" style="display:block; color:#888;">${i.s}</span>
                    </td>
                    <td class="chart-cell pts">${i.p}</td>
                </tr>
            `).join('');
            
            document.getElementById('news-grid').innerHTML = DATA.news.map(p => `
                <div class="post-card">
                    <div class="post-content">
                        <span class="post-meta">${p.m}</span>
                        <a href="${p.u}" target="_blank" class="post-h">${p.t}</a>
                        <div class="post-b">${p.b}</div>
                    </div>
                </div>
            `).join('');
        }
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Вставляем стили
if '</style>' in html:
    html = html.replace('</style>', extra_styles + '\n    </style>')

# Заменяем функцию render (находим начало и конец старой)
start_marker = "function render() {"
end_marker = "var isPlaying = false;" # Ориентир после функции

if start_marker in html and end_marker in html:
    parts = html.split(start_marker)
    after_render = parts[1].split(end_marker)
    html = parts[0] + new_render_logic + "\n        " + end_marker + after_render[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Bracket interactivity patched successfully.")
