import logging

import numpy as np
import supervision as sv
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class ObjectDetector:
    def __init__(self, model_name: str, confidence: float, iou: float):
        self.model = YOLO(model_name)
        self.confidence = confidence
        self.iou = iou
        logger.info("Loaded model: %s (device: %s)", model_name, self.model.device)

    def detect(self, frame: np.ndarray) -> sv.Detections:
        results = self.model(
            frame, conf=self.confidence, iou=self.iou, verbose=False
        )[0]
        return sv.Detections.from_ultralytics(results)

    def get_class_names(self) -> dict:
        return self.model.names

    def filter_classes(
        self, detections: sv.Detections, allowed_classes: list[str]
    ) -> sv.Detections:
        if not allowed_classes:
            return detections
        names = self.get_class_names()
        allowed_ids = {
            cid for cid, name in names.items() if name in allowed_classes
        }
        if detections.class_id is None or len(detections) == 0:
            return detections
        mask = np.array([cid in allowed_ids for cid in detections.class_id])
        return detections[mask]
