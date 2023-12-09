#!/bin/bash
# auth setup
export AUTH0_DOMAIN="ramgopalsiddh.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone"

export DATABASE_URL="postgresql://ram@localhost:5432/capstone"
# export DATABASE_URL="postgres:///capstone"
export FLASK_APP=app
export EXCITED="true"
export FLASK_ENVIRONMENT=debug

# message show after run script successfully
echo "setup.sh script executed successfully!"