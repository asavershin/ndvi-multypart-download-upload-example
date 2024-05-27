# NDVI Calculation and Upload to Minio

This Python script calculates Normalized Difference Vegetation Index (NDVI)  
from satellite imagery data (red and near-infrared bands), and uploads  
the resulting NDVI image to Minio, an object storage server, using  
its Python SDK. Multipart upload is utilized for efficient handling  
of large files. 

## Libraries Used:

- `rasterio`: A Python library for reading and writing geospatial raster datasets.
- `tempfile`: A module to create temporary files and directories.
- `minio`: Minio Python SDK for interacting with the Minio object storage server.

## Methods Used:

### rasterio.open():
- Used to open the red and near-infrared band images.

### tempfile.NamedTemporaryFile():
- Creates a named temporary file to store the NDVI image temporarily  
 before uploading it to Minio.

### rasterio.windows.Window():
- Defines a window to read the image in chunks for memory-efficient processing.

### rasterio.open(output_path, 'w', **profile):
- Opens the temporary file for writing the NDVI image.

### minio.Minio():
- Initializes the Minio client to connect to the Minio object storage server.

### minio_client.fput_object():
- Uploads the NDVI image file to Minio using the `fput_object` method, which  
 transfers the file directly from the local filesystem to the Minio server  
  without loading it into memory.

## Environment Variables:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Credentials required to access Minio.
- `AWS_HTTPS`, `GDAL_DISABLE_READDIR_ON_OPEN`, `AWS_VIRTUAL_HOSTING`, `AWS_S3_ENDPOINT`: Environment variables used by rasterio to configure the AWS S3 connection.

## Workflow:

1. Open red and near-infrared band images using rasterio.
2. Create a named temporary file for storing the NDVI image.
3. Calculate NDVI in chunks using rasterio.
4. Write NDVI data to the temporary file.
5. Initialize Minio client and upload the temporary NDVI file to Minio using `fput_object`.
6. Clean up the temporary file.

## Tags:

NDVI, Python, rasterio, Minio, multipart upload, satellite imagery, geospatial data
