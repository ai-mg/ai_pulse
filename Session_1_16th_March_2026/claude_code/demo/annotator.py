import numpy as np
import supervision as sv


class FrameAnnotator:
    def __init__(self, class_names: dict, trace_length: int = 60):
        self.class_names = class_names
        self.box_annotator = sv.BoxAnnotator(thickness=2)
        self.label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
        self.trace_annotator = sv.TraceAnnotator(
            thickness=2, trace_length=trace_length
        )

    def annotate(
        self, frame: np.ndarray, detections: sv.Detections
    ) -> np.ndarray:
        labels = self._build_labels(detections)

        annotated = self.box_annotator.annotate(
            scene=frame.copy(), detections=detections
        )
        annotated = self.label_annotator.annotate(
            scene=annotated, detections=detections, labels=labels
        )
        annotated = self.trace_annotator.annotate(
            scene=annotated, detections=detections
        )
        return annotated

    def _build_labels(self, detections: sv.Detections) -> list[str]:
        labels = []
        for i in range(len(detections)):
            class_id = (
                detections.class_id[i] if detections.class_id is not None else -1
            )
            class_name = self.class_names.get(class_id, "unknown")
            confidence = (
                detections.confidence[i]
                if detections.confidence is not None
                else 0.0
            )
            tracker_id = (
                detections.tracker_id[i]
                if detections.tracker_id is not None
                else "?"
            )
            labels.append(f"#{tracker_id} {class_name} {confidence:.2f}")
        return labels
