# 读取数据，ageBP和d18O,选取8000-8274 yr BP做皮尔逊相关分析

import pandas as pd
import numpy as np
from scipy import stats
# 读取数据
df = pd.read_excel('./data/董哥和双河.xlsx')

# 提取SH、DA和D4三个石笋的数据
# A-C列为SH石笋数据
SH_data = df.iloc[:, 0:3]
SH_data.columns = ['sample', 'ageBP', 'd18O']

# E-G列为DA石笋数据
DA_data = df.iloc[:, 4:7]
DA_data.columns = ['sample', 'ageBP', 'd18O']

# I-K列为D4石笋数据
D4_data = df.iloc[:, 8:11]
D4_data.columns = ['sample', 'ageBP', 'd18O']

# 筛选8000-8274 yr BP的数据
SH_filtered = SH_data[(SH_data['ageBP'] >= 8000) & (SH_data['ageBP'] <= 8274)]
DA_filtered = DA_data[(DA_data['ageBP'] >= 8000) & (DA_data['ageBP'] <= 8274)]
D4_filtered = D4_data[(D4_data['ageBP'] >= 8000) & (D4_data['ageBP'] <= 8274)]

print(f"SH石笋筛选后数据量: {len(SH_filtered)}")
print(f"DA石笋筛选后数据量: {len(DA_filtered)}")
print(f"D4石笋筛选后数据量: {len(D4_filtered)}")

# 由于三个石笋的采样点可能不同，需要对数据进行插值处理来对齐时间序列
# 创建统一的时间轴.3年插值
time_range = np.arange(8000, 8275, 3)

# 插值函数，将不规则的时间序列插值到统一时间轴
def interpolate_data(data, time_range):
    # 按年龄排序
    data = data.sort_values('ageBP')
    # 线性插值
    return np.interp(time_range, data['ageBP'], data['d18O'])

# 对三个石笋数据进行插值
SH_interp = interpolate_data(SH_filtered, time_range)
DA_interp = interpolate_data(DA_filtered, time_range)
D4_interp = interpolate_data(D4_filtered, time_range)

# 计算皮尔逊相关系数和p值
corr_SH_DA, p_SH_DA = stats.pearsonr(SH_interp, DA_interp)
corr_SH_D4, p_SH_D4 = stats.pearsonr(SH_interp, D4_interp)
corr_DA_D4, p_DA_D4 = stats.pearsonr(DA_interp, D4_interp)

# 输出相关分析结果
print("\n皮尔逊相关分析结果:")
print(f"SH-DA: 相关系数={corr_SH_DA:.4f}, p值={p_SH_DA:.4f}")
print(f"SH-D4: 相关系数={corr_SH_D4:.4f}, p值={p_SH_D4:.4f}")
print(f"DA-D4: 相关系数={corr_DA_D4:.4f}, p值={p_DA_D4:.4f}")
