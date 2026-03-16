# Real-Time Object Detection & Tracking

Detect and track objects in real-time using YOLOv8 + ByteTrack with live visualization.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Webcam (default)
python main.py

# Video file
python main.py --source path/to/video.mp4

# Larger model for better accuracy
python main.py --model yolov8s.pt

# Track only specific classes
python main.py --classes person car

# Save annotated output
python main.py --output output.mp4

# Adjust confidence threshold
python main.py --confidence 0.5
```

## All CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--source` | `0` | Webcam index or video file path |
| `--model` | `yolov8n.pt` | YOLOv8 model variant (n/s/m/l/x) |
| `--confidence` | `0.35` | Detection confidence threshold |
| `--iou` | `0.45` | NMS IoU threshold |
| `--display-width` | `1280` | Display window width |
| `--display-height` | `720` | Display window height |
| `--output` | None | Save annotated video to file |
| `--classes` | None | Filter to specific object classes |

## Controls

- Press `q` to quit
- `Ctrl+C` for graceful shutdown

## Architecture

```
main.py           → CLI args, pipeline loop, shutdown
config.py         → Centralized parameters (dataclass)
detector.py       → YOLOv8 inference → supervision Detections
tracker.py        → ByteTrack multi-object tracking
annotator.py      → Bounding boxes, labels, traces, FPS
video_source.py   → OpenCV video capture (context manager)
```
