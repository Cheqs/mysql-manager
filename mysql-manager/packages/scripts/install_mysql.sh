#!/bin/bash
#Time 2018-05-10
#Author xucl

PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PREFIX=/usr/local
SYSTEM=`uname -a |awk '{print $13}'`
USER=mysql
BASEDIR=${PREFIX}/mysql
SHELL=/sbin/nologin

PORT=$1
POOLSIZE=$2
VERSION=$3
USERNAME=$4
PASSWORD=$5

DATADIR=/data/mysql/mysql${PORT}
FILENAME=mysql-${VERSION}-linux-glibc2.12-${SYSTEM}

#解压MySQL文件
function step_unzip()
{
if [ -d "/usr/local/mysql" ];then
    echo "文件已存在" >> /tmp/install.log
else
    tar -xvzf /usr/local/src/${FILENAME}.tar.gz -C /opt/ &>/dev/null
    ln -s /opt/mysql-5.7.23-linux-glibc2.12-x86_64 /usr/local/mysql
    echo "文件解压成功" >> /tmp/install.log
fi
}

#创建用户
function step_user()
{
if [ `cat /etc/passwd |grep mysql|wc -l` == "0" ];then
        groupadd ${USER}
        useradd -s ${SHELL} -g ${USER} ${USER}
fi
}

#创建目录
function step_filedir()
{
mkdir -p ${DATADIR}/data
if [ $? -eq 0 ];then
  echo "data 目录创建成功"
else
  echo "data 目录创建失败"
  exit 2
fi

mkdir -p ${DATADIR}/logs
if [ $? -eq 0 ];then
  echo "logs 目录创建成功"
else
  echo "logs 目录创建失败"
  exit 2
fi

mkdir -p ${DATADIR}/tmp
if [ $? -eq 0 ];then
  echo "tmp 目录创建成功"
else
  echo "tmp 目录创建失败"
  exit 2
fi
}

#生成my.cnf
function step_mycnf()
{
cp -r /usr/local/src/temp.cnf my${PORT}.cnf
SERVERID=$RANDOM
sed -i "s/POOLSIZE/${POOLSIZE}/g" my${PORT}.cnf
sed -i "s/PORT/${PORT}/g" my${PORT}.cnf
sed -i "s/SERVERID/${SERVERID}/g" my${PORT}.cnf
mv my${PORT}.cnf ${DATADIR}/my${PORT}.cnf
echo "配置文件已生成"
}

#文件夹授权
function step_chown()
{
chown -R ${USER}:${USER} ${BASEDIR}
chown -R ${USER}:${USER} /opt/${FILENAME}
chown -R ${USER}:${USER} ${DATADIR}
echo "授权成功"
}

function step_yum()
{
yum install libaio numactl -y
}

#初始化MySQL
function init_mysql()
{
echo "数据库初始化中..."
${BASEDIR}/bin/mysqld  --defaults-file=${DATADIR}/my${PORT}.cnf --user=mysql --initialize-insecure
if [ $? -eq 0 ]; then
  echo "初始化成功">> /tmp/install.log
  ${BASEDIR}/bin/mysqld  --defaults-file=${DATADIR}/my${PORT}.cnf --user=mysql & &>/dev/null
else
  echo "初始化失败">>/tmp/install.log && exit 1
fi
}

function create_user()
{
#更改密码
sleep 10
/usr/local/mysql/bin/mysql -uroot -S /tmp/mysql${PORT}.sock -e "alter user user() identified by 'Lpx41JL1YqTANPg7';flush privileges;"  --connect-expired-password
#创建复制用户
/usr/local/mysql/bin/mysql -uroot -p"Lpx41JL1YqTANPg7" -S /tmp/mysql${PORT}.sock -e "grant replication slave on *.* to repl@'%' identified by 'kEQ5OzJno9gFXD3K';"
#创建监控用户
/usr/local/mysql/bin/mysql -uroot -p"Lpx41JL1YqTANPg7" -S /tmp/mysql${PORT}.sock -e "GRANT REPLICATION CLIENT,PROCESS,SELECT ON *.* TO 'zdbmonitor'@'localhost' identified by 'OWxFpcVEF39BeJD8'"
#创建远程管理账号
/usr/local/mysql/bin/mysql -uroot -p"Lpx41JL1YqTANPg7" -S /tmp/mysql${PORT}.sock -e "grant all privileges on *.* to ${USERNAME}@'%' identified by '${PASSWORD}' with grant option;flush privileges;"
}

echo "step1:解压文件"
step_unzip
echo "step2:创建账号"
step_user
echo "step3:创建目录"
step_filedir
echo "step4:生成配置文件"
step_mycnf
echo "step5:文件夹授权"
step_chown
echo "step6:yum依赖包安装"
step_yum
echo "step7:mysql初始化"
init_mysql
echo "step8:创建系统用户"
create_user