import os
import shutil
import subprocess
import json
from datetime import datetime
import zipfile

def log(message):
    """Дата и время."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def clone_repository(repo_url, destination):
    """Клонирование репозитория."""
    log(f"Клонирование репозитория из {repo_url} в {destination}...")
    subprocess.run(["git", "clone", repo_url, destination], check=True)

def clean_repository(root_path, source_code_path):
    """Очищаем корневую директорию."""
    log(f"Очистка репозитория в {root_path}, оставляем только {source_code_path}...")
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.abspath(item_path) != os.path.abspath(source_code_path):
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def create_version_file(source_code_path, version):
    """Создаём файл version.json."""
    log(f"Создание version.json в {source_code_path}...")
    files = ["server.js"]  
    version_data = {
        "name": "hello world",
        "version": version,
        "files": files
    }
    version_file_path = os.path.join(source_code_path, "version.json")
    with open(version_file_path, "w") as version_file:
        json.dump(version_data, version_file, indent=4)

def create_archive(source_code_path, archive_name):
    """Создаём архив с исходным кодом и файлом version.json."""
    log(f"Создание архива {archive_name}.zip из {source_code_path}...")
    with zipfile.ZipFile(f"{archive_name}.zip", "w") as archive:
        for root, _, files in os.walk(source_code_path):
            for file in files:
                file_path = os.path.join(root, file)
                archive.write(file_path, os.path.relpath(file_path, source_code_path))

def build_package(repo_url, source_code_path, version):
    """Сборочный процесс."""
    temp_dir = "temp_repo"
    try:
        clone_repository(repo_url, temp_dir)

        source_code_abs_path = os.path.abspath(os.path.join(temp_dir, source_code_path))
        if not os.path.exists(source_code_abs_path):
            raise FileNotFoundError(f"Путь до исходного кода {source_code_abs_path} не существует.")

        clean_repository(temp_dir, source_code_abs_path)

        create_version_file(source_code_abs_path, version)

        archive_name = "app01012024"  
        create_archive(source_code_abs_path, archive_name)

        log(f"Процесс сборки успешно завершён. Архив создан: {archive_name}.zip")
    except Exception as e:
        log(f"Ошибка: {e}")
    finally:
        
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


repo_url = "https://github.com/paulbouwer/hello-kubernetes"
source_code_path = "src/app"
version = "25.3000"

if __name__ == "__main__":
    build_package(repo_url, source_code_path, version)
