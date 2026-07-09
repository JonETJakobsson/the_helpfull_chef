"""MkDocs hook: rewrite OKF bundle-absolute links to relative links.

Recipe, ingredient and knowledge files use bundle-absolute Markdown links such as
``[Potatis](/ingredients/potatis.md)`` (per the Open Knowledge Format convention).
MkDocs treats a leading-slash link as site-absolute and does not rewrite the ``.md``
extension, which breaks the link on GitHub Pages (the site is served under a project
subpath like ``/the_helpfull_chef/``).

This hook converts every ``/foo/bar.md`` link into a path relative to the current page
*before* MkDocs resolves links, so MkDocs then produces correct URLs — including the
site base path and directory-style URLs.
"""
from __future__ import annotations

import posixpath
import re

_LINK = re.compile(r"\]\((/[^)#]+\.md)(#[^)]*)?\)")


def on_page_markdown(markdown, *, page, config, files, **kwargs):
    src_dir = posixpath.dirname(page.file.src_uri)

    def _replace(match: "re.Match[str]") -> str:
        target = match.group(1).lstrip("/")
        anchor = match.group(2) or ""
        rel = posixpath.relpath(target, src_dir) if src_dir else target
        return f"]({rel}{anchor})"

    return _LINK.sub(_replace, markdown)
