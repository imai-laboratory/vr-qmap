# ソケットライブラリ取り込み
import socket

# サーバーIPとポート番号
IPADDR = "127.0.1.1"
# PORT = 32777

# IPADDR = "0.0.0.0"
PORT = 50051

# ソケット作成
sock = socket.socket(socket.AF_INET)
# サーバーへ接続
sock.connect((IPADDR, PORT))

# byte 形式でデータ送信
sock.send("hello".encode("utf-8"))