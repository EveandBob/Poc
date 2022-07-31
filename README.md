#写在之前
项目中用到的函数简介：https://github.com/EveandBob/Introduction-to-some-functions-in-elliptic-curves-not-projects-

# 项目名称
实现Poc的网络交互实现

# 实验步骤
协议描述如下：

![Screenshot 2022-07-31 141133](https://user-images.githubusercontent.com/104854836/182012751-eed6c817-d6e1-4c9c-96ac-09283ed64ed5.jpg)


1.先写一个google服务器

2.先给google分配一个私钥b，然后随机生成一些用户名密码对

3.计算所有私钥密码对的k和h^b并制造一个{str(k),list(h)}

4.给cilent分配一个私钥a

5.然后计算k和h^a,并发送给google

6.google 收到后根据k查询到含有h^b的列表S

7.对发送过来的h^a进行b次乘方得到和h^ab，并将h^ab, 和S发送给cilent

8.cilent计算h^b后查询是否在S中，如果在说明密钥不安全

# 部分代码
1.cilent
```python
def set_n_p(name,password):
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
```
2.google
```python
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
```
#结果如下
![Screenshot 2022-07-31 142121](https://user-images.githubusercontent.com/104854836/182013024-4904b033-8a68-42bb-a5b2-e2aed0132a0d.jpg)
