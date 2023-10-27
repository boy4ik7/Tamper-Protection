import os
import hashlib

file_list = []
password = None
current_directory = os.path.dirname(os.path.abspath(__file__))
file_paths = None

# Чтение списка имен файлов из файла template.tbl
with open("template.tbl", "r") as template_file:
    file_list = [line.strip() for line in template_file]
    password = file_list[0]
    file_paths = [os.path.join(current_directory, name) for name in file_list[1:]]

while True:
    input_password = input("Введите пароль: ")
    hash_object = hashlib.sha256()
    hash_object.update(input_password.encode('utf-8'))
    input_password = hash_object.hexdigest()
    if input_password == password:
        print("1. Заблокировать операции")
        print("2. Разблокировать операции")
        print("3. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            for file_path in file_paths:
                try:
                    # Устанавливаем атрибут "только чтение" (read-only)
                    os.chmod(file_path, 0o444)  # Для Windows
                    # Скрываем файлы (делаем их атрибут "скрытый")
                    os.system(f'attrib +h "{file_path}"')  # Для Windows
                    print(f"Файл {file_path} защищен от изменения и удаления.")
                except FileNotFoundError:
                    print(f"Файл {file_path} не найден.")
                except Exception as e:
                    print(f"Произошла ошибка при защите файла {file_path}: {e}")
            print("Готово")
                    
        elif choice == "2":
            for file_path in file_paths:
                try:
                    # Снимаем атрибут "только чтение"
                    os.chmod(file_path, 0o666)  # Для Windows
                    # Отменяем скрытие файла
                    os.system(f'attrib -h "{file_path}"')  # Для Windows
                    print(f"Защита файла {file_path} отменена.")
                except FileNotFoundError:
                    print(f"Файл {file_path} не найден.")
                except Exception as e:
                    print(f"Произошла ошибка при отмене защиты файла {file_path}: {e}")
            print("Готово")
            
        elif choice == "3":
            break
        else:
            print("Неправильный выбор. Попробуйте снова.")
    else:
        print("Неверный пароль, попробуйте ещё...")
