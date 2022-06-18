import traceback
import json
import time
from datetime import datetime, timedelta

from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeSpotPriceHistoryRequest import DescribeSpotPriceHistoryRequest
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest

from ttlecs.utils.random_util import *
from ttlecs.core.context import Context
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest

URL_RESOURCE_DESC = "https://help.aliyun.com/document_detail/25378.html#xn4-n4-mn4-e4"
RUNNING_STATUS = 'Running'
CHECK_INTERVAL = 3
CHECK_TIMEOUT = 180


def time_format(target_time):
    _date = datetime.strptime(target_time, "%Y-%m-%dT%H:%MZ")
    local_time = _date + timedelta(hours=8)
    end_time = local_time.strftime("%Y-%m-%d %H:%M")
    return end_time


class Aliyun:
    def __init__(self, config_path):
        self.context = Context(config_path)
        self.access_id = self.context.get_config("specs", "access_id")
        self.access_secret = self.context.get_config("specs", "access_secret")
        self.region_id = self.context.get_config("specs", "region_id")

    def get_config(self, key, default_value=None):
        return self.context.get_config('specs', key, default_value)

    def desc_instance(self, tag_id='ttlecs', page_size=10, page_number=1):
        request = DescribeInstancesRequest()
        request.set_PageSize(page_size)
        request.set_PageNumber(page_number)

        tags = [{"Key": "source", "Value": tag_id}]
        request.set_Tags(tags)

        body = self._send_request(request, region=self.region_id)
        if body is not None:
            data = json.loads(body)
            if len(data['Instances']['Instance']) > 0:
                for instance in data['Instances']['Instance']:
                    public_ip = None
                    if instance['PublicIpAddress'] is not None and \
                            instance['PublicIpAddress']['IpAddress'] is not None and \
                            len(instance['PublicIpAddress']['IpAddress']) > 0:
                        public_ip = instance['PublicIpAddress']['IpAddress'][0]

                    print(
                        "[ID]:%s [IP]:%s [创建]:%s [到期]:%s" % (
                            instance['InstanceId'], public_ip, time_format(instance['StartTime']),
                            time_format(instance['AutoReleaseTime'])))
            else:
                print("当前没有存活实例")

    def dry_run_instance(self):
        return self.run_instance(True)

    def run_instance(self, dry_run=False):
        # 生成实例到期释放时间
        auto_release_hour = self.context.get_root_config('auto_release_hour')
        auto_release_at = None
        if auto_release_hour is not None:
            auto_release_at = datetime.datetime.utcnow() + datetime.timedelta(hours=auto_release_hour)
            auto_release_at = auto_release_at.isoformat(timespec='seconds') + "Z"

        request = RunInstancesRequest()
        password = self.get_config('password')
        if password == '<random>':
            password = strong_password()
            print("服务器密码:%s" % password)
        request.set_Password(password)
        request.set_DryRun(dry_run)
        request.set_AutoReleaseTime(auto_release_at)
        request.set_Amount(self.context.get_root_config('amount', 1))

        request.set_InstanceType(self.get_config('instance_type'))
        request.set_InstanceChargeType(self.get_config('instance_charge_type'))
        request.set_ImageId(self.get_config('image_id'))
        request.set_Period(self.get_config('period_hour'))
        request.set_PeriodUnit(self.get_config('period_unit', 'Hourly'))
        request.set_ZoneId(self.get_config('zone_id', 'random'))
        request.set_InternetChargeType(self.get_config('internet_charge_type'))
        request.set_VSwitchId(self.get_config('v_switch_id'))
        request.set_InstanceName(self.get_config('instance_name'))
        request.set_InternetMaxBandwidthOut(self.get_config('internet_max_bandwidth_out'))
        request.set_SpotStrategy(self.get_config('spot_strategy'))
        request.set_SystemDiskSize(self.get_config('system_disk_size'))
        request.set_SystemDiskCategory(self.get_config('system_disk_category', 'cloud_efficiency'))
        request.set_SecurityGroupId(self.get_config('security_group_id'))

        tags = [{"Key": "source", "Value": self.context.get_root_config("tag", "ttlecs")}]
        request.set_Tags(tags)

        body = self._send_request(request)
        if body is not None:
            data = json.loads(body)
            instance_ids = data['InstanceIdSets']['InstanceIdSet']
            print('服务器启动中，实例列表: {}'.format(', '.join(instance_ids)))
            print("--------------------")
            self._check_instance_status(instance_ids)

    def _check_instance_status(self, instance_ids):
        """
                每3秒中检查一次实例的状态，超时时间设为3分钟。
                :param instance_ids 需要检查的实例ID
                :return:
                """
        start = time.time()
        while True:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(json.dumps(instance_ids))
            response = self._send_request(request)
            data = json.loads(response)
            for instance in data['Instances']['Instance']:
                if RUNNING_STATUS in instance['Status']:
                    instance_ids.remove(instance['InstanceId'])
                    print("启动完成[%s] => IP:%s" % (
                        instance['InstanceId'],
                        instance['PublicIpAddress']['IpAddress']
                    ))

            if not instance_ids:
                break

            if time.time() - start > CHECK_TIMEOUT:
                print('Instances boot failed within {timeout}s: {ids}'
                      .format(timeout=CHECK_TIMEOUT, ids=', '.join(instance_ids)))
                break

            time.sleep(CHECK_INTERVAL)

    """
        获取实例列表
        - 默认只取第一个Region
    """

    def spots_resource(self):
        request = DescribeAvailableResourceRequest()
        request.set_accept_format('json')
        request.set_DestinationResource("InstanceType")
        request.set_InstanceChargeType("PostPaid")
        request.set_SpotStrategy("SpotAsPriceGo")

        print("规格说明")
        print("  %s" % self.URL_RESOURCE_DESC)

        response = self._send_request(request)
        info = json.loads(str(response, encoding='utf-8'))
        availableResources = \
            info['AvailableZones']['AvailableZone'][0]['AvailableResources']['AvailableResource'][0][
                'SupportedResources']['SupportedResource']
        print("库存规格与价格(%s):" % self.region_id)

        min_price_item = None
        min_price_item_price = 0
        for item in availableResources:
            if item['Status'] == 'Available' and item['StatusCategory'] == 'WithStock':
                itemType = item['Value']
                originPrice, SpotPrice = self._spots_prices(itemType)
                print("  %s: ￥%s -> ￥%s" % (itemType, originPrice, SpotPrice))
                if min_price_item is None or min_price_item_price > SpotPrice:
                    min_price_item = itemType
                    min_price_item_price = SpotPrice
                time.sleep(0.01)

    """
        获取实例历史价格
    """

    def _spots_prices(self, instance_type):
        request = DescribeSpotPriceHistoryRequest()
        request.set_accept_format('json')

        request.set_NetworkType("vpc")
        request.set_InstanceType(instance_type)
        request.set_OSType("linux")

        response = self._send_request(request)
        info = json.loads(str(response, encoding='utf-8'))
        item = info['SpotPrices']['SpotPriceType'][-1]
        return float(item['OriginPrice']), float(item['SpotPrice'])

    def _send_request(self, request, region=None):
        try:
            region = self.region_id if region is None else region
            client = AcsClient(self.access_id,
                               self.access_secret,
                               region)

            response = client.do_action_with_exception(request)
            return response
        except ClientException as e:
            print('失败. 未连接到阿里云服务器'
                  ' Code: {code}, Message: {msg}'
                  .format(code=e.error_code, msg=e.message))
        except ServerException as e:
            if e.error_code == "DryRunOperation":
                print("参数校验成功，可正确创建实例")
            else:
                print('失败. Aliyun 错误码.'
                      ' Code: {code}, Message: {msg}'
                      .format(code=e.error_code, msg=e.message))
        except Exception:
            print('未知系统异常')
            print(traceback.format_exc())
        return None


if __name__ == '__main__':
    pass
    # Aliyun().desc_instance(region_id='cn-hongkong', tag_id='ttlecs')
    # Aliyun().run_instance()
    # Aliyun()._check_instance_status(["i-j6catsgyxin6pswtg8xi"])
    # Aliyun().spots_resource()
    # print(Aliyun()._spots_prices('ecs.e4.small'))
