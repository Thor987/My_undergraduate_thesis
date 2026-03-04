'''
中国季风区石笋氧同位素相关分析
17个石笋氧同位素值储存在data_for_grapher.xlsx表格中
具体序列见论文表述，可在noaa网站检索获取https://www.ncei.noaa.gov/access/paleo-search/?dataTypeId=11
'''
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, zscore
import numpy as np

# 读取Excel文件
df = pd.read_excel('data_for_grapher.xlsx', sheet_name='W2')
# 初始化图形
# plt.figure(figsize=(12, 12))

# 获取所有样本列
sample_cols = [col for col in df.columns if col.startswith('sample')]
# 将样本分为两组
first_group = sample_cols[:11]  # 前13个样本
second_group = sample_cols[7:]  # 后11个样本

# 第一组相关分析
correlation_matrix_1 = pd.DataFrame(index=first_group, columns=first_group)
p_value_matrix_1 = pd.DataFrame(index=first_group, columns=first_group)

# 第二组相关分析
correlation_matrix_2 = pd.DataFrame(index=second_group, columns=second_group)
p_value_matrix_2 = pd.DataFrame(index=second_group, columns=second_group)

# 创建图形
fig1 = plt.figure(figsize=(10, 10))

sample_names = [
    "WY13", "QM09", "J13", "HF01", "SH", "DA", "D4", 
    "HS4", "BH2", "NH33", "LH4", "QT40", "LH2", "SB43", "SB27", "SB10", "SN29"
]

# 设置颜色循环
colors1 = plt.cm.tab20(np.linspace(0, 1, len(first_group)))
colors2 = plt.cm.tab20(np.linspace(0, 1, len(second_group)))

# 设置全局字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 计算相关性和绘制图形
for i, sample1 in enumerate(first_group):
    for j, sample2 in enumerate(first_group):
        # 获取数据
        idx1 = sample1.split('.')[1] if '.' in sample1 else ''
        idx2 = sample2.split('.')[1] if '.' in sample2 else ''
        
        age1 = f'ageBP.{idx1}' if idx1 else 'ageBP'
        d18O1 = f'd18O.{idx1}' if idx1 else 'd18O'
        age2 = f'ageBP.{idx2}' if idx2 else 'ageBP'
        d18O2 = f'd18O.{idx2}' if idx2 else 'd18O'
        
        sample1_data = df[[sample1, age1, d18O1]].dropna()
        sample2_data = df[[sample2, age2, d18O2]].dropna()
        
        # 筛选数据
        filtered1 = sample1_data[(sample1_data[age1] >= 7992) & (sample1_data[age1] <= 8270)].copy()
        filtered2 = sample2_data[(sample2_data[age2] >= 7992) & (sample2_data[age2] <= 8270)].copy()
        
        # 计算z分数
        filtered1['d18O_z'] = zscore(filtered1[d18O1])
        filtered2['d18O_z'] = zscore(filtered2[d18O2])
        
        # 插值
        common_ages = np.arange(7992, 8270, 10)
        interp1 = np.interp(common_ages, filtered1[age1], filtered1['d18O_z'])
        interp2 = np.interp(common_ages, filtered2[age2], filtered2['d18O_z'])
        
        # 计算相关系数和P值
        corr, p_value = pearsonr(interp1, interp2)
        correlation_matrix_1.loc[sample1, sample2] = corr
        p_value_matrix_1.loc[sample1, sample2] = p_value

        ax = plt.subplot(len(first_group), len(first_group), i * len(first_group) + j + 1)
        
        if i < j:  # 上三角：显示相关系数和显著性标记，并填色
            corr = correlation_matrix_1.iloc[i, j]
            p_value = p_value_matrix_1.iloc[i, j]
            
            # 创建一个矩形对象来填充整个子图区域
            rect = plt.Rectangle(
                (0, 0),     # 矩形的起始位置（左下角坐标）
                1, 1,       # 矩形的宽度和高度（这里是1表示填充整个子图）
                facecolor=plt.cm.coolwarm((corr + 1) / 2),  # 设置填充颜色
                # coolwarm是一个颜色映射，从蓝色（负相关）到红色（正相关）
                # (corr + 1) / 2 将相关系数从[-1,1]映射到[0,1]范围
                transform=ax.transAxes  # 使用轴的相对坐标系统
            )
            # 将矩形添加到当前子图中
            ax.add_patch(rect)
            
            # 分别显示相关系数和显著性标记
            plt.text(0.5, 0.5, f'{corr:.2f}', 
                    ha='center', va='center',  # 相关系数居中显示
                    color='black' if abs(corr) < 0.5 else 'white',
                    fontsize=17,
                    family='Times New Roman',
                    transform=ax.transAxes)
            
            # 显著性标记放在右上角
            significance = ''
            if p_value < 0.01:
                significance = '***'
            elif p_value < 0.05:
                significance = '**'
            elif p_value < 0.1:
                significance = '*'
            
            if significance:  # 只有当有显著性标记时才显示
                plt.text(0.95, 0.95, significance,  # 位置在右上角
                        ha='right', va='top',  # 右对齐，顶部对齐
                        color='black' if abs(corr) < 0.5 else 'white',
                        fontsize=12,  # 显著性标记字体稍小
                        family='Times New Roman',
                        transform=ax.transAxes)
            
        elif i > j:  # 下三角：显示折线图
            # 倒转y轴,即负值越大，越靠上
            # plt.gca().invert_yaxis()    
            plt.plot(common_ages, interp1, color=colors1[i], linewidth=1.5, alpha=1)
            plt.plot(common_ages, interp2, color=colors1[j], linewidth=1.5, alpha=1)
            
            # 设置坐标轴范围
            plt.xlim(7992, 8270)
            plt.ylim(-3, 3)
            # 倒转y轴,即负值越大，越靠上
            plt.gca().invert_yaxis()
            # 添加坐标轴标签
            # if i == len(first_group)-1:  # 最后一行
            #     ax.set_xlabel('Age (yr BP)', fontsize=12, family='Times New Roman')
            # if j == 0:  # 第一列
            #     ax.set_ylabel('Z-score', fontsize=12, family='Times New Roman')
            
            # 设置刻度
            ax.tick_params(axis='both', which='major', labelsize=12)
            
            # 只在特定位置显示刻度标签
            if i == len(first_group)-1:  # 最后一行显示x轴刻度
                plt.xticks([8000, 8100, 8200], ['8000', '', '8200'])
            else:
                plt.xticks([])
                
            if j == 0:  # 第一列显示y轴刻度
                plt.yticks([-2, 0, 2], ['-2', '0', '2'])
            else:
                plt.yticks([])
            
        else:  # 对角线：显示样本名称
            plt.text(0.5, 0.5, sample_names[i], 
                    ha='center', va='center', 
                    fontweight='bold', 
                    fontsize=20,
                    family='Times New Roman',
                    transform=ax.transAxes)
        
        if i > j:  # 为下三角的图添加边框
            ax.spines['left'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
            ax.spines['right'].set_visible(True)
            ax.spines['top'].set_visible(True)
        else:
            plt.axis('off')

plt.tight_layout()
# plt.show()
plt.savefig('W2_correlation_matrix.png', dpi=300)
fig2 = plt.figure(figsize=(9, 9))
# 第二组计算相关性和绘图
plt.figure(fig2.number)  # 切换到第二个图
for i, sample1 in enumerate(second_group):
    for j, sample2 in enumerate(second_group):
        ax = plt.subplot(len(second_group), len(second_group), i * len(second_group) + j + 1)
        
        # 获取数据
        idx1 = sample1.split('.')[1] if '.' in sample1 else ''
        idx2 = sample2.split('.')[1] if '.' in sample2 else ''
        
        age1 = f'ageBP.{idx1}' if idx1 else 'ageBP'
        d18O1 = f'd18O.{idx1}' if idx1 else 'd18O'
        age2 = f'ageBP.{idx2}' if idx2 else 'ageBP'
        d18O2 = f'd18O.{idx2}' if idx2 else 'd18O'
        
        sample1_data = df[[sample1, age1, d18O1]].dropna()
        sample2_data = df[[sample2, age2, d18O2]].dropna()
        
        # 筛选数据
        filtered1 = sample1_data[(sample1_data[age1] >= 7992) & (sample1_data[age1] <= 8270)].copy()
        filtered2 = sample2_data[(sample2_data[age2] >= 7992) & (sample2_data[age2] <= 8270)].copy()
        
        # 计算z分数
        filtered1['d18O_z'] = zscore(filtered1[d18O1])
        filtered2['d18O_z'] = zscore(filtered2[d18O2])
        
        # 插值
        common_ages = np.arange(7992, 8270, 10)
        filtered1 = filtered1.sort_values(by=age1)
        filtered2 = filtered2.sort_values(by=age2)
        
        interp1 = np.interp(common_ages, filtered1[age1], filtered1['d18O_z'])
        interp2 = np.interp(common_ages, filtered2[age2], filtered2['d18O_z'])
        
        # 计算相关系数和P值
        corr, p_value = pearsonr(interp1, interp2)
        correlation_matrix_2.loc[sample1, sample2] = corr
        p_value_matrix_2.loc[sample1, sample2] = p_value

        if i < j:  # 上三角：显示相关系数和显著性标记，并填色
            corr = correlation_matrix_2.iloc[i, j]
            p_value = p_value_matrix_2.iloc[i, j]
            
            # 创建一个矩形对象来填充整个子图区域
            rect = plt.Rectangle(
                (0, 0),     # 矩形的起始位置（左下角坐标）
                1, 1,       # 矩形的宽度和高度（这里是1表示填充整个子图）
                facecolor=plt.cm.coolwarm((corr + 1) / 2),  # 设置填充颜色
                # coolwarm是一个颜色映射，从蓝色（负相关）到红色（正相关）
                # (corr + 1) / 2 将相关系数从[-1,1]映射到[0,1]范围
                transform=ax.transAxes  # 使用轴的相对坐标系统
            )
            # 将矩形添加到当前子图中
            ax.add_patch(rect)
            
            # 分别显示相关系数和显著性标记
            plt.text(0.5, 0.5, f'{corr:.2f}', 
                    ha='center', va='center',  # 相关系数居中显示
                    color='black' if abs(corr) < 0.5 else 'white',
                    fontsize=17,
                    family='Times New Roman',
                    transform=ax.transAxes)
            
            # 显著性标记
            significance = ''
            if p_value < 0.01:
                significance = '***'
            elif p_value < 0.05:
                significance = '**'
            elif p_value < 0.1:
                significance = '*'
            
            if significance:  # 只有当有显著性标记时才显示
                plt.text(0.95, 0.95, significance,  # 位置在右上角
                        ha='right', va='top',  # 右对齐，顶部对齐
                        color='black' if abs(corr) < 0.5 else 'white',
                        fontsize=  12,  # 显著性标记字体稍小
                        family='Times New Roman',
                        transform=ax.transAxes)
            
        elif i > j:  # 下三角：显示折线图
            plt.plot(common_ages, interp1, color=colors2[i], linewidth=1.5, alpha=1)
            plt.plot(common_ages, interp2, color=colors2[j], linewidth=1.5, alpha=1)
            
            # 设置坐标轴范围
            plt.xlim(7992, 8270)
            plt.ylim(-3, 3)
            # 倒转y轴,即负值越大，越靠上
            plt.gca().invert_yaxis()
            # 添加坐标轴标签
            # if i == len(second_group)-1:  # 最后一行
            #     ax.set_xlabel('Age (yr BP)', fontsize=8, family='Times New Roman')
            # if j == 0:  # 第一列
            #     ax.set_ylabel('Z-score', fontsize=8, family='Times New Roman')
            
            # 设置刻度
            ax.tick_params(axis='both', which='major', labelsize=12)
            
            # 只在特定位置显示刻度标签
            if i == len(second_group)-1:  # 最后一行显示x轴刻度
                plt.xticks([8000, 8100, 8200], ['8000', '', '8200'])
            else:
                plt.xticks([])
                
            if j == 0:  # 第一列显示y轴刻度
                plt.yticks([-2, 0, 2], ['-2', '0', '2'])
            else:
                plt.yticks([])
            
        else:  # 对角线：显示样本名称
            plt.text(0.5, 0.5, sample_names[i+7], 
                    ha='center', va='center', 
                    fontweight='bold', 
                    fontsize= 18,
                    family='Times New Roman',
                    transform=ax.transAxes)
        
        if i > j:  # 为下三角的图添加边框
            ax.spines['left'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
            ax.spines['right'].set_visible(True)
            ax.spines['top'].set_visible(True)
        else:
            plt.axis('off')

plt.tight_layout()
# plt.show()
plt.savefig('E2_correlation_matrix.png', dpi=300)