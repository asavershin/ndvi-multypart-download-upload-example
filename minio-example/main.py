import os
import rasterio
import tempfile
from minio import Minio

import rasterio.windows

path_red_tif = "/vsis3/files/red.tif"
path_nir_tif = "/vsis3/files/nir.tif"

# Установка переменных среды
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ["AWS_SECRET_ACCESS_KEY"] = 'minioadmin'

bucket_name = "files"
object_name = "ndvi.tif"

chunk_size = 1024 

# Инициализация Minio клиента
minio_client = Minio('localhost:9000',
                  access_key='minioadmin',
                  secret_key='minioadmin',
                  secure=False)

with rasterio.Env(AWS_HTTPS='NO', GDAL_DISABLE_READDIR_ON_OPEN='YES', AWS_VIRTUAL_HOSTING=False, AWS_S3_ENDPOINT='localhost:9000'):
    with rasterio.open(path_red_tif) as red_tif, rasterio.open(path_nir_tif) as nir_tif:
        profile = red_tif.profile
        height, width = red_tif.shape

        print("Создание временного файла")
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            output_path = temp_file.name
            print("Начало записи во временный файл")
            with rasterio.open(output_path, 'w', **profile) as dst_ndvi:
                for offset_y in range(0, height, chunk_size):
                    for offset_x in range(0, width, chunk_size):
                        window = rasterio.windows.Window(offset_x, offset_y, min(chunk_size, width - offset_x), min(chunk_size, height - offset_y))

                        # Чтение красного и ближнего инфракрасного каналов
                        red_chunk = red_tif.read(window=window)
                        nir_chunk = nir_tif.read(window=window)

                        # Расчет NDVI
                        ndvi_chunk = (nir_chunk - red_chunk) / (nir_chunk + red_chunk)
                        dst_ndvi.write(ndvi_chunk, window=window)
            print("Загрузка временного файла в Minio")
            minio_client.fput_object(bucket_name, object_name, output_path, content_type='image/tiff')

            