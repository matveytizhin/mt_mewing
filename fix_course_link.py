#!/usr/bin/env python3
"""
Заменяет ссылку на название курса "Краниоформ (Методика естественной гармонизации)"
с https://doingmewing.ru/... на локальный index.html

Положи в папку DoingMewing и запусти: python fix_course_link.py
"""

import os
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP_FILES = {"index_fixed.html"}

# Паттерн: ссылка с текстом названия курса
COURSE_LINK_RE = re.compile(
    r'<a\s+href="https://doingmewing\.ru/teach/control/stream/view/id/\d+">'
    r'Краниоформ \(Методика естественной гармонизации\)'
    r'</a>',
    re.DOTALL
)

REPLACEMENT = '<a href="index.html">Краниоформ (Методика естественной гармонизации)</a>'

def main():
    print("🔗 Заменяем ссылку на название курса...\n")

    html_files = [
        f for f in os.listdir(CURRENT_DIR)
        if f.endswith(".html") and f not in SKIP_FILES
    ]

    replaced = 0

    for filename in sorted(html_files):
        filepath = os.path.join(CURRENT_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = COURSE_LINK_RE.sub(REPLACEMENT, content)

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  [OK] {filename}")
            replaced += 1
        else:
            print(f"  [--] {filename}: не найдено")

    print(f"\n✅ Готово! Обновлено файлов: {replaced}")

if __name__ == "__main__":
    main()
