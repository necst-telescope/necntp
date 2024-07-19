import time
import ntplib
import struct
import sysv_ipc

# 共有メモリのキー (NTP0に対応)
SHM_KEY = 0x4E545030

# 構造体のフォーマット
STRUCT_FORMAT = "iiqiqi4i2I8i"

def get_ntp_time(ntp_server="pool.ntp.org"):
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server, version=3)
        return response, time.time()
    except:
        return None, None

def write_to_shared_memory():
    try:
        # 共有メモリを作成または取得
        shm = sysv_ipc.SharedMemory(SHM_KEY, sysv_ipc.IPC_CREAT | 0o666, size=struct.calcsize(STRUCT_FORMAT))
    except sysv_ipc.ExistentialError:
        shm = sysv_ipc.SharedMemory(SHM_KEY)

    while True:
        ntp_response, local_time = get_ntp_time()
        if ntp_response is None:
            print("NTP時刻の取得に失敗しました。再試行します...")
            time.sleep(1)
            continue

        ntp_time = ntp_response.tx_time
        ntp_sec, ntp_frac = divmod(ntp_time, 1)
        local_sec, local_frac = divmod(local_time, 1)

        # データを準備
        data = struct.pack(STRUCT_FORMAT,
            0,  # mode
            0,  # count
            int(ntp_sec),  # clockTimeStampSec
            int(ntp_frac * 1e6),  # clockTimeStampUSec
            int(local_sec),  # receiveTimeStampSec
            int(local_frac * 1e6),  # receiveTimeStampUSec
            ntp_response.leap,  # leap
            ntp_response.precision,  # precision
            0,  # nsamples
            1,  # valid
            0,  # clockTimeStampNSec (未使用)
            0,  # receiveTimeStampNSec (未使用)
            0, 0, 0, 0, 0, 0, 0, 0  # dummy[8]
        )

        # 共有メモリに書き込み
        shm.write(data)

        print(f"NTP時刻を共有メモリに書き込みました: {time.ctime(ntp_sec)}")
        print(f"Leap indicator: {ntp_response.leap}, Precision: {ntp_response.precision}")
        time.sleep(1)  # 1秒ごとに更新

if __name__ == "__main__":
    write_to_shared_memory()
