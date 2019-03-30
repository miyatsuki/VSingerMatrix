#!/bin/bash
set -eu

BASE_DIR="$(cd $(dirname $0)/../; pwd)"
BIN_DIR="${BASE_DIR}/bin/"
DATA_DIR="${BASE_DIR}/data/"
PYTHON_COMMAND="${BASE_DIR}/env/bin/python"


${PYTHON_COMMAND} ${BIN_DIR}/fetch_video_info.py

${PYTHON_COMMAND} ${BIN_DIR}/create_song_list.py

if [[ -s "${DATA_DIR}/reject_song_list.tsv" ]]; then
	echo "reject_song_list is not null"
	exit 1
fi

${PYTHON_COMMAND} ${BIN_DIR}/filter_song_and_singers.py

${PYTHON_COMMAND} ${BIN_DIR}/create_singer_plot_data.py