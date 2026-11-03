#!/usr/bin/env python3
"""
Render the Module 1 video from scenes.py.

    pip install playwright && playwright install chromium   # once
    python3 build.py            # frames + video -> build/ and docs/assets/videos/
    python3 build.py --frames   # frames only (to preview)

Needs ffmpeg on PATH. Output: 1280x720, 30 fps, H.264, silent, captions burnt in.
"""
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

import scenes

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
OUT_DIR = os.path.join(HERE, "..", "..", "docs", "assets", "videos")
NAME = "01-the-ask-is-not-the-problem"
XF = 0.5          # crossfade between beats inside a scene
DIP = 0.3         # fade from/to background at scene edges
BG = "0xf6f1e9"


def page_html(body, caption):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{scenes.CSS}</style></head>"
            f"<body>{body}<div class='caption'>{caption}</div></body></html>")


def render_frames():
    os.makedirs(BUILD, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        for si, scene in enumerate(scenes.SCENES):
            row = []
            for bi, (body, caption, secs) in enumerate(scene):
                page.set_content(page_html(body, caption))
                page.wait_for_timeout(150)
                path = os.path.join(BUILD, f"s{si:02d}_b{bi:02d}.jpg")
                page.screenshot(path=path, type="jpeg", quality=92)
                row.append((path, secs))
            paths.append(row)
        browser.close()
    return paths


def render_scene(si, beats):
    out = os.path.join(BUILD, f"scene_{si:02d}.mp4")
    tmp = out[:-4] + ".part.mp4"
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for path, _ in beats:
        args += ["-framerate", "30", "-i", path]
    chains, total = [], 0.0
    for i, (_, secs) in enumerate(beats):
        chains.append(f"[{i}:v]format=yuv420p,loop=-1:1,trim=duration={secs},setpts=PTS-STARTPTS,fps=30[v{i}]")
    last = "v0"
    total = beats[0][1]
    for i in range(1, len(beats)):
        offset = total - XF
        chains.append(f"[{last}][v{i}]xfade=transition=fade:duration={XF}:offset={offset:.3f}[x{i}]")
        last = f"x{i}"
        total = offset + beats[i][1]
    chains.append(f"[{last}]fade=t=in:st=0:d={DIP}:color={BG},fade=t=out:st={total - DIP:.3f}:d={DIP}:color={BG},format=yuv420p[out]")
    args += ["-filter_complex", ";".join(chains), "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "20", "-r", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    subprocess.run(args, check=True)
    os.replace(tmp, out)
    return out


def ts(t):
    h, rem = divmod(t, 3600)
    m, sec = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}"


def write_script_and_captions():
    """SCRIPT.md (voice-over script) and a WebVTT caption track, from the same words."""
    vtt, md, t0 = ["WEBVTT", ""], ["# Narration script — Module 1: The ask is not the problem", "",
                                     "Read these lines as a voice-over. Timings match the rendered video.", ""], 0.0
    for si, scene in enumerate(scenes.SCENES):
        t = t0
        for bi, (_, caption, secs) in enumerate(scene):
            start = t
            end = t + secs - (XF if bi < len(scene) - 1 else 0)
            vtt += [f"{ts(start)} --> {ts(end)}", caption, ""]
            md.append(f"- **{ts(start)[3:8]}** {caption}")
            t = end
        t0 = t
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, f"{NAME}.vtt"), "w").write("\n".join(vtt))
    open(os.path.join(HERE, "SCRIPT.md"), "w").write("\n".join(md) + "\n")


def main():
    write_script_and_captions()
    if "--script" in sys.argv:
        return
    frames = render_frames()
    if "--frames" in sys.argv:
        print(f"{sum(len(r) for r in frames)} frames in {BUILD}")
        return
    files = [render_scene(si, beats) for si, beats in enumerate(frames)]
    listing = os.path.join(BUILD, "concat.txt")
    with open(listing, "w") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in files)
    os.makedirs(OUT_DIR, exist_ok=True)
    final = os.path.join(OUT_DIR, f"{NAME}.mp4")
    tmp = final[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listing,
                    "-c", "copy", "-movflags", "+faststart", tmp], check=True, cwd=BUILD)
    os.replace(tmp, final)
    poster = os.path.join(OUT_DIR, f"{NAME}.jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", frames[0][0][0], "-vf", "scale=1280:720",
                    "-q:v", "3", poster], check=True)
    print("wrote", final)


if __name__ == "__main__":
    main()
