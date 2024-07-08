import time
import board
import busio
import wifi
import socketpool
import ipaddress
import avoid_obstacles
import line_tracking

from BPI_PicoW_S3_Car import Motor, Servo, I2CPCF8574Interface, LCD, LCD1602

speed = 40
info = ''
lcd_print = ''

# Connect WIFI
ssid, pw = ('BPI-PicoW-S3', '12345678')

wifi.radio.start_ap(ssid=ssid, password=pw)
time.sleep(1)
print(f'WiFi AP mode Started! SSID is {ssid}, IP={wifi.radio.ipv4_address_ap}')

servo = Servo()
motor = Motor()

servo.set_angle(board.GP7,0)

pool = socketpool.SocketPool(wifi.radio)

BUFF_SIZE = 1024


def WiFi_control():
    global info, lcd_print
    connections = []

    try:
        print("Waiting for connections...")
        with pool.socket(pool.AF_INET, pool.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', 8080))
            server_socket.listen(5)

            while True:
                server_socket.settimeout(0.1)
                try:
                    connection, address = server_socket.accept()
                    print("Connected by", address)
                    connections.append(connection)
                except OSError:
                    pass

                for connection in list(connections):
                    buf = bytearray(BUFF_SIZE)
                    try:
                        size = connection.recv_into(buf)
                    except OSError as e:
                        if e.errno == errno.EAGAIN:
                            continue
                        else:
                            raise

                    if not size:
                        connection.close()
                        connections.remove(connection)
                        break

                    data = buf[:size].decode()
                    print("Received data:", repr(data))

                    if data == "obstacle_avoidance":
                        try:
                            avoid_obstacles_mark = 0
                            while True:
                                avoid_obstacles.test()

                                buf = bytearray(BUFF_SIZE)
                                try:
                                    size = connection.recv_into(buf)
                                except OSError as e:
                                    if e.errno == errno.EAGAIN:
                                        continue
                                    else:
                                        raise

                                if not size:
                                    break

                                data = buf[:size].decode()
                                print("Received data:", repr(data))
                        except KeyboardInterrupt:
                            motor.motor_stop()
                    else:
                        direction_commands = [
                            "forward",
                            "backward",
                            "left",
                            "right",
                            "left_backward",
                            "right_forward",
                            "right_backward",
                            "left_forward",
                            "turn_left",
                            "turn_right"
                        ]

                        if data in direction_commands:
                            motor.move(1, data, speed)
                            if "turn_" in data:
                                time.sleep(0.5)
                                motor.motor_stop()

                            lcd_print = data.replace("_", " ")
                        else:
                            lcd_print = "stop"
                            motor.motor_stop()

                    if info != lcd_print:
                        lcd_putstr = LCD1602()
                        lcd_putstr.lcd.clear()
                        lcd_putstr.lcd.print(lcd_print)
                        info = lcd_print
                        lcd_putstr.lcd.close()

    except Exception as e:
        print("Exception occurred:", e)
    finally:
        for connection in connections:
            connection.close()

while True:
    try:
        WiFi_control()
    except Exception as e:
        print("Exception occurred in main loop:", e)
    time.sleep(0.05)
