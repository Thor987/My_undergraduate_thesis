'''
*************************************************************
合并从TraCE21ka网站上下载的数据，时间范围为-9.7 ka BP到-6.7 ka BP

前置条件：
从https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm.trace.atm.proc.monthly_ave.html网站下载
TraCE21ka数据集（温度（TS）、降水（PRECC、PRECL）、经向和纬向风（U、V）等变量）
放在./data/AF/TS、./data/AF/PRECC、./data/AF/PRECL、./data/AF/Wind/U、./data/AF/Wind/V目录下
*************************************************************
'''
import xarray as xr
from glob import glob

##  温度和降水数据处理

# 打开多个文件并合并
# files = glob('./AF/TS/trace*.nc')
# files = glob('./AF/PRECC/trace*.nc')
files = glob('./AF/PRECL/trace*.nc')

ds = xr.open_mfdataset(files, combine='by_coords', drop_variables=['unneeded_var'])

# 解码时间坐标
ds = xr.decode_cf(ds)
# 将numpy数组转换为xarray.DataArray并指定变量名
ds_BP = xr.DataArray(
    # ds['TS'],
    # ds['PRECC'],
    ds['PRECL'],
    dims=['time', 'lat', 'lon'],
    coords={'time': ds['time'], 'lat': ds.lat, 'lon': ds.lon},
    # name='TS',
    # name='PRECC',
    name='PRECL'
)

# 保存结果
# ds_BP.to_netcdf('./AF/TS/TS_9700-6700a_BP.nc')
# ds_BP.to_netcdf('./AF/PRECC/PRECC_9700-6700a_BP.nc')
ds_BP.to_netcdf('./AF/PRECL/PRECL_9700-6700a_BP.nc')

##  风场数据处理

# 打开多个文件并合并
# files = glob('./AF/Wind/U/trace*.nc')
# 运行时注释一行
files = glob('./AF/Wind/V/trace*.nc')

ds = xr.open_mfdataset(files, combine='by_coords', drop_variables=['unneeded_var'])

# 解码时间坐标
ds = xr.decode_cf(ds)
# U(time=4800, lev=26, lat=48, lon=96);
# 取lev=867.16076hpa的数据
# 选择特定气压层(867.16076hPa)的数据
selected_level = 867.16076
ds = ds.sel(lev=selected_level, method='nearest')

# 将numpy数组转换为xarray.DataArray并指定变量名
ds_BP = xr.DataArray(
    # ds['U'],
    ds['V'],
    dims=['time', 'lat', 'lon'],
    coords={'time': ds['time'], 'lat': ds.lat, 'lon': ds.lon},
    # name='U',
    name='V',
)

# 保存结果
# ds_BP.to_netcdf('./AF/Wind/U/U_8500-7600a_BP.nc')
ds_BP.to_netcdf('./AF/Wind/V/V_8500-7600a_BP.nc')
