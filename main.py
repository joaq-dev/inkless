import argparse
import logging

from stamping.checker import check_similarity
from stamping.embed_watermark import embed_watermark
from stamping.embed_watermark import generate_watermark
from stamping.extract import extract_watermark

logging.basicConfig(level=logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--embed", help="File to embed stamp into")
    parser.add_argument("--extract", help="File to extract stamp from")
    parser.add_argument("--check", nargs=2, help="Check similarity between two files")
    parser.add_argument("--name", help="Your name")
    parser.add_argument("--email", help="Your email")
    parser.add_argument("--signature", help="Unique file signature")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.embed and args.name and args.email and args.signature:
        watermark = generate_watermark(args.name, args.email, args.signature)
        embed_watermark(args.embed, watermark)
    elif args.extract:
        extract_watermark(args.extract)
    elif args.check:
        check_similarity(args.check[0], args.check[1])
    else:
        logging.warning("Invalid usage. Use --embed, --extract, or --check with required parameters.")


if __name__ == "__main__":
    main()
