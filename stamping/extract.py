import os

SUPPORTED_EXTENSIONS = {".py": "#", ".c": "//", ".cpp": "//", ".mlx": "%", ".m": "%", ".v": "//"}

ENCODING_SYMBOLS = ["-", "_"]  # Use dashes and underscores for encoding


def decode_from_pattern(encoded_pattern):
    """Convert a pattern of dashes and underscores back to the original watermark."""
    binary_representation = ''.join("0" if char == "-" else "1" for char in encoded_pattern)
    watermark_chars = [chr(int(binary_representation[i:i + 8], 2)) for i in range(0, len(binary_representation), 8)]
    return "".join(watermark_chars)


def extract_watermark(filename):
    """Extract watermark from a file and detect partial removal."""
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    watermark_found = False
    partial_watermark_detected = False
    extracted_watermark = ""

    for line in lines:
        print(f"DEBUG: Checking line -> '{line.strip()}'")  # Debugging line

        if "Watermark:" in line:
            watermark_found = True
            extracted_watermark = line.strip()
            print("Extracted Watermark:", extracted_watermark)
            break
        elif all(char in ENCODING_SYMBOLS for char in line.strip()):  # Detect encoded watermark pattern
            extracted_watermark = decode_from_pattern(line.strip())
            if extracted_watermark.isalnum():  # Ensure it's a valid watermark
                partial_watermark_detected = True
                print("Extracted Watermark (Whitespace Encoded):", extracted_watermark)
                break

    if not watermark_found and not partial_watermark_detected:
        print("No watermark found in", filename)
    elif partial_watermark_detected:
        print("⚠ Warning: Watermark might have been tampered with!")