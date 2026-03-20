#!/usr/bin/env python3
"""
Сжимает все видео из папки videos/ в videos_compressed/
с сохранением той же иерархии папок.

Положи в папку DoingMewing и запусти: python compress_videos.py
"""

import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "videos")
DST_DIR = os.path.join(CURRENT_DIR, "videos_compressed")

CRF = 28  # качество: 23=лучше, 28=баланс, 32=меньше размер

def main():
    print("🎬 Сжимаем видео...\n")

    total = 0
    done = 0
    errors = 0

    # Считаем общее количество файлов
    for root, dirs, files in os.walk(SRC_DIR):
        for f in files:
            if f.endswith(".mp4"):
                total += 1

    print(f"Найдено файлов: {total}\n")

    for root, dirs, files in os.walk(SRC_DIR):
        for filename in sorted(files):
            if not filename.endswith(".mp4"):
                continue

            src_path = os.path.join(root, filename)

            # Строим путь назначения с той же иерархией
            rel_path = os.path.relpath(src_path, SRC_DIR)
            dst_path = os.path.join(DST_DIR, rel_path)

            # Создаём папку если нет
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            # Пропускаем если уже сжат
            if os.path.exists(dst_path):
                print(f"  [==] Уже есть: {rel_path}")
                done += 1
                continue

            src_size = os.path.getsize(src_path) / (1024 * 1024)
            print(f"  [{done+1}/{total}] {rel_path} ({src_size:.1f}MB)...")

            cmd = [
                "ffmpeg", "-i", src_path,
                "-vcodec", "libx264",
                "-crf", str(CRF),
                "-preset", "medium",
                "-acodec", "aac",
                "-b:a", "128k",
                "-y",        # перезаписывать без вопросов
                dst_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                dst_size = os.path.getsize(dst_path) / (1024 * 1024)
                ratio = src_size / dst_size if dst_size > 0 else 0
                print(f"         ✅ {src_size:.1f}MB → {dst_size:.1f}MB (x{ratio:.1f})")
                done += 1
            else:
                print(f"         ❌ Ошибка: {result.stderr[-200:]}")
                errors += 1

    print(f"\n✅ Готово! Сжато: {done}, ошибок: {errors}")
    print(f"Сжатые видео в папке: {DST_DIR}")

    # Итоговое сравнение размеров
    src_total = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, files in os.walk(SRC_DIR)
        for f in files if f.endswith(".mp4")
    ) / (1024 * 1024 * 1024)

    dst_total = sum(
        os.path.getsize(os.path.join(r, f))
        for r, _, files in os.walk(DST_DIR)
        for f in files if f.endswith(".mp4")
    ) / (1024 * 1024 * 1024)

    print(f"\nОригиналы:  {src_total:.2f} GB")
    print(f"Сжатые:     {dst_total:.2f} GB")
    print(f"Экономия:   {src_total - dst_total:.2f} GB")

if __name__ == "__main__":
    main()
