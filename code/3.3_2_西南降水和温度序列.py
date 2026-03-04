'''
计算西南地区8.2 ka 事件时段的温度和降水模拟（基于TraCE模式模拟结果）
'''
import xarray as xr
import numpy as np

###############################################
'''
计算西南地区（22°N to 35°N，98°E to 110°E）的
夏季降水和年降水量
'''
################################################

# 读取NC文件
ds_precc = xr.open_dataset('./AF/PRECC/PRECC_9700-6700a_BP.nc')
ds_precl = xr.open_dataset('./AF/PRECL/PRECL_9700-6700a_BP.nc')

# 根据经纬度裁剪(南方 西)  
ds_precc_south_west = ds_precc.where((ds_precc.lat >= 22) & (ds_precc.lat <= 35) & (ds_precc.lon >= 98) & (ds_precc.lon <= 112), drop=True)
ds_precl_south_west = ds_precl.where((ds_precl.lat >= 22) & (ds_precl.lat <= 35) & (ds_precl.lon >= 98) & (ds_precl.lon <= 112), drop=True)

# 按照lon、lat 相加
ds_precip_south_west = ds_precc_south_west['PRECC'] + ds_precl_south_west['PRECL']
# 将降水单位m/s转换为mm/day
ds_precip_south_west = ds_precip_south_west * 86400 * 1000
# print(ds_precip_south_west.shape)

## 计算年际平均降水
# 计算区域平均值，排除NAN值
# 使用skipna=True参数自动忽略NAN值
monthly_mean_precip_south_west = ds_precip_south_west.mean(dim=['lat', 'lon'], skipna=True)
# 时间范围是-8.5到-6.7 ka BP，步长为0.001 ka（1年）
time_values = np.arange(-9.7, -6.7, 0.001)

# 计算年平均值（每年）
yearly_mean_precip_south_west = monthly_mean_precip_south_west.groupby_bins('time', bins=len(time_values)).mean()
# 计算十年平均值（每10年）
decadal_mean_precip_south_west = monthly_mean_precip_south_west.groupby_bins('time', bins=len(time_values)//10).mean()
# 将DataArray转换为DataFrame

# 南方 西
monthly_mean_df_precip_south_west = monthly_mean_precip_south_west.to_dataframe(name='Precip')
yearly_mean_df_precip_south_west = yearly_mean_precip_south_west.to_dataframe(name='Precip_yearly')
decadal_mean_df_precip_south_west = decadal_mean_precip_south_west.to_dataframe(name='Precip_decadal')

# 保存到csv
# 南方 西
monthly_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_yearly/new_monthly_south_west.csv')
yearly_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_yearly/new_yearly_south_west.csv')
decadal_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_yearly/new_decadal_south_west.csv')


## 计算夏季平均降水
# 计算每个时间点对应的月份
# 时间值的小数部分代表月份，0.000083 = 1个月
months = 12 - ((((ds_precc.time.values+0.000082547) % 1) / 0.000083333333333333333333333333333333333333333333333333).astype(int)-1) % 12

# 筛选5、6、7、8、9月的数据
summer_months = (months >= 5) & (months <= 9)
print(sum(summer_months))
# 提取夏季降水数据
ds_precip_south_west_summer = ds_precip_south_west.isel(time=summer_months)
# # 计算区域平均值，排除NAN值
# # 使用skipna=True参数自动忽略NAN值
monthly_mean_precip_south_west = ds_precip_south_west_summer.mean(dim=['lat', 'lon'], skipna=True)
# # 时间范围是-8.5到-6.7 ka BP，步长为0.001 ka（1年）
time_values = np.arange(-9.7, -6.7, 0.001)

# # 计算年平均值（每年）
yearly_mean_precip_south_west = monthly_mean_precip_south_west.groupby_bins('time', bins=len(time_values)).mean()
# # 计算十年平均值（每10年）
decadal_mean_precip_south_west = monthly_mean_precip_south_west.groupby_bins('time', bins=len(time_values)//10).mean()
# # 将DataArray转换为DataFrame
# 南方 西
monthly_mean_df_precip_south_west = monthly_mean_precip_south_west.to_dataframe(name='Precip')
yearly_mean_df_precip_south_west = yearly_mean_precip_south_west.to_dataframe(name='Precip_yearly')
decadal_mean_df_precip_south_west = decadal_mean_precip_south_west.to_dataframe(name='Precip_decadal')

# 南方 西
monthly_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_JJA/new_monthly_JJA_south_west_JJA.csv')
yearly_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_JJA/new_yearly_JJA_south_west_JJA.csv')
decadal_mean_df_precip_south_west.to_csv('./AF/PRECC/mean_csv/NS_JJA/new_decadal_JJA_south_west_JJA.csv')
###############################################
'''
计算西南地区（22°N to 35°N，98°E to 110°E）的
年均温距平
'''
################################################

ds_tas_s = xr.open_dataset('./AF/TS/TS_9700-6700a_BP.nc')
ds_tas_s = ds_tas_s.where((ds_tas_s.lat >= 22) & (ds_tas_s.lat <= 35) & (ds_tas_s.lon >= 98) & (ds_tas_s.lon <= 112), drop=True)
print(ds_tas_s.TS.shape)
# # # 使用skipna=True参数自动忽略NAN值
monthly_mean_tas_s = ds_tas_s['TS'].mean(dim=['lat', 'lon'], skipna=True)

# # # 单位转换
# monthly_mean_tas_s = monthly_mean_tas_s - 273.15
monthly_mean_tas_s = monthly_mean_tas_s - 273.15

# # 时间范围是-8.5到-6.7 ka BP，步长为0.001 ka（1年）
time_values = np.arange(-9.7, -6.7, 0.001)
# 计算年平均值
yearly_mean_tas_s = monthly_mean_tas_s.groupby_bins('time', bins=len(time_values)).mean()

# 计算十年平均值
decadal_mean_tas_s = monthly_mean_tas_s.groupby_bins('time', bins=len(time_values)//10).mean()

# # 计算半百年平均值（每100年）
half_centennial_mean = monthly_mean_tas_s.groupby_bins('time', bins=len(time_values)//100).mean()

# 将DataArray转换为DataFrame
monthly_mean_df_tas_s = monthly_mean_tas_s.to_dataframe(name='TS')
yearly_mean_df_tas_s = yearly_mean_tas_s.to_dataframe(name='TS_yearly')
decadal_mean_df_tas_s = decadal_mean_tas_s.to_dataframe(name='TS_decadal')
half_centennial_mean_df = half_centennial_mean.to_dataframe(name='TS_centennial')
print(len(decadal_mean_df_tas_s))
# 保存到csv
monthly_mean_df_tas_s.to_csv('./AF/TS/mean_csv/new_monthly_mean_southwest.csv')
yearly_mean_df_tas_s.to_csv('./AF/TS/mean_csv/new_yearly_mean_southwest.csv')
decadal_mean_df_tas_s.to_csv('./AF/TS/mean_csv/new_decadal_mean_southwest.csv')
half_centennial_mean_df.to_csv('./AF/TS/mean_csv/new_centennial_mean_southwest.csv')

## 后续画图操作均在Grapher软件中进行