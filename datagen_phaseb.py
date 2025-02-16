#!/usr/bin/env python3
# datagen_b.py

# DISCLAIMER: THIS SCRIPT IS A GUIDE FOR PHASE B DATA GENERATION.
# It creates sample data files required by Phase B tasks.
#
# Usage: uv run datagen_b.py <email> [--root=<data_directory>]
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "faker",
#     "pillow",
# ]
# ///

import os
import sys
import sqlite3
import subprocess
import shutil
from faker import Faker
from PIL import Image, ImageDraw

# Configuration dictionary for Phase B
config = {"root": "/data"}

def write_file(path, content):
    full_path = os.path.join(config["root"], path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

# ------------------------------
# B4: Create a dummy Git repository for cloning
# ------------------------------
def b4_create_dummy_repo():
    # Create a dummy repository in /tmp/dummy_repo_b
    repo_path = os.path.join("/tmp", "dummy_repo_b")
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.makedirs(repo_path, exist_ok=True)
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    # Create a dummy file and commit it
    dummy_file = os.path.join(repo_path, "dummy.txt")
    with open(dummy_file, "w") as f:
        f.write("Initial content for Phase B dummy repo.")
    subprocess.run(["git", "add", "dummy.txt"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)
    print(f"Dummy Git repository created at {repo_path}")
    return repo_path

# ------------------------------
# B5: Create a SQLite database for SQL query testing
# ------------------------------
def b5_create_db():
    db_path = os.path.join(config["root"], "test_b5.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE numbers (value INTEGER)")
    # Insert sample data (you can modify these values as needed)
    values = [10, 20, 30, 40]
    cur.executemany("INSERT INTO numbers (value) VALUES (?)", [(v,) for v in values])
    conn.commit()
    conn.close()
    print(f"SQLite database created at {db_path} with table 'numbers'")
    return db_path

# ------------------------------
# B7: Generate an image file for image processing
# ------------------------------
def b7_create_image():
    # Create a simple red image of 100x100 pixels
    img_path = os.path.join(config["root"], "test_image_b7.jpg")
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)
    print(f"Image created at {img_path}")
    return img_path

# ------------------------------
# B8: Generate a simulated audio file (with .mp3 extension)
# ------------------------------
def b8_create_audio():
    # Create a text file with .mp3 extension containing known text
    audio_path = os.path.join(config["root"], "test_audio_b8.mp3")
    transcript = "This is a simulated transcription for Phase B audio."
    with open(audio_path, "w") as f:
        f.write(transcript)
    print(f"Simulated audio file created at {audio_path}")
    return audio_path

# ------------------------------
# B9: Generate a Markdown file for conversion
# ------------------------------
def b9_create_markdown():
    md_path = os.path.join(config["root"], "sample_b9.md")
    md_content = "# Sample Markdown for Phase B\n\nThis is a test markdown file for conversion."
    write_file("sample_b9.md", md_content)
    print(f"Markdown file created at {md_path}")
    return md_path

# ------------------------------
# B10: Generate a CSV file for filtering
# ------------------------------
def b10_create_csv():
    csv_path = os.path.join(config["root"], "test_b10.csv")
    rows = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
        {"name": "Charlie", "age": "30"},
        {"name": "Diana", "age": "40"},
    ]
    import csv
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV file created at {csv_path}")
    return csv_path

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Phase B data files")
    parser.add_argument("email", help="Seed email for generating data")
    parser.add_argument("--root", default="/data", help="Root directory for generated files")
    args = parser.parse_args()
    config["email"] = args.email
    config["root"] = os.path.abspath(args.root)
    os.makedirs(config["root"], exist_ok=True)

    print("Generating Phase B data files...")
    print("Files will be created at", config["root"])

    # Generate dummy Git repository for B4
    b4_repo = b4_create_dummy_repo()

    # Create SQLite database for B5
    b5_db = b5_create_db()

    # Create image for B7
    b7_img = b7_create_image()

    # Create simulated audio file for B8
    b8_audio = b8_create_audio()

    # Create Markdown file for B9
    b9_md = b9_create_markdown()

    # Create CSV file for B10
    b10_csv = b10_create_csv()

    print("Phase B data generation complete.")
