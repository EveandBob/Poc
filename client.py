from gmssl import sm3
import random
import socket
import json

word_list="abcdefghijklmnopqrstuvwxyz01234567879ABCDEFGHIJKLMNOPQRSTUVWXYZ"

p=183098279506203032585672015556481356895433099175829350516865574456251142212399509186098717532002836316029172717064905390726814136845921061314005168389646174640787069223302047006857766177211326533029585074534146652187191198182208648430186816735301842059779512924870617261542452069664198893445696097298817406257817222526359987413279224948628812641779106028508278318339377060293128585113611648639173879
n=p-1

s_key= random.randrange(1,n)



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

def set_n_p(name,password):
    print("账户："+name)
    print("密码：" + password)
    M_ = name.encode() + password.encode()
    e = sm3.sm3_hash(list(M_))
    k = e[0:2]
    h = pow_mod(int(e, 16), s_key, p)

    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口号
    s.connect((host, port))
    s.send(k.encode())
    s.recv(1024).decode()
    s.send(str(h).encode())
    temp=s.recv(1024).decode()
    if temp=="991199":
        print("账户密码安全")
        return 0
    else:
        hab = int(s.recv(3096).decode())
        hb_list=json.loads(temp)
        hb=pow_mod(hab,get_inverse(s_key,p),p)
        if hb in hb_list:
            print("账户密码不安全")
            return 0
        else:
            print("账户密码安全")
            return 0

set_n_p('MQSF6O3B','uXMjoN')

