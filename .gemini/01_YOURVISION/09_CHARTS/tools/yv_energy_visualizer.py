#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YourVision Playlist Energy Arc Visualizer
Parses a tracklist and outputs a modern, premium vector SVG graph showing the energy flow.
No external dependencies.
"""

import sys
import os
import re

DEFAULT_OUTPUT_DIR = "/home/levdanskiy/GEMINI_PROJECT/01_YOURVISION/05_ASSETS/visuals"
DEFAULT_OUTPUT_FILE = "energy_arc.svg"

def parse_tracklist(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR: File {filepath} not found.")
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    tracks = []
    # Match pattern: Number - Artist - Track - Genre - Energy
    track_pattern = re.compile(r"^\s*(\d+)\s*-\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+?)\s*-\s*(low|mid|high)\s*$", re.IGNORECASE)
    
    for idx, line in enumerate(lines, 1):
        line_str = line.strip()
        if not line_str or line_str.startswith("#") or line_str.startswith("//"):
            continue
            
        match = track_pattern.match(line_str)
        if match:
            num, artist, title, genre, energy = match.groups()
            tracks.append({
                "number": int(num),
                "artist": artist.strip(),
                "title": title.strip(),
                "genre": genre.strip(),
                "energy": energy.lower().strip()
            })
            
    return tracks

def generate_svg(tracks, output_path):
    if not tracks:
        print("ERROR: No tracks parsed from file.")
        sys.exit(1)
        
    # SVG Dimensions
    width = 900
    height = 450
    padding_left = 80
    padding_right = 50
    padding_top = 80
    padding_bottom = 60
    
    # Plotting boundaries
    plot_width = width - padding_left - padding_right
    plot_height = height - padding_top - padding_bottom
    
    # Energy to Y-coordinate mapping
    # High -> top, Low -> bottom
    y_high = padding_top + plot_height * 0.15
    y_mid = padding_top + plot_height * 0.50
    y_low = padding_top + plot_height * 0.85
    
    energy_map = {
        "low": y_low,
        "mid": y_mid,
        "high": y_high
    }
    
    # X coordinates
    num_points = len(tracks)
    if num_points > 1:
        x_step = plot_width / (num_points - 1)
    else:
        x_step = plot_width
        
    points = []
    for i, t in enumerate(tracks):
        x = padding_left + i * x_step
        y = energy_map.get(t["energy"], y_mid)
        points.append((x, y, t))
        
    # Start SVG content
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    
    # SVG Definitions (Gradients, Filters)
    svg.append("""  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120624"/>
      <stop offset="50%" stop-color="#080212"/>
      <stop offset="100%" stop-color="#020005"/>
    </linearGradient>
    
    <!-- Neon Pink Glow for High Energy Line -->
    <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="60%" stop-color="#ccff00"/>
      <stop offset="100%" stop-color="#ff007f"/>
    </linearGradient>
    
    <!-- Semi-transparent Area Fill Gradient -->
    <linearGradient id="area-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff007f" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#00f5ff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#00f5ff" stop-opacity="0.00"/>
    </linearGradient>
    
    <!-- Glow Filter -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>""")
    
    # Background
    svg.append(f'  <rect width="{width}" height="{height}" fill="url(#bg-grad)" />')
    
    # Horizontal grid lines
    svg.append(f'  <!-- Grid Lines -->')
    svg.append(f'  <line x1="{padding_left}" y1="{y_high}" x2="{width - padding_right}" y2="{y_high}" stroke="rgba(255, 0, 127, 0.15)" stroke-width="1" stroke-dasharray="4,4" />')
    svg.append(f'  <line x1="{padding_left}" y1="{y_mid}" x2="{width - padding_right}" y2="{y_mid}" stroke="rgba(0, 245, 255, 0.15)" stroke-width="1" stroke-dasharray="4,4" />')
    svg.append(f'  <line x1="{padding_left}" y1="{y_low}" x2="{width - padding_right}" y2="{y_low}" stroke="rgba(204, 255, 0, 0.15)" stroke-width="1" stroke-dasharray="4,4" />')
    
    # Grid Labels
    font_family = "font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; font-weight: 900; font-style: italic; font-size: 11px; letter-spacing: 0.1em;"
    svg.append(f'  <text x="{padding_left - 15}" y="{y_high + 4}" fill="#ff007f" text-anchor="end" style="{font_family}">🔴 HIGH</text>')
    svg.append(f'  <text x="{padding_left - 15}" y="{y_mid + 4}" fill="#00f5ff" text-anchor="end" style="{font_family}">🟡 MID</text>')
    svg.append(f'  <text x="{padding_left - 15}" y="{y_low + 4}" fill="#ccff00" text-anchor="end" style="{font_family}">🟢 LOW</text>')
    
    # Build Path
    path_data = []
    for i, (x, y, _) in enumerate(points):
        if i == 0:
            path_data.append(f"M {x} {y}")
        else:
            path_data.append(f"L {x} {y}")
            
    path_str = " ".join(path_data)
    
    # Fill Area under the curve
    fill_path = f"{path_str} L {points[-1][0]} {y_low + 30} L {points[0][0]} {y_low + 30} Z"
    svg.append(f'  <!-- Area Fill -->')
    svg.append(f'  <path d="{fill_path}" fill="url(#area-grad)" />')
    
    # Draw glowing line
    svg.append(f'  <!-- Glow Line -->')
    svg.append(f'  <path d="{path_str}" fill="none" stroke="url(#line-grad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" filter="url(#neon-glow)" />')
    
    # Draw markers & labels
    svg.append(f'  <!-- Markers and Labels -->')
    for i, (x, y, track) in enumerate(points):
        # Determine node color based on energy
        color = "#00f5ff"
        if track["energy"] == "high":
            color = "#ff007f"
        elif track["energy"] == "low":
            color = "#ccff00"
            
        # Draw node
        svg.append(f'  <circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{color}" stroke-width="3" filter="url(#neon-glow)" />')
        
        # Track label above the node
        label_family = "font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; font-size: 10px; font-weight: 700;"
        svg.append(f'  <text x="{x}" y="{y - 15}" fill="#fff" text-anchor="middle" style="{label_family} font-weight: 900;">#{track["number"]}</text>')
        
        # Song artist/title snippet at the bottom (diagonal rotation for compact fit)
        title_snippet = track["title"]
        if len(title_snippet) > 12:
            title_snippet = title_snippet[:10] + ".."
            
        svg.append(f'  <text x="{x}" y="{y_low + 35}" fill="rgba(255, 255, 255, 0.6)" text-anchor="middle" transform="rotate(-30, {x}, {y_low + 35})" style="{label_family} font-size: 8px;">{title_snippet}</text>')
        
    # Title Header
    header_family = "font-family: 'Unbounded', 'Inter Tight', sans-serif; font-weight: 900; font-size: 16px; font-style: italic; letter-spacing: 0.15em;"
    svg.append(f'  <text x="{width // 2}" y="45" fill="#fff" text-anchor="middle" style="{header_family}">YOURVISION PLAYLIST ENERGY ARC</text>')
    
    # Footer branding
    footer_family = "font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; font-weight: 700; font-size: 9px; letter-spacing: 0.2em; opacity: 0.4;"
    svg.append(f'  <text x="{width - padding_right}" y="{height - 15}" fill="#fff" text-anchor="end" style="{footer_family}">YourVision x levdanskiy</text>')
    
    svg.append('</svg>')
    
    # Write SVG
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"✅ Energy Arc SVG generated successfully at {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 yv_energy_visualizer.py <tracklist_file.txt> [output_file.svg]")
        print("Defaulting to sample tracklist audit or manual tracklist file...")
        sys.exit(1)
        
    tracklist_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Create output directory if it doesn't exist
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FILE)
        
    print(f"Parsing tracklist: {tracklist_path}...")
    tracks = parse_tracklist(tracklist_path)
    
    # Sort tracks descending by track number (typical playlist countdown order)
    # But for plotting the flow we want timeline order (from start to end of playlist, e.g. from lowest track number in file to highest, or as ordered in the file)
    # The file has countdown order: 20 -> 19 -> ... -> 6.
    # To plot flow (first track played to last track played), we reverse the order
    tracks.reverse()
    
    print(f"Parsed {len(tracks)} tracks. Generating SVG...")
    generate_svg(tracks, output_path)

if __name__ == "__main__":
    main()
