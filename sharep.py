import subprocess as sp
import socket as sk
import time
from win32 import win32gui
import psutil
from win32 import win32process
from pynput.keyboard import Key, Listener, Controller
import multiprocessing
import os

conn = 0

def proces():
    i=0
    kut = ""
    #while i <= 1:

    time.sleep(1)

    w=win32gui

    w.GetWindowText (w.GetForegroundWindow())

    pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())

    kut = psutil.Process(pid[-1]).name()
    print(kut)
    if(kut == "vlc.exe"):
        listen()
    else:
        proces()
def ket(key):
    global conn
    keyb = Controller()
    #print(key)
    if key == Key.space :
        conn.send(b"#&#")
        print("space pressed")
    proces()
def listen():
    with Listener(on_press=ket) as listener:
        listener.join()

pi = '''
For more information
open cmd if in windows and type ipconfig to get your ip address connected to your wifi or ethernet 
open terminal in linux and type ifconfig to get your ip address connected to your wifi or ethernet
'''

def client():
         print(pi)
         ip = input("Enter Your IP Address:")
                
         port  = int(input("Port Number:"))

         csk = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
         csk.connect((ip, port))

         pc_name = str(sk.gethostname()) + " connected :)"
         csk.send(pc_name.encode('utf-8'))

         file_name = csk.recv(20).decode('utf-8')
         print(file_name)

         f = open(file_name, 'wb')

         while True :
                data = csk.recv(999999)
                print("recieved : ",round(len(data) / 1024, 2), " KB")
                if data[len(data)-3:] == b"#&#" :
                    break
                f.write(data)
                    
                  

         print('Data Recieved')
         f.close()
         csk.send("Thank you".encode('utf-8'))
         os.popen("start "+file_name)
         keyb = Controller()
         while(1):
             data = csk.recv(5).decode('utf-8')
             if(data == "#&#"):
                keyb.press(" ")
                keyb.release(" ")
                print("space pressed")
         csk.close()

def server():
         global conn
         print("You are the host. First Make File ready ")
         filename = input("Enter Complete File Name (Note* :File should be present in this folder) : ")
         print(pi)
         ip = input("Enter Your IP Address:")
         try :
                  f = open(filename, 'rb').read()
                  print("Processing ... ")
                  print("File is ready to send")
                    
                  ssk = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                  port  = int(input("Port Number:"))
                  ssk.bind((ip, port))
                  print("Socket Created")
                  ssk.listen(1)
                  conn, adrr = ssk.accept()
                  print('Connection from : ',str(adrr))
                  pc_name = conn.recv(1024).decode('utf-8')
                  print(pc_name)
                  
                  print("sending data ...")

                  conn.send(filename.encode('utf-8'))
                  time.sleep(0.6)
                  conn.send(f)
                  conn.send(b"#&#")
                  tk = conn.recv(1024)
                  print(tk.decode('utf-8'))
                  #ssk.close()
                  os.popen("start "+filename)
                  proces()
                  ssk.close()
         except Exception as e:
                  print(e)
while(1):
        i = input("enter se for server and cl for client or close for exit:")
        if(i=="se"):
                server()
        elif(i=="cl"):
                client()
        elif(i=="close"):
                print("Bye")
        else:
                print("wrong option")
