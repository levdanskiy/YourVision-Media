#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YourVision Charts Quality Control (QC) Validator
Audits tracklists against the official YourVision Charts Manual guidelines.
"""

import sys
import re

# Emojis representing countries (regional flag pairs)
FLAG_REGEX = re.compile(r"[\U0001F1E6-\U0001F1FF]{2}")

def lint_typography(text):
    errors = []
    # Check for forbidden dashes
    if "—" in text:
        errors.append("ERROR: Forbidden long dash (—) found. Use short hyphen (-).")
    if "–" in text:
        errors.append("ERROR: Forbidden medium dash (–) found. Use short hyphen (-).")
    
    # Check for straight quotes around Cyrillic text
    if re.search(r'"[а-яА-ЯёЁ\s]+"', text):
        errors.append("WARNING: Straight quotes used for Russian text. Use «ёлочки» instead.")
        
    return errors

def validate_tracklist(filepath):
    print("=" * 60)
    print(f"Auditing YourVision Tracklist: {filepath}")
    print("=" * 60)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
        
    # Check global file typography first
    global_typo = lint_typography("".join(lines))
    for err in global_typo:
        print(err)
        
    tracks = []
    track_pattern = re.compile(r"^\s*(\d+)\s*-\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+?)\s*-\s*(low|mid|high)\s*$", re.IGNORECASE)
    
    line_errors = 0
    parsed_tracks = []
    
    for idx, line in enumerate(lines, 1):
        line_str = line.strip()
        if not line_str or line_str.startswith("#") or line_str.startswith("//"):
            continue
            
        # Lint line typography
        typos = lint_typography(line_str)
        for t in typos:
            print(f"Line {idx}: {t}")
            line_errors += 1
            
        match = track_pattern.match(line_str)
        if not match:
            # Let us see if it matches with a slightly wrong format
            if "-" in line_str:
                print(f"Line {idx}: ERROR: Incorrect format. Expected 'Number - Artist - Track - Genre/Role - Energy'.")
                print(f"  Got: {line_str}")
                line_errors += 1
            continue
            
        num, artist, title, genre, energy = match.groups()
        parsed_tracks.append({
            "line": idx,
            "number": int(num),
            "artist": artist.strip(),
            "title": title.strip(),
            "genre": genre.strip(),
            "energy": energy.lower().strip()
        })
        
    if not parsed_tracks:
        print("\nResult: No tracks parsed. Check file formatting.")
        return False
        
    print(f"\nSuccessfully parsed {len(parsed_tracks)} tracks.")
    
    # Rule Checks
    warnings = []
    errors = []
    
    # 1. Artist Limit (1 artist = 1 track)
    artists = [t["artist"] for t in parsed_tracks]
    seen_artists = set()
    for art in artists:
        # Simple normalization to avoid case discrepancies
        norm_art = art.lower().replace(" feat. ", " & ").replace(" and ", " & ")
        if norm_art in seen_artists:
            errors.append(f"Artist violation: '{art}' appears multiple times.")
        seen_artists.add(norm_art)
        
    # 2. Energy limits
    energies = [t["energy"] for t in parsed_tracks]
    
    # Max 2 high-energy tracks in a row
    for i in range(len(energies) - 2):
        if energies[i] == "high" and energies[i+1] == "high" and energies[i+2] == "high":
            errors.append(f"Energy violation: 3 high-energy tracks in a row (tracks around line {parsed_tracks[i]['line']}).")
            
    # 3. Energy Arc (Low -> Mid -> High -> Mid)
    if len(energies) >= 5:
        # Check start energy
        if energies[0] == "high":
            warnings.append("Energy arc warning: Tracklist starts with 'high' energy. Soft start is preferred.")
        # Check end energy
        if energies[-1] == "high":
            warnings.append("Energy arc warning: Tracklist ends with 'high' energy. Soft ending/afterglow is preferred.")
            
    # 4. Genre Limits (Max 3 identical subgenres in a row)
    genres = [t["genre"].lower() for t in parsed_tracks]
    for i in range(len(genres) - 3):
        if genres[i] == genres[i+1] == genres[i+2] == genres[i+3]:
            warnings.append(f"Genre accumulation: 4 tracks of genre '{parsed_tracks[i]['genre']}' in a row (line {parsed_tracks[i]['line']}).")
            
    # 5. Global Diversity Check (If > 12 tracks, check flags as proxy for countries)
    # Extract flag emojis from the title or artist name
    flags = []
    for t in parsed_tracks:
        found_flags = FLAG_REGEX.findall(t["artist"]) + FLAG_REGEX.findall(t["title"])
        flags.extend(found_flags)
        
    unique_flags = set(flags)
    if len(parsed_tracks) >= 15:
        print(f"Diversity Telemetry: Found {len(unique_flags)} unique countries (flags: {', '.join(unique_flags)})")
        if len(unique_flags) < 10 and len(flags) > 0:
            warnings.append(f"Diversity Warning: Under 10 unique countries found ({len(unique_flags)} flags total). Manual requires at least 10 countries for global lists.")
            
    # Print Audits
    print("\n--- AUDIT SUMMARY ---")
    if errors:
        print(f"❌ FAILED: Found {len(errors)} critical manual violation(s):")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✅ Critical rules passed successfully.")
        
    if warnings:
        print(f"⚠️ WARNINGS ({len(warnings)}):")
        for wrn in warnings:
            print(f"  - {wrn}")
            
    if line_errors:
        print(f"⚠️ Formatting / Typo issues: {line_errors} issue(s) detected.")
        
    print("-" * 60)
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 yv_qc_validator.py <tracklist_file.txt>")
        sys.exit(1)
    success = validate_tracklist(sys.argv[1])
    sys.exit(0 if success else 1)
