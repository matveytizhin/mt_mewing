#!/usr/bin/env python3
"""
Скрипт делает две вещи для всех HTML уроков:
1. Заменяет href в кнопках "Следующий урок" и "Предыдущий урок" на локальные .html
2. Заменяет блоки lite-block-live-wrapper (онлайн-видео) на локальные <video> теги

Положи в папку DoingMewing (рядом с html файлами) и запусти:
    python fix_all.py
"""

import os
import re

# ─────────────────────────────────────────────────────────────────────────────
# Порядок уроков: [локальный_html, папка_с_видео или None]
# ─────────────────────────────────────────────────────────────────────────────
LESSONS = [
    ("Моя_история.html",                                    None),
    ("Информация.html",                                     None),
    ("Техника_безопасности__напряжение_затылка.html",       "03_Техника_безопасности__напряжение_затылка"),
    ("Подготовка.html",                                     None),
    ("Максилла_-_кость_молодости_и_красоты.html",           "05_Максилла_-_кость_молодости_и_красоты"),
    ("Краткий_гид_по_курсу_частые_вопросы_и_важные_рекомендации.html", None),
    ("Мьюинг_и_осанка_рта_как_опора_черепа.html",          "07_Мьюинг_и_осанка_рта_как_опора_черепа"),
    ("Расслабляем_напряженные_структуры.html",              "08_Расслабляем_напряженные_структуры"),
    ("Краниальная_гимнастика__расслабление_швов_черепа_и_клиновидной_кости.html",
                                                            "09_Краниальная_гимнастика__расслабление_швов_черепа_и_клиновидной_кости"),
    ("Краниальная_гимнастика__приемы_на_расслабление_твердой_мозговой_оболочки.html",
                                                            "10_Краниальная_гимнастика__приемы_на_расслабление_твердой_мозговой_оболочки"),
    ("Правильное_положение_языка.html",                     "11_Правильное_положение_языка"),
    ("Учимся_правильно_дышать.html",                        "12_Учимся_правильно_дышать"),
    ("Учимся_правильно_глотать.html",                       "13_Учимся_правильно_глотать"),
    ("Упражнение_Маккензи.html",                            "14_Упражнение_Маккензи"),
    ("Упражнения_языком.html",                              "15_Упражнения_языком"),
    ("Мануальное_моделирование_костей_лицевого_черепа__расслабляем_центральный_небный_шов.html",
                                                            "16_Мануальное_моделирование_костей_лицевого_черепа__расслабляем_центральный_небный_шов"),
    ("Мануальные_приемы_на_расширение,_выдвижение,_поднятие_максилл_и_скуловых_костей.html",
                                                            "17_Мануальные_приемы_на_расширение_выдвижение_поднятие_максилл_и_скуловых_костей"),
    ("Приемы_на_глаза_и_запавшие_виски.html",               "18_Приемы_на_глаза_и_запавшие_виски"),
    ("Расслабляем_лоб_и_межбровную_область.html",           "19_Расслабляем_лоб_и_межбровную_область"),
    ("Приемы_на_нос_и_против_носогубок.html",               "20_Приемы_на_нос_и_против_носогубок"),
    ("Остеопатические_приемы_на_нижнюю_челюсть.html",       "21_Остеопатические_приемы_на_нижнюю_челюсть"),
    ("Чьюинг__капа,_твердая_жвачка,_эспандер.html",         "22_Чьюинг__капа_твердая_жвачка_эспандер"),
    ("Бонсмешинг.html",                                     "23_Бонсмешинг"),
    ("Медитативная_дыхательная_практика_на_раскрытие_лица.html",
                                                            "24_Медитативная_дыхательная_практика_на_раскрытие_лица"),
    ("Приемы_для_улучшения_зрения.html",                    "25_Приемы_для_улучшения_зрения"),
    ("Массаж_десен.html",                                   "26_Массаж_десен"),
    ("Отёки_на_мьюинге.html",                               "27_Отёки_на_мьюинге"),
    ("Заключение.html",                                     "28_Заключение"),
    ("Бонус__Как_я_испортила_себе_лицо__опасные_приемы.html","29_Бонус__как_я_испортила_себе_лицо__опасные_приемы"),
    ("Новые_курсы.html",                                    None),
]

VIDEOS_DIR = "videos"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# Получить список видеофайлов из папки, отсортированных по номеру
# ─────────────────────────────────────────────────────────────────────────────
def get_videos(folder_name):
    if folder_name is None:
        return []
    folder_path = os.path.join(CURRENT_DIR, VIDEOS_DIR, folder_name)
    if not os.path.isdir(folder_path):
        return []
    files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    # Сортируем по числу в начале имени (1__, 2__, ...)
    def sort_key(name):
        m = re.match(r'^(\d+)', name)
        return int(m.group(1)) if m else 999
    files.sort(key=sort_key)
    return [os.path.join(VIDEOS_DIR, folder_name, f) for f in files]

# ─────────────────────────────────────────────────────────────────────────────
# Построить HTML тег <video> для одного файла
# ─────────────────────────────────────────────────────────────────────────────
def make_video_tag(video_path):
    return (
        f'\n<video controls width="100%" style="max-width: 800px; display: block; margin: 16px 0;">\n'
        f'  <source src="{video_path}" type="video/mp4">\n'
        f'  Ваш браузер не поддерживает видео.\n'
        f'</video>\n'
    )

# ─────────────────────────────────────────────────────────────────────────────
# Паттерн для блока lite-block-live-wrapper (жадный минимум)
# ─────────────────────────────────────────────────────────────────────────────
VIDEO_BLOCK_RE = re.compile(
    r'<div[^>]+class="[^"]*lite-block-live-wrapper[^"]*o-lt-video[^"]*"[^>]*>.*?</div>\s*</div>\s*</script>',
    re.DOTALL
)

# Более точный паттерн — ищем скрипт + следующий div
VIDEO_BLOCK_RE2 = re.compile(
    r'(<script>[\s\S]*?</script>\s*\n?\s*)'
    r'(<div[^>]+class="[^"]*lite-block-live-wrapper[^"]*o-lt-video[^"]*"[^>]*>)',
    re.DOTALL
)

# ─────────────────────────────────────────────────────────────────────────────
# Паттерн для ссылок следующего/предыдущего урока
# ─────────────────────────────────────────────────────────────────────────────
NEXT_LINK_RE = re.compile(
    r'<a([^>]+)href="https://doingmewing\.ru/pl/teach/control/lesson/view\?id=\d+"([^>]*)>'
    r'(Следующий урок[\s\S]*?)</a>',
    re.DOTALL
)
PREV_LINK_RE = re.compile(
    r'<a([^>]+)href="https://doingmewing\.ru/pl/teach/control/lesson/view\?id=\d+"([^>]*)>'
    r'([\s\S]*?Предыдущий урок[\s\S]*?)</a>',
    re.DOTALL
)

# ─────────────────────────────────────────────────────────────────────────────
# ОСНОВНАЯ ОБРАБОТКА
# ─────────────────────────────────────────────────────────────────────────────
def process_file(html_file, prev_html, next_html, video_folder):
    filepath = os.path.join(CURRENT_DIR, html_file)
    if not os.path.exists(filepath):
        print(f"  [??] Файл не найден: {html_file}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # ── 1. Следующий урок ────────────────────────────────────────────────────
    if next_html:
        def replace_next(m):
            return f'<a{m.group(1)}href="{next_html}"{m.group(2)}>{m.group(3)}</a>'
        new_content = NEXT_LINK_RE.sub(replace_next, content)
        if new_content != content:
            content = new_content
            changes.append(f"следующий → {next_html}")

    # ── 2. Предыдущий урок ───────────────────────────────────────────────────
    if prev_html:
        def replace_prev(m):
            return f'<a{m.group(1)}href="{prev_html}"{m.group(2)}>{m.group(3)}</a>'
        new_content = PREV_LINK_RE.sub(replace_prev, content)
        if new_content != content:
            content = new_content
            changes.append(f"предыдущий → {prev_html}")

    # ── 3. Видео блоки ───────────────────────────────────────────────────────
    videos = get_videos(video_folder)
    if videos:
        video_idx = [0]  # счётчик через список чтобы работало в замыкании

        def replace_video(m):
            idx = video_idx[0]
            if idx < len(videos):
                tag = make_video_tag(videos[idx])
                video_idx[0] += 1
                # Оставляем оригинальный div после тега видео (для структуры страницы)
                return tag + m.group(2)
            return m.group(0)

        new_content = VIDEO_BLOCK_RE2.sub(replace_video, content)
        if new_content != content:
            content = new_content
            changes.append(f"видео вставлено: {video_idx[0]} шт. из {len(videos)}")

    # ── Сохраняем ────────────────────────────────────────────────────────────
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] {html_file}: {', '.join(changes)}")
    else:
        print(f"  [--] {html_file}: изменений нет")


def main():
    print("🔧 Обрабатываем HTML уроки...\n")

    for i, (html_file, video_folder) in enumerate(LESSONS):
        prev_html = LESSONS[i - 1][0] if i > 0 else None
        next_html = LESSONS[i + 1][0] if i < len(LESSONS) - 1 else None
        process_file(html_file, prev_html, next_html, video_folder)

    print("\n✅ Готово!")


if __name__ == "__main__":
    main()
