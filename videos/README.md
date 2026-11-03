# Videos

Every module has two videos:

1. **An animated explainer** (about 2–3 minutes), rendered from code so anyone can fix a typo, translate the captions or restyle it, then re-render. The narration is burnt in as captions, and also shipped as a `.vtt` caption track and a `SCRIPT.md` you can record as a voice-over.
2. **A walkthrough** you record yourself: a screen recording of doing the lab with an AI tutor. Each module folder has a `WALKTHROUGH_SCRIPT.md`.

## Re-render an explainer

```bash
pip install playwright && playwright install chromium   # once; also needs ffmpeg
cd videos/01-the-ask-is-not-the-problem
python3 build.py            # writes docs/assets/videos/01-….mp4, .jpg poster and .vtt
python3 build.py --frames   # just the still frames, to preview in build/
python3 build.py --script   # just SCRIPT.md and the .vtt
```

Edit `scenes.py` to change what's on screen or what the captions say. Each scene is a list of beats `(html, caption, seconds)`; beats cross-fade into each other. Output is 1280×720, 30 fps, H.264.

## Adding a voice-over

Record `SCRIPT.md` line by line to its timings, export as `voice.m4a`, then:

```bash
ffmpeg -i ../../docs/assets/videos/01-the-ask-is-not-the-problem.mp4 -i voice.m4a \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest with-voice.mp4
```
