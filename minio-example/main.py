import tempfile

import numpy as np
import rasterio
from minio import Minio

# # Конфигурация Minio
minio_url = "localhost:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "files"
object_name = "image.tif"

# # Подключение к Minio
minio_client = Minio(minio_url, access_key=access_key, secret_key=secret_key, secure=False)
print("Читаем из minio")

ndvi = []

# Получение данных из Minio
with tempfile.NamedTemporaryFile(suffix=".tif") as temp_file:
    minio_client.fget_object(bucket_name, object_name, temp_file.name)
    with rasterio.open(temp_file.name) as src:
        print("Читаем каналы")
        # Чтение каналов RED и NIR
        red = src.read(3)
        nir = src.read(5)
        red_height, red_width = red.shape
        nir_height, nir_width = nir.shape
        print(f"RED: высота={red_height}, ширина={red_width}")
        print(f"NIR: высота={nir_height}, ширина={nir_width}")
        print("закончили читать каналы")

        red = red.astype(float)
        nir = nir.astype(float)
        print("Начинаем считать NDVI")
        # Расчет NDVI
        ndvi = (nir - red) / (nir + red)
        ndvi_height, ndvi_width = ndvi.shape
        print(f"NDVI: высота={ndvi_height}, ширина={ndvi_width}")
        print("Закончили подсчёт ndvi")

        print("Меняем метаинформацию")
        # Получение профиля изображения
        profile = src.profile

        # Изменение параметров профиля для сохранения NDVI
        profile.update(dtype=rasterio.float32, count=1)


print("Сохраняем файл")
# Сохранение NDVI в новый файл

with tempfile.NamedTemporaryFile(suffix=".tif") as ndvi_temp_file:
    with rasterio.open(ndvi_temp_file.name, "w", **profile) as dst:
        dst.write(ndvi, 1)
    # Загрузка NDVI обратно в Minio
    # file_size = os.path.getsize(ndvi_temp_file.name)
    minio_client.fput_object(bucket_name, "ndvi.tif", ndvi_temp_file.name, content_type="image/tiff")

print("Закончили парсить снимок")