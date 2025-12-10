My machine 

```bash
uv pip install --link-mode=copy torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
