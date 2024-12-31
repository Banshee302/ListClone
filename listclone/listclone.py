import os
import hashlib
import tarfile
import argparse
from pathlib import Path

def hash_file(file_path):
    """Generate a SHA-256 hash for the given file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def create_lcone(folder_path, lcone_path):
    """Create a .lcone file (tarball) from the specified folder."""
    with tarfile.open(lcone_path, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))

def extract_lcone(lcone_path, extract_to):
    """Extract the .lcone file to the specified directory."""
    with tarfile.open(lcone_path, "r:gz") as tar:
        tar.extractall(path=extract_to)

def main():
    parser = argparse.ArgumentParser(description='LIST-CLONE v1.0')
    parser.add_argument('--file', type=str, help='Path to the file or folder to process')
    parser.add_argument('--hash', action='store_true', help='Hash the specified file')
    parser.add_argument('--archive', type=str, help='Create a .lcone file from the specified folder')
    parser.add_argument('--extract', type=str, help='Extract a .lcone file to the specified directory')
    args = parser.parse_args()

    if args.hash and args.file:
        hash_value = hash_file(args.file)
        print(f"Hash for {args.file}: {hash_value}")

    elif args.archive and args.file:
        create_lcone(args.file, args.archive)
        print(f"Created {args.archive} from {args.file}")

    elif args.extract and args.file:
        extract_lcone(args.file, args.extract)
        print(f"Extracted {args.file} to {args.extract}")

    else:
        print("""
        LIST-CLONE v1.0
        
        Usage:
        python listclone.py --file /path/to/file --hash (for hashing)
        python listclone.py --file /path/to/folder --archive /path/to/output.lclone
        python listclone.py --file /path/to/input.lcone --extract /path/to/output_folder
        """)

if __name__ == "__main__":
    main()
