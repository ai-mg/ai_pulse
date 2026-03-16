# Real-Time Object Detection & Tracking System — Implementation Plan

## Summary
Build a Python application that captures video from a webcam or file, runs YOLOv8 detection, tracks objects across frames with persistent IDs using ByteTrack, and displays annotated live video with bounding boxes, labels, confidence scores, tracking IDs, motion traces, and FPS.

## Files to Create

| File | Responsibility |
|------|----------------|
| `requirements.txt` | Pinned dependencies |
| `config.py` | Centralized tunable parameters (dataclass) with `from_args()` bridge |
| `detector.py` | YOLOv8 model loading + inference → `sv.Detections` |
| `tracker.py` | ByteTrack wrapper for persistent tracking IDs |
| `annotator.py` | Draws boxes, labels, traces, FPS overlay (receives FPS as param) |
| `video_source.py` | OpenCV VideoCapture abstraction — iterator + context manager |
| `main.py` | Entry point: argparse, pipeline orchestration, graceful shutdown |
| `.gitignore` | Ignore `__pycache__/`, `*.pt`, `*.pyc` |
| `README.md` | Usage docs |

## Key Architecture Decisions
1. **YOLOv8n** (nano) as default — fastest variant, configurable via `--model`
2. **ByteTrack** via `supervision` — zero extra deps, fast IoU-based tracking
3. **supervision** for annotation — production-quality box/label/trace annotators
4. **Modular structure** — single-responsibility files, easy to swap components
5. **Synchronous pipeline** — sufficient for YOLOv8n + GPU (60+ FPS)

## Implementation Steps
1. Create `requirements.txt` with tightly pinned versions → `pip install`
2. Create `config.py` with dataclass + `from_args()` method
3. Create `video_source.py` — context manager + iterator, validates source
4. Create `detector.py` — YOLOv8 wrapper with `detect(frame)` method
5. Create `tracker.py` — ByteTrack wrapper with `update(detections)` method
6. Create `annotator.py` — annotation layer (FPS passed in, not computed)
7. Create `main.py` — argparse with `--source`, `--model`, `--confidence`, `--output`, `--classes` flags; frame loop with FPS timing; signal handling; `try/finally` cleanup
8. Create `.gitignore` and `README.md`
9. End-to-end test with webcam and video file

## Dependencies
| Package | Version | Status |
|---------|---------|--------|
| `ultralytics` | ==8.3.0 | Must install |
| `supervision` | ==0.27.0 | Already installed |
| `opencv-python` | >=4.8.0 | Already installed |
| `numpy` | >=1.24.0 | Already installed |
| `torch` / `torchvision` | 2.8.0 / 0.23.0 | Already installed |

## Risks & Mitigations
- **No webcam** → `VideoSource` checks `cap.isOpened()`, raises `RuntimeError`
- **No GPU** → auto CPU fallback, warning logged
- **OpenCV conflict** → runtime check for `cv2.imshow` availability
- **High-res input** → resize before annotation, not just inference
- **Tracker drift** → tunable `lost_track_buffer` and matching thresholds
- **Long sessions** → trace length capped via config parameter
- **Shutdown** → `signal.SIGINT` handler + `try/finally` + context manager

## Review Verdict: **Approved with suggestions** (all incorporated above)
Key improvements from review: tighter version pinning, context manager for video source, FPS computed in main loop, config-to-argparse bridge via `from_args()`, `.gitignore`, `--output` and `--classes` CLI flags.
