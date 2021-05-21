#基于UDP的数据转发
#客户端发送给到服务端A，服务端A转发到服务端B,输入'quit'时停止
#本地转发

#客户端

import socket
import time

host = '127.0.0.1'  #本地地址
port = 3333  #连接服务端A的端口号
Clnt_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #创建基于UDP的套接字
ServA_addr = (host, port)

while True:
    start = time.time() #标记开始时间
    print(time.strftime('%Y-%m%d %H:%M:%S', time.localtime(start)))  #输出当前时间
    datas = input('请输入传输内容：')
    Clnt_socket.sendto(datas.encode('utf-8'), ServA_addr)  #转为二进制编码形式发送数据
    now = time.time()
    run_time = (now - start)/100.0  #运行时间
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
    print('run_time：%f seconds \n'%run_time)
    if datas == 'quit':
        break   #输入quit是停止
    
    
    
#服务端A

import socket
import time

#服务端A的地址及端口
hostA = '127.0.0.1'
portA = 3333  #此端口号与客户端一致
ServA_addr = (hostA, portA)
ServA_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
#服务端B的地址及端口
hostB = '127.0.0.1'
portB = 5555 #与服务端C的端口号相同
ServB_addr = (hostB, portB)

ServA_socket.bind(ServA_addr)  #将A套接字绑定到服务端A上，接收客户端的消息
ServA_socket.settimeout(100)  #设置time out 时间为100s

while True:
    try:
        now = time.time()
        datas , Clntaddr= ServA_socket.recvfrom(1024)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('服务端A:客户端 %s 发来信息：%s \n'%(Clntaddr, datas.decode('utf-8')))  #解码输出
        
        ServA_socket.sendto(datas, ServB_addr)  #转发给服务端B
        if datas == b'quit':  #传输quit时停止传输
            break
    except socket.timeout:
        print('time out!')  #停滞每一百秒提示一次time out


#服务端B

import socket
import time

#服务端B的地址及端口
hostB = '127.0.0.1'
portB = 5555
ServB_addr = (hostB, portB)
ServB_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServB_socket.bind(ServB_addr)  #将B套接字绑定到服务端B上,接收A的消息

while True:
    now = time.time()
    datas , ServA_addr = ServB_socket.recvfrom(1024)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('服务端B:服务端A %s 发来信息：%s \n'%(ServA_addr, datas.decode('utf-8')))  #解码输出
        
    if datas == b'quit':  #传输quit时停止传输
         break
    
    
    

