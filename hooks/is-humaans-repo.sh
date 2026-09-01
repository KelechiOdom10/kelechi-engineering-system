#!/bin/bash

set -eu

root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 1
origin=$(git -C "$root" config --get remote.origin.url 2>/dev/null || true)

case "$origin" in
  git@github.com:humaans/humaans.git|ssh://git@github.com/humaans/humaans.git|https://github.com/humaans/humaans.git|https://github.com/humaans/humaans)
    exit 0
    ;;
esac

exit 1
