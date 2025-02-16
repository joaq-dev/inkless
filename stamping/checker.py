import ast
import hashlib
from difflib import SequenceMatcher


def file_hash(filename):
    # SHA 256 Hash
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_similarity(file1, file2):
    # Similarity Checking
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        code1, code2 = f1.read(), f2.read()

    # Hash Comparison
    hash1, hash2 = file_hash(file1), file_hash(file2)
    if hash1 == hash2:
        print("✅ Files are identical")
        return

    # Text Similarity
    similarity = SequenceMatcher(None, code1, code2).ratio() * 100
    print(f"🔹 Hash Similarity: {similarity:.2f}%")

    # AST Structure Comparison (For Python Only)
    try:
        ast1, ast2 = ast.parse(code1), ast.parse(code2)
        if ast.dump(ast1) == ast.dump(ast2):
            print("✅ AST Structure Match: HIGH (Code logic is very similar)")
        else:
            print("🔹 AST Structure Match: LOW (Code has been altered significantly)")
    except SyntaxError:
        print("AST check skipped (Non-Python file)")

    print("🔍 Similarity check complete")
