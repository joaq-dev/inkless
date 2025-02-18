import os
import sys
import unittest
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stamping.embed_watermark import embed_watermark
from stamping.extract import extract_watermark


class TestExtractWhitespace(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_sample.py"

        # Create the test file first before embedding the watermark
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("def test_function():\n    print(\"Hello, World!\")\n")

        embed_watermark(self.test_file, "Gumayusi", "guma@example.com", "ProjectX")  # Use actual watermarking function

        # Simulate removing the comment watermark while keeping the encoded pattern
        with open(self.test_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(self.test_file, "w", encoding="utf-8") as f:
            for line in lines:
                if "Watermark:" not in line:
                    f.write(line)  # Remove comment-based watermark but keep encoded pattern

    def test_extract_whitespace_watermark(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        extract_watermark(self.test_file)
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue().strip()

        print("Extracted Watermark Output:\n", output)  # Debugging output

        self.assertIn("Extracted Watermark (Whitespace Encoded):", output)  # Ensure encoded watermark is detected

    def test_missing_watermark(self):
        with open(self.test_file, "w") as f:
            f.write("def test_function():\n    print(\"Hello, World!\")")  # No watermark

        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        extract_watermark(self.test_file)
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue().strip()

        self.assertIn("No watermark found", output)  # Ensure missing watermark is detected

    def tearDown(self):
        os.remove(self.test_file)


if __name__ == "__main__":
    unittest.main()
