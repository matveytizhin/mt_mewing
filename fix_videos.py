#!/usr/bin/env python3
"""
Заменяет блоки o-lt-video (с iframe getcourse + скрипт subscribeChannel)
на локальные <video> теги.

Положи в папку DoingMewing и запусти: python fix_videos.py
"""

import os
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(CURRENT_DIR, "videos")
SKIP_FILES = {"index.html", "index_fixed.html"}

# Маппинг: html файл → папка с видео
LESSON_VIDEOS = {
    "Техника_безопасности__напряжение_затылка.html":       "03_Техника_безопасности__напряжение_затылка",
    "Максилла_-_кость_молодости_и_красоты.html":           "05_Максилла_-_кость_молодости_и_красоты",
    "Мьюинг_и_осанка_рта_как_опора_черепа.html":          "07_Мьюинг_и_осанка_рта_как_опора_черепа",
    "Расслабляем_напряженные_структуры.html":              "08_Расслабляем_напряженные_структуры",
    "Краниальная_гимнастика__расслабление_швов_черепа_и_клиновидной_кости.html":
                                                            "09_Краниальная_гимнастика__расслабление_швов_черепа_и_клиновидной_кости",
    "Краниальная_гимнастика__приемы_на_расслабление_твердой_мозговой_оболочки.html":
                                                            "10_Краниальная_гимнастика__приемы_на_расслабление_твердой_мозговой_оболочки",
    "Правильное_положение_языка.html":                     "11_Правильное_положение_языка",
    "Учимся_правильно_дышать.html":                        "12_Учимся_правильно_дышать",
    "Учимся_правильно_глотать.html":                       "13_Учимся_правильно_глотать",
    "Упражнение_Маккензи.html":                            "14_Упражнение_Маккензи",
    "Упражнения_языком.html":                              "15_Упражнения_языком",
    "Мануальное_моделирование_костей_лицевого_черепа__расслабляем_центральный_небный_шов.html":
                                                            "16_Мануальное_моделирование_костей_лицевого_черепа__расслабляем_центральный_небный_шов",
    "Мануальные_приемы_на_расширение,_выдвижение,_поднятие_максилл_и_скуловых_костей.html":
                                                            "17_Мануальные_приемы_на_расширение_выдвижение_поднятие_максилл_и_скуловых_костей",
    "Приемы_на_глаза_и_запавшие_виски.html":               "18_Приемы_на_глаза_и_запавшие_виски",
    "Расслабляем_лоб_и_межбровную_область.html":           "19_Расслабляем_лоб_и_межбровную_область",
    "Приемы_на_нос_и_против_носогубок.html":               "20_Приемы_на_нос_и_против_носогубок",
    "Остеопатические_приемы_на_нижнюю_челюсть.html":       "21_Остеопатические_приемы_на_нижнюю_челюсть",
    "Чьюинг__капа,_твердая_жвачка,_эспандер.html":         "22_Чьюинг__капа_твердая_жвачка_эспандер",
    "Бонсмешинг.html":                                     "23_Бонсмешинг",
    "Медитативная_дыхательная_практика_на_раскрытие_лица.html":
                                                            "24_Медитативная_дыхательная_практика_на_раскрытие_лица",
    "Приемы_для_улучшения_зрения.html":                    "25_Приемы_для_улучшения_зрения",
    "Массаж_десен.html":                                   "26_Массаж_десен",
    "Отёки_на_мьюинге.html":                               "27_Отёки_на_мьюинге",
    "Заключение.html":                                     "28_Заключение",
    "Бонус__Как_я_испортила_себе_лицо__опасные_приемы.html":"29_Бонус__как_я_испортила_себе_лицо__опасные_приемы",
}

# Паттерн: весь блок от <div class="...o-lt-video..."> до </script>
# Блок заканчивается на </div><script>...</script>
VIDEO_BLOCK_RE = re.compile(
    r'<div[^>]+class="[^"]*lite-block-live-wrapper[^"]*o-lt-video[^"]*"[^>]*>'  # открывающий div
    r'[\s\S]*?'           # содержимое (iframe и т.д.)
    r'</div><script>'     # конец div + начало скрипта
    r'[\s\S]*?'           # содержимое скрипта
    r'</script>',         # конец скрипта
    re.DOTALL
)

def get_videos(folder_name):
    """Возвращает отсортированный список путей к видео в папке."""
    folder_path = os.path.join(VIDEOS_DIR, folder_name)
    if not os.path.isdir(folder_path):
        return []
    files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    def sort_key(name):
        m = re.match(r'^(\d+)', name)
        return int(m.group(1)) if m else 999

    files.sort(key=sort_key)
    return [f"videos/{folder_name}/{f}" for f in files]

def make_video_tag(src):
    return (
        f'\n<video controls width="100%" style="max-width: 800px; display: block; margin: 16px 0;">\n'
        f'  <source src="{src}" type="video/mp4">\n'
        f'  Ваш браузер не поддерживает видео.\n'
        f'</video>\n'
    )

def process_file(html_file, video_folder):
    filepath = os.path.join(CURRENT_DIR, html_file)
    if not os.path.exists(filepath):
        print(f"  [??] Файл не найден: {html_file}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Считаем сколько блоков o-lt-video в файле
    blocks = VIDEO_BLOCK_RE.findall(content)
    if not blocks:
        print(f"  [--] {html_file}: блоков видео не найдено")
        return

    videos = get_videos(video_folder) if video_folder else []

    if not videos:
        print(f"  [!!] {html_file}: найдено {len(blocks)} блоков, но нет видеофайлов в папке")
        return

    if len(blocks) != len(videos):
        print(f"  [!!] {html_file}: блоков={len(blocks)}, видеофайлов={len(videos)} — несовпадение!")

    video_idx = [0]

    def replace_block(m):
        idx = video_idx[0]
        if idx < len(videos):
            tag = make_video_tag(videos[idx])
            video_idx[0] += 1
            return tag
        else:
            # Видео закончились — удаляем блок без замены
            video_idx[0] += 1
            return ""

    new_content = VIDEO_BLOCK_RE.sub(replace_block, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  [OK] {html_file}: заменено {video_idx[0]} блоков → {len(videos)} видео")

def main():
    print("🎬 Заменяем блоки видео на локальные <video> теги...\n")

    for html_file, video_folder in LESSON_VIDEOS.items():
        process_file(html_file, video_folder)

    print("\n✅ Готово!")

if __name__ == "__main__":
    main()
