#!/usr/bin/env python3
"""
Заменяет ссылки в кнопках "Следующий урок" и "Предыдущий урок"
на локальные .html файлы.

Положи в папку DoingMewing и запусти: python fix_nav.py
"""

import os
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Порядок уроков — точные имена файлов
LESSONS = [
    "Моя_история.html",
    "Информация.html",
    "Техника_безопасности__напряжение_затылка.html",
    "Подготовка.html",
    "Максилла_-_кость_молодости_и_красоты.html",
    "Краткий_гид_по_курсу__частые_вопросы_и_важные_рекомендации.html",
    "Мьюинг_и_осанка_рта_как_опора_черепа.html",
    "Расслабляем_напряженные_структуры.html",
    "Краниальная_гимнастика__расслабление_швов_черепа_и_клиновидной_кости.html",
    "Краниальная_гимнастика__приемы_на_расслабление_твердой_мозговой_оболочки.html",
    "Правильное_положение_языка.html",
    "Учимся_правильно_дышать.html",
    "Учимся_правильно_глотать.html",
    "Упражнение_Маккензи.html",
    "Упражнения_языком.html",
    "Мануальное_моделирование_костей_лицевого_черепа__расслабляем_центральный_небный_шов.html",
    "Мануальные_приемы_на_расширение,_выдвижение,_поднятие_максилл_и_скуловых_костей.html",
    "Приемы_на_глаза_и_запавшие_виски.html",
    "Расслабляем_лоб_и_межбровную_область.html",
    "Приемы_на_нос_и_против_носогубок.html",
    "Остеопатические_приемы_на_нижнюю_челюсть.html",
    "Чьюинг__капа,_твердая_жвачка,_эспандер.html",
    "Бонсмешинг.html",
    "Медитативная_дыхательная_практика_на_раскрытие_лица.html",
    "Приемы_для_улучшения_зрения.html",
    "Массаж_десен.html",
    "Отёки_на_мьюинге.html",
    "Заключение.html",
    "Бонус__Как_я_испортила_себе_лицо__опасные_приемы.html",
]

# Паттерн: ссылка на getcourse с текстом "Следующий урок" или "Предыдущий урок"
LINK_RE = re.compile(
    r'<a([^>]+)href="https://doingmewing\.ru/pl/teach/control/lesson/view\?id=\d+"([^>]*)>([\s\S]*?)</a>',
    re.DOTALL
)

def process_file(filepath, prev_html, next_html):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    def replace_link(m):
        attrs1 = m.group(1)
        attrs2 = m.group(2)
        inner = m.group(3)

        if "Следующий урок" in inner and next_html:
            changes.append(f"следующий → {next_html}")
            return f'<a{attrs1}href="{next_html}"{attrs2}>{inner}</a>'
        elif "Предыдущий урок" in inner and prev_html:
            changes.append(f"предыдущий → {prev_html}")
            return f'<a{attrs1}href="{prev_html}"{attrs2}>{inner}</a>'
        else:
            return m.group(0)  # не трогаем

    content = LINK_RE.sub(replace_link, content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] {os.path.basename(filepath)}: {', '.join(changes)}")
    else:
        print(f"  [--] {os.path.basename(filepath)}: изменений нет")

def main():
    print("🔗 Исправляем навигацию между уроками...\n")

    for i, html_file in enumerate(LESSONS):
        filepath = os.path.join(CURRENT_DIR, html_file)

        if not os.path.exists(filepath):
            print(f"  [??] Файл не найден: {html_file}")
            continue

        prev_html = LESSONS[i - 1] if i > 0 else None
        next_html = LESSONS[i + 1] if i < len(LESSONS) - 1 else None

        process_file(filepath, prev_html, next_html)

    print("\n✅ Готово!")

if __name__ == "__main__":
    main()
