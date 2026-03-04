%% 该代码实现了SH石笋氧同位素的连续小波变换分析
% Written January 1998 by C. Torrence 相关函数请参照
% https://github.com/ct6502/wavelets/tree/main
%% 以下代码在Matlab环境中运行 
load 'OO18.txt'   % 加载数据
sst = OO18;

variance = std(sst)^2;
sst = (sst - mean(sst))/sqrt(variance) ;

n = length(sst);
dt = 2.38;     % 采样间隔
time = [0:length(sst)-1]*dt + 7975.6;  % 构建时间轴
xlim = [7950,8300];  % 绘图范围
pad = 1;       % 用零填充时间序列
dj = 0.25;     % 每个倍频程4个子倍频程
s0 = 2*dt;     % 起始尺度
j1 = 7/dj;     % 进行7个2的幂次方的尺度分析
lag1 = 0.9;    % 红噪声背景的滞后1自相关
mother = 'Morlet';  % 使用Morlet小波

% 小波变换
[wave,period,scale,coi] = wavelet(sst,dt,pad,dj,s0,j1,mother);
power = (abs(wave)).^2 ;       % 计算小波功率谱

% 显著性检验
[signif,fft_theor] = wave_signif(1.0,dt,scale,0,lag1,-1,-1,mother);
sig95 = (signif')*(ones(1,n));  % 扩展显著性水平为矩阵
sig95 = power ./ sig95;         % 比值>1表示功率显著


figure('Position', [100, 100, 800, 400]);
levels = [0.0625,0.125,0.25,0.5,1,2,4,8,16,32,64,128,256] ;

Yticks = 2.^(fix(log2(min(period))):fix(log2(128))); % 限制 Y 轴到 128 年
% 假设 Z 是数据矩阵
Z = log2(power); % 使用log2(power)作为数据矩阵
Z(Z > 4) = 4; % 将超出上限的值设置为 4
Z(Z < -4) = -4; % 将低于下限的值设置为 -4
% 绘制填充色
contourf(time, log2(period), Z, log2(levels), 'LineColor', 'none');
hold on;
% 绘制等高线
contour(time,log2(period),Z,log2(levels));
% 绘制显著性区域
contourf(time, log2(period), sig95, [-99, 1], 'LineColor', 'none', 'FaceAlpha', 0.001); % 半透明填充显著性区域
% 绘制影响锥
plot(time,log2(coi),'k', 'LineWidth', 1) % 影响锥，黑色加粗

xlabel('Time (year)')
ylabel('Period (years)')
% 设置标题、坐标轴标签和刻度标签的字体
set(gca, 'FontName', 'Times New Roman');  % 设置当前坐标轴的字体
set(get(gca, 'Title'), 'FontName', 'Times New Roman');  % 设置标题字体
set(get(gca, 'XLabel'), 'FontName', 'Times New Roman');  % 设置 X 轴标签字体
set(get(gca, 'YLabel'), 'FontName', 'Times New Roman');  % 设置 Y 轴标签字体
set(gca,'XLim',xlim(:))
set(gca,'YLim',log2([min(period),148]), ...
    'YDir','reverse', ...
    'YTick',log2(Yticks(:)), ...
    'YTickLabel',Yticks)
set(gca, 'FontSize', 22); % Adjust font size as needed
set(gca, 'LineWidth', 3); % 设置坐标轴边框的粗细
set(gca, 'Box', 'on');     % 确保边框显示
hold on
contour(time,log2(period),sig95,[-99,1],'k', 'LineWidth', 1.5); % 显著性区域，黑色加粗

hold off
colormap(parula); % 可选配色
colorbar('eastoutside');



