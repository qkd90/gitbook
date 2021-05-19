#### Linux:root下的文件-anaconda-ks.cfg

一进入 CentOS7，输入 ls，却发现只有一个文件 anaconda-ks.cfg，所以就了解一下。

这个文件是在 Linux:root 下的。

据说，系统安装的时候生成的一个文件，通过这个文件可以修改成自动安装的脚本，用于自动安装同样配置的系统。

     auth --enableshadow --passalgo=sha512
    
    cdrom
    
    graphical
    
    firstboot --enable
    ignoredisk --only-use=sda
    
    keyboard --vckeymap=cn --xlayouts='cn'
    
    lang zh_CN.UTF-8
    
    network  --bootproto=dhcp --device=ens33 --onboot=off --ipv6=auto --no-activate
    network  --hostname=localhost.localdomain


    rootpw --iscrypted $6$rVL0xfcD/P.iK5lH$YItt8GnW6Zaa15QxD3hDcZmBv3SA7HOemRlF0TdwmW2yDNP7xMLlWpYOELYBjbOFDJU9UrvEv1/5JeyoTf6ya0
    
    services --enabled="chronyd"
    
    timezone Asia/Shanghai --isUtc
    user --name=yvan --password=$6$5psWNNldUM4.7BW0$4Re9lI/XLRTugvyPIoJwM3U6TIVjqfaAnzk/64yos13t75ZBG9KSEnvl/P4X/NgJMeBiyIez90g7bwOEWQu3B. --iscrypted --gecos="yvan"
    
    bootloader --append=" crashkernel=128M" --location=mbr --boot-drive=sda
    autopart --type=lvm
    
    clearpart --all --initlabel --drives=sda
    
    %packages
    @^minimal
    @core
    chrony
    kexec-tools
    
    %end
    
    %addon com_redhat_kdump --enable --reserve-mb='128M'
    
    %end
    
    %anaconda
    pwpolicy root --minlen=6 --minquality=1 --notstrict --nochanges --notempty
    pwpolicy user --minlen=6 --minquality=1 --notstrict --nochanges --emptyok
    pwpolicy luks --minlen=6 --minquality=1 --notstrict --nochanges --notempty
    %end 

注意看：

![](https://upload-images.jianshu.io/upload_images/3037211-21b6eebf13390745.png)

有个坑

这里是 off，表示安装 CentOS7 mini 时，未激活网络。这也表示一开始是没有网的。

