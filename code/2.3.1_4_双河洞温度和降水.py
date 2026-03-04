'''
本代码用于计算双河洞区域(28º-28.5ºN,107º-107.5ºE)的多年降水和温度数据平均值(CRU数据)
'''
import xarray as xr
import os
os.environ['USE_PATH_FOR_GDAL_PYTHON'] = 'YES'
# 读取NetCDF文件
ds = xr.open_dataset('./data/CRU/processed_data_precip.nc')
ds_temp = xr.open_dataset('./data/CRU/processed_data_temp.nc')

# 将时间转换为datetime格式
ds['time'] = xr.decode_cf(ds).time
ds_temp['time'] = xr.decode_cf(ds_temp).time

# 提取1979-2024年的数据
ds = ds.sel(time=slice('1979-01-01', '2019-12-31'))
ds_temp = ds_temp.sel(time=slice('1979-01-01', '2019-12-31'))

# 按经纬度计算双河站点的降水
# 双河站点经纬度
lon = 107.25
lat = 28.25
# 计算双河站点降水，使用线性插值
shuanghe_precip = ds['pr'].sel(lon=lon, lat=lat, method='nearest')
shuanghe_temp = ds_temp['tas'].sel(lon=lon, lat=lat, method='nearest')
# 计算双河站点降水的多年月份平均
shuanghe_precip_mean = shuanghe_precip.groupby('time.month').mean('time')
shuanghe_temp_mean = shuanghe_temp.groupby('time.month').mean('time')

# 计算5-9月的降水量
summer_precip = shuanghe_precip_mean[4:9].sum().values  # 添加.values转换为数值
total_precip = shuanghe_precip_mean.sum().values  # 添加.values转换为数值
summer_ratio = (summer_precip / total_precip) * 100

# # 打印结果
# print(f"5-9月降水量：{summer_precip:.2f} mm")
# print(f"年总降水量：{total_precip:.2f} mm")
# print(f"5-9月降水占全年的比例：{summer_ratio:.2f}%")

# 将DataArray转换为DataFrame并保存为csv
shuanghe_precip_mean.to_dataframe('precipitation').to_csv('../grapher/shuanghe_precip_mean.csv')
shuanghe_temp_mean.to_dataframe('temperature').to_csv('../grapher/shuanghe_temp_mean.csv')

# 后续出图在Grapher中完成