#!/bin/sh

CURRENT_DIR=${PWD}

# build the frontend app
mkdir -p tmp
cd tmp
git clone https://github.com/ninoseki/arq-dashboard-frontend.git

cd arq-dashboard-frontend
npm install
npm run build

trash -r ${CURRENT_DIR}/arq_dashboard/frontend/
mkdir -p ${CURRENT_DIR}/arq_dashboard/frontend/
cp -r dist/ ${CURRENT_DIR}/arq_dashboard/frontend/

# remove tmp dir
rm -rf ${CURRENT_DIR}/tmp/arq-dashboard-frontend