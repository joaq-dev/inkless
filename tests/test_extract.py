import os
import sys
import unittest
from io import StringIO

from stamping.extract import extract_watermark

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_sample.py"
        with open(self.test_file, "w") as f:
            f.write("# Watermark: test12345\n\ndef test_function():\n    print(\"Hello, World!\")")

    def test_extract_watermark(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        extract_watermark(self.test_file)
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue()
        self.assertIn("Watermark:", output)  # Ensure watermark is detected

    def tearDown(self):
        os.remove(self.test_file)


if __name__ == "__main__":
    unittest.main()
