from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    model_name: str = "yolov8n.pt"
    confidence_threshold: float = 0.35
    iou_threshold: float = 0.45
    track_activation_threshold: float = 0.25
    lost_track_buffer: int = 30
    minimum_matching_threshold: float = 0.8
    frame_rate: int = 30
    minimum_consecutive_frames: int = 1
    input_source: str = "0"
    display_width: int = 1280
    display_height: int = 720
    trace_length: int = 60
    output_path: Optional[str] = None
    classes: list[str] = field(default_factory=list)

    @classmethod
    def from_args(cls, args) -> "Config":
        config = cls(
            model_name=args.model,
            confidence_threshold=args.confidence,
            iou_threshold=args.iou,
            input_source=args.source,
            display_width=args.display_width,
            display_height=args.display_height,
            output_path=args.output,
            classes=args.classes if args.classes else [],
        )
        return config

    @property
    def video_source(self):
        """Return int for webcam index or str for file path."""
        if self.input_source.isdigit():
            return int(self.input_source)
        return self.input_source
