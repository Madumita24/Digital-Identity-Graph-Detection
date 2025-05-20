#!/bin/bash

# Start FastAPI (port 8000)
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (port 8501)
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0

# Keep container alive
wait
