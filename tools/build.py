#!/usr/bin/env python3
"""Build helper for the Juggle repo.

1. Regenerates .cursor/rules/juggle.mdc from AGENTS.md (one source of truth).
2. Builds dist/juggle.zip (SKILL.md, references and scripts) for Claude.ai upload and GitHub
   releases. Zip root is the juggle/ folder.

Run from anywhere: python3 tools/build.py
"""
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "skills", "juggle")

MDC_HEADER = (
    "---\n"
    'description: "Juggle: keep every request when the person layers or queues extra messages while you work."\n'
    "globs:\n"
    "alwaysApply: true\n"
    "---\n\n"
)
MDC_INTRO = (
    "These rules come from the Juggle skill (https://github.com/HYDERMAA/juggle). Keep this file at\n"
    "`.cursor/rules/juggle.mdc` in your project so Cursor applies it to every chat.\n"
)


def build_mdc():
    with open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8") as fh:
        text = fh.read()
    text = re.sub(r"(# Juggle rules for AI agents\n\n)(.*?\n)\n", lambda m: m.group(1) + MDC_INTRO + "\n", text, count=1, flags=re.S)
    out = os.path.join(ROOT, ".cursor", "rules", "juggle.mdc")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(MDC_HEADER + text)
    return out


def _add(z, arc, data, mode=0o644):
    info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = mode << 16
    z.writestr(info, data)


def build_zip():
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    out = os.path.join(dist, "juggle.zip")
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(SKILL_DIR):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for name in sorted(filenames):
                if name.endswith(".pyc") or name == ".DS_Store":
                    continue
                full = os.path.join(dirpath, name)
                arc = os.path.join("juggle", os.path.relpath(full, SKILL_DIR)).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    _add(z, arc, fh.read(), 0o755 if name.endswith(".py") else 0o644)
    return out


if __name__ == "__main__":
    print("wrote", os.path.relpath(build_mdc(), ROOT))
    print("wrote", os.path.relpath(build_zip(), ROOT))
