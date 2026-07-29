#!/bin/bash

SESSION="clustering-poc"

# Remove a sessão caso ela já exista
tmux kill-session -t "$SESSION" 2>/dev/null

# Cria a sessão
tmux new-session -d -s "$SESSION"

# Painel 1
tmux send-keys -t "$SESSION":0.0 "python3 main.py" C-m

# Divide verticalmente
tmux split-window -h -t "$SESSION"

# Painel 2
tmux send-keys -t "$SESSION":0.1 "uvicorn app.api:app --reload" C-m

# Ajusta o tamanho dos painéis
tmux select-layout -t "$SESSION" even-horizontal

# Anexa à sessão
tmux attach -t "$SESSION"