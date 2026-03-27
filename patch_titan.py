import os

# Стили для Титанической Сетки
titan_styles = """
        .battle-box { padding: 25px !important; min-height: 180px; display: flex; flex-direction: column; justify-content: center; }
        .battle-box-small { min-height: 100px; opacity: 0.6; padding: 15px !important; }
        
        .team-song { font-size: 1.3rem !important; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
        .team-artist { font-size: 0.9rem !important; color: var(--accent-cyan) !important; font-weight: 400; }
        .team-score { font-size: 1.5rem !important; color: #fff !important; }
        
        .winner-glow { background: rgba(204, 255, 0, 0.05) !important; border-color: var(--accent-acid) !important; box-shadow: 0 0 30px rgba(204, 255, 0, 0.1); }
        .winner-tag-large { font-size: 1.2rem; color: var(--accent-acid); text-shadow: 0 0 15px var(--accent-acid); margin-left: 10px; }
        
        .score-bar-bg { height: 6px !important; margin-top: 8px; background: rgba(255,255,255,0.1) !important; }
        .score-bar-fill { box-shadow: 0 0 10px var(--accent-pink); }
        
        .vs-label-large { font-size: 0.8rem; letter-spacing: 0.5em; color: var(--text-dim); margin: 15px 0 !important; }
"""

# Новая логика рендеринга
titan_render = """
        function render() {
            const bubble = (c, st) => `<div class="country-bubble ${st}"><img src="${getHeartUrl(c.id)}" class="heart-bubble"><span class="country-name">${c.id.toUpperCase()}</span></div>`;
            document.getElementById('grid-qualifiers').innerHTML = DATA.qualifiers.map(c => bubble(c, 'status-q')).join('');
            document.getElementById('grid-eliminated').innerHTML = DATA.eliminated.map(c => bubble(c, 'status-el')).join('');
            
            document.getElementById('bracket-body').innerHTML = DATA.battles.map(b => {
                const isMajor = b.status === 'FINISHED' || b.status === 'LIVE';
                return `
                <div class="battle-box ${b.status === 'LIVE' ? 'status-live' : ''} ${!isMajor ? 'battle-box-small' : ''}">
                    <div class="battle-n">${b.n}</div>
                    <div class="battle-qf-label">${b.qf}</div>
                    
                    <div class="battle-team ${b.w===1?'team-win winner-glow':(b.w===2?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t1)}" style="width:35px; height:35px; border-radius:50%; border: 2px solid rgba(255,255,255,0.1);">
                        <div class="team-info">
                            <span class="team-song">${b.s1}</span>
                            <span class="team-artist">${b.a1}</span>
                        </div>
                        <span class="team-score">${b.sc1}${b.w===1?' <span class="winner-tag-large">★</span>':''}</span>
                    </div>
                    
                    ${isMajor ? `<div class="score-bar-bg"><div class="score-bar-fill" style="width:${b.sc1}"></div></div>` : ''}
                    
                    <div class="vs-label-large">VS</div>
                    
                    <div class="battle-team ${b.w===2?'team-win winner-glow':(b.w===1?'team-lose':'')}">
                        <img src="${getHeartUrl(b.t2)}" style="width:35px; height:35px; border-radius:50%; border: 2px solid rgba(255,255,255,0.1);">
                        <div class="team-info">
                            <span class="team-song">${b.s2}</span>
                            <span class="team-artist">${b.a2}</span>
                        </div>
                        <span class="team-score">${b.sc2}${b.w===2?' <span class="winner-tag-large">★</span>':''}</span>
                    </div>
                    
                    ${isMajor && b.sc2 ? `<div class="score-bar-bg"><div class="score-bar-fill" style="width:${b.sc2}; background:var(--accent-cyan); box-shadow: 0 0 10px var(--accent-cyan);"></div></div>` : ''}
                </div>
            `}).join('');

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

# Применяем новые стили
if '</style>' in html:
    html = html.replace('</style>', titan_styles + '\n    </style>')

# Заменяем render
start_marker = "function render() {"
end_marker = "var isPlaying = false;"
if start_marker in html and end_marker in html:
    parts = html.split(start_marker)
    after_render = parts[1].split(end_marker)
    html = parts[0] + titan_render + "\n        " + end_marker + after_render[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Titan Bracket Patch applied.")
