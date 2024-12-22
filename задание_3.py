
import re
from collections import defaultdict

def generate_versions(template):
    """
    Генерируем два номера версий для шаблона.
    Шаблон вида: 3.7.*, 3.*.1, 1.2.3.*
    """
    parts = template.split(".")
    versions = []

    for i, part in enumerate(parts):
        if part == "*":
            parts[i] = "7"
            versions.append(".".join(parts))
            parts[i] = "3"
            versions.append(".".join(parts))
            break

    return versions


def parse_config(config_string):
    """Смотрим конфигурацию."""
    config = eval(config_string)
    return config


def version_is_older(version, comparison_version):
    """Проверяем версию."""
    v1_parts = list(map(int, version.split(".")))
    v2_parts = list(map(int, comparison_version.split(".")))

    return v1_parts < v2_parts


def main():
    version = "3.7.3"
    config_string = '''{
        "Sh1": "3.7.*",
        "Sh2": "3.*.1",
        "Sh3": "1.2.3.*"
    }'''

    config = parse_config(config_string)

    all_versions = set()
    for key, template in config.items():
        versions = generate_versions(template)
        all_versions.update(versions)

    sorted_versions = sorted(all_versions, key=lambda x: list(map(int, x.split("."))))

    print("Сортированный список всех версий:")
    for version in sorted_versions:
        print(version)

    print("\nСписок версий, меньших текущей версии:")
    for version in sorted_versions:
        if version_is_older(version, version):
            print(version)


if __name__ == "__main__":
    main()