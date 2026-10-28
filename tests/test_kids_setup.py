"""No-network checks before creating or uploading a children's Short."""

import unittest

from pipeline.channel_presets import get_preset
from pipeline.youtube_destination import KIDS_CHANNEL_ID, verify_kids_channel
from pipeline.youtube_metadata import build_upload_body


class KidsSetupTests(unittest.TestCase):
    def test_children_preset_uses_arabic_and_3d_cartoon(self):
        preset = get_preset("kids_learning")
        self.assertEqual(preset["language"], "ar")
        self.assertEqual(preset["tts_voice"], "ar-SA-ZariyahNeural")
        self.assertTrue(preset["made_for_kids"])
        self.assertEqual(preset["category_id"], "27")
        self.assertIn("3D cartoon", preset["image_style_suffix"])
        self.assertGreaterEqual(len(preset["topic_pool"]), 20)

    def test_private_upload_declares_kids_audience(self):
        preset = get_preset("kids_learning")
        body = build_upload_body(
            "تعلم حرف الألف", "درس قصير وممتع",
            privacy_status="private",
            category_id=preset["category_id"],
            made_for_kids=preset["made_for_kids"],
        )
        self.assertEqual(body["status"]["privacyStatus"], "private")
        self.assertIs(body["status"]["selfDeclaredMadeForKids"], True)
        self.assertEqual(body["snippet"]["categoryId"], "27")

    def test_other_channels_keep_separate_audience_setting(self):
        body = build_upload_body("Other video", "Description")
        self.assertIs(body["status"]["selfDeclaredMadeForKids"], False)

    def test_kids_channel_id_is_fixed_and_authorized(self):
        self.assertEqual(KIDS_CHANNEL_ID, "UCp54Cb0oNUWfuyf39tS1rCA")
        verify_kids_channel({"items": [{"id": KIDS_CHANNEL_ID}]})

    def test_wrong_channel_or_no_channel_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "not authorized"):
            verify_kids_channel({"items": [{"id": "UC_wrong_channel"}]})
        with self.assertRaisesRegex(RuntimeError, "not authorized"):
            verify_kids_channel({"items": []})


if __name__ == "__main__":
    unittest.main()
