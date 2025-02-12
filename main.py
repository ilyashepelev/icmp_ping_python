import socket
import struct
import time


def send_ping(dest_ip):
    # Create a raw socket
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # Define the ICMP Echo Request packet
    icmp_packet = struct.pack('!BBHHH', 8, 0, 0, 0, 1) + b'pingdata'

    # Calculate the ICMP checksum
    checksum = 0
    for i in range(0, len(icmp_packet), 2):
        checksum += (icmp_packet[i] << 8) + icmp_packet[i + 1]

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF

    # 1 байт Тип сообщения (8 эхо запрос)
    # 1 байт Код сообщения (0)
    # 2 байта Контрольная сумма
    # 2 байта Идентификатор Задает идентификатор приложения, отправляющего эти данные. Для этого кода он просто использует номер идентификатора программы.
    # 2 байта Установка порядкового номера. Это поможет вам определить, о каком пакете запроса ICMP идет речь, если вы отправите несколько пакетов подряд. Это поможет вам сделать такие вещи, как расчет потери пакетов ICMP.
    icmp_packet = struct.pack('!BBHHH', 8, 0, checksum, 0, 1) + b'pingdata'

    # Send the ICMP packet
    icmp_socket.sendto(icmp_packet, (dest_ip, 0))

    # Receive the ICMP reply
    try:
        icmp_socket.settimeout(2.0)
        response, _ = icmp_socket.recvfrom(1024)
        icmp_type = struct.unpack('!B', response[20:21])[0]

        icmp_socket.close()

        # icmp_header = response[20:28]
        # typee, code, checksum, p_id, sequence = struct.unpack(
        #     'bbHHh', icmp_header)
        # print(typee)
        # print(code)
        # print(checksum)
        # print(p_id)
        # print(sequence)
        # Check if it's an Echo Reply (ICMP type 0)

        if icmp_type == 0:
            return True
    except socket.error:
        pass

    return False


def main():
    tStart = time.time()
    for i in range(1, 256):
        dest_ip = f'192.168.1.{i}'

        success = send_ping(dest_ip)

        if success:
            print(f'{i} Доступен')
        else:
            print(f'{i} Не доступен')
    tEnd = time.time()
    print(tEnd - tStart)

if __name__ == "__main__":
    main()
