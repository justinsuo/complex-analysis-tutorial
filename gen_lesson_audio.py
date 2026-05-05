#!/usr/bin/env python3
"""Generate Edge Neural TTS audio + word-timing JSON for every lesson scene.

Reads scenes.json (produced by extract_scenes.js) and writes
lesson_audio/<sceneId>.mp3 and lesson_audio/<sceneId>.json.
"""

import asyncio
import json
import sys
from pathlib import Path

import edge_tts

VOICE = 'en-US-AvaMultilingualNeural'  # high-quality neural female voice
OUT_DIR = Path(__file__).parent / 'lesson_audio'
OUT_DIR.mkdir(exist_ok=True)
SCENES_JSON = Path(__file__).parent / 'scenes.json'

CONCURRENCY = 2  # edge-tts is rate-sensitive; keep concurrency low
MAX_RETRIES = 6

async def gen_one(scene):
    sid = scene['id']
    text = scene['text']
    mp3_path = OUT_DIR / f'{sid}.mp3'
    json_path = OUT_DIR / f'{sid}.json'
    if mp3_path.exists() and mp3_path.stat().st_size > 1000 and json_path.exists():
        return 'cached'

    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            audio_data = bytearray()
            word_data = []
            async for chunk in communicate.stream():
                ctype = chunk.get('type')
                if ctype == 'audio':
                    audio_data.extend(chunk['data'])
                elif ctype == 'WordBoundary':
                    start = chunk['offset'] / 10_000_000.0
                    duration = chunk['duration'] / 10_000_000.0
                    word_data.append({
                        'text': chunk['text'],
                        'start': round(start, 3),
                        'end': round(start + duration, 3),
                    })
            if audio_data:
                mp3_path.write_bytes(bytes(audio_data))
                json_path.write_text(json.dumps({
                    'words': word_data,
                    'voice': VOICE,
                    'text': text,
                }))
                # tiny pacing delay between successful requests
                await asyncio.sleep(0.15)
                return 'generated' if attempt == 0 else f'generated (retry {attempt})'
            last_err = 'no audio'
        except Exception as e:
            last_err = str(e)
        # backoff: 1, 2, 4, 8, 16, 32 seconds
        await asyncio.sleep(min(60, 2 ** attempt))
    raise RuntimeError(f'failed after {MAX_RETRIES} attempts: {last_err}')

async def main():
    scenes = json.loads(SCENES_JSON.read_text())
    print(f'Found {len(scenes)} scenes. Generating audio in lesson_audio/ ...')
    sem = asyncio.Semaphore(CONCURRENCY)
    counts = {'generated': 0, 'cached': 0, 'failed': 0}
    done = 0
    total = len(scenes)

    async def task(s):
        nonlocal done
        async with sem:
            try:
                result = await gen_one(s)
                if result == 'generated':
                    counts['generated'] += 1
                elif result == 'cached':
                    counts['cached'] += 1
                else:
                    counts['failed'] += 1
            except Exception as e:
                counts['failed'] += 1
                print(f'  ✗ {s["id"]}: {e}', file=sys.stderr)
            done += 1
            if done % 25 == 0 or done == total:
                print(f'  progress: {done}/{total}  '
                      f"(new={counts['generated']}, cached={counts['cached']}, fail={counts['failed']})")

    await asyncio.gather(*[task(s) for s in scenes])
    print(f'\nDone. {counts}')
    print(f'Output: {OUT_DIR.resolve()}')

if __name__ == '__main__':
    asyncio.run(main())
