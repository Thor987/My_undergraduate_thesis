'''
*************************************************************
计算8.2ka事件期间环流的差异（相对于8.0ka-7.9ka）
*************************************************************
'''
# ./AF/Wind/文件夹下为经向和纬向的风场数据
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import set_font

set_font.set_font()
# 读取NC文件并检查内容
ds_U = xr.open_dataset('./AF/Wind/U/U_8500-7600a_BP.nc')
ds_V = xr.open_dataset('./AF/Wind/V/V_8500-7600a_BP.nc')

# # 根据经纬度裁剪
ds_U = ds_U.where((ds_U.lat >= 0) & (ds_U.lat <= 60) & (ds_U.lon >= 60) & (ds_U.lon <= 150), drop=True)
ds_V = ds_V.where((ds_V.lat >= 0) & (ds_V.lat <= 60) & (ds_V.lon >= 60) & (ds_V.lon <= 150), drop=True)

# 定义时间范围（单位：千年 BP）
time_range_1 = slice(-8.3, -8.0)  # 8000-8100 BP
time_range_2 = slice(-8.0, -7.9)  # 8000-7900 BP

# 筛选时间范围并计算时间平均
## 计算夏季（6、7、8）
# 计算每个时间点对应的月份并筛选夏季数据
time_values = ds_U.time.values
ds_U = ds_U['U']
ds_V = ds_V['V']

# 计算月份
months = 12 - ((((time_values+0.000082547) % 1) / 0.000083333333333333333333333333333333333333333333333333).astype(int)-1) % 12

# 使用布尔索引获取夏季时间值
summer_mask = (months >= 6) & (months <= 8)
summer_times = time_values[summer_mask]
print("夏季月份数量:", len(summer_times))

# 使用实际的时间值选择夏季数据
ds_U_summer = ds_U.sel(time=summer_times)
ds_V_summer = ds_V.sel(time=summer_times)

# 计算时间范围内的平均值
# 经向
ds_U_1 = ds_U_summer.sel(time=time_range_1).mean(dim='time')
ds_U_2 = ds_U_summer.sel(time=time_range_2).mean(dim='time')
# 纬向
ds_V_1 = ds_V_summer.sel(time=time_range_1).mean(dim='time')
ds_V_2 = ds_V_summer.sel(time=time_range_2).mean(dim='time')

# 计算差异
U_diff = ds_U_1 - ds_U_2
V_diff = ds_V_1 - ds_V_2

# 创建经纬度网格
lon, lat = np.meshgrid(ds_U.lon, ds_U.lat)
# 绘制风场图
plt.figure(figsize=(15, 10))
# 使用geopandas加载世界地图
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# 裁剪到研究区域
world = world.cx[60:150, 0:60]
# 绘制地图
world.plot(ax=plt.gca(), color='lightgray', edgecolor='gray', alpha=0.3)
# 计算风速大小
wind_speed = np.sqrt(U_diff.values**2 + V_diff.values**2)
# 绘制风场
q = plt.quiver(lon, lat, U_diff.values, V_diff.values,
               wind_speed,
               cmap='rainbow',
               scale=5,
               width=0.003)
# 移除默认标签
plt.xlabel('')
plt.ylabel('')
# 设置刻度
ax = plt.gca()
# 设置经度刻度（20度间隔）
xticks = np.arange(60, 151, 20)
ax.set_xticks(xticks)
ax.set_xticklabels([f'{x}°E' for x in xticks], fontsize=22)  # 增大字号
# 设置纬度刻度（10度间隔）
yticks = np.arange(0, 61, 10)
ax.set_yticks(yticks)
ax.set_yticklabels([f'{y}°N' for y in yticks], fontsize=22)  # 增大字号
# 移除标题
# plt.title('' , fontsize=24)

# 调整颜色条标签字体大小
cbar = plt.colorbar(q, label='风速 (m/s)')
cbar.ax.set_ylabel('风速 (m/s)', fontsize=20)
cbar.ax.tick_params(labelsize=20)

# 调整参考箭头的字体大小
plt.quiverkey(q, 0.9, 1.02, 0.5, r'0.5 m/s', labelpos='E', fontproperties={'size': 20})
# 设置显示范围
plt.xlim(60, 150)
plt.ylim(1, 60)
# 添加网格
plt.grid(True, linestyle='--', alpha=0.5)
# 保存和显示图形
plt.tight_layout()
plt.savefig('./AF/Wind/wind_field_difference.png', dpi=300, bbox_inches='tight')
plt.show()