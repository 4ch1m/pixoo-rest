#!/bin/bash

curl -s -X 'POST' \
  -F "gif_file=@$(dirname "$(realpath "${0}")")/duck.gif;type=image/gif" \
  "http://localhost:8000/sendGif?skip_first_frame=false&animation_speed=100"
