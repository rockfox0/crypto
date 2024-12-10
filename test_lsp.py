import cv2
import numpy as np
import os

# LSB 隐藏算法
def hide_lsb(block, data, img):
    si = img.shape
    N = si[1] // block[1]  # 水平方向的块数
    M = si[0] // block[0]  # 垂直方向的块数
    out = img.copy()
    lend = len(data)
    idx = 0

    for i in range(M):
        rst, red = i * block[0], (i + 1) * block[0]
        for j in range(N):
            if idx >= lend:
                break
            bit = data[idx]
            cst, ced = j * block[1], (j + 1) * block[1]
            for row in range(rst, red):
                for col in range(cst, ced):
                    out[row, col] = (int(out[row, col]) & ~1) | bit
            idx += 1
    return out

# LSB 提取算法
def dh_lsb(block, img):
    si = img.shape
    N = si[1] // block[1]
    M = si[0] // block[0]
    out = []
    thr = (block[0] * block[1] + 1) // 2

    for i in range(M):
        rst, red = i * block[0], (i + 1) * block[0]
        for j in range(N):
            cst, ced = j * block[1], (j + 1) * block[1]
            tmp = np.sum((img[rst:red, cst:ced] & 1).flatten())
            out.append(1 if tmp >= thr else 0)
    return out

# 将数字转换为二进制
def convert_to_binary(data):
    return [int(bit) for bit in bin(data)[2:].zfill(32)]  # 填充到32位

# 将二进制数据转换回整数
def convert_to_int(binary_data):
    return int("".join(map(str, binary_data)), 2)

# 计算误码率
def calculate_ber(original_data, extracted_data):
    original_bits = convert_to_binary(original_data)  # 转为二进制
    len_d = len(original_bits)
    extracted_bits = extracted_data[:len_d]
    error_count = np.sum(np.abs(np.array(original_bits) - np.array(extracted_bits)))
    ber = error_count / len_d
    return ber, error_count

# 主程序部分
pn = r"D:\\wdnmd\\Crypto\\pythonProject"
fn = "ggb.bmp"
image_path = os.path.join(pn, fn)

# 加载原始图像并转换为灰度值
s = cv2.imread(image_path)
if s is None:
    raise FileNotFoundError(f"文件未找到: {image_path}")
if len(s.shape) >= 3:
    l = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
else:
    l = s

# 隐藏数据相关操作
block = (3, 3)
data = 2321  # 需要隐藏的数字
binary_data = convert_to_binary(data)  # 转换为二进制数据

si = l.shape
sN = (si[0] // block[0]) * (si[1] // block[1])
tN = len(binary_data)

# 如果载体图像尺寸不足以隐藏秘密信息，则在垂直方向上复制填充图像
if sN < tN:
    multiple = np.ceil(tN / sN).astype(int)
    tmp = np.tile(l, (multiple, 1))
    l = tmp[:tN]

# 执行隐藏并保存结果
stegoed = hide_lsb(block, binary_data, l)
stego_path = os.path.join(pn, "hidden1.bmp")
cv2.imwrite(stego_path, stegoed)
print(f"隐写完成，结果保存到: {stego_path}")

# 加载隐藏了数据的载体图像
hidden_path = stego_path
y = cv2.imread(hidden_path, cv2.IMREAD_GRAYSCALE)
if y is None:
    raise FileNotFoundError(f"文件未找到: {hidden_path}")

# 提取数据
out = dh_lsb(block, y)

# 提取数据后转换为整数
extracted_data = convert_to_int(out[:len(binary_data)])

# 计算误码率
ber, error_count = calculate_ber(data, out)

# 输出提取结果和误码率
print(f"原始数据: {data}")
print(f"提取数据: {extracted_data}")
print(f"误码率: {ber:.2%}, 错误数: {int(error_count)}")

# 额外的误码率计算
len_d = min(len(binary_data), len(out))
rate = np.sum(np.abs(np.array(out[:len_d]) - np.array(binary_data[:len_d]))) / len_d
error_num = len_d * rate
print(f"LSB: len: {len_d}， error rate: {rate}， error num: {error_num}")
