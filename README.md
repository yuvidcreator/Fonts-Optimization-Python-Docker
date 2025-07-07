# Font-Files Compression & Optimisation using Python

--  This mini project is helpful for those who are working on HTML Jinj2 templates
--  My Project's One of objective is about HTML to PDF Generation automation pipeline
    for customly designed PDF Reports generation.

## Technology stack -- for Fonts Optimisation.

1. Python
2. HTML + CSS
3. Jinja2
4. Docker (To test/deploy on any platform/OS)

# Objective --

--  From "templates" directory , read all the HTML files and auto detect mentioned/used font files regardless of any extensions.
--  Then using BeautifulSoup package, extract all contents from all html files and detect only those fonts files which are used.
--  Then Detect / pick only those font files from "fonts" directory, then as per create a new "required_chars.txt" which will be available in "output" directory.
--  As per "required_chars.txt" file's chars, optimise, compress all possible font files from "fonts" directory and save them in "output" directory.
--  Finally, use the "output" directory's fonts to generate PDF report using "WeasyPrint" (for Python) or any of your choice of package.

# Benefit -- Why, "only used characters" specific "Font Files"" optimiztion is necessary?

--  Speedily rendering html contnet before PDF generation.
--  better allocation of resources (CPU, Memory) for PDF generation.
--  Optimised PDF size.
--  Optimised PDF rendering time.
--  Optimised Doc/PDF processing speed.
--  Only used chars are included in finally saved .woff & woff2 files.
--  Final Saved font files are compressed with very less size.
--  e.g. NotoSansCJKjp-VF.ttf file size is about 35mb, as per html chracters it reduced for .woff2 Size: 43 KB & for .woff Size: 53 KB.
--  Very Huge reduction in font files size.
--  This technique can be further used in Django or any other HTML engine framework for amy HTML rendering tasks.

# Projects Folder Structure --

Project/
├── Dockerfile
├── html_font_optimizer.py
├── templates/               ← Your HTML templates + partials/
├── fonts/                   ← All available font files
├── output/              ← Output optimized fonts

# Pre-Requisite --

fonts related @font-face or `<link />` tag's must be mentioned in .html templates

# Inital Setup --

--  Manually create folders ==> templates & fonts.
--  Then cappy paste your all html templetes to "templates" directory.
--  Then copy all font files (which are used in html/css files) to "fonts" directory.
--  CSS file path's not included in this script, you can modify python script as per your requirement, e.g. read font files path from CSS ("static/css/*.css") files as well.
--  Then follow below steps to dockerize cli application.

## Step 1 - Build Docker image

docker build -t font-html-optimizer .

## Step 2 - Run Docker container (Use any one of below command)

docker run --rm 
    -v "$PWD/templates:/app/templates"
    -v "$PWD/fonts:/app/fonts"
    -v "$PWD/output:/app/output"
    font-html-optimizer

or

docker run --rm -v "$PWD/templates:/app/templates" -v "$PWD/fonts:/app/fonts" -v "$PWD/output:/app/output" font-html-optimizer

## Setp 3 - Once all fonts get saved in output directory, you can use them in your project.

--  You can use them in your project by copying them to your project's static/fonts directory.
--  Only ensure final code review for HTML / CSS templates before using them in production.

# IMP Note : Use .woff or woff2 --> saved font files from output directory.

--  For comparative files sizes , use log file generated in "output" directory.
--  e.g. In your project, if you used "NotoSansCJKjp-VF.ttf" file before optimization,
    and when you replaced all fonts with newly saved (copy-pasting) fonts to your projects static/fonts directory,
    "make sure that all fonts files extension must be replced by .woff or woff2 files only".
