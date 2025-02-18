import argparse
import logging
import os
from itertools import combinations  # For comparing all file pairs in a folder

from stamping.checker import check_similarity
from stamping.embed_watermark import embed_watermark
from stamping.extract import extract_watermark, verify_identity

logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--embed", nargs='+', help="Files or folder to embed stamp into")
    parser.add_argument("--extract", nargs='+', help="Files or folder to extract stamp from")
    parser.add_argument("--verify", nargs='+', help="Verify identity using name, email, and signature")
    parser.add_argument("--check", nargs='+', help="Check similarity between files or all files in a folder")
    parser.add_argument("--name", help="Your name (Required for embedding & verification)")
    parser.add_argument("--email", help="Your email (Required for embedding & verification)")
    parser.add_argument("--signature", help="Unique file signature (Required for embedding & verification)")
    return parser.parse_args()


def process_files_in_folder(folder, action, *args):
    """Helper function to process all files in a given folder."""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            logging.info(f"Processing file: {filename}")
            if action == "embed":
                embed_watermark(file_path, *args)
            elif action == "extract":
                extract_watermark(file_path)
            elif action == "verify":
                verify_identity(file_path, *args)
            elif action == "check":
                check_similarity(file_path, *args)


def compare_files_in_folder(folder, files_to_check=None):
    """Compare all files in a folder or compare specific files."""
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if files_to_check:
        files = [file for file in files if file in files_to_check]

    for file1, file2 in combinations(files, 2):
        logging.info(f"Checking similarity between {file1} and {file2}")
        check_similarity(file1, file2)


def main():
    args = parse_arguments()

    if args.embed and args.name and args.email and args.signature:
        if os.path.isdir(args.embed[0]):
            process_files_in_folder(args.embed[0], "embed", args.name, args.email, args.signature)
        else:
            for file in args.embed:
                if os.path.isfile(file):
                    embed_watermark(file, args.name, args.email, args.signature)
                else:
                    logging.warning(f"{file} is not a valid file!")

    elif args.extract:
        if os.path.isdir(args.extract[0]):
            process_files_in_folder(args.extract[0], "extract")
        else:
            for file in args.extract:
                if os.path.isfile(file):
                    extract_watermark(file)
                else:
                    logging.warning(f"{file} is not a valid file!")

    elif args.verify and args.name and args.email and args.signature:
        if os.path.isdir(args.verify[0]):
            process_files_in_folder(args.verify[0], "verify", args.name, args.email, args.signature)
        else:
            for file in args.verify:
                if os.path.isfile(file):
                    verify_identity(file, args.name, args.email, args.signature)
                else:
                    logging.warning(f"{file} is not a valid file!")

    elif args.check:
        if os.path.isdir(args.check[0]):
            folder_path = args.check[0]
            files_to_check = args.check[1:] if len(args.check) > 1 else None
            compare_files_in_folder(folder_path, files_to_check)
        else:
            if len(args.check) == 2 and os.path.isfile(args.check[0]) and os.path.isfile(args.check[1]):
                check_similarity(args.check[0], args.check[1])
            else:
                logging.warning("Invalid files provided for similarity check!")

    else:
        logging.warning("Invalid usage. Use --embed, --extract, --verify, or --check with required parameters.")


if __name__ == "__main__":
    main()
