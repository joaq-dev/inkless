import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from stamping.embed_watermark import embed_watermark, generate_watermark

class TestEmbedWatermark(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_sample.py"
        with open(self.test_file, "w") as f:
            f.write("""
    def test_function():
        print("Hello, World!")

    def another_function():
        return 42

    class SampleClass:
        def method(self):
            pass
    """)

    def test_generate_watermark(self):
        wm1 = generate_watermark("Alice", "alice@example.com", "ProjectX")
        wm2 = generate_watermark("Alice", "alice@example.com", "ProjectX")
        self.assertEqual(wm1, wm2)  # Ensures watermark consistency

    def test_embed_watermark(self):
        embed_watermark(self.test_file, "Alice", "alice@example.com", "ProjectX")
        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertIn("Watermark:", content)  # Ensures watermark is added

    def tearDown(self):
        os.remove(self.test_file)


if __name__ == "__main__":
    unittest.main()
