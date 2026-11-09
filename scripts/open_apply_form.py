#!/usr/bin/env python3
"""Open the stallholder apply form on apply.html without brittle exact-HTML matches.

Usage:
  python3 scripts/open_apply_form.py \\
    --form-url 'https://docs.google.com/forms/d/e/.../viewform' \\
    --opened-notice '１２月１日（火）・１２月１６日（水）の出店募集を開始しました。' \\
    --button-label '１２月１日（火）・１６日（水）の出店を申し込む' \\
    [--dry-run]

Replaces:
  - apply-notice__label 受付開始予定 → 受付開始
  - first apply-notice__item (the next-opening teaser) → opened notice span
  - the main CTA under btn--center → new form link + label

Does NOT require the previous closed button wording or the exact teaser dates
to match character-for-character (that is what aborted the 2026-11-09 23:30 job).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = ROOT / "apply.html"


def open_apply(html: str, form_url: str, opened_notice: str, button_label: str) -> str:
    if "docs.google.com/forms" not in form_url or "/viewform" not in form_url:
        raise SystemExit("form URL must be a Google Form .../viewform link")

    if "受付開始予定" not in html and 'apply-notice__label">受付開始</p>' in html:
        raise SystemExit("apply.html already looks open (label is 受付開始); abort")

    if "受付開始予定" not in html:
        raise SystemExit("apply-notice__label '受付開始予定' not found; abort")

    html2, n = re.subn(
        r'(<p class="apply-notice__label">)受付開始予定(</p>)',
        r"\1受付開始\2",
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit("failed to flip apply-notice__label; abort")

    # First notice item only: whatever the teaser currently says → opened copy.
    item_re = re.compile(
        r'(<div class="apply-notice-list">\s*'
        r'<p class="apply-notice__item">)'
        r'.*?'
        r'(</p>)',
        re.DOTALL,
    )
    replacement = (
        r"\1\n"
        f'              <span class="apply-notice__date">{opened_notice}</span>\n'
        r"            \2"
    )
    html3, n = item_re.subn(replacement, html2, count=1)
    if n != 1:
        raise SystemExit("failed to replace first apply-notice__item; abort")

    btn_re = re.compile(
        r'(<div class="btn btn--center(?:\s+btn--apply)?"><a )'
        r'[^>]*>'
        r'[^<]*'
        r'(</a></div>)',
        re.DOTALL,
    )
    btn_html = (
        r"\1"
        f'target="_blank" class="btn__item btn__item--apply u-btn-bg-clr u-btn-clr u-font" '
        f'href="{form_url}" rel="noopener">{button_label}'
        r"\2"
    )
    html4, n = btn_re.subn(btn_html, html3, count=1)
    if n != 1:
        raise SystemExit("failed to replace btn--center CTA; abort")

    return html4


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--form-url", required=True)
    ap.add_argument("--opened-notice", required=True)
    ap.add_argument("--button-label", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file", type=Path, default=APPLY)
    args = ap.parse_args()

    raw = args.file.read_text(encoding="utf-8")
    out = open_apply(raw, args.form_url, args.opened_notice, args.button_label)
    if args.dry_run:
        print("dry-run ok: notice label, first item, and CTA would update")
        return 0
    args.file.write_text(out, encoding="utf-8")
    print(f"updated {args.file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
