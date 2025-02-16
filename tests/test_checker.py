import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from stamping.checker import check_similarity
from io import StringIO



class TestChecker(unittest.TestCase):
    def setUp(self):
        self.original_file = "original.py"
        self.modified_file = "modified.py"
        with open(self.original_file, "w") as f:
            f.write("def test_function():\n    print(\"Hello, World!\")")
        with open(self.modified_file, "w") as f:
            f.write("def test_function():\n    print(\"Hello, Universe!\")")

    def test_check_similarity(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        check_similarity(self.original_file, self.modified_file)
        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue()
        print(output.strip())
        self.assertIn("Similarity check complete", output)  # Ensure function runs

    def tearDown(self):
        os.remove(self.original_file)
        os.remove(self.modified_file)


if __name__ == "__main__":
    unittest.main()