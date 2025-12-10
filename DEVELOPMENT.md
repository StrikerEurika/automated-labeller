# Local Development Setup

This guide will help you run the project locally for development.

## Project Overview

This is a full-stack application with:

- **Backend**: FastAPI + PyTorch (GroundingDINO + SAM models)
- **Frontend**: Vue 3 + Vite

## Prerequisites

- Python 3.12+
- Node.js 20.19.0+ or 22.12.0+
- Git
- CUDA 11.8+ (optional, for GPU support)

## Backend Setup

### 1. Set up Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

The project uses Git-based dependencies that need special handling:

```bash
# Install PyTorch first (with CUDA 11.8 support)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install fastapi uvicorn python-multipart Pillow supervision==0.15.0

# Install GroundingDINO and SAM from GitHub
pip install git+https://github.com/IDEA-Research/GroundingDINO.git
pip install git+https://github.com/facebookresearch/segment-anything.git
```

**Note**: If you encounter issues with the GroundingDINO version tag, use:

```bash
pip install git+https://github.com/IDEA-Research/GroundingDINO.git@main
```

### 3. Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); import grounding_dino; import sam2; print('All imports successful!')"
```

### 4. Run Backend Server

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc docs: `http://localhost:8000/redoc`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend

# Install Node dependencies
npm install
```

### 2. Run Development Server

```bash
# From the frontend directory
npm run dev
```

The frontend will be available at: `http://localhost:5173` (or another port if 5173 is busy)

### 3. Build for Production

```bash
npm run build
npm run preview  # Preview the production build
```

---

## Running Both Services Together

### Option 1: Two Terminal Windows (Recommended for Development)

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

Then open your browser to `http://localhost:5173`

### Option 2: Docker Compose (For Production-like Environment)

```bash
# From project root
docker-compose up
```

This will:

- Build and run the backend on `http://localhost:8000`
- Build and run the frontend on `http://localhost:8080`
- Automatically set up networking between services

---

## API Endpoints

The backend provides the following endpoints:

- `GET /api/v1/health` - Health check
- `POST /api/v1/annotate` - Annotate image with prompt
- Other endpoints defined in `backend/app/routes/`

Check the interactive docs at `http://localhost:8000/docs` for full API specification.

---

## Troubleshooting

### Issue: Git dependency installation fails

**Solution**: Update the dependencies in `requirements.txt` to use available branches:

```bash
pip install git+https://github.com/IDEA-Research/GroundingDINO.git@main
```

### Issue: CUDA/GPU not detected

**Solution**:

- Verify CUDA installation: `nvidia-smi`
- Install CPU-only PyTorch if GPU unavailable:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Port already in use

**Change port in backend**:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Change port in frontend** (Vite will auto-detect):

- Just run `npm run dev` and it will use the next available port

### Issue: CORS errors

The backend CORS is configured to allow:

- `http://localhost:8080`
- `http://localhost:5173`

If using different ports, update `backend/app/main.py`:

```python
allow_origins=["http://localhost:YOUR_PORT"]
```

---

## Development Workflow

1. **Backend changes**: The `--reload` flag auto-restarts the server
2. **Frontend changes**: Vite's HMR automatically refreshes the browser
3. **Model changes**: Restart the backend server if you modify `app/models/`
4. **Routes changes**: No restart needed for route changes with `--reload`

---

## Project Structure

```
automated-labeller/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app setup
│   │   ├── models/            # ML models (GroundingDINO, SAM)
│   │   └── routes/            # API endpoints
│   ├── weights/               # Pre-trained model weights
│   └── requirements.txt
│
├── frontend/                   # Vue 3 + Vite application
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page views
│   │   ├── api/               # API client (client.ts)
│   │   └── main.js            # Entry point
│   └── package.json
│
├── docker-compose.yml         # Docker configuration
└── systemd/                   # Systemd service file
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [GroundingDINO GitHub](https://github.com/IDEA-Research/GroundingDINO)
- [Segment Anything GitHub](https://github.com/facebookresearch/segment-anything)
