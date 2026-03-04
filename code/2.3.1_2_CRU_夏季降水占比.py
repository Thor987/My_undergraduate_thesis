'''
本代码用于计算CRU数据集的夏季降水占比，并以0.55为阈值进行二值化，并将结果保存为NetCDF文件。
'''
import xarray as xr
import numpy as np
import os
os.environ['USE_PATH_FOR_GDAL_PYTHON'] = 'YES'

# 读取NetCDF文件
ds = xr.open_dataset('./data/CRU/processed_data_precip.nc')

# 将时间转换为datetime格式
ds['time'] = xr.decode_cf(ds).time

# 提取1979-2024年的数据
ds = ds.sel(time=slice('1979-01-01', '2024-12-31'))

# 计算MJJAS（5-9月）总降水
mjjas = ds['pr'].sel(time=np.in1d(ds['time.month'], [5,6,7,8,9]))
# print(len(mjjas))
# print(mjjas.shape)
mjjassum = mjjas.sum('time')
# print(mjjassum.shape)
# 计算全年总降水
precip = ds['pr'].sel(time=np.in1d(ds['time.month'], [1,2,3,4,5,6,7,8,9,10,11,12]))
# print(len(precip))
# print(precip.shape)
precip_sum = precip.sum('time')
# print(precip_sum.shape)
# 计算夏季降水占比
anomaly = mjjassum/precip_sum
# print(anomaly.shape)
# 如果大于0.55，则标记为1，否则为0
anomaly = np.where(anomaly > 0.55, 1, 0)
# 将numpy数组转换为xarray.DataArray
anomaly_da = xr.DataArray(anomaly, dims=['lat', 'lon'], coords={'lat': ds.lat, 'lon': ds.lon})
# 保存为NetCDF文件
anomaly_da.to_netcdf('./results/precip_summer_r_CRU.nc')
print("处理完成，结果已保存为precip_summer_r_CRU.nc")
