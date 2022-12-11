# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Skiylia'
copyright = '2022, Jack Lloyd-Walters'
author = 'Jack Lloyd-Walters'

release = '0.0'
version = '0.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

html_logo = '_images/Skiylia_Logo_text.svg'

html_favicon = '_images/Skiylia_Logo.ico'

html_static_path = ['_images','_static']

# -- Options for EPUB output
epub_show_urls = 'footnote'
