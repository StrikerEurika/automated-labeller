import torch
from typing import List, Tuple
from groundingdino.util.inference import load_model, load_image, predict
from groundingdino.util import box_ops
from PIL import Image
import numpy as np
from app.models.vision import BaseDetector


class GroundingDINO(BaseDetector):
    def __init__(self, config_path: str, ckpt_path: str, device="cuda"):
        self.model = load_model(config_path, ckpt_path, device=device)
        self.device = device

    def predict(self, image: Image.Image, prompts: List[str], box_threshold=0.35, text_threshold=0.25):
        # Prepare image
        image_np = np.array(image.convert("RGB"))

        # Join prompts with periods
        text_prompt = ". ".join(prompts) + "." if prompts else ""

        # Predict boxes
        boxes, logits, phrases = predict(
            model=self.model,
            image=image_np,
            caption=text_prompt,
            box_threshold=box_threshold,
            text_threshold=text_threshold
        )

        # Convert boxes from normalized [0,1] to pixel coordinates
        if len(boxes) > 0:
            W, H = image.size
            boxes = boxes * torch.Tensor([W, H, W, H]).to(self.device)
            boxes = box_ops.box_cxcywh_to_xyxy(boxes).tolist()
        else:
            boxes = []

        return boxes, logits.tolist(), phrases
