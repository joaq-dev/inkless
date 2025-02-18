import argparse
import logging
import os
from itertools import combinations  # For comparing all file pairs in a folder

from stamping.checker import check_similarity
from stamping.embed_watermark import embed_watermark
from stamping.extract import extract_watermark

logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--embed", nargs='+', help="Files or folder to embed stamp into")
    parser.add_argument("--extract", nargs='+', help="Files or folder to extract stamp from")
    parser.add_argument("--check", nargs='+', help="Check similarity between files or all files in a folder")
    parser.add_argument("--name", help="Your name")
    parser.add_argument("--email", help="Your email")
    parser.add_argument("--signature", help="Unique file signature")
    return parser.parse_args()


def process_files_in_folder(folder, action, *args):
    """Helper function to process all files in a given folder."""
    # Get all files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # Ensure it's a file and not a subdirectory
        if os.path.isfile(file_path):
            logging.info(f"Processing file: {filename}")
            # Perform the action based on the specified action
            if action == "embed":
                embed_watermark(file_path, *args)
            elif action == "extract":
                extract_watermark(file_path)
            elif action == "check":
                check_similarity(file_path, *args)


def compare_files_in_folder(folder, files_to_check=None):
    """Compare all files in a folder or compare specific files."""
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    # If specific files are provided, we compare only those
    if files_to_check:
        files = [file for file in files if file in files_to_check]

    # Compare all pairs of files
    for file1, file2 in combinations(files, 2):
        logging.info(f"Checking similarity between {file1} and {file2}")
        check_similarity(file1, file2)


def main():
    args = parse_arguments()

    # Embed watermark into files or folder
    if args.embed and args.name and args.email and args.signature:
        if os.path.isdir(args.embed[0]):
            # If a folder is specified
            folder_path = args.embed[0]
            process_files_in_folder(folder_path, "embed", args.name, args.email, args.signature)
        else:
            # If specific files are specified
            for file in args.embed:
                if os.path.isfile(file):
                    embed_watermark(file, args.name, args.email, args.signature)
                else:
                    logging.warning(f"{file} is not a valid file!")

    # Extract watermark from files or folder
    elif args.extract:
        if os.path.isdir(args.extract[0]):
            # If a folder is specified
            folder_path = args.extract[0]
            process_files_in_folder(folder_path, "extract")
        else:
            # If specific files are specified
            for file in args.extract:
                if os.path.isfile(file):
                    extract_watermark(file)
                else:
                    logging.warning(f"{file} is not a valid file!")

    # Check similarity between files or all files in a folder
    elif args.check:
        if os.path.isdir(args.check[0]):
            # If a folder is specified
            folder_path = args.check[0]
            files_to_check = args.check[1:] if len(args.check) > 1 else None
            compare_files_in_folder(folder_path, files_to_check)
        else:
            # If specific files are specified
            file1, file2 = args.check
            if os.path.isfile(file1) and os.path.isfile(file2):
                check_similarity(file1, file2)
            else:
                logging.warning(f"One or both files provided for checking do not exist or are invalid!")

    # Invalid usage
    else:
        logging.warning("Invalid usage. Use --embed, --extract, or --check with required parameters.")


if __name__ == "__main__":
    main()
