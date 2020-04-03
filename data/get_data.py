import pandas as pd
import numpy as np
import requests


class Data:
    # 高德地图Key
    DefaultKey = "343a06bc22f6c6026eda2f38626c900e"

    # 步行路径规划URL前缀
    ReqURLForWalk = "http://restapi.amap.com/v3/direction/walking?origin="

    # 骑行路径规划URL前缀
    ReqURLForBicycle = "http://restapi.amap.com/v4/direction/bicycling?origin="

    # 地理编码：通过地址获取坐标URL前缀
    ReqURLForGeo = "https://restapi.amap.com/v3/geocode/geo?address="

    # 逆地理编码：通过坐标获取地址URL前缀
    ReqURLForReGeo = "https://restapi.amap.com/v3/geocode/regeo?output=JSON&radius=1000" \
                     "&extensions=all&location="

    # 测量距离：通过坐标获取出发点与目的地URL前缀
    DistanceForGeo = "https://restapi.amap.com/v3/distance?output=JSON&origin="

    # 城市名:城市名可改为任何有效地址
    # cities = np.array(pd.read_table('cities.txt'))

    # 城市数量
    city_num = 0

    # 城市坐标：确保程序的快速运行，本地已保存城市坐标
    # locations = np.array(pd.read_table('locations', header=None))

    # 路网:确保程序的快速运行，本地已保存路网
    # load_net = np.array(pd.read_table('load_net', header=None)).reshape(city_num, city_num)

    def __init__(self, city_path, location_path, load_net_path):
        # 城市名:城市名可改为任何有效地址
        self.cities = np.array(pd.read_table(city_path))

        # 城市数量
        self.city_num = self.cities.shape[0]

        # 城市坐标：确保程序的快速运行，本地已保存城市坐标
        self.locations = np.array(pd.read_table(location_path, header=None))

        # 路网:确保程序的快速运行，本地已保存路网
        self.load_net = np.array(pd.read_table(load_net_path, header=None)).reshape(self.city_num, self.city_num)

    # 通过高德地图获取城市坐标
    def get_location(self):
        # 记录城市经纬度
        locations = []

        for city in self.cities:
            url = self.ReqURLForGeo + city + '&key=' + self.DefaultKey
            result = requests.get(url=url[0], timeout=30)
            if result.status_code == 200:
                location = result.json()['geocodes'][0]['location']
                locations.append(location)

        return locations

    # 通过高德地图获取路网
    def get_load_net(self):
        locations = self.get_location()

        load_net = np.zeros((self.city_num, self.city_num))

        for i in range(self.city_num - 1):
            origins = locations[i + 1:]  # len(origins) <= 100
            dest = locations[i]
            url = self.DistanceForGeo + '&key=' + self.DefaultKey + '&destination=' + dest + '&origins=' + origins[0]
            for origin in origins[1:]:
                url = url + '|' + origin

            respond = requests.get(url=url, timeout=60)
            if respond.status_code == 200:
                results = respond.json()['results']
                for j in range(len(origins)):
                    distance = results[j]['distance']
                    load_net[i, i + j + 1] = float(distance)
                    load_net[i + j + 1, i] = float(distance)

        return load_net


if __name__ == '__main__':
    data = Data()
    cities = data.cities
    locations = data.locations
    load_net = data.load_net
    print(locations)

    # 利用高德地图获取城市坐标和路网
    # locations = data.get_location()
    # load_net = data.get_load_net()
