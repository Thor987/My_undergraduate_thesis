'''
本代码用于计算降水年较差（MJJAS-DJFM）
后续处理：在ArcGIS中将NC文件转为TIFF，后使用栅格计算器计算
夏季降水占比大于0.55且降水年较差大于2mm/day的区域作为中国季风区
至此，Fig2a计算结束
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
ds = ds.sel(time=slice('1979-05-01', '2024-4-01'))

# 计算MJJAS（5-9月）平均降水
mjjas = ds['pr'].sel(time=np.in1d(ds['time.month'], [5,6,7,8,9]))
# print(len(mjjas))
# print(mjjas.shape)
mjjas_mean = mjjas.mean('time')
# print(mjjas_mean.shape)
# 计算DJFM（12月-次年3月）平均降水
djfm = ds['pr'].sel(time=np.in1d(ds['time.month'], [11,12,1,2,3]))
# print(len(djfm))
# print(mjjas.shape)
djfm_mean = djfm.mean('time')
# print(djfm_mean.shape)
# 计算MJJAS和DJFM的差值
anomaly = mjjas_mean - djfm_mean
# print(anomaly.shape)
# 将结果保存为NetCDF文件
anomaly.to_netcdf('./results/precip_anomaly_CRU.nc')