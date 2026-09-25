import json

transcript_path = r'C:\Users\brunn\.gemini\antigravity\brain\c8c49699-ea26-483c-9ce6-af511f5bdc47\.system_generated\logs\transcript.jsonl'

with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if 100 <= idx <= 120:
            data = json.loads(line)
            print(f"--- Line {idx} ({data.get('type')}) ---")
            print(data.get('content', '')[:600].encode('ascii', 'replace').decode('ascii'))
