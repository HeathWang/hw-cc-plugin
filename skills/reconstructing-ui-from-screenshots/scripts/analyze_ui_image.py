#!/usr/bin/env python3
"""Measure colors, bounds, and component candidates in a UI reference image."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw


MAX_RELATIVE_SCALE_DELTA = 0.0025


def parse_dimensions(value: str) -> tuple[float, float]:
    normalized = value.lower().replace("×", "x")
    parts = normalized.split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("dimensions must use WIDTHxHEIGHT")

    try:
        width, height = (float(part) for part in parts)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "dimensions must contain numeric values"
        ) from error

    if not all(math.isfinite(number) for number in (width, height)):
        raise argparse.ArgumentTypeError("dimensions must be finite")
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("dimensions must be positive")
    return width, height


def parse_frame(value: str) -> tuple[float, float, float, float]:
    parts = value.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "reference frame must use X,Y,WIDTH,HEIGHT"
        )
    try:
        x, y, width, height = (float(part) for part in parts)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "reference frame must contain numeric values"
        ) from error

    if not all(math.isfinite(number) for number in (x, y, width, height)):
        raise argparse.ArgumentTypeError("reference frame values must be finite")
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError(
            "reference frame width and height must be positive"
        )
    return x, y, width, height


def positive_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("value must be finite and positive")
    return number


def color_count(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 256:
        raise argparse.ArgumentTypeError("colors must be between 1 and 256")
    return number


def load_rgba(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGBA")


def visible_bbox(image: Image.Image) -> list[int] | None:
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 0 else 0).getbbox()
    return list(bbox) if bbox else None


def dominant_colors(image: Image.Image, count: int) -> list[dict[str, Any]]:
    rgba = np.asarray(image)
    visible = rgba[:, :, 3] > 0
    pixels = rgba[:, :, :3][visible]
    if pixels.size == 0:
        return []

    stride = max(1, math.ceil(len(pixels) / 100_000))
    sample = pixels[::stride].reshape((-1, 1, 3)).astype(np.uint8)
    quantized = Image.fromarray(sample, mode="RGB").quantize(
        colors=count,
        method=Image.Quantize.MEDIANCUT,
    )
    palette = quantized.getpalette()
    total = sample.shape[0]
    colors: list[dict[str, Any]] = []
    for pixel_count, palette_index in quantized.getcolors(maxcolors=total) or []:
        offset = palette_index * 3
        rgb = palette[offset : offset + 3]
        colors.append(
            {
                "hex": "#" + "".join(f"{channel:02X}" for channel in rgb),
                "rgb": rgb,
                "share": round(pixel_count / total, 6),
            }
        )
    return sorted(colors, key=lambda item: item["share"], reverse=True)


def component_boxes(image: Image.Image) -> list[list[int]]:
    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    image_area = image.width * image.height
    minimum_area = max(16, round(image_area * 0.00005))
    boxes: list[list[int]] = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        area = width * height
        if area < minimum_area or area > image_area * 0.98:
            continue
        boxes.append([x, y, width, height])
    boxes.sort(key=lambda box: (box[1], box[0], -box[2] * box[3]))
    return boxes[:200]


def coordinate_mapping(
    image_size: tuple[int, int],
    viewport: tuple[float, float] | None,
    dpr: float | None,
    reference_frame: tuple[float, float, float, float] | None = None,
) -> dict[str, Any]:
    if any(number <= 0 or not math.isfinite(number) for number in image_size):
        raise ValueError("image dimensions must be finite and positive")
    if viewport is not None and any(
        number <= 0 or not math.isfinite(number) for number in viewport
    ):
        raise ValueError("viewport dimensions must be finite and positive")
    if dpr is not None and (dpr <= 0 or not math.isfinite(dpr)):
        raise ValueError("DPR must be finite and positive")

    dpr_report: dict[str, Any] = {
        "status": "provided" if dpr is not None else "unconfirmed",
        "value": dpr,
        "matches_image_scale": None,
    }
    report: dict[str, Any] = {
        "status": "needs_confirmation",
        "reference_size_px": list(image_size),
        "target_viewport_logical": list(viewport) if viewport else None,
        "reference_frame_logical": None,
        "reference_frame_source": None,
        "logical_origin": None,
        "image_to_layout_scale": None,
        "device_dpr": dpr_report,
        "conversion_note": (
            "Target viewport is missing. Do not copy image pixels into layout "
            "constants or infer device DPR from image dimensions."
        ),
        "warnings": [
            "Provide --viewport WIDTHxHEIGHT before converting image pixels "
            "to logical layout units."
        ],
    }
    if viewport is None:
        return report

    frame = reference_frame or (0.0, 0.0, viewport[0], viewport[1])
    if any(not math.isfinite(number) for number in frame):
        raise ValueError("reference frame values must be finite")
    frame_x, frame_y, frame_width, frame_height = frame
    if frame_width <= 0 or frame_height <= 0:
        raise ValueError("reference frame width and height must be positive")

    scale_x = image_size[0] / frame_width
    scale_y = image_size[1] / frame_height
    if not math.isfinite(scale_x) or not math.isfinite(scale_y):
        raise ValueError("image-to-layout scale must be finite")
    relative_delta = abs(scale_x - scale_y) / max(scale_x, scale_y)
    is_uniform = relative_delta <= MAX_RELATIVE_SCALE_DELTA
    frame_within_viewport = (
        frame_x >= 0
        and frame_y >= 0
        and frame_x + frame_width <= viewport[0]
        and frame_y + frame_height <= viewport[1]
    )
    conversion_ready = is_uniform and frame_within_viewport
    average_scale = (scale_x + scale_y) / 2 if is_uniform else None
    dpr_matches = (
        dpr is not None
        and abs(scale_x - dpr) / dpr <= MAX_RELATIVE_SCALE_DELTA
        and abs(scale_y - dpr) / dpr <= MAX_RELATIVE_SCALE_DELTA
    )
    dpr_report["matches_image_scale"] = dpr_matches if dpr is not None else None

    warnings = [
        "Image-to-layout scale describes this file's resampling or export "
        "scale; it is not device DPR unless independently confirmed."
    ]
    if not is_uniform:
        warnings.append(
            "Horizontal and vertical scales exceed the allowed uniformity "
            "tolerance; confirm crop, viewport, and export resizing."
        )
    if not frame_within_viewport:
        warnings.append(
            "Reference frame extends outside the target viewport; confirm its "
            "logical origin and bounds."
        )
    if dpr is not None and not dpr_matches:
        warnings.append(
            "Provided DPR does not match the image-to-layout scale, so the "
            "image was likely resized or cropped after capture."
        )

    report.update(
        {
            "status": "confirmed" if conversion_ready else "needs_review",
            "reference_frame_logical": list(frame),
            "reference_frame_source": (
                "provided" if reference_frame is not None else "full_viewport"
            ),
            "logical_origin": [frame_x, frame_y],
            "image_to_layout_scale": {
                "x": round(scale_x, 6),
                "y": round(scale_y, 6),
                "uniform": round(average_scale, 6)
                if average_scale is not None
                else None,
                "is_uniform": is_uniform,
                "relative_delta": round(relative_delta, 6),
                "maximum_relative_delta": MAX_RELATIVE_SCALE_DELTA,
            },
            "conversion_note": (
                (
                    "Convert with the reference-frame origin: logical_x = "
                    "origin_x + image_x / scale_x and logical_y = origin_y + "
                    "image_y / scale_y. This image-to-layout scale is not "
                    "device DPR."
                )
                if conversion_ready
                else (
                    "Conversion blocked: resolve mapping warnings before "
                    "using image measurements as layout constants."
                )
            ),
            "warnings": warnings,
        }
    )
    return report


def measurement_checklist(mapping: dict[str, Any]) -> dict[str, Any]:
    coordinate_ready = mapping["status"] == "confirmed"
    return {
        "coordinate_system": {
            "status": "ready" if coordinate_ready else "blocked",
            "required_before_layout_constants": True,
            "record": [
                "reference_size_px",
                "target_viewport_logical",
                "reference_frame_and_logical_origin",
                "image_to_layout_scale_x_y",
                "device_dpr_and_source",
                "crop_or_resampling_notes",
            ],
        },
        "system_ui": {
            "status": "pending_manual",
            "record": [
                "safe_area_insets_logical",
                "status_and_navigation_bar_bounds",
                "app_content_origin",
            ],
        },
        "major_geometry": {
            "status": "pending_manual",
            "record": [
                "container_bounds",
                "major_component_bounds",
                "corner_radii",
                "content_clipping_or_overflow",
            ],
        },
        "spacing": {
            "status": "pending_manual",
            "record": [
                "outer_margins",
                "component_gaps",
                "content_insets",
                "alignment_axes",
            ],
        },
        "typography": {
            "status": "pending_manual",
            "record": [
                "font_family_weight_size",
                "line_height",
                "text_baselines",
                "letter_spacing_and_alignment",
            ],
        },
        "colors_and_effects": {
            "status": "pending_manual",
            "record": [
                "solid_region_color_samples",
                "opacity",
                "borders",
                "shadows_or_blur",
            ],
        },
        "assets": {
            "status": "pending_manual",
            "record": [
                "asset_source_and_variant",
                "intrinsic_dimensions_px",
                "visible_alpha_bounds",
                "content_mode_and_logical_size",
            ],
        },
    }


def analyze_reference(
    image: Image.Image,
    path: Path,
    color_count: int,
    viewport: tuple[float, float] | None = None,
    dpr: float | None = None,
    reference_frame: tuple[float, float, float, float] | None = None,
) -> tuple[dict[str, Any], list[list[int]]]:
    boxes = component_boxes(image)
    mapping = coordinate_mapping(
        (image.width, image.height),
        viewport,
        dpr,
        reference_frame=reference_frame,
    )
    report = {
        "path": str(path),
        "size_px": [image.width, image.height],
        "aspect_ratio": round(image.width / image.height, 6),
        "coordinate_units": {
            "reference": "image_px",
            "target": "logical_layout_units",
        },
        "visible_alpha_bbox_image_px_xyxy": visible_bbox(image),
        "coordinate_mapping": mapping,
        "measurement_checklist": measurement_checklist(mapping),
        "dominant_colors": dominant_colors(image, color_count),
        "candidate_component_boxes_image_px_xywh": boxes,
        "candidate_box_note": (
            "Image-pixel edge candidates only; verify semantics and convert "
            "through confirmed coordinate mapping."
        ),
    }
    return report, boxes


def save_annotated(
    image: Image.Image,
    boxes: list[list[int]],
    output: Path,
) -> None:
    annotated = image.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    for index, (x, y, width, height) in enumerate(boxes):
        draw.rectangle((x, y, x + width, y + height), outline="#FF00FF", width=2)
        draw.text((x + 2, y + 2), str(index), fill="#FF00FF")
    output.parent.mkdir(parents=True, exist_ok=True)
    annotated.save(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect dimensions, colors, and candidate bounds in a UI image."
    )
    parser.add_argument("reference", type=Path)
    parser.add_argument("--json", dest="json_output", type=Path)
    parser.add_argument("--annotated", type=Path)
    parser.add_argument("--colors", type=color_count, default=10)
    parser.add_argument(
        "--viewport",
        type=parse_dimensions,
        metavar="WIDTHxHEIGHT",
        help="Target logical viewport; this determines image-to-layout scale.",
    )
    parser.add_argument(
        "--dpr",
        type=positive_float,
        help="Confirmed device pixel ratio; never inferred from image dimensions.",
    )
    parser.add_argument(
        "--reference-frame",
        type=parse_frame,
        metavar="X,Y,WIDTH,HEIGHT",
        help=(
            "Logical frame represented by a cropped reference. Omit only when "
            "the image represents the full target viewport."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    reference = load_rgba(args.reference)
    report, boxes = analyze_reference(
        reference,
        args.reference,
        args.colors,
        viewport=args.viewport,
        dpr=args.dpr,
        reference_frame=args.reference_frame,
    )

    if args.annotated:
        save_annotated(reference, boxes, args.annotated)

    serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
