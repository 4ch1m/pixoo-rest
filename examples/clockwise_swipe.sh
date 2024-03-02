#!/bin/bash

PIXOO_REST_URL="http://localhost:5100"

START_PARAMS="start_x=32&start_y=32"

function swipe() {
  local COLOR_PARAMS="r=${1}&g=${2}&b=${3}"

  for i in {-1..64}; do
    curl -s -X POST \
      -d "${START_PARAMS}&stop_x=${i}&stop_y=-1&${COLOR_PARAMS}&push_immediately=true" \
      "${PIXOO_REST_URL}/line"
  done

  for i in {0..64}; do
    curl -s -X POST \
      -d "${START_PARAMS}&stop_x=64&stop_y=${i}&${COLOR_PARAMS}&push_immediately=true" \
      "${PIXOO_REST_URL}/line"
  done

  for i in {63..-1}; do
    curl -s -X POST \
      -d "${START_PARAMS}&stop_x=${i}&stop_y=64&${COLOR_PARAMS}&push_immediately=true" \
      "${PIXOO_REST_URL}/line"
  done

  for i in {63..0}; do
    curl -s -X POST \
      -d "${START_PARAMS}&stop_x=-1&stop_y=${i}&${COLOR_PARAMS}&push_immediately=true" \
      "${PIXOO_REST_URL}/line"
  done

}

swipe 0 255 0 > /dev/null
