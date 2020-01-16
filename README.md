# autocronjob
# 欢迎大家随时提bug

### 依赖

```
yum -y install wget gcc epel-release git mysql-devel
pip install redis
yum -y install python36 python36-devel
```

### 虚拟环境

```
cd /opt
python3.6 -m venv py3
```

### 自动载入虚拟环境

```
# git clone前，将server/client的主机公钥放在gitlab上
git clone  git@gitlab.hobot.cc:ptd/ap/dlp/autocronjob.git
git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc
source ~/.bashrc
echo "source /opt/py3/bin/activate" > /opt/autocronjob/.env
```

### 项目下载和安装

```
cd  /opt/autocronjob/
cd ssh_key/
chmod 600 id_rsa
cd ..
pip install --upgrade pip setuptools
pip install -r requirements.txt
cd apps/utils/django-celery-beat-master/
python  setup.py  install
```

### 创建目录
```
mkdir  /data/logs/web/  -p
mkdir /data/logs/{nginx,celery}
mkdir /data/pid/
mkdir /etc/conf.d/

chmod 755 /data/logs/ -R
chmod 755 /data/pid/
```

### 配置autocronjob.conf

填写上mysql和redis相关信息，没有的不需要填写

### 生成表文件

```
cd ../../../
python manage.py makemigrations
python manage.py migrate
```

### 配置admin初始密码

```
python  createsuperuser.py
```

### 安装和配置supervisor

```
yum install -y supervisor
systemctl enable supervisord
systemctl start supervisord
cp -ra  supervisord.conf /etc/supervisord.conf
supervisorctl reread
supervisorctl update
```

### 启动nginx

```
cp -ra nginx.conf /etc/nginx/nginx.conf
nginx -s reload
```

## server
### celeryd 和 celerybeat

```
cp -ra server_celery /etc/conf.d
mv /etc/conf.d/server_celery /etc/conf.d/celery
cp -ra celery.service celerybeat.service /etc/systemd/system/
chmod 755 /etc/systemd/system/celery.service /etc/systemd/system/celerybeat.service 

systemctl daemon-reload
systemctl start celery
systemctl start celerybeat
```

## client端

```
cat /opt/autocronjob/ssh_key/id_rsa.pub  >> /root/.ssh/authorized_keys
```

>注意：
调度器的日志，涉及到autocronjob 到client worker主机名的解析

```
cp -ra client_celery /etc/conf.d
mv /etc/conf.d/client_celery /etc/conf.d/celery
cp -ra celery.service /etc/systemd/system/
chmod 755 /etc/systemd/system/celery.service
systemctl daemon-reload
systemctl start celery
```
