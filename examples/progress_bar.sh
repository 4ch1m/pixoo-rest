#!/bin/bash

PIXOO_REST_URL="http://localhost:5100"

SCREEN_SIZE_X=64
SCREEN_SIZE_Y=64

MAX_SCREEN_VALUE_X=$((SCREEN_SIZE_X - 1))
MAX_SCREEN_VALUE_Y=$((SCREEN_SIZE_Y - 1))

function progress_bar() {

  curl -s -X POST \
    -d "r=0&g=0&b=0&push_immediately=false" \
    "${PIXOO_REST_URL}/fill"

  TOP_LEFT_X="top_left_x=0"
  TOP_LEFT_Y="top_left_y=$(printf "%.0f\n" "$((MAX_SCREEN_VALUE_Y - (SCREEN_SIZE_Y * ${1} / 100)))")"
  BOTTOM_RIGHT_X="bottom_right_x=${MAX_SCREEN_VALUE_X}"
  BOTTOM_RIGHT_Y="bottom_right_y=${MAX_SCREEN_VALUE_Y}"

  curl -s -X POST \
    -d "${TOP_LEFT_X}&${TOP_LEFT_Y}&${BOTTOM_RIGHT_X}&${BOTTOM_RIGHT_Y}&r=255&g=0&b=0&push_immediately=false" \
    "${PIXOO_REST_URL}/rectangle"

  curl -s -X POST \
    -d "text=${1}%20%25&x=0&y=0&r=255&g=255&b=255&push_immediately=true" \
    "${PIXOO_REST_URL}/text"

}

for i in {1..100}; do

  # do something meaningful here ...

  progress_bar ${i} > /dev/null

  sleep 1

done
