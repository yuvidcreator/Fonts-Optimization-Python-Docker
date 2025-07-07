# Folder Structure --
project/
├── Dockerfile
├── html_font_optimizer.py
├── templates/               ← Your HTML templates + partials/
├── input_fonts/                   ← All available font files
├── final_fonts/              ← Output optimized fonts


# optimize-fonts-html.sh – Full Logic (Runs Inside Docker)


# Step -
docker build -t font-html-optimizer .

docker run --rm \
    -v "$PWD/templates:/app/templates" \
    -v "$PWD/fonts:/app/fonts" \
    -v "$PWD/output:/app/output" \
    font-html-optimizer

or 

docker run --rm -v "$PWD/templates:/app/templates" -v "$PWD/fonts:/app/fonts" -v "$PWD/output:/app/output" font-html-optimizer