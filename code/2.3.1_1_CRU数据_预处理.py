'''
本代码用于处理CRU降水和温度数据，即将逐年的降水和温度数据合并为一个文件，便于后续处理。
前置工作，从https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-global-and-regional?tab=download下载CRU降水和温度数据
'''
import xarray as xr
from glob import glob

# 打开多个文件并合并
files = glob('./data/CRU/CRU_Precip/CRU_total_precipitation_mon_0.5x0.5_global_*.nc')
ds = xr.open_mfdataset(files, combine='by_coords', drop_variables=['unneeded_var'])

# 解码时间坐标
ds['time'] = xr.decode_cf(ds).time
# 将时间转换为NetCDF支持的格式
ds['time'] = ds['time'].astype('datetime64[s]')
# 选择特定时间范围
ds = ds.sel(time=slice('1979-01-01', '2019-12-31'))
# 保存为新的NetCDF文件
ds.to_netcdf('./data/CRU/processed_data_precip.nc')


# 打开多个文件并合并
files = glob('./data/CRU/CRU_Temp/CRU_mean_temperature_mon_0.5x0.5_global_*.nc')
ds = xr.open_mfdataset(files, combine='by_coords', drop_variables=['unneeded_var'])

# 解码时间坐标
ds['time'] = xr.decode_cf(ds).time
# 将时间转换为NetCDF支持的格式
ds['time'] = ds['time'].astype('datetime64[s]')
# 选择特定时间范围
ds = ds.sel(time=slice('1979-01-01', '2019-12-31'))
# 保存为新的NetCDF文件
ds.to_netcdf('./data/CRU/processed_data_temp.nc')