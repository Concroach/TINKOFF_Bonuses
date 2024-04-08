import shutil
import os

folder = 'src'

async def clear_src_folder():
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Не удалось удалить {file_path}. Причина: {e}")

    print(f"Все содержимое папки {folder} было удалено.")