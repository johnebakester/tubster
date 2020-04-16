import argparse

from app import app


parser = argparse.ArgumentParser(description="Companion uploader for the Tub!")
parser.add_argument(
    "source",
    help="Source directory within which the manuscripts of lyrical nature reside.",
)
parser.add_argument(
    "--host",
    dest="filehost",
    default="pixeldrain",
    help="Preferred filehost. Either pixeldrain or catbox",
)


def main():
    args = vars(parser.parse_args())
    app(**args)


if __name__ == "__main__":
    main()
