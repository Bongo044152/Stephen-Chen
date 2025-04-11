# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # 確保能正確匯入上層模組

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Stephen-Chen'
copyright = '2025, 陳心璿'
author = '陳心璿'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # 自動從 docstring 產生文件
    'sphinx.ext.napoleon',       # 支援 Google / NumPy style docstring
    'sphinx.ext.viewcode',       # 讓文件有原始碼連結
    'sphinx.ext.autosummary',    # 自動產生 summary table
]

autosummary_generate = True       # 自動建立 autosummary 頁面
# 顯示 class 裡成員（像 method、attribute）時，順序依照你程式碼的原始定義來排（不是亂序或字母排序）
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,              # 包含 class 中的所有成員（method、屬性等）
    'undoc-members': True,        # 即使沒 docstring 的成員也列出來
    'private-members': False,     # 不包含以 _ 開頭的 private 成員（你可以改成 True）
    'special-members': '__init__',# 顯示特殊方法（如 __init__）
    'inherited-members': True,    # 顯示從父類別繼承的成員
    'show-inheritance': True,     # 在 class 說明中顯示繼承關係
}

templates_path = ['_templates']
exclude_patterns = [
    '_build',                 # Sphinx 產出
    'Thumbs.db',              # Windows 系統檔
    '.DS_Store',              # macOS 系統檔
    'scrappp/*',              # 垃圾
    '.venv/*',
    '__pycache__/*',          # Python 快取
    '*.pyc',                  # 編譯後的中繼檔
    '*.txt',
    # '*.md',
    '*.ipynb',
    'professor_data.db', 
    'download_chrome.ps1',
    'scrapy.cfg',
    # 'README.md',
    'requirements.txt',
    'data',
    # "chrome",
    # "chromedriver",
    ".git",
    "docs",
    "config"
]

autodoc_mock_imports = [
    'selenium',  # 忽略 selenium 模組，以免出現執行 chrome.exe 之類的錯誤，電腦就是笨!
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
