import hashlib
import os

def generate_watermark(name, email, signature):
    #Generate a unique watermark based on user information
    data = f"{name}-{email}-{signature}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]

SUPPORTED_EXTENSIONS = {".py": "#", ".c": "//", ".cpp": "//", ".mlx": "%", ".m": "%"}


def add_whitespace_watermark(code, watermark):
    return code + "\n" + " " * 4 + "".join([char + "  " for char in watermark]) + "\n"


def add_comment_watermark(code, extension, watermark):
    comment_symbol = SUPPORTED_EXTENSIONS.get(extension, "#")
    return f"{comment_symbol} Watermark: {watermark}\n" + code


def embed_watermark(filename, name, email, signature):
    #Embed watermark into a file
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return

    watermark = generate_watermark(name, email, signature)

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    code = add_comment_watermark(code, extension, watermark)
    code = add_whitespace_watermark(code, watermark)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Watermark embedded in {filename}")

