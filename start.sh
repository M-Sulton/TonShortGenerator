#!/bin/bash
export LLM_PROVIDER=openai
export LLM_BASE_URL="http://127.0.0.1:20128/v1"
export LLM_API_KEY="sk-6b3ac6ef8e3b70c9-937mk1-0f0bd527"
export LLM_MODEL="ag/gemini-3.8-flash"
export GEMINI_API_KEY="sk-6b3ac6ef8e3b70c9-937mk1-0f0bd527"
export UPLOAD_POST_API_KEY="disabled"
export DISABLE_YOUTUBE_URL=false

cd /home/ubuntu/TonShortGenerator/upstream_openshorts
exec /home/ubuntu/TonShortGenerator/venv/bin/uvicorn app:app --host 127.0.0.1 --port 3015
