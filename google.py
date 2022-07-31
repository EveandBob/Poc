from gmssl import sm3
import random
import socket

word_list="abcdefghijklmnopqrstuvwxyz01234567879ABCDEFGHIJKLMNOPQRSTUVWXYZ"

p=183098279506203032585672015556481356895433099175829350516865574456251142212399509186098717532002836316029172717064905390726814136845921061314005168389646174640787069223302047006857766177211326533029585074534146652187191198182208648430186816735301842059779512924870617261542452069664198893445696097298817406257817222526359987413279224948628812641779106028508278318339377060293128585113611648639173879
n=p-1

u_list=[]
p_list=[]

s_key= random.randrange(1,n)

def get_bitsize(num):
    len=0
    while num/256:
        len+=1
        num=int (num/256)
    return len

def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num),byteorder='big', signed=False)
def bytes_to_int(bytes):
    return int.from_bytes(bytes,byteorder='big')

def pow_mod(a, b, n):
    a = a % n
    ans = 1
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while b != 0:
        if b & 1:
            ans = (ans * a) % n
        b >>= 1
        a = (a * a) % n
    return ans


def XGCD(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x, y, d = XGCD(b, a % b)
        return y, (x - (a // b) * y), d


def get_inverse(a, b):
    return XGCD(a, b)[0] % b

def get_name_pass():
    for i in range(100):
        namelen = random.randrange(6, 10)
        passwordlen = random.randrange(6, 10)
        name = ''
        password = ''
        for j in range(namelen):
            name += word_list[random.randrange(0, 62)]
        for j in range(passwordlen):
            password += word_list[random.randrange(0, 62)]
        u_list.append(name)
        p_list.append(password)

dic={}
def get_K_h():
    for i in range(100):
        M_ = u_list[i].encode() + p_list[i].encode()
        e = sm3.sm3_hash(list(M_))
        k=e[0:2]
        h=pow_mod(int(e,16),s_key,p)
        dic.setdefault(k,[]).append(h)





if __name__=="__main__":
    get_name_pass()
    get_K_h()
    print("ok")
    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    s.bind((host, port))  # 绑定端口
    s.listen(5)  # 等待客户端连接
    c, addr = s.accept()
    k = c.recv(1024).decode()
    c.send("0".encode())
    ha=int(c.recv(1024).decode())
    hab=pow_mod(ha,s_key,p)
    a=list(dic.keys())
    print(a)
    print(type(a))
    if k in list(dic.keys()):
        c.send(str(dic[k]).encode())
        c.send(str(hab).encode())
    else:
        c.send("991199".encode())