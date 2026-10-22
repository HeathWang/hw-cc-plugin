#!/usr/bin/env python3
"""Measure colors, bounds, and component candidates in a UI reference image."""

from __future__ import annotations

import argparse
import json
import math
import re
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


def parse_roi(value: str) -> tuple[int, int, int, int]:
    frame = parse_frame(value)
    if any(number < 0 for number in frame[:2]) or any(
        not number.is_integer() for number in frame
    ):
        raise argparse.ArgumentTypeError(
            "ROI must contain non-negative integer X,Y,WIDTH,HEIGHT values"
        )
    return tuple(int(number) for number in frame)


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
    with Image.open(path) as source:
        image = source.convert("RGBA")
        image.info.update(source.info)
    return image


def visible_bbox(image: Image.Image) -> list[int] | None:
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 0 else 0).getbbox()
    return list(bbox) if bbox else None


def source_image_metadata(image: Image.Image) -> dict[str, Any]:
    embedded_size: tuple[int, int] | None = None
    source: str | None = None

    for key in ("XML:com.adobe.xmp", "xmp"):
        payload = image.info.get(key)
        if not payload:
            continue
        text = (
            payload.decode("utf-8", errors="ignore")
            if isinstance(payload, bytes)
            else str(payload)
        )
        width = re.search(
            r"(?:PixelXDimension|ImageWidth)(?:[^>]*>\s*|=[\"'])(\d+)",
            text,
        )
        height = re.search(
            r"(?:PixelYDimension|ImageLength)(?:[^>]*>\s*|=[\"'])(\d+)",
            text,
        )
        if width and height:
            embedded_size = (int(width.group(1)), int(height.group(1)))
            source = "xmp"
            break

    if embedded_size is None:
        try:
            exif_ifd = image.getexif().get_ifd(34665)
            width = exif_ifd.get(40962)
            height = exif_ifd.get(40963)
            if width and height:
                embedded_size = (int(width), int(height))
                source = "exif"
        except (AttributeError, KeyError, TypeError, ValueError):
            pass

    decoded_size = (image.width, image.height)
    relation = "unavailable"
    if embedded_size == decoded_size:
        relation = "matches_decoded"
    elif embedded_size is not None:
        source_width, source_height = embedded_size
        if source_width == image.width and source_height > image.height:
            relation = "likely_vertical_crop"
        elif source_height == image.height and source_width > image.width:
            relation = "likely_horizontal_crop"
        else:
            source_ratio = source_width / source_height
            decoded_ratio = image.width / image.height
            relative_delta = abs(source_ratio - decoded_ratio) / max(
                source_ratio,
                decoded_ratio,
            )
            relation = (
                "likely_resampled"
                if relative_delta <= MAX_RELATIVE_SCALE_DELTA
                else "crop_or_resample"
            )

    return {
        "decoded_size_px": list(decoded_size),
        "embedded_source_size_px": (
            list(embedded_size) if embedded_size is not None else None
        ),
        "embedded_dimension_source": source,
        "dimension_relation": relation,
    }


def _merge_similar_colors(
    colors: list[dict[str, Any]],
    distance: float = 12.0,
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for color in sorted(colors, key=lambda item: item["share"], reverse=True):
        rgb = np.asarray(color["rgb"], dtype=np.float64)
        match = next(
            (
                item
                for item in merged
                if np.linalg.norm(rgb - np.asarray(item["rgb"])) <= distance
            ),
            None,
        )
        if match is None:
            merged.append(dict(color))
            continue
        match["share"] = round(match["share"] + color["share"], 6)
    return sorted(merged, key=lambda item: item["share"], reverse=True)


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
    return _merge_similar_colors(colors)


def frequent_exact_colors(
    image: Image.Image,
    count: int,
) -> list[dict[str, Any]]:
    rgba = np.asarray(image.convert("RGBA"))
    pixels = rgba[:, :, :3][rgba[:, :, 3] > 0]
    if pixels.size == 0:
        return []
    stride = max(1, math.ceil(len(pixels) / 100_000))
    sample = pixels[::stride].astype(np.uint32)
    packed = (sample[:, 0] << 16) | (sample[:, 1] << 8) | sample[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    order = np.argsort(counts)[::-1][: count * 3]
    colors = []
    for index in order:
        value = int(values[index])
        rgb = [(value >> 16) & 255, (value >> 8) & 255, value & 255]
        colors.append(
            {
                "hex": "#" + "".join(f"{channel:02X}" for channel in rgb),
                "rgb": rgb,
                "share": round(int(counts[index]) / len(sample), 6),
            }
        )
    return _merge_similar_colors(colors)[:count]


def _region_shape(width: int, height: int, fill_ratio: float) -> str:
    aspect = width / height
    if 0.85 <= aspect <= 1.15 and 0.65 <= fill_ratio <= 0.88:
        return "circle_or_ellipse"
    if fill_ratio < 0.96:
        return "rounded_rectangle_or_panel"
    return "rectangle"


def flat_color_regions(
    image: Image.Image,
    count: int = 20,
) -> list[dict[str, Any]]:
    rgb = np.asarray(image.convert("RGB"))
    rgb16 = rgb.astype(np.int16)
    image_area = image.width * image.height
    minimum_area = max(16, round(image_area * 0.0005))
    palette = frequent_exact_colors(image, max(12, count))
    regions: list[dict[str, Any]] = []

    for color in palette:
        target = np.asarray(color["rgb"], dtype=np.int16)
        distance = np.max(
            np.abs(rgb16 - target),
            axis=2,
        )
        mask = (distance <= 4).astype(np.uint8)
        _, _, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        for x, y, width, height, area in stats[1:]:
            if area < minimum_area:
                continue
            fill_ratio = area / (width * height)
            image_share = area / image_area
            is_canvas = (
                width >= image.width * 0.95
                and height >= image.height * 0.95
                and image_share >= 0.1
            )
            if fill_ratio < 0.5 and not is_canvas:
                continue
            regions.append(
                {
                    "hex": color["hex"],
                    "rgb": color["rgb"],
                    "bbox_image_px_xywh": [
                        int(x),
                        int(y),
                        int(width),
                        int(height),
                    ],
                    "area_px": int(area),
                    "image_share": round(image_share, 6),
                    "fill_ratio": round(fill_ratio, 4),
                    "shape": (
                        "background_or_canvas"
                        if is_canvas
                        else _region_shape(
                            int(width),
                            int(height),
                            fill_ratio,
                        )
                    ),
                }
            )
    regions.sort(key=lambda item: item["area_px"], reverse=True)
    return regions[:40]


def ui_palette(
    regions: list[dict[str, Any]],
    count: int = 10,
) -> list[dict[str, Any]]:
    totals: dict[str, dict[str, Any]] = {}
    for region in regions:
        item = totals.setdefault(
            region["hex"],
            {
                "hex": region["hex"],
                "rgb": region["rgb"],
                "area_px": 0,
            },
        )
        item["area_px"] += region["area_px"]
    return sorted(
        totals.values(),
        key=lambda item: item["area_px"],
        reverse=True,
    )[:count]


def component_boxes(image: Image.Image) -> list[list[int]]:
    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    group_width = max(7, round(image.width * 0.012))
    edges = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        np.ones((3, group_width), np.uint8),
    )
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
    return boxes[:80]


def shape_candidates(image: Image.Image) -> list[dict[str, Any]]:
    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    minimum_dimension = min(image.width, image.height)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.4,
        minDist=max(30, round(minimum_dimension * 0.15)),
        param1=120,
        param2=max(24, round(minimum_dimension * 0.18)),
        minRadius=max(8, round(minimum_dimension * 0.03)),
        maxRadius=max(10, round(minimum_dimension * 0.48)),
    )
    if circles is None:
        return []

    candidates = []
    for center_x, center_y, radius in np.round(circles[0]).astype(int):
        candidates.append(
            {
                "shape": "circle",
                "center_image_px": [int(center_x), int(center_y)],
                "radius_image_px": int(radius),
                "bbox_image_px_xywh": [
                    int(center_x - radius),
                    int(center_y - radius),
                    int(radius * 2),
                    int(radius * 2),
                ],
            }
        )
    candidates.sort(key=lambda item: item["radius_image_px"], reverse=True)
    return candidates[:6]


def _offset_boxes(
    boxes: list[list[int]],
    offset: tuple[int, int],
) -> list[list[int]]:
    offset_x, offset_y = offset
    return [
        [x + offset_x, y + offset_y, width, height]
        for x, y, width, height in boxes
    ]


def convert_boxes_to_logical(
    boxes: list[list[int]],
    mapping: dict[str, Any],
) -> list[list[float]]:
    if mapping["status"] != "confirmed":
        return []
    scale = mapping["image_to_layout_scale"]
    origin_x, origin_y = mapping["logical_origin"]
    return [
        [
            round(origin_x + x / scale["x"], 4),
            round(origin_y + y / scale["y"], 4),
            round(width / scale["x"], 4),
            round(height / scale["y"], 4),
        ]
        for x, y, width, height in boxes
    ]


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
    roi: tuple[int, int, int, int] | None = None,
) -> tuple[dict[str, Any], list[list[int]]]:
    analysis_image = image
    offset = (0, 0)
    if roi is not None:
        x, y, width, height = roi
        if (
            x < 0
            or y < 0
            or width <= 0
            or height <= 0
            or x + width > image.width
            or y + height > image.height
        ):
            raise ValueError("ROI must stay within the reference image")
        analysis_image = image.crop((x, y, x + width, y + height))
        offset = (x, y)

    boxes = _offset_boxes(component_boxes(analysis_image), offset)
    shapes = shape_candidates(analysis_image)
    if offset != (0, 0):
        for shape in shapes:
            shape["center_image_px"][0] += offset[0]
            shape["center_image_px"][1] += offset[1]
            shape["bbox_image_px_xywh"][0] += offset[0]
            shape["bbox_image_px_xywh"][1] += offset[1]
    regions = flat_color_regions(
        analysis_image,
        count=max(16, color_count * 2),
    )
    if offset != (0, 0):
        for region in regions:
            x, y, width, height = region["bbox_image_px_xywh"]
            region["bbox_image_px_xywh"] = [
                x + offset[0],
                y + offset[1],
                width,
                height,
            ]
    mapping = coordinate_mapping(
        (image.width, image.height),
        viewport,
        dpr,
        reference_frame=reference_frame,
    )
    logical_boxes = convert_boxes_to_logical(boxes, mapping)
    logical_regions = convert_boxes_to_logical(
        [region["bbox_image_px_xywh"] for region in regions],
        mapping,
    )
    for region, logical_box in zip(regions, logical_regions):
        region["bbox_logical_xywh"] = logical_box
    logical_shapes = convert_boxes_to_logical(
        [shape["bbox_image_px_xywh"] for shape in shapes],
        mapping,
    )
    for shape, logical_box in zip(shapes, logical_shapes):
        shape["bbox_logical_xywh"] = logical_box

    report = {
        "path": str(path),
        "size_px": [image.width, image.height],
        "aspect_ratio": round(image.width / image.height, 6),
        "source_image_metadata": source_image_metadata(image),
        "analysis_roi_image_px_xywh": list(roi) if roi else None,
        "coordinate_units": {
            "reference": "image_px",
            "target": "logical_layout_units",
        },
        "visible_alpha_bbox_image_px_xyxy": visible_bbox(image),
        "coordinate_mapping": mapping,
        "measurement_checklist": measurement_checklist(mapping),
        "dominant_colors": dominant_colors(analysis_image, color_count),
        "ui_palette": ui_palette(regions, color_count),
        "major_flat_regions": regions,
        "shape_candidates": shapes,
        "candidate_component_boxes_image_px_xywh": boxes,
        "candidate_component_boxes_logical_xywh": (
            logical_boxes if logical_boxes else None
        ),
        "candidate_box_note": (
            "Image-pixel edge candidates only; verify semantics and convert "
            "through confirmed coordinate mapping."
        ),
    }
    return report, boxes


def compact_summary(report: dict[str, Any]) -> dict[str, Any]:
    mapping = report["coordinate_mapping"]
    return {
        "path": report["path"],
        "size_px": report["size_px"],
        "source_image_metadata": report["source_image_metadata"],
        "analysis_roi_image_px_xywh": report["analysis_roi_image_px_xywh"],
        "coordinate_mapping": {
            "status": mapping["status"],
            "reference_frame_logical": mapping["reference_frame_logical"],
            "logical_origin": mapping["logical_origin"],
            "image_to_layout_scale": mapping["image_to_layout_scale"],
            "warnings": mapping["warnings"],
        },
        "ui_palette": report["ui_palette"][:8],
        "major_flat_regions": report["major_flat_regions"][:10],
        "shape_candidates": report["shape_candidates"],
        "candidate_component_count": len(
            report["candidate_component_boxes_image_px_xywh"]
        ),
    }


def save_annotated(
    image: Image.Image,
    boxes: list[list[int]],
    output: Path,
    major_regions: list[dict[str, Any]] | None = None,
    shapes: list[dict[str, Any]] | None = None,
) -> None:
    annotated = image.convert("RGB")
    draw = ImageDraw.Draw(annotated)
    for index, region in enumerate(major_regions or []):
        x, y, width, height = region["bbox_image_px_xywh"]
        draw.rectangle(
            (x, y, x + width, y + height),
            outline="#00B7FF",
            width=3,
        )
        draw.text((x + 2, y + 2), f"R{index}", fill="#00B7FF")
    for index, shape in enumerate(shapes or []):
        x, y, width, height = shape["bbox_image_px_xywh"]
        draw.ellipse(
            (x, y, x + width, y + height),
            outline="#00C853",
            width=3,
        )
        draw.text((x + 2, y + 2), f"S{index}", fill="#00C853")
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
    parser.add_argument(
        "--roi",
        type=parse_roi,
        metavar="X,Y,WIDTH,HEIGHT",
        help=(
            "Analyze a focused pixel region while preserving coordinates "
            "relative to the complete reference."
        ),
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a compact decision-oriented JSON summary.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress stdout; useful when writing --json.",
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
        roi=args.roi,
    )

    if args.annotated:
        save_annotated(
            reference,
            boxes,
            args.annotated,
            report["major_flat_regions"],
            report["shape_candidates"],
        )

    serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(serialized + "\n", encoding="utf-8")
    if not args.quiet:
        if args.summary or args.json_output:
            print(
                json.dumps(
                    compact_summary(report),
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                )
            )
        else:
            print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
