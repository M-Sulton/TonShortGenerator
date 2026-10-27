import os
import sys
import uuid
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, Request, BackgroundTasks, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

app = FastAPI(title="TonShortGenerator", version="1.0.0")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

# In-memory job tracker
jobs = {}

def sanitize_text(text: str) -> str:
    # Escape characters for ffmpeg drawtext
    return text.replace("\\", "\\\\").replace("'", "\u2019").replace(":", "\\:").replace("%", "\\%")

async def generate_voice(text: str, voice: str, out_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    await communicate.save(out_path)

def build_srt(words: List[str], total_sec: float, srt_path: str):
    if not words:
        return
    chunk_size = 3
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    dur_per_chunk = total_sec / max(len(chunks), 1)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, ch in enumerate(chunks):
            start = idx * dur_per_chunk
            end = min((idx + 1) * dur_per_chunk, total_sec)
            
            s_h = int(start // 3600)
            s_m = int((start % 3600) // 60)
            s_s = int(start % 60)
            s_ms = int((start - int(start)) * 1000)
            
            e_h = int(end // 3600)
            e_m = int((end % 3600) // 60)
            e_s = int(end % 60)
            e_ms = int((end - int(end)) * 1000)
            
            f.write(f"{idx+1}\n")
            f.write(f"{s_h:02d}:{s_m:02d}:{s_s:02d},{s_ms:03d} --> {e_h:02d}:{e_m:02d}:{e_s:02d},{e_ms:03d}\n")
            f.write(f"{' '.join(ch).upper()}\n\n")

def get_audio_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def render_short_video(job_id: str, title: str, script: str, voice: str, bg_theme: str):
    job_dir = OUTPUT_DIR / job_id
    job_dir.mkdir(exist_ok=True)
    
    audio_path = str(job_dir / "voice.mp3")
    srt_path = str(job_dir / "subs.srt")
    out_mp4 = str(job_dir / "tonshort.mp4")
    
    try:
        jobs[job_id]["status"] = "generating_audio"
        jobs[job_id]["progress"] = 20
        asyncio.run(generate_voice(script, voice, audio_path))
        
        jobs[job_id]["status"] = "building_subtitles"
        jobs[job_id]["progress"] = 40
        dur = get_audio_duration(audio_path)
        words = script.split()
        build_srt(words, dur, srt_path)
        
        jobs[job_id]["status"] = "rendering_video"
        jobs[job_id]["progress"] = 65
        
        # Color schemes inspired by YouTube Shorts Red theme
        color1, color2 = "#0F0F0F", "#270808"
        accent = "#FF0000"
        if bg_theme == "neon_red":
            color1, color2 = "#140003", "#380009"
        elif bg_theme == "cyber_dark":
            color1, color2 = "#0a0a0c", "#181824"
        elif bg_theme == "pure_black":
            color1, color2 = "#000000", "#181818"

        clean_title = sanitize_text(title)
        
        # Subtitle styling via FFmpeg subtitles filter
        # Ass style: Alignment=2 (Bottom center), MarginV=280, Fontname=DejaVu Sans, Fontsize=24, Bold=1
        sub_style = "Fontname=DejaVu Sans,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,BorderStyle=4,Bold=1,MarginV=280"
        escaped_srt = srt_path.replace(":", "\\:").replace("\\", "/")

        filter_complex = (
            f"color=c={color1}:s=1080x1920:d={dur} [bg];"
            f"drawbox=y=0:h=220:color=#FF0000@0.9:t=fill [header];"
            f"[bg][header] overlay=0:0 [v1];"
            f"[v1] drawtext=text='YOUTUBE SHORTS':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=60:bold=1,"
            f"drawtext=text='{clean_title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=120:bold=1,"
            f"drawbox=x=80:y=300:w=920:h=1200:color=white@0.05:t=fill,"
            f"drawbox=x=76:y=296:w=928:h=1208:color=#FF0000@0.6:t=4,"
            f"drawtext=text='TON SHORT GENERATOR':fontcolor=#FF4444:fontsize=28:x=(w-text_w)/2:y=340:bold=1,"
            f"subtitles='{escaped_srt}':force_style='{sub_style}',"
            f"drawtext=text='tonhermes.web.id':fontcolor=white@0.5:fontsize=24:x=(w-text_w)/2:y=1820 [vout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={color1}:s=1080x1920:d={dur}",
            "-i", audio_path,
            "-filter_complex", filter_complex,
            "-map", "[vout]", "-map", "1:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "faster", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            out_mp4
        ]

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {proc.stderr[-400:]}")
            
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["video_url"] = f"/output/{job_id}/tonshort.mp4"
        jobs[job_id]["duration"] = round(dur, 1)

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def start_generate(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    script: str = Form(...),
    voice: str = Form("id-ID-ArdiNeural"),
    theme: str = Form("neon_red")
):
    if not title.strip() or not script.strip():
        raise HTTPException(status_code=400, detail="Title and script are required.")
    
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "id": job_id,
        "title": title,
        "status": "queued",
        "progress": 5,
        "created_at": "",
        "video_url": None,
        "error": None
    }
    
    background_tasks.add_task(render_short_video, job_id, title, script, voice, theme)
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/status/{job_id}")
async def job_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/jobs")
async def list_jobs():
    return list(jobs.values())
