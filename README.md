Project Structure

```bash
autoannotate/
├── backend/                 # FastAPI + PyTorch
│   ├── app/
│   │   ├── main.py
│   │   ├── models/          # GroundingDINO, SAM wrappers
│   │   ├── schemas.py       # Pydantic models
│   │   ├── routes/
│   │   │   ├── annotate.py
│   │   │   └── batch.py
│   │   └── utils/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                # Vue 3 + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── Canvas.vue
│   │   │   └── PromptPanel.vue
│   │   ├── views/
│   │   │   └── AnnotateView.vue
│   │   ├── api/
│   │   │   └── client.ts    # Axios API wrapper
│   │   └── main.ts
│   ├── Dockerfile
│   └── tailwind.config.js
│
├── docker-compose.yml
├── systemd/autoannotate.service
└── README.md
``` 

