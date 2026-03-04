'''
对SH石笋氧同位素全记录进行断点分析，
应数据提供者要求目前(2025年5月13日)SH石笋的氧同位素数据尚未公开，
公开后可在noaa网站获取
'''
# 定义断点模型
def break_model(x, t, t_break):
    """线性断点模型
    参数:
        x: 模型参数 [斜率1, 截距1, 斜率2, 截距2]
        t: 时间序列
        t_break: 断点位置
    返回:
        断点模型的值
    """
    return np.where(t < t_break, x[0] * t + x[1], x[2] * t + x[3])

# 定义加权最小二乘法的目标函数
def objective(x, t, y, t_break):
    """目标函数
    参数:
        x: 模型参数 [斜率1, 截距1, 斜率2, 截距2]
        t: 时间序列
        y: 观测值
        t_break: 断点位置
    返回:
        残差平方和
    """
    residuals = y - break_model(x, t, t_break)
    return np.sum(residuals**2)

# 暴力搜索找到最佳断点
def find_best_breakpoint(t, y):
    """暴力搜索最佳断点
    参数:
        t: 时间序列
        y: 观测值
    返回:
        最佳断点位置
    """
    best_t_break = None
    best_score = np.inf
    for t_break in t:
        # 添加参数约束条件
        bounds = [(-10, 10), (-1000, 1000), (-10, 10), (-1000, 1000)]
        x0 = np.array([0, 0, 0, 0])
        result = minimize(objective, x0, args=(t, y, t_break), bounds=bounds)
        if result.fun < best_score:
            best_score = result.fun
            best_t_break = t_break
    return best_t_break

# 使用自举法估计断点的置信区间
def bootstrap_breakpoint_confidence_interval(t, y, n_iterations=1000):
    """自举法估计断点的置信区间
    参数:
        t: 时间序列
        y: 观测值
        n_iterations: 自举法迭代次数
    返回:
        断点位置的置信区间
    """
    breakpoints = []
    for _ in range(n_iterations):
        t_resampled, y_resampled = resample(t, y)
        best_t_break = find_best_breakpoint(t_resampled, y_resampled)
        breakpoints.append(best_t_break)
    # 去除异常值
    breakpoints = np.array(breakpoints)
    breakpoints = breakpoints[~np.isnan(breakpoints)]
    return np.percentile(breakpoints, [2.5, 97.5])
if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from scipy.optimize import minimize
    from sklearn.utils import resample

    # 导入数据
    df = pd.read_excel('XX.xlsx')
    # 确保数据转换为NumPy数组
    data = df[['ageBP', 'O']].to_numpy()
    time = data[:, 0]
    observations_O = data[:, 1]
    # 对O进行断点分析
    best_t_break = find_best_breakpoint(time, observations_O)
    ci = bootstrap_breakpoint_confidence_interval(time, observations_O)
    print(f"最佳断点: {best_t_break} 置信区间: {ci}")
