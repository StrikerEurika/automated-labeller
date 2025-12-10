from fastapi import APIRouter, File, UploadFile, Form
from app.models.grounding_dino import GroundingDINO
from app.models.sam import SAM
from PIL import Image
import io
import base64
import numpy as np
import warnings

# Suppress known deprecation warnings from dependencies
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="groundingdino")

router = APIRouter()

# Initialize models (singleton - load once at startup in real app)
# Use CPU to avoid CUDA out of memory errors
g_dino = GroundingDINO("weights/groundingdino/config.py",
                       "weights/groundingdino/groundingdino_swint_ogc.pth", device="cpu")
sam = SAM("weights/sam/sam_vit_h_4b8939.pth", device="cpu")


def mask_to_rle(mask):
    # Optional: compress mask for JSON
    from pycocotools import mask as mask_utils
    return mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))


@router.post("/annotate")
async def annotate(
    image: UploadFile = File(...),
    prompts: str = Form("car, tree")  # comma-separated
):
    contents = await image.read()
    pil_img = Image.open(io.BytesIO(contents)).convert("RGB")

    prompt_list = [p.strip() for p in prompts.split(",") if p.strip()]

    boxes, scores, labels = g_dino.predict(pil_img, prompt_list)
    masks = sam.segment(pil_img, boxes)

    # Convert masks to base64-encoded PNG for preview (simpler than RLE for frontend)
    mask_images = []
    for mask in masks:
        mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
        buf = io.BytesIO()
        mask_img.save(buf, format="PNG")
        mask_b64 = base64.b64encode(buf.getvalue()).decode()
        mask_images.append(mask_b64)

    return {
        "boxes": boxes,
        "scores": scores,
        "labels": labels,
        "masks_b64": mask_images  # frontend can overlay as <img src="data:image/png;base64,...">
    }
