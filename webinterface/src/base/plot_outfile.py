import struct
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import os
import numpy as np
import re
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
def read_out_file(filename):
    # 初始化結果
    time_data = []
    channel_data = {}  # 通道數據，鍵為通道編號，值為數據列表
    channel_ids = {}  # 通道 ID，鍵為通道編號，值為名稱

    try:
        with open(filename, "rb") as binfobj:
            # Step 1: 讀取檔案頭（12 字節）
            header = binfobj.read(12)
            if not header.startswith(b"FuP_pHyS"):
                print("錯誤：檔案不是有效的 .out 檔案")
                return None, None, None

            # 檢查字節序
            platform = header[-4:].decode('utf-8', errors='ignore')
            littlebyteorder = ["PCD%", "PCS%", "DEC%", "AXP%"]
            bigbyteorder = ["SUN%", "HPU%", "HPA%", "IBM%"]
            if platform in littlebyteorder:
                byteorder = "little"
                fmt = "<f"  # 小端序浮點數
            elif platform in bigbyteorder:
                byteorder = "big"
                fmt = ">f"  # 大端序浮點數
            else:
                print("錯誤：無法識別檔案的字節序")
                return None, None, None

            # Step 2: 讀取通道數量（4 字節）
            chunk = binfobj.read(4)
            nchannels = int(struct.unpack(fmt, chunk)[0])
            if nchannels <= 0:
                print("錯誤：檔案不包含通道數據")
                return None, None, None

            # Step 3: 讀取版本號（4 字節）
            chunk = binfobj.read(4)
            version = struct.unpack(fmt, chunk)[0]
            if version != 2.0:
                print(f"錯誤：檔案版本為 {version}，僅支援 2.0")
                return None, None, None

            # Step 4: 讀取通道 ID（32 字節 × 通道數量）
            channel_ids["time"] = "Time(s)"
            for ch in range(1, nchannels + 1):
                chname = binfobj.read(32).decode('utf-8', errors='ignore').strip()
                chname = chname.replace("  ", " ")  # 清理多餘空格
                channel_ids[ch] = chname

            # Step 5: 讀取短標題（60 字節 × 2）
            short_title = ""
            ln1 = binfobj.read(60).decode('utf-8', errors='ignore').strip()
            ln2 = binfobj.read(60).decode('utf-8', errors='ignore').strip()
            if ln1:
                short_title += ln1
            if ln2:
                short_title += "\n" + ln2
            print("短標題:", short_title)

            # Step 6: 計算數據部分的行數
            total_bytes = os.path.getsize(filename)
            begin_nondata_bytes = 12 + 4 + 4 + 32 * nchannels + 60 * 2
            end_nondata_bytes = 8
            databytes = total_bytes - begin_nondata_bytes - end_nondata_bytes
            ncols = nchannels + 2  # 通道數 + 時間 + 通道計數
            nrows = int(databytes / (ncols * 4))  # 每值 4 字節

            # Step 7: 讀取數據部分
            for _ in range(nrows):
                # 讀取通道數（4 字節，忽略或驗證）
                chunk = binfobj.read(4)
                if not chunk:
                    break
                # 讀取時間（4 字節）
                chunk = binfobj.read(4)
                if not chunk:
                    break
                time_val = struct.unpack(fmt, chunk)[0]
                time_data.append(time_val)
                # 讀取通道數據（4 字節 × 通道數）
                for ch in range(1, nchannels + 1):
                    chunk = binfobj.read(4)
                    if not chunk:
                        break
                    val = struct.unpack(fmt, chunk)[0]
                    if ch not in channel_data:
                        channel_data[ch] = []
                    channel_data[ch].append(val)

    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return None, None, None

    return time_data, channel_data, channel_ids


def get_channel_id_name(busdata,channel_id):   

    # 使用正則表達式匹配
    # [A-Z]{4} 匹配 4 個大寫字母 (ANGL)
    # \d+ 匹配一個或多個數字 (1131)
    # \d{2}\.\d{3} 匹配 xx.xxx 格式的小數 (25.000)
    pattern = r'([A-Z]{4})\s+(\d+)\[.*?\s+(\d{2}\.\d{3})\]'
    match = re.match(pattern, channel_id)

    # 提取結果
    if match:
        angl = match.group(1)  # ANGL
        number = match.group(2)  # 1131
        decimal = match.group(3)  # 25.000
        print(f"ANGL: {angl}, Number: {number}, Decimal: {decimal}")
    else:
        print("No match found")

    print(f"type(number)--> {type(number)}")
    name = busdata["name"][np.where(busdata["num"]==number)][0]
    
    return f"{angl} {number} [{name}] {decimal}"


    # name = {busdata["name"][np.where(busdata["num"]==part2)][0]}
    # # print(f"提取到的第二部分: {part2}")
    # return f"{part1} {part2} [{name}] {part3}"


def plot_channels(time_data, channel_data, channel_ids, busdata, jpg_file_path):
    font_path = '../Data/PlotFont/font/SimHei.ttf'  # 替換成你的字體路徑
    fm.fontManager.addfont(font_path)
    # 設置默認字體
    plt.rcParams['font.family'] = ['SimHei']  # 替換成你的字體名稱

    # 設置圖表大小和周邊背景顏色（灰色）
    plt.figure(figsize=(10, 6), facecolor='lightgray')
    ax = plt.gca()
    
    # 設置繪圖區域背景為白色
    ax.set_facecolor('white')

    # 調整圖表右側邊距，為圖例留出空間
    plt.subplots_adjust(right=0.75)

    # 定義線條顏色，與圖片匹配
    colors = ['green', 'red', 'blue', 'gray', 'yellow']
    color_idx = 0

    # 繪製每條通道的線條
    for ch_num, ch_data in channel_data.items():
        if ch_num in channel_ids and ch_num != "time":  # 跳過時間通道
            labelname = get_channel_id_name(busdata,channel_ids[ch_num])
            plt.plot(time_data, ch_data, label=labelname, color=colors[color_idx % len(colors)])
            color_idx += 1
    
    # 設置 X 和 Y 軸標籤
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Angle", fontsize=12)

    # 設置 Y 軸範圍，與圖片一致
    # plt.ylim(25, 50)

    # 設置圖例，放置在圖表右側外部
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderpad=0.5, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10, frameon=False)

    # 啟用格線
    plt.grid(True)

    # 保存圖表
    plt.savefig(f'{jpg_file_path}', dpi=100, bbox_inches='tight')
    plt.close()

def datatoexcel(time_data, channel_data, channel_ids, excel_path):
    # --- 保存 Excel 部分 ---
    # 創建數據字典，第一列為 Time
    data = {"Time": time_data}

    # 添加每個通道的數據，標頭為 channel_ids
    for ch_num, ch_data in channel_data.items():
        if ch_num in channel_ids and ch_num != "time":  # 跳過時間通道
            data[channel_ids[ch_num]] = ch_data

    # 創建 DataFrame
    df = pd.DataFrame(data)
    df.to_excel(f'{excel_path}', index=False)


if __name__ == '__main__':
    time_data, channel_data, channel_ids = read_out_file(dynamic_out_files)
    if time_data is not None:
        plot_channels(time_data, channel_data, channel_ids, busdata, jpg_file_path)
        datatoexcel(time_data, channel_data, channel_ids, excel_path)    
    else:
        print("無法讀取檔案")




   