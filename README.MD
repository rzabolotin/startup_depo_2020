# Проект Defect detector
*Поиск неисправностей ЖД пути по видео*

Проект выполнен в рамках хакатона **"Стартап депо"**.  
г.Хабаровск 11-13 декабря 2020 года.

## Задача
Необходимо проанализировать видеофайл со съемкой ЖД-пути, и найти на нем неисправности. [Подробное задание](docs/задание.md)


## Структура проекта

1) Поиск стыков методом поиска прямых линий в кадре
2) Строим маршрут рельса, и ищем типичные (для стыка) отклонения
3) Детекция объектов (стык, болт) на фотографии со стыком
4) Разработка GUI приложения
...

## Как запустить
1) Данные скачать из [этого файла](https://drive.google.com/file/d/10fy1fkY_BXHtykaI0ml0b4OKg_Mw8XW8/view?usp=sharing) и положить в директорию `data`  
2) Установить программу `tesseract OCR` [отсюда](https://digi.bib.uni-mannheim.de/tesseract/)
3) В файле `4. GUI application\config.py` укажите путь до бинарника tesseract
```
pytesseract.pytesseract.tesseract_cmd = r"C:\ПУТЬ\ДО\КАТАЛОГА\УСТАНОВКИ\tesseract.exe"
```
5) Установите необходимые библиотеки python
```
pip install -r "4. GUI application\requirements.txt"
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
git clone https://github.com/DGMaxime/detectron2-windows.git
pip install -e detectron2-windows
```
* строка установки pytorch определяется на [сайте pytorch](https://pytorch.org/get-started/locally/)
* detectron2 устанавливается  из неофициально форка (официальная версия не поддерживает платформу Windows)

6) Запустить программу 
```
python 4. GUI application\defect_detector.py
```

**Блоконоты jupyter notebook из разделов 1, 2 и 3 запускались в среде Anacondа**  
Установка зависимостей, если это требуется, проиходит прямо в них.
...

## Примеры работы
TODO
Примеры скриншотов и видео работы программы
..

## Состав команды

## Результат
Презентация 1 и 2
Текст выступления
Победа в хакатоне




