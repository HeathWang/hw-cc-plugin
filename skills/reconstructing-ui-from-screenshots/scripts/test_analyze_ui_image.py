#!/usr/bin/env python3

import importlib.util
import argparse
import unittest
from pathlib import Path

from PIL import Image


SCRIPT_PATH = Path(__file__).with_name("analyze_ui_image.py")
SPEC = importlib.util.spec_from_file_location("analyze_ui_image", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyzer)


class CoordinateMappingTests(unittest.TestCase):

    def test_parses_viewport_dimensions(self) -> None:
        self.assertEqual(analyzer.parse_dimensions("393x852"), (393.0, 852.0))

    def test_rejects_non_finite_dimensions_and_dpr(self) -> None:
        for dimensions in ("nanx852", "393xinf", "-infx852"):
            with self.subTest(dimensions=dimensions):
                with self.assertRaises(argparse.ArgumentTypeError):
                    analyzer.parse_dimensions(dimensions)

        for dpr in ("nan", "inf", "-inf"):
            with self.subTest(dpr=dpr):
                with self.assertRaises(argparse.ArgumentTypeError):
                    analyzer.positive_float(dpr)

    def test_rejects_non_finite_reference_frame(self) -> None:
        for frame in ("nan,0,100,100", "0,inf,100,100", "0,0,-inf,100"):
            with self.subTest(frame=frame):
                with self.assertRaises(argparse.ArgumentTypeError):
                    analyzer.parse_frame(frame)

    def test_validates_color_count_range(self) -> None:
        self.assertEqual(analyzer.color_count("1"), 1)
        self.assertEqual(analyzer.color_count("256"), 256)
        for count in ("0", "257"):
            with self.subTest(count=count):
                with self.assertRaises(argparse.ArgumentTypeError):
                    analyzer.color_count(count)

    def test_distinguishes_resampling_scale_from_unconfirmed_dpr(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(472, 1024),
            viewport=(393.0, 852.0),
            dpr=None,
        )

        self.assertEqual(mapping["status"], "confirmed")
        self.assertAlmostEqual(mapping["image_to_layout_scale"]["x"], 472 / 393, places=6)
        self.assertAlmostEqual(mapping["image_to_layout_scale"]["y"], 1024 / 852, places=6)
        self.assertTrue(mapping["image_to_layout_scale"]["is_uniform"])
        self.assertEqual(mapping["device_dpr"]["status"], "unconfirmed")
        self.assertIn("not device DPR", mapping["conversion_note"])

    def test_missing_viewport_blocks_pixel_to_layout_conversion(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(472, 1024),
            viewport=None,
            dpr=None,
        )
        checklist = analyzer.measurement_checklist(mapping)

        self.assertEqual(mapping["status"], "needs_confirmation")
        self.assertIsNone(mapping["image_to_layout_scale"])
        self.assertEqual(checklist["coordinate_system"]["status"], "blocked")
        self.assertTrue(checklist["coordinate_system"]["required_before_layout_constants"])

    def test_non_uniform_mapping_requires_review(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(472, 1024),
            viewport=(393.0, 800.0),
            dpr=3.0,
        )

        self.assertEqual(mapping["status"], "needs_review")
        self.assertFalse(mapping["image_to_layout_scale"]["is_uniform"])
        self.assertFalse(mapping["device_dpr"]["matches_image_scale"])
        self.assertIn("blocked", mapping["conversion_note"])

    def test_uniform_scale_tolerance_is_strict(self) -> None:
        accepted = analyzer.coordinate_mapping(
            image_size=(401, 1000),
            viewport=(400.0, 1000.0),
            dpr=None,
        )
        rejected = analyzer.coordinate_mapping(
            image_size=(402, 1000),
            viewport=(400.0, 1000.0),
            dpr=None,
        )

        self.assertEqual(accepted["status"], "confirmed")
        self.assertEqual(rejected["status"], "needs_review")

    def test_rejects_scale_overflow_from_extreme_viewport(self) -> None:
        with self.assertRaises(ValueError):
            analyzer.coordinate_mapping(
                image_size=(1, 1),
                viewport=(5e-324, 1.0),
                dpr=None,
            )

    def test_cropped_reference_uses_logical_frame_origin(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(400, 600),
            viewport=(393.0, 852.0),
            dpr=None,
            reference_frame=(20.0, 100.0, 200.0, 300.0),
        )

        self.assertEqual(mapping["status"], "confirmed")
        self.assertEqual(mapping["reference_frame_logical"], [20.0, 100.0, 200.0, 300.0])
        self.assertEqual(mapping["logical_origin"], [20.0, 100.0])
        self.assertEqual(mapping["image_to_layout_scale"]["uniform"], 2.0)
        self.assertIn("origin_x", mapping["conversion_note"])

    def test_reference_frame_outside_viewport_blocks_conversion(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(400, 600),
            viewport=(393.0, 852.0),
            dpr=None,
            reference_frame=(300.0, 700.0, 200.0, 300.0),
        )

        self.assertEqual(mapping["status"], "needs_review")
        self.assertIn("blocked", mapping["conversion_note"])

    def test_checklist_covers_required_measurement_groups(self) -> None:
        mapping = analyzer.coordinate_mapping(
            image_size=(472, 1024),
            viewport=(393.0, 852.0),
            dpr=None,
        )
        checklist = analyzer.measurement_checklist(mapping)

        self.assertEqual(
            set(checklist),
            {
                "coordinate_system",
                "system_ui",
                "major_geometry",
                "spacing",
                "typography",
                "colors_and_effects",
                "assets",
            },
        )
        self.assertEqual(checklist["coordinate_system"]["status"], "ready")
        self.assertEqual(checklist["major_geometry"]["status"], "pending_manual")

    def test_report_labels_reference_coordinates_as_image_pixels(self) -> None:
        image = Image.new("RGBA", (20, 40), "#FFFFFF")
        report, _ = analyzer.analyze_reference(
            image=image,
            path=Path("reference.png"),
            color_count=1,
            viewport=(10.0, 20.0),
        )

        self.assertEqual(report["coordinate_units"]["reference"], "image_px")
        self.assertIn("visible_alpha_bbox_image_px_xyxy", report)
        self.assertIn("candidate_component_boxes_image_px_xywh", report)
        self.assertNotIn("visible_alpha_bbox_xyxy", report)


if __name__ == "__main__":
    unittest.main()
