import pandas as pd
import matplotlib
# 在导入 pyplot 之前设置后端为 Agg (针对无显示器的服务器环境)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 1. 加载数据
cat_path = '/home/jclou/loujc_work/sofia/GAMA/1300-1350/Dec-0011_09_05_arcdrift/Dec-0011_09_05_arcdrift_cat.txt'
columns = ["name", "id", "x", "y", "z", "x_min", "x_max", "y_min", "y_max", "z_min", "z_max", 
           "n_pix", "f_min", "f_max", "f_sum", "rel", "flag", "rms", "w20", "w50", "wm50", 
           "z_w20", "z_w50", "z_wm50", "ell_maj", "ell_min", "ell_pa", "ell3s_maj", "ell3s_min", 
           "ell3s_pa", "kin_pa", "err_x", "err_y", "err_z", "err_f_sum", "snr", "snr_max", 
           "ra", "dec", "freq", "x_peak", "y_peak", "z_peak", "ra_peak", "dec_peak", "freq_peak"]

# 读取数据，处理空格分隔符
df = pd.read_csv(cat_path, sep='\s+', comment='#', names=columns)

# 2. 绘图
plt.figure(figsize=(12, 7))

# 使用 SNR 大小来控制点的大小，颜色代表频率
# 注意：s 参数代表面积，如果 SNR 很大，建议开方或缩小倍数
scatter = plt.scatter(df['ra'], df['dec'], c=df['freq']/1e6, s=df['snr']*2, 
                      cmap='RdYlBu', alpha=0.7, edgecolors='k')

plt.colorbar(scatter, label='Frequency (MHz)')
plt.gca().invert_xaxis()  # 天文学习惯：RA 左大右小
plt.xlabel('Right Ascension (J2000, deg)', fontsize=12)
plt.ylabel('Declination (J2000, deg)', fontsize=12)
plt.title(f'Spatial Distribution of {len(df)} HI Sources (FAST - GAMA)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# 标注信噪比最高的前 10 个源（比 5 个能看更多关键信息）
top_n = 10
df_sorted = df.sort_values('snr', ascending=False).head(top_n)
for i, row in df_sorted.iterrows():
    plt.annotate(int(row['id']), (row['ra'], row['dec']), 
                 textcoords="offset points", xytext=(0,10), ha='center',
                 fontsize=9, fontweight='bold')

# 3. 保存图片而不是显示
output_fig = '/home/jclou/loujc_work/sofia/GAMA/1300-1350/Dec-0011_09_05_arcdrift/fast_hi_distribution.png'
plt.savefig(output_fig, dpi=300, bbox_inches='tight')
print(f"图像已成功保存至: {output_fig}")

# 释放内存
plt.close()