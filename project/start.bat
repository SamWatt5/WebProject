@echo off



cd backend
./install
./start

cd ../backend
npm install
npm run dev