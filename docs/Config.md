# 配置文件说明
### 配置项说明
* vendor:：ECS供应商，可选：aliyun
* version：配置文件版本号，可选：1
* amount：购买ECS的数量，整数型，例如 1
* auto_release_hour：ECS自动释放的时间，整数型，单位小时，例如 1
* tag：ECS上的标签，用于list子命令时筛选ECS，字符串，默认 ttlecs
* commands：ECS启动后要自动执行的命令
  * enable：是否启用命令执行，可选：True,False
  * content: 待执行的命令内容
* specs：购买ECS的规格
  * access_id
  * access_secret
  * region_id
  * instance_type
  * image_id
  * password
  * internet_max_bandwidth_out
  * system_disk_size
  * period_hour
  * period_unit
  * zone_id
  * system_disk_category
  * instance_charge_type
  * internet_charge_type
  * v_switch_id
  * instance_name
  * spot_strategy
  * security_group_id

specs 中的配置项可直接参与云厂商的配置文档，TTLECS只做透传
* 阿里云：https://help.aliyun.com/document_detail/63440.html
### 配置项范例
网络代理 (抢占式实例, 按流量付费, 适用于无视频的场景)
```
vendor: aliyun
version: 1
amount: 1
auto_release_hour: 1
tag: ttlecs
commands:
    enable: True
    content: >
        yum install -y docker;
        service docker start;
        docker pull shadowsocks/shadowsocks-libev;
        docker run -e PASSWORD=pwd8388 -p8388:8388 -p8388:8388/udp -d shadowsocks/shadowsocks-libev
specs:
    access_id: <Your Access ID>
    access_secret: <Your Access Secret>
    password: <Your ECS Password>
    v_switch_id: <Your ECS Switch ID>
    security_group_id: sg-j6c4o1iw43la0ze0uxja
    region_id: cn-hongkong
    instance_type: ecs.xn4.small
    image_id: centos_7_9_x64_20G_alibase_20220426.vhd
    internet_max_bandwidth_out: 5
    system_disk_size: 40
    period_hour: 1
    period_unit: Hourly
    zone_id: random
    system_disk_category: cloud_efficiency
    instance_charge_type: PostPaid
    internet_charge_type: PayByTraffic
    instance_name: TTLECS
    spot_strategy: SpotAsPriceGo
```