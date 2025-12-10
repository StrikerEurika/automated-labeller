# ml_service.py
import torch
from groundingdino.util.inference import load_model, load_image, predict
from segment_anything import sam_model_registry, SamPredictor
import cv2
import numpy as np
from typing import Dict, Tuple, List
import time

class VisionFoundationService:
    def __init__(self, device="cuda"):
        self.device = device
        self.grounding_dino_model = load_model(
            "groundingdino/config/GroundingDINO_SwinT_OGC.py",
            "groundingdino/weights/groundingdino_swint_ogc.pth"
        )
        self.sam_model = sam_model_registry["vit_h"](
            checkpoint="sam_vit_h_4b8939.pth"
        ).to(device)
        self.sam_predictor = SamPredictor(self.sam_model)
    
    async def annotate_image(self, image_path: str, prompt: str) -> Dict:
        start_time = time.time()
        
        # Load and preprocess image
        image_source, image = load_image(image_path)
        
        # Grounding DINO detection
        boxes, logits, phrases = predict(
            model=self.grounding_dino_model,
            image=image,
            caption=prompt,
            box_threshold=0.3,
            text_threshold=0.25
        )
        
        # SAM segmentation
        self.sam_predictor.set_image(image_source)
        transformed_boxes = self.sam_predictor.transform.apply_boxes_torch(
            boxes, image_source.shape[:2]
        )
        masks, _, _ = self.sam_predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes,
            multimask_output=False,
        )
        
        # Format results
        results = {
            "detections": [
                {
                    "bbox": box.tolist(),
                    "confidence": float(conf),
                    "label": label
                }
                for box, conf, label in zip(boxes, logits, phrases)
            ],
            "masks": [
                {
                    "mask": mask.cpu().numpy().tolist(),
                    "bbox": box.tolist()
                }
                for mask, box in zip(masks, boxes)
            ],
            "processing_time": time.time() - start_time
        }
        
        return results
    
    async def batch_process(self, image_paths: List[str], prompt: str) -> List[Dict]:
        results = []
        for img_path in image_paths:
            result = await self.annotate_image(img_path, prompt)
            results.append(result)
        return results