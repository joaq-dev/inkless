import hashlib
import os
import random

def generate_watermark(name, email, signature):
    """Generate a unique watermark based on user information."""
    data = f"{name}-{email}-{signature}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]


SUPPORTED_EXTENSIONS = {".py": "#", ".c": "//", ".cpp": "//", ".mlx": "%", ".m": "%", ".v": "//"}

ENCODING_SYMBOLS = ["-", "_"]  # Use dashes and underscores for encoding


def convert_to_pattern(watermark):
    """Convert the watermark into a pattern of dashes and underscores."""
    binary_representation = ''.join(format(ord(char), '08b') for char in watermark)  # Convert to binary
    encoded_pattern = ''.join(ENCODING_SYMBOLS[int(bit)] for bit in binary_representation)  # Map to pattern
    return encoded_pattern


def generate_comment_watermark(watermark):
    """Generate a hidden comment watermark as a string of numbers and letters with a subtle prefix."""
    return f"/* marker: {watermark} */"  # Hidden comment watermark with subtle identifier


def insert_watermark_in_code(code, watermark, extension):
    """Insert both the encoded and comment watermark as comments into the code."""
    encoded_watermark = convert_to_pattern(watermark)
    comment_watermark = generate_comment_watermark(watermark)

    comment_symbol = SUPPORTED_EXTENSIONS.get(extension, "#")  # Determine correct comment syntax

    # Encoded watermark with a unique identifier
    encoded_comment = f"{comment_symbol} _sigil_ {encoded_watermark}"

    lines = code.splitlines()
    num_lines = len(lines)

    # Choose random positions for each watermark
    encoded_position = random.randint(0, num_lines - 1) if num_lines > 1 else 0
    comment_position = random.randint(0, num_lines - 1) if num_lines > 1 else 0

    # Ensure the positions are not the same to avoid placing both in one spot
    while encoded_position == comment_position:
        comment_position = random.randint(0, num_lines - 1)

    # Insert the comment watermark at a random line
    lines.insert(comment_position, comment_watermark)

    # Insert the encoded watermark as a comment at another random line
    lines.insert(encoded_position, encoded_comment)

    return "\n".join(lines)


def embed_watermark(filename, name, email, signature):
    """Embed watermark into a file."""
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return

    watermark = generate_watermark(name, email, signature)

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    # Embed watermark in the code
    code = insert_watermark_in_code(code, watermark, extension)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Watermark embedded in {filename}")
