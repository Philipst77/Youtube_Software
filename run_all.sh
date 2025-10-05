#!/bin/bash
echo "🚀 Starting Flask backend..."
cd "$(dirname "$0")/Youtube_Software/backend"
source .venv/bin/activate
python3 app.py &
BACKEND_PID=$!

echo "🌐 Starting Vite frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait a few seconds to make sure both servers start
sleep 5

# 🌍 Auto-open browser to frontend
if command -v wslview &> /dev/null; then
  wslview "http://localhost:5173"
elif command -v xdg-open &> /dev/null; then
  xdg-open "http://localhost:5173"
elif command -v open &> /dev/null; then
  open "http://localhost:5173"
else
  echo "🌐 Please open http://localhost:5173 manually"
fi


echo ""
echo "✅ Both backend and frontend are running!"
echo "Backend: http://127.0.0.1:5001"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both."

# Wait for processes to end
wait $BACKEND_PID $FRONTEND_PID
