# Automated Labeller

An intelligent image annotation tool powered by AI that combines **Grounding DINO** (zero-shot object detection) and **SAM** (Segment Anything Model) for automated, text-prompt-based image segmentation and annotation.

## Features

- **Text-Prompted Detection**: Use natural language prompts (e.g., "car", "tree", "person") to detect objects
- **High-Quality Segmentation**: Automatic mask generation using Meta's Segment Anything Model
- **Interactive Canvas**: Real-time visualization of bounding boxes and segmentation masks
- **RESTful API**: FastAPI backend with comprehensive API documentation
- **Modern UI**: Vue 3 + Tailwind CSS responsive interface
- **GPU Acceleration**: CUDA support for fast inference (CPU fallback available)

## Architecture

### Tech Stack

**Backend:**

- FastAPI (Python web framework)
- PyTorch (Deep learning framework)
- Grounding DINO (Text-to-detection model)
- Segment Anything Model (Instance segmentation)
- OpenCV & PIL (Image processing)

**Frontend:**

- Vue 3 (Progressive framework)
- Vite (Build tool)
- Tailwind CSS (Styling)
- Axios (HTTP client)

**Infrastructure:**

- Docker & Docker Compose
- systemd (Service management)
- NVIDIA CUDA (GPU support)

### Project Structure

```
automated-labeller/
├── backend/                    # FastAPI + PyTorch Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models/            # ML model wrappers
│   │   │   ├── grounding_dino.py
│   │   │   ├── sam.py
│   │   │   └── vision.py
│   │   └── routes/
│   │       └── annotate.py    # Annotation endpoints
│   ├── weights/               # Model checkpoint files
│   │   ├── groundingdino/
│   │   │   ├── config.py
│   │   │   └── groundingdino_swint_ogc.pth (662MB)
│   │   └── sam/
│   │       └── sam_vit_h_4b8939.pth (2.4GB)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                   # Vue 3 Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnnotationCanvas.vue
│   │   │   ├── Canvas.vue
│   │   │   └── GeospatialMap.vue
│   │   ├── views/
│   │   │   └── AnnotateView.vue
│   │   ├── api/
│   │   │   └── client.ts      # API client
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── notes/                      # Development documentation
├── systemd/                    # System service files
├── dokcer-compose.yml         # Docker orchestration
└── README.md
```

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

### Required Software

- **Python 3.12+** (tested with Python 3.14.2)
- **Node.js 20.19.0+ or 22.12.0+** (tested with v22.20.0)
- **npm 10.0+** (tested with v10.9.3)
- **Git** (for cloning and dependencies)
- **pip** (Python package manager)

### Optional (for GPU acceleration)

- **NVIDIA GPU** with CUDA support
- **CUDA Toolkit 11.8+**
- **NVIDIA Container Toolkit** (for Docker GPU support)

### System Requirements

- **RAM**: 16GB minimum (8GB for models + 8GB for system)
- **Disk Space**: ~10GB (3GB for model weights + dependencies)
- **OS**: Linux (Fedora/Ubuntu/Debian), macOS, Windows with WSL2

---

## Complete Setup Guide

This guide will walk you through setting up the project from scratch. Follow these steps carefully to ensure a working installation.

### Step 1: Clone the Repository

```bash
git clone https://github.com/StrikerEurika/automated-labeller.git
cd automated-labeller
```

### Step 2: Download Model Weights

The models require large checkpoint files that are not included in the repository. Download them manually:

#### 2.1. Create Weights Directories

```bash
mkdir -p backend/weights/groundingdino
mkdir -p backend/weights/sam
```

#### 2.2. Download Grounding DINO Weights (662MB)

```bash
cd backend/weights/groundingdino

# Download the model checkpoint
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

# Create the config file (or copy from the project if it exists)
# The config.py file should already be in the repository
cd ../../..
```

**Alternative manual download:** Visit [Grounding DINO Releases](https://github.com/IDEA-Research/GroundingDINO/releases) and download `groundingdino_swint_ogc.pth`

#### 2.3. Download SAM Weights (2.4GB)

```bash
cd backend/weights/sam

# Download the SAM ViT-H model
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

cd ../../..
```

**Alternative manual download:** Visit [SAM Checkpoints](https://github.com/facebookresearch/segment-anything#model-checkpoints) and download `sam_vit_h_4b8939.pth`

#### 2.4. Verify Downloads

```bash
ls -lh backend/weights/groundingdino/
# Should show: groundingdino_swint_ogc.pth (~662MB)

ls -lh backend/weights/sam/
# Should show: sam_vit_h_4b8939.pth (~2.4GB)
```

### Step 3: Backend Setup

#### 3.1. Create Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows
```

**Important:** Always activate the virtual environment before running backend commands!

#### 3.2. Install PyTorch (CUDA 11.8 or CPU)

Choose the appropriate installation based on your GPU availability:

**For CUDA 11.8+ (GPU acceleration):**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For CPU only (no GPU):**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**For CUDA 12.1+ (newer GPUs):**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### 3.3. Install Core Dependencies

```bash
# Install FastAPI and essential packages
pip install fastapi uvicorn python-multipart Pillow opencv-python numpy
```

#### 3.4. Install AI Model Dependencies

These require git and may take a few minutes:

```bash
# Install Grounding DINO from GitHub
pip install git+https://github.com/IDEA-Research/GroundingDINO.git

# Install Segment Anything from GitHub
pip install git+https://github.com/facebookresearch/segment-anything.git
```

**Troubleshooting:**

- If `GroundingDINO` installation fails with version errors, try:
  ```bash
  pip install git+https://github.com/IDEA-Research/GroundingDINO.git@main
  ```
- Ensure you have `gcc`, `g++`, and `python-dev` installed for compiling extensions
- On Ubuntu/Debian: `sudo apt-get install build-essential python3-dev`
- On Fedora: `sudo dnf install gcc gcc-c++ python3-devel`

#### 3.5. Verify Installation

```bash
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
```

Expected output:

```
PyTorch: 2.x.x+cu118  (or +cpu)
CUDA Available: True  (or False for CPU)
```

```bash
python3 -c "from groundingdino.util.inference import load_model; from segment_anything import sam_model_registry; print('✓ All models imported successfully!')"
```

#### 3.6. Test Backend Server

```bash
# From backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test the API:**

- Open browser: `http://localhost:8000/docs` (Interactive API documentation)
- You should see the FastAPI Swagger UI with `/api/v1/annotate` endpoint

Press `Ctrl+C` to stop the server for now.

### Step 4: Frontend Setup

Open a **new terminal** (keep backend terminal available for later).

#### 4.1. Install Node Dependencies

```bash
cd frontend  # From project root

# Install all dependencies
npm install
```

This will install:

- Vue 3
- Vite
- Tailwind CSS
- Axios
- Other dev dependencies

#### 4.2. Verify Installation

```bash
npm list --depth=0
```

Should show all dependencies including:

- `vue@^3.5.25`
- `axios@^1.7.7`
- `vite@^7.2.4`

#### 4.3. Test Frontend Development Server

```bash
npm run dev
```

You should see:

```
VITE v7.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Test the frontend:**

- Open browser: `http://localhost:5173`
- You should see the Vue app interface

Press `Ctrl+C` to stop the server.

### Step 5: Run the Complete Application

Now run both backend and frontend together.

#### 5.1. Start Backend (Terminal 1)

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5.2. Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

#### 5.3. Access the Application

1. Open browser: **http://localhost:5173**
2. You should see the Automated Labeller interface
3. Upload an image
4. Enter text prompts (e.g., "car, tree, person")
5. Click "Auto-Annotate"
6. View the detected objects and segmentation masks

### Step 6: Verify Everything Works

**Test the annotation pipeline:**

1. **Upload a test image** (use any image with common objects)
2. **Enter prompts:** `car, tree, building, person`
3. **Submit** and wait for processing
4. **Check results:** You should see bounding boxes and masks overlaid on the image

**Debugging checklist if it doesn't work:**

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] No CORS errors in browser console (F12 → Console)
- [ ] Model weights exist in `backend/weights/` directories
- [ ] Virtual environment activated in backend terminal

---

## Docker Deployment (Alternative Setup)

For production or easier deployment, use Docker Compose:

### Prerequisites for Docker

- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Container Toolkit (for GPU support)

### Build and Run

```bash
# From project root
docker-compose up --build
```

This will:

- Build backend image with CUDA support
- Build frontend image with Nginx
- Start both services with proper networking
- Mount model weights from `backend/weights/`

**Access:**

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Note:** The docker-compose.yml expects NVIDIA GPU. For CPU-only:

1. Remove the `runtime: nvidia` line
2. Remove the `deploy.resources.reservations` section
3. Update backend code to use `device="cpu"`

---

## API Documentation

### Endpoint: POST /api/v1/annotate

Annotates an image based on text prompts.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameters:
  - `image` (file): Image file (JPEG, PNG)
  - `prompts` (string): Comma-separated text prompts (e.g., "car, tree")

**Response:**

```json
{
  "detections": [
    {
      "label": "car",
      "box": [x1, y1, x2, y2],
      "score": 0.95,
      "mask_base64": "iVBORw0KGg..."
    }
  ]
}
```

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/api/v1/annotate" \
  -F "image=@test.jpg" \
  -F "prompts=car,tree,person"
```

**Interactive Docs:** Visit `http://localhost:8000/docs` for full API testing interface.

---

## Configuration

### Backend Configuration

**CORS Origins** (`backend/app/main.py`):

```python
allow_origins=["http://localhost:8080", "http://localhost:5173"]
```

**Model Device** (`backend/app/routes/annotate.py`):

```python
g_dino = GroundingDINO(..., device="cpu")  # Change to "cuda" for GPU
sam = SAM(..., device="cpu")  # Change to "cuda" for GPU
```

**Detection Thresholds** (`backend/app/models/grounding_dino.py`):

```python
box_threshold=0.35  # Bounding box confidence threshold
text_threshold=0.25  # Text prompt matching threshold
```

### Frontend Configuration

**API Base URL** (`frontend/src/api/client.ts`):

```typescript
baseURL: "http://localhost:8000/api/v1";
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'groundingdino'"

**Solution:** Install from GitHub:

```bash
pip install git+https://github.com/IDEA-Research/GroundingDINO.git@main
```

#### 2. "CUDA out of memory"

**Solution:** Switch to CPU mode:

```python
# In backend/app/routes/annotate.py
g_dino = GroundingDINO(..., device="cpu")
sam = SAM(..., device="cpu")
```

Or reduce batch size / image resolution.

#### 3. "CORS policy" error in browser

**Solution:** Ensure backend CORS includes your frontend URL:

```python
allow_origins=["http://localhost:5173"]  # Add your port
```

#### 4. Model weights not found

**Error:** `FileNotFoundError: weights/groundingdino/...`

**Solution:** Download weights as described in Step 2, ensure they're in:

- `backend/weights/groundingdino/groundingdino_swint_ogc.pth`
- `backend/weights/sam/sam_vit_h_4b8939.pth`

#### 5. Port already in use

**Backend (8000):**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001  # Use different port
```

**Frontend (5173):**
Vite will automatically use next available port (5174, 5175, etc.)

#### 6. Slow inference / timeout

**Solutions:**

- Use GPU instead of CPU
- Reduce image size before upload
- Increase timeout in `frontend/src/api/client.ts`:
  ```typescript
  timeout: 120000; // 2 minutes
  ```

---

## Development Workflow

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm run test
```

### Code Structure Guidelines

- **Backend models** are in `backend/app/models/`
- **API routes** are in `backend/app/routes/`
- **Frontend components** are in `frontend/src/components/`
- **API client** logic is in `frontend/src/api/client.ts`

### Making Changes

1. **Backend changes:** Auto-reload is enabled with `--reload` flag
2. **Frontend changes:** Hot Module Replacement (HMR) is automatic
3. **Model changes:** Restart backend server to reload models

---

## systemd Service (Linux)

To run as a system service on Linux:

1. **Edit service file:**

```bash
sudo nano /etc/systemd/system/autoannotate.service
```

2. **Copy content from** `systemd/autoannotate.service` and update:

   - `WorkingDirectory` to your project path
   - `User` to your username

3. **Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable autoannotate
sudo systemctl start autoannotate
sudo systemctl status autoannotate
```

---

## Project Dependencies Summary

### Backend (Python)

```
fastapi         - Web framework
uvicorn         - ASGI server
torch           - Deep learning framework
torchvision     - Computer vision utilities
groundingdino   - Zero-shot detection model
segment-anything - Instance segmentation
Pillow          - Image processing
opencv-python   - Computer vision
numpy           - Numerical computing
```

### Frontend (Node.js)

```
vue             - Progressive framework
vite            - Build tool
axios           - HTTP client
tailwindcss     - CSS framework
vue-router      - Routing
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is for educational and research purposes.

**Model Licenses:**

- [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) - Apache 2.0
- [Segment Anything](https://github.com/facebookresearch/segment-anything) - Apache 2.0

---

## Acknowledgments

- **Grounding DINO** by IDEA Research
- **Segment Anything Model (SAM)** by Meta AI
- FastAPI and Vue.js communities

---

## Support

For issues and questions:

- GitHub Issues: [Create an issue](https://github.com/StrikerEurika/automated-labeller/issues)
- Documentation: See `notes/` directory for detailed development notes

---

## Honestness

This project is 90% generated by AI (ChatGPT-4) and 10% human-edited. Use responsibly and verify results. The most problems I solved myself were related to dependency management and model integration. I want to be transparent about the AI assistance in this project.

**Happy Annotating!**
