import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os


def visualize_single_password(password: str, segments_8b: list, segments_08b: list, 
                               cut_position_func, caculate_jaccard_distance_func,
                               cut_position_with_tags_func, save_path: str = None):
    """視覺化單個密碼在兩個模型的切割位置"""
    
    # 取得切割位置
    cuts_8b = set(cut_position_func(password, segments_8b))
    cuts_08b = set(cut_position_func(password, segments_08b))
    
    # 取得切割位置及 tags
    cuts_tags_8b = cut_position_with_tags_func(password, segments_8b)
    cuts_tags_08b = cut_position_with_tags_func(password, segments_08b)
    
    pw_len = len(password)
    fig_width = max(14, pw_len * 1.2)
    fig, axes = plt.subplots(2, 1, figsize=(fig_width, 10))
    
    # 繪製函數 (顯示每個 segment 的 tag)
    def draw_password_bar_with_segments(ax, pw, segments, title, line_color, tag_color):
        # 繪製每個字元
        for i, char in enumerate(pw):
            ax.text(i + 0.5, 0.5, char, ha='center', va='center', fontsize=14, fontweight='bold')
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=False, edgecolor='gray'))
        
        # 計算每個 segment 的位置範圍並顯示 tag
        current_pos = 0
        for idx, seg in enumerate(segments):
            text = seg['text'].strip()
            tag = seg.get('tag', 'X')
            seg_len = len(text)
            
            if seg_len > 0:
                # segment 中心位置
                seg_center = current_pos + seg_len / 2
                # 交錯高度避免重疊
                y_offset = -0.7 if idx % 2 == 0 else -1.3
                # 顯示 tag (字體放大)
                ax.text(seg_center, y_offset, tag, ha='center', va='top', 
                       fontsize=14, color=tag_color, fontweight='bold')
                # 畫底線標示範圍
                ax.plot([current_pos + 0.1, current_pos + seg_len - 0.1], 
                       [y_offset + 0.15, y_offset + 0.15], 
                       color=tag_color, linewidth=2, alpha=0.5)
            
            # 繪製切割線（除了最後一個 segment）
            current_pos += seg_len
            if current_pos < pw_len:
                ax.axvline(x=current_pos, color=line_color, linewidth=3, linestyle='-')
                ax.text(current_pos, 1.2, f'{current_pos}', ha='center', va='bottom', 
                       fontsize=11, color=line_color)
        
        ax.set_xlim(0, pw_len)
        ax.set_ylim(-2.0, 2.0)
        ax.set_title(title, fontsize=12)
        ax.set_xticks(range(pw_len + 1))
        ax.set_yticks([])
    
    # 產生 segments 摘要
    seg_summary_8b = " | ".join([f"{s['text'].strip()}({s.get('tag','X')})" for s in segments_8b if s['text'].strip()])
    seg_summary_08b = " | ".join([f"{s['text'].strip()}({s.get('tag','X')})" for s in segments_08b if s['text'].strip()])
    
    title_8b = f'8B Model: {seg_summary_8b}'
    title_08b = f'0.8B Model: {seg_summary_08b}'
    
    # 8B 模型 (切割線紅色, tag黑色)
    draw_password_bar_with_segments(axes[0], password, segments_8b, title_8b, 'red', 'black')
    
    # 0.8B 模型 (切割線綠色, tag綠色)
    draw_password_bar_with_segments(axes[1], password, segments_08b, title_08b, 'green', 'green')
    
    # 計算 Jaccard Distance 顯示在標題
    jac_dist = caculate_jaccard_distance_func(cuts_8b, cuts_08b)
    plt.suptitle(f'Password: "{password}" | Jaccard Distance: {jac_dist:.2f}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"已儲存: {save_path}")
    else:
        plt.show()
    plt.close()


def draw_histogram(jac_distance: list, save_path: str = 'stastic/second_time/jaccard_histogram.png'):
    """繪製 Jaccard Distance 分佈直方圖"""
    plt.figure(figsize=(10, 5))
    plt.hist(jac_distance, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(x=np.mean(jac_distance), color='red', linestyle='--', 
                label=f'Mean: {np.mean(jac_distance):.3f}')
    plt.axvline(x=np.median(jac_distance), color='orange', linestyle='--',
                label=f'Median: {np.median(jac_distance):.3f}')
    plt.xlabel('Jaccard Distance')
    plt.ylabel('Count')
    plt.title('Distribution of Jaccard Distance (8B vs 0.8B)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"已儲存: {save_path}")


def draw_heatmap(jac_distance: list, save_path: str = 'stastic/second_time/jaccard_heatmap.png'):
    """繪製 Jaccard Distance 熱力圖"""
    n = len(jac_distance)
    side = int(np.ceil(np.sqrt(n)))
    padded = jac_distance + [np.nan] * (side * side - n)
    matrix = np.array(padded).reshape(side, side)
    matrix = np.flipud(matrix)  # 上下翻轉，使 y 軸由下到上為 0-9
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(matrix,
                annot=True,
                fmt='.2f',
                cmap='RdYlGn_r',
                vmin=0, vmax=1,
                cbar_kws={'label': 'Jaccard Distance'},
                yticklabels=list(range(side-1, -1, -1)))  # y 軸標籤: 9,8,7...0
    plt.title('Jaccard Distance Heatmap (8B vs 0.8B)')
    plt.xlabel('Password Index (column)')
    plt.ylabel('Password Index (row)')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"已儲存: {save_path}")


def draw_sorted_bar(password: list, jac_distance: list, 
                    save_path: str = 'stastic/second_time/jaccard_sorted_bar.png'):
    """繪製排序後的橫條圖"""
    sorted_pairs = sorted(zip(password, jac_distance), key=lambda x: x[1], reverse=True)
    sorted_pw, sorted_dist = zip(*sorted_pairs)
    
    fig, ax = plt.subplots(figsize=(12, 16))
    colors = plt.cm.RdYlGn_r(np.array(sorted_dist))
    ax.barh(range(len(sorted_dist)), sorted_dist, color=colors)
    ax.set_yticks(range(len(sorted_pw)))
    ax.set_yticklabels(sorted_pw, fontsize=8)
    ax.set_xlabel('Jaccard Distance')
    ax.set_title('Segmentation Difference (Sorted by Distance)')
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"已儲存: {save_path}")


def draw_all_different_passwords(diff_list: list, data_bigger_b: list, data_smaller_b: list,
                                  cut_position_func, caculate_jaccard_distance_func,
                                  cut_position_with_tags_func,
                                  output_dir: str = 'stastic/second_time/single_passwords'):
    """產生所有有差異的單個密碼切割圖"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n產生所有有差異的單個密碼切割圖...")
    for item in diff_list:
        i = item['index']
        safe_pw = item['password'].replace('/', '_').replace('\\', '_')[:20]
        visualize_single_password(
            data_bigger_b[i][0],
            data_bigger_b[i][1],
            data_smaller_b[i][1],
            cut_position_func,
            caculate_jaccard_distance_func,
            cut_position_with_tags_func,
            save_path=f'{output_dir}/{i:03d}_{safe_pw}.png'
        )
    print(f"總共儲存 {len(diff_list)} 個有差異的密碼視覺化圖到 {output_dir}/")
