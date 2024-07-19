import time
import struct
import sysv_ipc

# 共有メモリのキー (NTP0に対応)
SHM_KEY = 0x4E545030

# 構造体のフォーマット
STRUCT_FORMAT = "iiqiqi4i2I8i"
STRUCT_SIZE = struct.calcsize(STRUCT_FORMAT)

def read_from_shared_memory():
    try:
        # 共有メモリを取得
        shm = sysv_ipc.SharedMemory(SHM_KEY)
    except sysv_ipc.ExistentialError:
        print("共有メモリが存在しません。")
        return

    while True:
        # 共有メモリからデータを読み取り
        data = shm.read(STRUCT_SIZE)
        if len(data) != STRUCT_SIZE:
            print(f"データのサイズが期待されるサイズと一致しません: {len(data)}バイト")
            time.sleep(1)
            continue

        unpacked_data = struct.unpack(STRUCT_FORMAT, data)

        # データの解釈
        clockTimeStampSec = unpacked_data[2]
        clockTimeStampUSec = unpacked_data[3]
        receiveTimeStampSec = unpacked_data[4]
        receiveTimeStampUSec = unpacked_data[5]
        leap = unpacked_data[6]
        precision = unpacked_data[7]
        valid = unpacked_data[9]

        ntp_time = clockTimeStampSec + (clockTimeStampUSec / 1e6)
        local_time = receiveTimeStampSec + (receiveTimeStampUSec / 1e6)

        print(f"共有メモリから読み取ったNTP時刻: {time.ctime(ntp_time)}")
        print(f"Leap indicator: {leap}, Precision: {precision}")
        print(f"ローカル受信時刻: {time.ctime(local_time)}")

        time.sleep(1)  # 1秒ごとに更新

if __name__ == "__main__":
    read_from_shared_memory()
