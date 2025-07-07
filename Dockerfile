FROM python:3.11-slim-bookworm

LABEL maintainer="Yuvraaj"
WORKDIR /app

# System dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential fontconfig woff2 libbrotli-dev \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# # Python tools
# RUN pip install --no-cache-dir fonttools brotli

# # Copy project templates & scripts
# COPY templates/ /app/templates/
# COPY input_fonts/ /app/input_fonts/
# COPY optimize-fonts-html.sh /usr/local/bin/optimize-fonts-html-docker
# RUN chmod +x /usr/local/bin/optimize-fonts-html-docker

# ENTRYPOINT ["optimize-fonts-html-docker"]


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential woff2 libbrotli-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fonttools brotli beautifulsoup4

COPY html_font_optimizer.py /app/html_font_optimizer.py
COPY templates/ /app/templates/
COPY fonts/ /app/fonts/

ENTRYPOINT ["python", "html_font_optimizer.py"]
