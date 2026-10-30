"""Dependency-free checks for the four-page static website.

Run: python scripts/check-site.py [--base-url http://127.0.0.1:8787]
The optional HTTP checks target a local preview, never production.
"""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, unquote, urljoin, urlsplit
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "public"
DOMAIN = "https://solvrahydraulics.com"
ROUTES = ("/", "/product/", "/applications/", "/early-evaluation/")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Element:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return "".join(c.text() if isinstance(c, Element) else c for c in self.children)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack, self.elements = [self.root], []
        self.feed(source)
        assert len(self.stack) == 1, "Unclosed HTML element"

    def handle_starttag(self, tag, attrs):
        el = Element(tag, attrs)
        self.stack[-1].children.append(el)
        self.elements.append(el)
        if tag == "br":
            el.children.append(" ")
        if tag not in VOID:
            self.stack.append(el)

    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, f"Invalid nesting at </{tag}>"
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def find(self, tag, **attrs):
        return [el for el in self.elements if el.tag == tag and all(el.attrs.get(k) == v for k, v in attrs.items())]

    def one(self, tag, **attrs):
        matches = self.find(tag, **attrs)
        assert len(matches) == 1, f"Expected one {tag} {attrs}, found {len(matches)}"
        return matches[0]


def page_file(route):
    return ROOT / route.lstrip("/") / "index.html"


def normalize(text):
    return " ".join(text.split())


def check():
    documents = {route: Document(page_file(route).read_text(encoding="utf-8-sig")) for route in ROUTES}
    assert set(ROOT.rglob("*.html")) == {page_file(r) for r in ROUTES}, "Expected exactly four public HTML pages"
    titles, descriptions, headings = [], [], []
    all_links = set()
    for route, doc in documents.items():
        assert doc.one("html").attrs.get("lang") == "en"
        title = normalize(doc.one("title").text())
        description = doc.one("meta", name="description").attrs["content"]
        h1 = normalize(doc.one("h1").text())
        assert title and description and h1
        titles.append(title); descriptions.append(description); headings.append(h1)
        assert doc.one("link", rel="canonical").attrs["href"] == DOMAIN + route
        for key, value in (("og:title", title), ("og:description", description), ("og:url", DOMAIN + route), ("og:type", "website")):
            assert doc.one("meta", property=key).attrs["content"] == value, (route, key)
        assert doc.one("meta", property="og:image").attrs["content"] == DOMAIN + "/assets/atlas-map.webp"
        assert doc.one("meta", name="twitter:card").attrs["content"] == "summary_large_image"
        assert not doc.find("meta", name="keywords"), "No keyword stuffing"
        assert not any("verification" in el.attrs.get("name", "") for el in doc.find("meta"))
        main = doc.one("main", id="main")
        assert main.attrs.get("tabindex") == "-1", "Skip link target must be focusable"
        ids = [el.attrs["id"] for el in doc.elements if "id" in el.attrs]
        assert len(ids) == len(set(ids)), (route, "duplicate IDs")
        last_level = 0
        for el in doc.elements:
            if re.fullmatch(r"h[1-6]", el.tag):
                level = int(el.tag[1])
                assert level <= last_level + 1, (route, "heading level skipped")
                last_level = level
        for label in ("Main navigation", "Footer navigation"):
            menu = doc.one("nav", **{"aria-label": label})
            links = [el for el in menu.children if isinstance(el, Element) and el.tag == "a"]
            assert [el.attrs["href"] for el in links] == list(ROUTES)
            assert [el.attrs["href"] for el in links if el.attrs.get("aria-current") == "page"] == [route]
        footer = doc.one("footer")
        assert "© 2026 Solvra Hydraulics LLC" in footer.text()
        assert "info@solvrahydraulics.com" in footer.text()
        assert "subject to readiness and validation" in footer.text()
        assert not any(doc.find(tag) for tag in ("form", "iframe", "video", "input", "button")), "No unready interaction workflows"
        for image in doc.find("img"):
            assert image.attrs.get("src") == "/assets/solvra-icon.png", "Only the approved icon belongs in HTML"
            assert all(key in image.attrs for key in ("alt", "width", "height"))
        for script in doc.find("script"):
            assert route == "/" and script.attrs.get("type") == "application/ld+json", "No executable client scripts"
            org = json.loads(script.text())
            assert org["@type"] == "Organization" and org["name"] == "Solvra Hydraulics LLC"
            assert org["email"] == "info@solvrahydraulics.com"
            assert not any(key in org for key in ("offers", "aggregateRating", "review"))
        text = normalize(doc.root.text())
        forbidden = r"\b(transient|surge|water hammer|AI|SCADA|digital.twin|multiphase|Newton.Raphson|Picard|optimization|unlimited|industry.leading|certified|pricing|beta available)\b"
        assert not re.search(forbidden, text, re.I), (route, "unapproved public claim")
        assert "in development" in text.lower() and "2027" in text
        if route != "/product/":
            assert "Synergi" not in text and "DNV" not in text
        for el in doc.elements:
            for attr in ("href", "src"):
                ref = el.attrs.get(attr)
                if ref is None:
                    continue
                assert ref and ref != "#", "No placeholder links"
                parsed = urlsplit(ref)
                if parsed.scheme == "mailto":
                    assert parsed.path == "info@solvrahydraulics.com"
                    continue
                if parsed.scheme:
                    assert parsed.scheme == "https" and parsed.netloc == "solvrahydraulics.com", "Unexpected external request"
                target = urlsplit(urljoin(DOMAIN + route, ref))
                relative = unquote(target.path).lstrip("/")
                path = ROOT / relative
                if target.path.endswith("/"):
                    assert target.path in ROUTES
                    path /= "index.html"
                assert path.is_file(), (route, "missing asset/page", ref)
                if target.fragment:
                    target_doc = documents[target.path]
                    assert any(n.attrs.get("id") == target.fragment for n in target_doc.elements), (route, "missing anchor", ref)
                all_links.add(target.path)
        print(f"PASS {route}: metadata, headings, navigation, links, assets, and content guardrails")
    assert len(set(titles)) == len(set(descriptions)) == len(set(headings)) == 4, "Page SEO text must be unique"
    product = documents["/product/"]
    panel = product.one("div", **{"class": "import-panel"})
    panel_text = normalize(panel.text())
    assert "supported legacy Synergi Gas models" in panel_text
    assert "reviewed and validated" in panel_text
    assert "not affiliated with, sponsored by, or endorsed by DNV" in panel_text
    assert product.root.text().count("Synergi Gas") == 1
    inquiry = next(el for el in documents["/early-evaluation/"].find("a") if "?subject=" in el.attrs.get("href", ""))
    assert parse_qs(urlsplit(inquiry.attrs["href"]).query) == {"subject": ["Solvra Early Evaluation Inquiry"]}
    stylesheet = (ROOT / "styles.css").read_text(encoding="utf-8-sig")
    for ref in re.findall(r'url\("([^"]+)"\)', stylesheet):
        assert (ROOT / ref.lstrip("/")).is_file(), ref
        all_links.add(ref)
    assert ":focus-visible" in stylesheet and "prefers-reduced-motion" in stylesheet
    robots = (ROOT / "robots.txt").read_text()
    assert "User-agent: *" in robots and "Allow: /" in robots and f"Sitemap: {DOMAIN}/sitemap.xml" in robots
    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    locs = [el.text for el in sitemap.findall("{*}url/{*}loc")]
    assert locs == [DOMAIN + route for route in ROUTES]
    assert not sitemap.findall(".//{*}lastmod"), "No invented publication dates"
    print(f"PASS unique SEO, exact four-URL sitemap, robots, mailto subject, and import disclaimer; {len(all_links)} distinct local targets")
    return all_links


def check_http(base_url, targets):
    parsed = urlsplit(base_url)
    assert parsed.scheme == "http" and parsed.hostname in ("127.0.0.1", "localhost", "::1"), "HTTP checks are local-only"
    for path in sorted(targets | set(ROUTES) | {"/robots.txt", "/sitemap.xml"}):
        with urlopen(base_url.rstrip("/") + path, timeout=10) as response:
            assert response.status == 200, (path, response.status)
    for route in ROUTES[1:]:
        with urlopen(base_url.rstrip("/") + route.rstrip("/"), timeout=10) as response:
            assert response.status == 200 and urlsplit(response.url).path == route, "Directory URL must resolve correctly"
    for path in ("/missing-v2-check/", "/product/missing-page/", "/assets/missing-v2-check.png"):
        try:
            urlopen(base_url.rstrip("/") + path, timeout=10)
        except HTTPError as error:
            assert error.code == 404, (path, error.code)
        else:
            raise AssertionError("Unknown URLs must return HTTP 404")
    print("PASS local HTTP pages/assets, slashless redirects, robots/sitemap, and three real 404 responses")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    options = parser.parse_args()
    targets = check()
    if options.base_url:
        check_http(options.base_url, targets)
