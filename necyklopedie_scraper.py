import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
import time

BASE_URL = "https://necyklopedie.org"
START_PATH = "/wiki/Kategorie:Nejlepší_články"
OUTPUT_DIR = "llm_clean_txt"
DELAY = 1
MAX_DEPTH = 1 # max start depth
DEEP_ITER = 100 # number of deeping iterations
DEPP_INC  = 1 # depth increment size for iteration
# total_max_depth = MAX_DEPTH + (DEEP_ITER - 1) * DEPP_INC

visited = set()
os.makedirs(OUTPUT_DIR, exist_ok=True)


BLACKLIST_PHRASES = [
    "Tento článek",
    "Tematicky se překrývá",
    "Kategorie:",
    "Editovat",
]


def clean_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-").rstrip()


def clean_text(text):
    # odstranění referencí [1], [23]
    text = re.sub(r"\[\d+\]", "", text)

    # odstranění vícenásobných mezer
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_valid_paragraph(text):
    if len(text) < 120:
        return False

    for phrase in BLACKLIST_PHRASES:
        if phrase in text:
            return False

    return True

import re

REPLACEMENTS = {
    r"\displaystyle": "",
    r"\infty": "∞",
    r"\cdot": "·",
    r"\times": "×",
    r"\leq": "≤",
    r"\geq": "≥",
}

def clean_latex(text):
    # <math> bloky (Wikipedia)
    text = re.sub(r"<math.*?>(.*?)</math>", r"\1", text, flags=re.DOTALL)

    # $$...$$ a $...$
    text = re.sub(r"\$\$(.*?)\$\$", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\$(.*?)\$", r"\1", text, flags=re.DOTALL)

    # \frac{a}{b} → a/b
    text = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", text)

    # \sqrt{a} → √a
    text = re.sub(r"\\sqrt\{([^{}]*)\}", r"√\1", text)

    # ostatní jednoargumentové příkazy (ponechá obsah)
    text = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", text)

    # konkrétní náhrady
    for key, value in REPLACEMENTS.items():
        text = text.replace(key, value)

    # odstranění zbylých LaTeX příkazů bez argumentu
    text = re.sub(r"\\[a-zA-Z]+", "", text)

    return text.strip()

def normalize_final_text(text):
    # odstraní mezery na začátku a konci řádků
    lines = [line.strip() for line in text.split("\n")]

    # zahodí prázdné řádky
    lines = [line for line in lines if line]

    # spojí odstavce jedním prázdným řádkem
    return clean_latex("\n\n".join(lines))

def extract_clean_text(soup):
    content = soup.find("div", class_="mw-parser-output")
    if not content:
        return ""

    # odstranit rušivé části
    for tag in content.find_all([
        "table", "style", "script", "sup"
    ]):
        tag.decompose()

    for selector in [
        ".infobox",
        ".navbox",
        ".metadata",
        ".toc",
        ".thumb",
        ".mw-editsection",
        ".hatnote"
    ]:
        for tag in content.select(selector):
            tag.decompose()

    paragraphs = content.find_all("p")
    cleaned = []

    for p in paragraphs:
        text = clean_text(p.get_text())
        if is_valid_paragraph(text):
            cleaned.append(text)

    raw_text = "\n\n".join(cleaned)
    return normalize_final_text(raw_text)


def crawl(path, depth):
    full_url = urljoin(BASE_URL, path)
    if full_url in visited:
        return
    
    if depth > MAX_DEPTH:
        return

    print("Stahuji:", full_url)
    visited.add(full_url)

    try:
        r = requests.get(full_url)
        r.raise_for_status()
    except:
        return

    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.find("h1")
    if not title_tag:
        return

    title = title_tag.get_text()
    filename = clean_filename(title) + ".txt"

    text = extract_clean_text(soup)

    if len(text) > 300:
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(text)

    time.sleep(DELAY)

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and ":" not in href:
            crawl(href, depth + 1)


if __name__ == "__main__":
    # use IDS algoritm
    for i in range(DEEP_ITER):
        MAX_DEPTH += DEPP_INC
        crawl(START_PATH, 0)

    print("Hotovo.")