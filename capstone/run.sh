#!/bin/bash
set -eux
set -o pipefail

./setup.sh
export FLASK_APP=app
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=debug
flask run --reload