from abc import ABC
from typing import List, Tuple

import torch


class BaseDetector(ABC):
    def detect(
        self, images: List[torch.Tensor]
    ) -> List[List[Tuple[int, int, int, int]]]:
        raise NotImplementedError


class BaseSegmenter(ABC):
    def segment(self, image, boxes: List) -> List:
        raise NotImplementedError
