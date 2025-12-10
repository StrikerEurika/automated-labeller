from segment_anything import sam_model_registry, SamPredictor
from PIL import Image
import numpy as np
import torch
from typing import List
from app.models.vision import BaseSegmenter


class SAM(BaseSegmenter):
    def __init__(self, ckpt_path: str, model_type="vit_h", device="cuda"):
        sam = sam_model_registry[model_type](checkpoint=ckpt_path)
        sam.to(device=device)
        self.predictor = SamPredictor(sam)
        self.device = device

    def segment(self, image: Image.Image, boxes: List[List[float]]):
        image_np = np.array(image.convert("RGB"))
        self.predictor.set_image(image_np)
        masks = []

        if not boxes:
            return masks

        input_boxes = torch.tensor(boxes, device=self.device)
        transformed_boxes = self.predictor.transform.apply_boxes_torch(
            input_boxes, image_np.shape[:2])
        masks_raw, _, _ = self.predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes,
            multimask_output=False,
        )

        for mask in masks_raw:
            masks.append(mask[0].cpu().numpy())  # HxW bool array

        return masks
