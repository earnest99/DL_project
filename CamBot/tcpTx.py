import cv2
import socket
import struct
import pickle
import time


def send_video():
    # 카메라 설정
    cap = cv2.VideoCapture(0)  # 카메라 장치 번호 설정 (일반적으로 0)

    while True:
        try:
            # 소켓 생성 및 연결
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("192.168.0.12", 9020))  # 서버 IP 주소와 포트 번호 설정
            server_socket.listen(1)  # 클라이언트 연결 대기

            print("Waiting for connection...")
            conn, addr = server_socket.accept()  # 클라이언트 연결 수락
            print("Connected to:", addr)

            while True:
                ret, frame = cap.read()  # 프레임 캡처
                if not ret:
                    break

                # JPEG로 인코딩
                _, buffer = cv2.imencode(".jpg", frame)
                data = pickle.dumps(buffer)

                # 데이터 크기 전송
                size = struct.pack("L", len(data))
                conn.sendall(size)

                # 데이터 전송
                conn.sendall(data)
                time.sleep(0.05)

            # 소켓 종료
            conn.close()
            server_socket.close()

        except Exception as e:
            print("Error:", e)
            time.sleep(1)  # 1초 대기 후 다시 연결 시도


if __name__ == "__main__":
    send_video()
