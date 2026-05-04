#!/usr/bin/env python3
import os
import json
import datetime

WORLD_BIBLE = "/home/levdanskiy/.gemini/CORE/knowledge/WORLD_BIBLE.json"

def record_event(channel, summary):
    """Records a summary of what happened in a channel to the World Bible."""
    if not os.path.exists(WORLD_BIBLE):
        data = {"history": [], "current_vibe": "Stable"}
    else:
        with open(WORLD_BIBLE, 'r') as f:
            data = json.load(f)
    
    event = {
        "timestamp": str(datetime.datetime.now()),
        "channel": channel,
        "summary": summary
    }
    data["history"].append(event)
    # Ограничиваем историю последними 10 событиями для динамики
    data["history"] = data["history"][-10:]
    
    with open(WORLD_BIBLE, 'w') as f:
        json.dump(data, f, indent=4)
    return "✅ World Bible Updated."

def get_context_for_synergy():
    """Returns the last 3 events to inject into the next post's prompt."""
    if not os.path.exists(WORLD_BIBLE):
        return ""
    with open(WORLD_BIBLE, 'r') as f:
        data = json.load(f)
    
    history = data.get("history", [])
    if not history: return ""
    
    context = "\n🔗 **WORLD SYNERGY (Recent Events):**\n"
    for e in history[-3:]:
        context += f"- In {e['channel']}: {e['summary']}\n"
    return context

if __name__ == "__main__":
    # Test record
    print(record_event("SYSTEM", "Hive Mind V11.0 Activated. World-Building mode ON."))
