import argparse
import logging
import signal
import sys
import time

import cv2

from annotator import FrameAnnotator
from config import Config
from detector import ObjectDetector
from tracker import ObjectTracker
from video_source import VideoSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

_shutdown = False


def _signal_handler(signum, frame):
    global _shutdown
    logger.info("Received signal %s, shutting down...", signum)
    _shutdown = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time object detection and tracking with YOLOv8 + ByteTrack"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source: webcam index (0, 1, ...) or path to video file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="YOLOv8 model variant (default: yolov8n.pt)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.35,
        help="Detection confidence threshold (default: 0.35)",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="NMS IoU threshold (default: 0.45)",
    )
    parser.add_argument(
        "--display-width",
        type=int,
        default=1280,
        help="Display window width (default: 1280)",
    )
    parser.add_argument(
        "--display-height",
        type=int,
        default=720,
        help="Display window height (default: 720)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save annotated output video (e.g., output.mp4)",
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        type=str,
        default=None,
        help="Filter to specific classes (e.g., --classes person car)",
    )
    return parser.parse_args()


def run(config: Config):
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    with VideoSource(config.video_source) as source:
        detector = ObjectDetector(
            config.model_name, config.confidence_threshold, config.iou_threshold
        )
        tracker_obj = ObjectTracker(
            track_activation_threshold=config.track_activation_threshold,
            lost_track_buffer=config.lost_track_buffer,
            minimum_matching_threshold=config.minimum_matching_threshold,
            frame_rate=config.frame_rate,
            minimum_consecutive_frames=config.minimum_consecutive_frames,
        )
        annotator = FrameAnnotator(
            detector.get_class_names(), config.trace_length
        )

        writer = None
        if config.output_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(
                config.output_path,
                fourcc,
                source.fps,
                (config.display_width, config.display_height),
            )
            logger.info("Recording output to: %s", config.output_path)

        try:
            for frame in source:
                if _shutdown:
                    break

                t_start = time.perf_counter()

                detections = detector.detect(frame)
                detections = detector.filter_classes(detections, config.classes)
                tracked = tracker_obj.update(detections)

                annotated = annotator.annotate(frame, tracked)
                annotated = cv2.resize(
                    annotated, (config.display_width, config.display_height)
                )

                elapsed = time.perf_counter() - t_start
                fps = 1.0 / elapsed if elapsed > 0 else 0.0
                cv2.putText(
                    annotated,
                    f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2,
                )

                if writer is not None:
                    writer.write(annotated)

                cv2.imshow("Object Detection & Tracking", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            if writer is not None:
                writer.release()
                logger.info("Output saved to: %s", config.output_path)
            cv2.destroyAllWindows()
            logger.info("Shutdown complete.")


def main():
    args = parse_args()
    config = Config.from_args(args)
    logger.info("Starting with config: %s", config)
    run(config)


if __name__ == "__main__":
    main()
