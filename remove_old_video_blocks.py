#!/usr/bin/env python3
"""
Удаляет старые блоки o-lt-video из всех HTML файлов.
Блок выглядит так:
    <div ... class="lite-block-live-wrapper o-lt-video ...">
        ... много содержимого ...
    </div>  ← закрывающий div всего блока

Положи в папку DoingMewing и запусти: python remove_old_video_blocks.py
"""

import os
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_FILES = {"index.html", "index_fixed.html"}

def remove_video_blocks(content):
    """
    Находит все <div ... class="...o-lt-video..."> и удаляет их целиком,
    считая вложенные теги (баланс div).
    """
    result = []
    i = 0
    removed = 0

    while i < len(content):
        # Ищем начало блока o-lt-video
        match = re.search(
            r'<div[^>]+class="[^"]*lite-block-live-wrapper[^"]*o-lt-video[^"]*"[^>]*>',
            content[i:]
        )

        if not match:
            # Больше нет блоков — добавляем остаток
            result.append(content[i:])
            break

        abs_start = i + match.start()

        # Добавляем всё до начала блока
        result.append(content[i:abs_start])

        # Находим конец блока — считаем баланс <div> / </div>
        block_start = abs_start + len(match.group(0))
        depth = 1
        j = block_start

        while j < len(content) and depth > 0:
            open_tag = content.find('<div', j)
            close_tag = content.find('</div>', j)

            if close_tag == -1:
                # Нет закрывающего тега — аварийный выход
                j = len(content)
                break

            if open_tag != -1 and open_tag < close_tag:
                depth += 1
                j = open_tag + 4
            else:
                depth -= 1
                j = close_tag + 6

        # j теперь указывает сразу после закрывающего </div> блока
        removed += 1
        i = j

    return ''.join(result), removed


def main():
    print("🧹 Удаляем старые блоки o-lt-video...\n")

    html_files = [
        f for f in os.listdir(CURRENT_DIR)
        if f.endswith(".html") and f not in SKIP_FILES
    ]

    total_removed = 0

    for filename in sorted(html_files):
        filepath = os.path.join(CURRENT_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content, removed = remove_video_blocks(content)

        if removed > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  [OK] {filename}: удалено блоков: {removed}")
            total_removed += removed
        else:
            print(f"  [--] {filename}: блоков не найдено")

    print(f"\n✅ Готово! Всего удалено блоков: {total_removed}")


if __name__ == "__main__":
    main()
