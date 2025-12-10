# Frontend-Backend Integration Fixes

## Issues Found and Fixed

### 1. **Missing Axios Dependency**

- **Problem**: Frontend was trying to use axios without installing it
- **Fix**: Added `axios@^1.7.7` to `frontend/package.json` dependencies
- **Action**: Ran `npm install` to install the package

### 2. **Incorrect API Base URL**

- **Problem**: Frontend API client was calling `http://localhost:8000` directly, but backend routes are registered under `/api/v1` prefix
  - Frontend was calling: `/annotate`
  - Should call: `/api/v1/annotate`
- **Fix**: Updated `frontend/src/api/client.ts` to use `http://localhost:8000/api/v1` as base URL
- **Result**: Now when frontend calls `/annotate`, it correctly reaches `http://localhost:8000/api/v1/annotate`

### 3. **Missing Type Imports in Backend Models**

- **Problem**:
  - `grounding_dino.py` was missing `from typing import List, Tuple`
  - `sam.py` was missing `import torch` and `from typing import List`
  - Both were missing imports for base classes
- **Fix**: Added all missing imports to both files

### 4. **Incorrect Image Processing in GroundingDINO**

- **Problem**: Code was calling `self._image_preprocess()` which doesn't exist
- **Fix**: Changed to use numpy array directly from PIL Image, which matches the GroundingDINO API

### 5. **Improved Error Handling**

- **Problem**: Frontend error alerts were not informative
- **Fix**: Updated error message to display actual error details for easier debugging

## How to Test

### Terminal 1 - Backend:

```bash
cd backend
source venv/bin/activate  # or .venv/bin/activate on your system
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:

```bash
cd frontend
npm run dev
```

### Browser:

1. Open `http://localhost:5173` (or whatever port Vite shows)
2. Upload an image
3. Enter prompts (e.g., "car, tree")
4. Click "Auto-Annotate"
5. Should see annotations appear on the canvas

## Configuration

**Frontend → Backend Communication:**

- Frontend API calls go to: `http://localhost:8000/api/v1`
- CORS is configured on backend to allow:
  - `http://localhost:8080`
  - `http://localhost:5173`

If you change ports, update:

1. Frontend base URL in `frontend/src/api/client.ts`
2. Backend CORS origins in `backend/app/main.py`

## Next Steps if Issues Persist

1. **Check backend logs**: Look for any errors in the terminal where backend is running
2. **Check browser console**: Open DevTools (F12) → Console tab for frontend errors
3. **Test API directly**: Visit `http://localhost:8000/docs` to test the API endpoints manually
4. **Check CORS headers**: Make sure the OPTIONS request returns proper CORS headers
