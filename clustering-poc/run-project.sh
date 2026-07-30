#!/bin/bash

SESSION="clustering-poc"

# Remove session if existing
tmux kill-session -t "$SESSION" 2>/dev/null

# Create session
tmux new-session -d -s "$SESSION"

# Panel 1
tmux send-keys -t "$SESSION":0.0 "python3 main.py" C-m

# Split vertically x2
tmux split-window -h -t "$SESSION"
tmux split-window -h -t "$SESSION"

# Panel 2
tmux send-keys -t "$SESSION":0.1 "uvicorn app.api:app --reload" C-m

# Panel 3
tmux send-keys -t "$SESSION":0.2 "streamlit run app/streamlit_app.py" C-m

# Fix panel layout
tmux select-layout -t "$SESSION" even-horizontal

# Attach to session
tmux attach -t "$SESSION"