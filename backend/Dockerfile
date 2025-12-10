FROM nvidia/cuda:11.8-devel-fedora38

RUN dnf install -y python3 python3-pip git && dnf clean all

WORKDIR /app

COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Download model weights (or mount at runtime)
# RUN mkdir -p weights/groundingdino weights/sam
# RUN wget -O weights/groundingdino/groundingdino_swint_ogc.pth https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0/groundingdino_swint_ogc.pth
# RUN wget -O weights/sam/sam_vit_h_4b8939.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]