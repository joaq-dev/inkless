import os

SUPPORTED_EXTENSIONS = {".py": "#", ".c": "//", ".cpp": "//", ".mlx": "%", ".m": "%"}


def extract_watermark(filename):
    """Extract watermark from a file."""
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if "Watermark:" in line:
            print("Extracted Watermark:", line.strip())
            return
        elif "  " in line:  # Detect whitespace encoding
            decoded = "".join([char.strip() for char in line.split("  ")])
            print("Extracted Watermark (Whitespace Encoded):", decoded)
            return

    print("No watermark found in", filename)
