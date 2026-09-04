#!/bin/bash
# Chạy bot ở chế độ ngầm (background)
python bot.py &
# Khởi chạy Flask Server bằng Gunicorn
gunicorn app:app