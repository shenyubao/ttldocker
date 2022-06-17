template_aliyun = """vendor: aliyun
version: 1
amount: 1
auto_release_hour: 1
tag: ttlecs
specs:
    access_id: <Your Access ID Here>
    access_secret: <Your Access Secret Here>
    password: <Your Password Here>
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
    v_switch_id: vsw-j6cvylyohfwc073u9j3sg
    instance_name: None
    spot_strategy: SpotAsPriceGo
    security_group_id: sg-j6c4o1iw43la0ze0uxja
"""