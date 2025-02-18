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
    extracted_watermark = ""
    encoded_watermark_found = False
    extracted_encoded_watermark = ""

    # Look for the hidden comment watermark (e.g., /* marker: abc123xyz */)
    for line in lines:
        if "marker:" in line:
            # Extract everything after "marker:"
            start_idx = line.find("marker:") + len("marker:")
            extracted_watermark = line[start_idx:].strip().replace("*/", "").strip()
            print("Extracted Watermark (Hidden Comment):", extracted_watermark)
            watermark_found = True

        # Look for a pattern of dashes and underscores prefixed by "_sigil_"
        if "_sigil_" in line:
            encoded_watermark_found = True
            extracted_encoded_watermark = line.split("_sigil_")[1].strip()
            print("Extracted Watermark (Encoded):", extracted_encoded_watermark)
            decoded_watermark = decode_from_pattern(extracted_encoded_watermark)
            print("Decoded Watermark:", decoded_watermark)

    if not watermark_found and not encoded_watermark_found:
        print("No watermark found in", filename)
