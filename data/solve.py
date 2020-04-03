# coding: UTF-8
import matplotlib.pyplot as plt
from data.get_data import Data
import numpy as np


class Solve():
    def __init__(self, cities, locations, load_net):
        self.cities = cities
        self.locations = locations
        self.load_net = load_net

    def fun(self, s):
        dis = 0
        for i in range(len(s) - 1):
            dis += self.load_net[int(s[i]), int(s[i + 1])]

        dis += self.load_net[int(s[0]), int(s[-1])]
        return dis

    def result(self, s, fits):
        data = np.zeros((len(s) + 1, 2))
        names = []
        for i in range(len(s)):
            location = self.locations[int(s[i])][0]
            lng = location.split(',', 1)[0]
            lat = location.split(',', 1)[1]
            data[i, 0] = float(lng)
            data[i, 1] = float(lat)
            names.append(self.cities[int(s[i])])
        data[len(s), :] = data[0, :]

        plt.figure(1)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        x = np.arange(0, len(fits))
        plt.plot(x, fits, color='r')
        plt.xlabel('迭代次数')
        plt.ylabel('目标函数值')
        plt.title('禁忌搜索求解TSP')

        plt.figure(2)
        plt.scatter(data[:-1, 0], data[:-1, 1], s=75, c='r', alpha=0.5)
        plt.plot(data[:, 0], data[:, 1], 'g')
        for i in range(len(s)):
            plt.annotate(self.cities[int(s[i])][0], xy=(data[i, 0], data[i, 1]), xycoords='data', xytext=(+10, +10),
                         textcoords="offset points")

        plt.show()


if __name__ == '__main__':
    Solve(1, 2).result([1, 2, 3], [1, 2, 3])
