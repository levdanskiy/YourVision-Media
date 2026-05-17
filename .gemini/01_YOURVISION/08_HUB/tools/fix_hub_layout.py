import re

with open("/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS
if "/* MEDIA & POLLS */" not in html:
    css_to_add = """
        /* MEDIA & POLLS */
        .post-image, .post-video { width: 380px; height: auto; max-height: 550px; float: left; margin-right: 30px; margin-bottom: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: block; }
        .post-b { display: block; line-height: 1.7; font-size: 1.1rem; color: #ccc; }
        .post-b a { color: var(--accent-cyan); text-decoration: none; font-weight: 700; border-bottom: 1px dashed var(--accent-cyan); }
        .post-b a:hover { color: #fff; border-bottom-style: solid; }
        .poll-container { margin-top: 25px; display: flex; flex-direction: column; gap: 12px; clear: both; padding-top: 10px; }
        .poll-option { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 18px 25px; border-radius: 12px; font-size: 1rem; color: #fff; font-weight: 700; display: flex; align-items: center; transition: 0.3s; }
        .poll-option::before { content: "○"; margin-right: 15px; color: var(--accent-cyan); font-weight: 900; }
    </style>"""
    html = html.replace("    </style>", css_to_add)

# 2. Add linkify function
if "function linkify" not in html:
    linkify_func = """
        function linkify(text) {
            const urlPattern = /(\\b(https?|ftp|file):\\/\\/[-A-Z0-9+&@#\\/%?=~_|!:,.;]*[-A-Z0-9+&@#\\/%=~_|])/ig;
            return text.replace(urlPattern, '<a href="$1" target="_blank">$1</a>');
        }

        function render() {"""
    html = html.replace("        function render() {", linkify_func)

# 3. Update news render block
news_render_new = r"""            document.getElementById('news-grid').innerHTML = DATA.news.map(p => {
                const title = replaceFlags(p.t.replace(/\*/g, ''));
                const body = linkify(replaceFlags(p.b.replace(/\*/g, '')));
                const isLV = p.id === "lv";
                
                let mediaHtml = "";
                if (p.isVideo && p.vid) {
                    mediaHtml = `<video class="post-video" src="${p.vid}" autoplay loop muted playsinline controls></video>`;
                } else if (p.img && !p.img.includes("telegram.org/img/emoji")) {
                    mediaHtml = `<img class="post-image" src="${p.img}">`;
                }

                let pollHtml = "";
                if (p.poll && p.poll.options) {
                    pollHtml = `<div class="poll-container">${p.poll.options.map(opt => `<div class="poll-option">${opt}</div>`).join("")}</div>`;
                }

                return `
                <div class="post-card ${isLV ? 'post-lv' : 'post-yv'}">
                    <div class="post-content">
                        <div class="post-header">
                            <span class="post-meta">${p.m}</span>
                            <span class="source-badge ${isLV ? 'badge-lv' : 'badge-yv'}">${isLV ? 'Marginalia' : 'YourVision'}</span>
                        </div>
                        <a href="${p.u}" target="_blank" class="post-h">${title}</a>
                        ${mediaHtml}
                        <div class="post-b">${body}</div>
                        ${pollHtml}
                        <div style="clear:both;"></div>
                    </div>
                </div>`;
            }).join('');"""

# Precise matching for the old news grid line
pattern = re.compile(r"document\.getElementById\('news-grid'\)\.innerHTML = DATA\.news\.map\(p => \{.*?\}\)\.join\(''\);", re.DOTALL)
html = pattern.sub(news_render_new, html)

with open("/home/levdanskiy/.gemini/01_YOURVISION/08_HUB/index.html", "w", encoding="utf-8") as f:
    f.write(html)
