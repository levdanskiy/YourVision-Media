import re

with open("/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Полная функция render() со всеми блоками: Qualifiers, Eliminated, Bracket, Chart, News
new_render_js = r"""        function render() {
            if (!window.DATA) return;
            
            const bubble = (c, st) => `<div class="country-bubble ${st}">
                <img src="${getHeartUrl(c.id)}" class="heart-bubble heart-shape" style="width:30px; height:30px;">
                <div class="bubble-info">
                    <span class="bubble-country">${c.id.toUpperCase()}</span>
                    <b style="font-family:'Inter Tight', sans-serif; font-weight:900; text-transform:uppercase; font-size:0.85rem; color:var(--accent-pink);">${c.a}</b>
                </div>
            </div>`;
            
            document.getElementById('grid-qualifiers').innerHTML = DATA.qualifiers.map(c => bubble(c, 'status-q')).join('');
            document.getElementById('grid-eliminated').innerHTML = DATA.eliminated.map(c => bubble(c, 'status-el')).join('');

            document.getElementById('bracket-body').innerHTML = DATA.battles.map(b => `
                <div class="battle-box ${b.status === 'LIVE' ? 'status-live' : ''}">
                    <div style="font-size:0.6rem; color:#777; margin-bottom:12px; font-weight:900; text-transform:uppercase; letter-spacing:0.1em;">${b.n}</div>
                    
                    <div class="battle-team ${b.w===1 ? 'winner-glow' : ''}" style="display:flex; align-items:center; gap:12px; margin-bottom:8px; padding:2px;">
                        <img src="${getHeartUrl(b.t1)}" class="heart-shape" style="width:35px; height:35px;"> 
                        <div style="display:flex; flex-direction:column; gap:2px;">
                            <span style="font-family:'Inter Tight', sans-serif; font-weight:900; text-transform:uppercase; font-size:0.9rem; color:#fff;">${b.a1}</span>
                            <span style="font-family:'Inter', sans-serif; font-size:0.75rem; color:var(--accent-cyan); opacity:0.8;">${b.s1 || ''}</span>
                        </div>
                        <span class="score" style="margin-left:auto; color:var(--accent-pink); font-weight:900; font-size:1.1rem;">${b.sc1}</span>
                    </div>

                    <div class="battle-team ${b.w===2 ? 'winner-glow' : ''}" style="display:flex; align-items:center; gap:12px; padding:2px;">
                        <img src="${getHeartUrl(b.t2)}" class="heart-shape" style="width:35px; height:35px;"> 
                        <div style="display:flex; flex-direction:column; gap:2px;">
                            <span style="font-family:'Inter Tight', sans-serif; font-weight:900; text-transform:uppercase; font-size:0.9rem; color:#fff;">${b.a2}</span>
                            <span style="font-family:'Inter', sans-serif; font-size:0.75rem; color:var(--accent-cyan); opacity:0.8;">${b.s2 || ''}</span>
                        </div>
                        <span class="score" style="margin-left:auto; color:var(--accent-pink); font-weight:900; font-size:1.1rem;">${b.sc2}</span>
                    </div>
                </div>`).join('');

            document.getElementById('chart-list').innerHTML = DATA.chart.map(i => `
                <tr class="chart-row">
                    <td class="chart-cell rank">${i.r}</td>
                    <td class="chart-cell"><img src="${i.img}" class="track-cover heart-shape" style="width:45px; height:45px;"></td>
                    <td class="chart-cell info-cell">
                        <b style="font-family:'Inter Tight', sans-serif; font-size:0.85rem; color:var(--accent-pink); text-transform:uppercase; display:block; line-height:1.1;">${i.a}</b>
                        <small style="font-family:'Inter', sans-serif; font-size:0.75rem; color:var(--accent-cyan); opacity:0.8;">${i.s}</small>
                    </td>
                    <td class="chart-cell pts">${i.p}</td>
                </tr>`).join('');

            document.getElementById('news-grid').innerHTML = DATA.news.map(p => {
                const title = replaceFlags(p.t.replace(/\*/g, ''));
                const body = replaceFlags(linkify(p.b.replace(/\*/g, '')));
                const isLV = p.id === "lv";
                let mediaHtml = p.isVideo ? `<video class="post-video" src="${p.vid}" autoplay loop muted playsinline controls style="width:280px; float:left; margin-right:20px; border-radius:12px;"></video>` : (p.img ? `<img class="post-image" src="${p.img}" style="width:280px; float:left; margin-right:20px; border-radius:12px;">` : "");
                return `<div class="post-card" style="padding:40px; margin-bottom:40px; background:rgba(255,255,255,0.01); border:1px solid rgba(255,255,255,0.05); border-radius:25px; overflow:hidden;">
                    <div style="font-size:0.7rem; color:var(--accent-cyan); font-weight:900; margin-bottom:15px; text-transform:uppercase;">${p.m} | ${isLV?'MARGINALIA':'YOURVISION'}</div>
                    <div style="font-family:'Inter Tight', sans-serif; font-size:2.2rem; font-weight:900; color:#fff; line-height:1.1; margin-bottom:25px; text-transform:uppercase;">${title}</div>
                    <div style="overflow:hidden;">${mediaHtml}<div style="font-size:1.1rem; line-height:1.8; color:var(--text-main);">${body}</div></div>
                    <div style="clear:both;"></div>
                </div>`;
            }).join('');
        }"""

# Заменяем обрезанную функцию render на полную
html = re.sub(r"function render\(\) \{.*?\}", new_render_js, html, flags=re.DOTALL)

with open("/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Render logic for News and Chart restored successfully.")
