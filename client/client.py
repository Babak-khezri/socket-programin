from cgitb import text
import re
import socket
import tkinter as tk

IP = '127.0.0.1'
PORT = 5000

FORMAT = 'utf-8'
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def get_request(entry,response):
    request = entry.get()
    allow_requests = ['get', 'put', 'ls', 'quit']
    request = request.split(" ")
    if request[0] in allow_requests:
        entry.delete(0, tk.END)
        client.send(request[0].lower().encode(FORMAT))
        request_handler(request,response)
    else:
        print("not allowed")


def graphic_setup():

    def Keyboard_Controll(event):
        key = event.keysym
        if key == 'Return':
            get_request(entry,T)
    
    def font(size):
        return ("Times", size, 'bold')

    win = tk.Tk()
    win.resizable(False, False)  # Lock change size
    win.title('Typing speed')
    win['background'] = '#77c9d4'  # Change main background
    tk.Label(win, text='SOCKET PROJECT', font=font(20),bg='#77c9d4').grid(row=0, column=0, columnspan=10)
    entry = tk.Entry(win)
    entry.config(font=font(16), bg="#57bc90")
    entry.grid(row=3, column=0, columnspan=1)
    win.bind('<Key>',Keyboard_Controll)
    send_btn = tk.Button(text='Send', font=font(13), command=lambda: get_request(entry,T), bg="#015249")
    send_btn.grid(row=3, column=1, columnspan=1)
    tk.Label(win, text='='*36, font=font(14), bg='#77c9d4').grid(row=4, column=0, columnspan=10)
    T = tk.Label(win, text="",width=44, height=10, font=font(12))
    T.grid(row=5, columnspan=2)
    tk.mainloop()


def request_handler(request,response):
    text_response = "request => {}\n\n".format(request[0])
    if request[0].lower() == "put":
        try:
            filename = request[1]
            file = open(filename, 'r')
            data = file.read()
            file.close()
            client.send(filename.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
            client.send(data.encode(FORMAT))
        except Exception:
            print("File not found!")
            return

    elif request[0].lower() == 'get':
        filename = request[1]
        client.send(filename.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")
        if 'not' not in msg:
            file = open(filename, 'w')
            data = client.recv(SIZE).decode(FORMAT)
            file.write(data)
            file.close()
    elif request[0].lower() == 'ls':
        list_of_files = client.recv(SIZE).decode(FORMAT)
        text_response = text_response + 'list of files in server : \n' + list_of_files
        print(list_of_files)
    response.config(text=text_response)
    response.grid(row=5, columnspan=2)



if __name__ == '__main__':
    graphic_setup()
