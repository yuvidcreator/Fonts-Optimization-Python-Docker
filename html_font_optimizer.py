#!/usr/bin/env python3

import os
import re
import sys
import pathlib
from fontTools import subset
from bs4 import BeautifulSoup

# Environment paths
TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", "/app/templates")
FONT_SRC_DIR = os.environ.get("FONT_SRC_DIR", "/app/fonts")
DEST_DIR = os.environ.get("DEST_DIR", "/app/output")
REQUIRED_CHARS_PATH = os.environ.get("REQUIRED_CHARS_PATH", "/app/output/required_chars.txt")
LOG_FILE = os.path.join(DEST_DIR, "font_optimization_report.log")

os.makedirs(DEST_DIR, exist_ok=True)

# Step 1: Extract characters from HTML (text content only)
def extract_visible_text_characters(template_dir):
    characters = set()
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = soup.get_text()
                    characters.update(text)
    return "".join(sorted(characters))

# # Step 2: Detect local font files used in HTML templates
# def detect_used_font_files(template_dir, font_dir):
#     used_fonts = set()
#     font_pattern = re.compile(r"url\(['\"]?([^'\")]+?\.(ttf|woff2?|otf))['\"]?\)", re.IGNORECASE)

#     for root, _, files in os.walk(template_dir):
#         for file in files:
#             if file.endswith(".html"):
#                 with open(os.path.join(root, file), "r", encoding="utf-8") as f:
#                     content = f.read()
#                     matches = font_pattern.findall(content)
#                     for match in matches:
#                         font_path = match[0].strip("\"'")
#                         font_file = os.path.basename(font_path)
#                         local_font_path = os.path.join(font_dir, font_file)
#                         if os.path.isfile(local_font_path):
#                             used_fonts.add(font_file)
#                         else:
#                             print(f"⚠️  Referenced font not found locally: {font_file}")
#     return used_fonts


# Step 2: Detect all font file names (of any extension) used in HTML templates (by basename only)
def detect_used_font_files(template_dir, font_dir):
    used_fonts = set()
    font_pattern = re.compile(r"url\(['\"]?([^'\")]+)['\"]?\)", re.IGNORECASE)

    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = font_pattern.findall(content)
                    for match in matches:
                        font_name = os.path.basename(match.strip())
                        name_without_query = font_name.split('?')[0]  # strip version/hash/query
                        for font_file in os.listdir(font_dir):
                            if font_file.startswith(name_without_query.split('.')[0]):
                                used_fonts.add(font_file)
                                break
    return used_fonts



# Step 3: Subset fonts and save .woff and .woff2
def subset_fonts(font_files, used_chars):
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        for font_file in font_files:
            input_path = os.path.join(FONT_SRC_DIR, font_file)
            if not os.path.isfile(input_path):
                log.write(f"⚠️  Skipping missing font: {font_file}\n")
                continue

            base_name = os.path.splitext(font_file)[0]
            log.write(f"\n🔧 Processing: {font_file}\n")
            original_size = os.path.getsize(input_path)
            log.write(f"   Original Size: {original_size // 1024} KB\n")

            for flavor in ["woff2", "woff"]:
                output_path = os.path.join(DEST_DIR, f"{base_name}.{flavor}")
                try:
                    subset.main([
                        input_path,
                        f"--output-file={output_path}",
                        f"--flavor={flavor}",
                        f"--text={used_chars}",
                        "--no-hinting",
                        "--layout-features=*",
                        "--drop-tables+=DSIG",
                        "--drop-tables+=LTSH"
                    ])
                    final_size = os.path.getsize(output_path)
                    log.write(f"   ➤ .{flavor} Size: {final_size // 1024} KB\n")
                except Exception as e:
                    log.write(f"⚠️  .{flavor} failed: {font_file} — {e}\n")

if __name__ == "__main__":
    print("📑 Extracting visible characters from templates...")
    characters = extract_visible_text_characters(TEMPLATE_DIR)
    os.makedirs(os.path.dirname(REQUIRED_CHARS_PATH), exist_ok=True)
    with open(REQUIRED_CHARS_PATH, "w", encoding="utf-8") as f:
        f.write(characters)
    print(f"✅ Characters written to {REQUIRED_CHARS_PATH} ({len(characters)} chars)")

    print("🔎 Detecting font files used in templates...")
    used_fonts = detect_used_font_files(TEMPLATE_DIR, FONT_SRC_DIR)
    print(f"✅ Found {len(used_fonts)} used fonts: {', '.join(used_fonts)}")

    print("🚀 Starting font optimization...")
    subset_fonts(used_fonts, characters)
    print(f"✅ Font optimization completed. Output → {DEST_DIR}")
