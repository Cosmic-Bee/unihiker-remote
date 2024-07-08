import socket
import time
from unihiker import GUI
from pinpong.board import Board

server_ip = '192.168.4.1'
server_port = 8080

def send_command(s, command):
    try:
        s.sendall(command.encode())
        print(f"Sent: {command.strip()}")
    except (BrokenPipeError, ConnectionResetError, OSError):
        print("Connection lost. Reconnecting...")
        s.close()
        s = connect_to_server()
        s.sendall(command.encode())
    return s

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            print("Connected to server")
            return s
        except (ConnectionRefusedError, OSError) as e:
            if isinstance(e, OSError) and e.errno == 101:
                print("Network is unreachable. Retrying in 5 seconds...")
            else:
                print("Connection failed. Retrying in 5 seconds...")
            s.close()
            time.sleep(5)

def initialize_gui():
    gui = GUI()
    gui.draw_image(x=0, y=0, w=320, h=320, image="images/remote.png")
    return gui

def draw_buttons(gui):
    commands = {
        'turn_left': 'images/arrows-turn-left.png',
        'turn_right': 'images/arrows-turn-right.png',
        'left_forward': 'images/arrows-top-left.png',
        'forward': 'images/arrows-top.png',
        'right_forward': 'images/arrows-top-right.png',
        'left': 'images/arrows-left.png',
        'stop': 'images/stop.png',
        'right': 'images/arrows-right.png',
        'left_backward': 'images/arrows-bottom-left.png',
        'backward': 'images/arrows-bottom.png',
        'right_backward': 'images/arrows-bottom-right.png',
        'obstacle_avoidance': 'images/obstacle-avoid.png'
    }

    button_positions = [
        ('turn_left', 30, 80), ('obstacle_avoidance', 90, 80), ('turn_right', 150, 80),
        ('left_forward', 30, 140), ('forward', 90, 140), ('right_forward', 150, 140),
        ('left', 30, 200), ('stop', 90, 200), ('right', 150, 200),
        ('left_backward', 30, 260), ('backward', 90, 260), ('right_backward', 150, 260)
    ]

    for command, x, y in button_positions:
        gui.draw_image(x=x, y=y, w=60, h=60, image=commands[command], onclick=lambda cmd=command: button_click(cmd))

def button_click(command):
    global connection_socket
    connection_socket = send_command(connection_socket, command)

Board("UNIHIKER").begin()
gui = initialize_gui()

connection_socket = connect_to_server()

gui.draw_image(x=0, y=0, w=320, h=320, image="images/background.png")
draw_buttons(gui)

while True:
    time.sleep(1)
