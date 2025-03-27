@echo off

cd backend
./install
./start

cd ../../frontend
npm install
npm run dev