#!/bin/bash

# Script để activate virtual environment cho dự án Thunderbolts
# Sử dụng: ./activate_venv.sh [command]

# Kiểm tra xem .venv có tồn tại không
if [ ! -d ".venv" ]; then
    echo "Virtual environment không tồn tại. Đang tạo mới..."
    python3 -m venv .venv
    echo "Virtual environment đã được tạo."
fi

# Activate virtual environment
echo "Đang activate virtual environment..."
source .venv/bin/activate

# Kiểm tra xem có command được truyền vào không
if [ $# -eq 0 ]; then
    echo "Virtual environment đã được activate."
    echo "Sử dụng: ./activate_venv.sh [command] để chạy command trong venv"
    echo "Ví dụ: ./activate_venv.sh python main.py"
    echo "Ví dụ: ./activate_venv.sh pytest"
    echo "Ví dụ: ./activate_venv.sh pip install package_name"
else
    echo "Chạy command: $@"
    exec "$@"
fi
