#!/bin/bash
set -eu

BASE_DIR="$(cd $(dirname $0)/../; pwd)"
BIN_DIR="${BASE_DIR}/bin/"
DATA_DIR="${BASE_DIR}/data/"
PYTHON_COMMAND="python"


${PYTHON_COMMAND} ${BIN_DIR}/fetch_video_info.py

${PYTHON_COMMAND} ${BIN_DIR}/create_song_list.py

${PYTHON_COMMAND} ${BIN_DIR}/create_singer_plot_data.py
