import os
from bs4 import BeautifulSoup

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def test_local_resources_exist():
    html_path = os.path.join(REPO_ROOT, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    src_attrs = []
    for tag in soup.find_all(['img', 'video', 'source']):
        if tag.name == 'source' and tag.get('src', '').startswith('http'):
            continue
        src = tag.get('src') or tag.get('href')
        if src:
            if src.startswith('http') or src.startswith('https'):
                continue
            src_attrs.append(src)

    missing = [p for p in src_attrs if not os.path.exists(os.path.join(REPO_ROOT, p))]
    assert not missing, f"Missing files referenced in HTML: {missing}"
