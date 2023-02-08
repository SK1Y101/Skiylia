# Configuration file for the Sphinx documentation builder.

import os
import re
import sys

sys.path.insert(0, os.path.abspath(".."))
# -- Project information

from SkiyliaLexer import SkiyliaLexer  # isort: skip

project = "Skiylia Lang"
copyright = "2022, Jack Lloyd-Walters"
author = "Jack Lloyd-Walters"

with open("../../src/skiylia.py", "r") as f:
    skiylia_source = f.readlines()

rnum = {"major": None, "minor": None, "patch": None, "ident": None}
for line in skiylia_source:
    if None not in set(rnum.values()):
        break
    for k in rnum.keys():
        search = re.search(rf"{k} = .+", line)
        if search:
            rnum[k] = search.group().replace(f"{k} = ", "").strip().strip('"')

# Full version, including tags
release = f"{rnum['major']}.{rnum['minor']}.{rnum['patch']}" + (
    f"-{rnum['ident']}" if rnum["ident"] else ""
)
# shortened version name
version = ".".join(release.split(".")[:2])

# code-highlighting
from sphinx.highlighting import lexers

lexers["skiylia"] = SkiyliaLexer()


# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_tabs.tabs",
    "sphinx_rtd_dark_mode",
]

pygments_style = "sphinx"
highlight_language = "none"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "skiylia": ("https://skiylia.readthedocs.io", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

classic = "classic"
rtd = "sphinx_rtd_theme"
html_theme = classic

skiylia_light_grey = "#eeebee"
skiylia_grey = "#cfd3d7"
skiylia_light_blue = "#a2ddef"
skiylia_dark_blue = "#a2ceef"

skiylia_text = "#5C5962"
skiylia_bg = "#ffffff"

html_theme_options = {
    "bgcolor": skiylia_bg,
    "textcolor": skiylia_text,
    "linkcolor": skiylia_light_blue,
    "visitedlinkcolor": skiylia_dark_blue,
    "headtextcolor": skiylia_text,
    "headlinkcolor": skiylia_light_blue,
    "footerbgcolor": skiylia_dark_blue,
    "footertextcolor": skiylia_text,
    "sidebarbgcolor": "#f2f2f2",
    "sidebarbtncolor": skiylia_dark_blue,
    "sidebartextcolor": skiylia_text,
    "sidebarlinkcolor": skiylia_light_blue,
    "relbarbgcolor": skiylia_light_blue,
    "relbartextcolor": skiylia_text,
    "relbarlinkcolor": skiylia_text,
    "codebgcolor": skiylia_light_grey,
    # "codetextcolor": skiylia_text,
}

html_logo = "_images/Skiylia_Logo_text.svg"

html_favicon = "_images/Skiylia_Logo.ico"

html_static_path = ["_images", "_static"]

html_css_files = [
    "css/custom.css",
]

# -- Options for EPUB output
epub_show_urls = "footnote"

# -- Options for dark theming
default_dark_mode = True
