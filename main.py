import json
import logging
from pathlib import Path
from backups.backup_manager import BackupManager
from backups.scheduler import Scheduler

def setup_logging(log_level: str):
    """
    Настраивает логирование.
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Некорректный уровень логирования: {log_level}")
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def load_config(config_path: str) -> dict:
    """
    Загружает конфигурацию из JSON-файла.
    """
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)

def main():
    # Загружаем конфигурацию
    config_path = Path("config.json")
    if not config_path.is_file():
        raise FileNotFoundError(f"Файл конфигурации {config_path} не найден.")
    
    config = load_config(config_path)
    
    # Настраиваем логирование
    setup_logging(config.get("log_level", "INFO"))
    
    # Создаем менеджер резервного копирования
    manager = BackupManager(
        source_dirs=config["directories_to_backup"],
        destination_dir=config["backup_destination"]
    )
    
    # Запускаем планировщик
    scheduler = Scheduler(task=manager.perform_backup, interval=config["backup_period"])
    scheduler.start()
    
    try:
        logging.info("Программа запущена. Нажмите Ctrl+C для выхода.")
        while True:
            pass  # Программа работает в фоне
    except KeyboardInterrupt:
        logging.info("Завершение работы...")
        scheduler.stop()

if __name__ == "__main__":
    main()
