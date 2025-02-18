import hashlib
import os

SUPPORTED_EXTENSIONS = {".py": "#", ".c": "//", ".cpp": "//", ".mlx": "%", ".m": "%", ".v": "//"}

ENCODING_SYMBOLS = ["-", "_"]  # Use dashes and underscores for encoding


def generate_watermark(name, email, signature):
    """Recreate the watermark from given credentials."""
    data = f"{name}-{email}-{signature}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]  # First 16 hex characters


def decode_from_pattern(encoded_pattern):
    """Convert a pattern of dashes and underscores back to the original watermark."""
    binary_representation = ''.join("0" if char == "-" else "1" for char in encoded_pattern)
    watermark_chars = [chr(int(binary_representation[i:i + 8], 2)) for i in range(0, len(binary_representation), 8)]
    return "".join(watermark_chars)


def extract_watermark(filename):
    """Extract watermark from a file."""
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    extracted_watermark = None
    extracted_encoded_watermark = None

    for line in lines:
        if "marker:" in line:
            start_idx = line.find("marker:") + len("marker:")
            extracted_watermark = line[start_idx:].strip().replace("*/", "").strip()
            print("Extracted Watermark (Hidden Comment):", extracted_watermark)

        if "_sigil_" in line:
            extracted_encoded_watermark = line.split("_sigil_")[1].strip()
            print("Extracted Watermark (Encoded):", extracted_encoded_watermark)
            decoded_watermark = decode_from_pattern(extracted_encoded_watermark)
            print("Decoded Watermark:", decoded_watermark)

    if not extracted_watermark and not extracted_encoded_watermark:
        print("No watermark found in", filename)

    return extracted_watermark


def verify_identity(filename, name, email, signature):
    """Verify if the extracted watermark matches the given name, email, and signature."""
    extracted_watermark = extract_watermark(filename)

    if extracted_watermark:
        expected_watermark = generate_watermark(name, email, signature)
        if extracted_watermark == expected_watermark:
            print(f"✅ Verified: The file '{filename}' was authorized under {name} ({email})")
        else:
            print(f"❌ Identity Mismatch: The given details do not match the watermark in '{filename}'")
    else:
        print(f"❌ No watermark found in '{filename}', cannot verify identity.")
