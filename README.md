# TTLECS
基于云服务（阿里云等）创建带有TTL（Time To Alive）能力的服务器实例，通过小时级的生命周期控制，降低硬件成本开销。本项目封装了云服务的API细节、提供创建实例后的预置命令下发，提供了更易于被集成和运维的命令行工具。

## 产品能力
1. 支持通过Yaml定义ECS购买模版，并支持到期自动释放
2. 支持实例开启后执行自定义命令、运行docker容器
3. 支持一键询价、查询最低价（阿里云抢占式实例）
4. 支持标准命令行一键购买，便于与Crontab集成

## 使用场景
1. 网络加速场景，仅在办公时间段开通代理服务  
2. 大数据计算场景，仅在夜间扩容大数据集群实例
3. 有明显业务高峰的场景，仅在高峰时间扩容业务服务器
4. 成本对比
    * 数据来自阿里云香港Region（ 2022.6.5 ）
    * 当前阿里云抢占式实例有优惠，优惠期结束后的价格参考常规价
   
| 场景    | 规格                                                      | 包月成本           | 使用时长(月) | 资源成本(月)                                 | 降幅百分比                       |
|-------|---------------------------------------------------------|----------------|---------|-----------------------------------------|-----------------------------|
| 网络加速  | 规格：ecs.xn4.small<br/>CPU：1c<br/>内存：1g<br/>系统盘：40g<br/>带宽上限：5M<br/>按使用流量计费 | ¥73.97+￥1.0/GB | 8h*30d  | 优惠期：￥6.96+￥1.0/GB<br/>常规价：￥30.0+￥1.0/GB | 优惠期：90.59%<br/>常规价：54.98%   |
| 大数据计算 | 规格：ecs.g6.8xlarge<br/>CPU：32c<br/>内存：128g<br/>系统盘：200g  | ￥6777.20       | 8h*30d  | 优惠期：￥1353.36<br/>常规价：￥3441.6            | 优惠期：80.03%<br/>常规价：49.21%   |
| 业务服务  | 规格：ecs.g7.xlarge<br/>CPU：4c<br/>内存：16g<br/>系统盘：100g     | ￥1040.15       | 2h*30d  | 优惠期：￥27.78<br/>常规价：￥109.2               | 优惠期：97.32%    <br/>常规价：89.50% |


## 快速开始
1. 安装 ttlecs
```
$ pip3 install ttlecs
```
2. 生成配置文件
```
$ ttlecs template > ~/.ttlecs/config.yaml
````
3. 生成服务器实例 
```
$ ttlecs dayrun --config ~/.ttlecs/config.yaml
> 参数校验成功，可正确创建实例

$ ttlecs run --config ~/.ttlecs/config.yaml
>  实例创建中，列表: i-j6cgzuz5omckbahcpdfj
>  --------------------
>  正在启动实例
>  [i-j6cgzuz5omckbahcpdfj] 已启动, IP:['47.243.40.83']
>  --------------------
>  开始执行命令:yum install -y docker; service docker start; docker pull shadowsocks/shadowsocks-libev; docker run -e PASSWORD=pwd8388 -p8388:8388 -p8388:8388/udp -d shadowsocks/shadowsocks-libev
>  正在获取命令结果
>  [i-j6cgzuz5omckbahcpdfj] 命令执行完成, 执行结果:Success
```
5. 查看实例列表
```
$ ttlecs list --config ~/.ttlecs/config.yaml
> [ID]:i-j6cgzuz5omcjwziab0eg [IP]:47.243.244.73 [创建]:2022-06-18 14:01 [到期]:2022-06-18 15:00
```


## 其他文档
[配置项说明](docs/Config.md)

[常见问题](docs/QA.md)

## License
* MIT License
