import rasterio
import numpy as np

print("Начали парсить снимок")
# Открытие изображения
with rasterio.open('image.TIF') as src:
    print("Читаем каналы")
    # Чтение каналов RED и NIR
    red = src.read(3)
    nir = src.read(5)
    print("закончили читать каналы")

    red = red.astype(np.float32)
    nir = nir.astype(np.float32)
    np.seterr(divide='ignore', invalid='ignore')
    print("Начинаем считать NDVI")
    # Расчет NDVI
    ndvi = (nir - red) / (nir + red)
    print("Закончили подсчёт ndvi")
    # Получение профиля изображения
    profile = src.profile

    # Изменение параметров профиля для сохранения NDVI
    profile.update(dtype=rasterio.float32, count=1)

    # Сохранение NDVI в новый файл
    with rasterio.open('ndvi.tif', 'w', **profile) as dst:
        dst.write(ndvi, 1)

print("Закончили парсить снимок")
