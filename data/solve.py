# coding: UTF-8
import matplotlib.pyplot as plt
from data.get_data import Data
import numpy as np


class Solve():
    plt.rcParams['font.sans-serif'] = ['AR PL UKai CN']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    def __init__(self, cities, locations, load_net):
        self.cities = cities
        self.locations = locations
        self.load_net = load_net
        self.city_num = cities.shape[0]

    def fun(self, s):
        dis = 0
        for i in range(len(s) - 1):
            dis += self.load_net[int(s[i]), int(s[i + 1])]

        dis += self.load_net[int(s[0]), int(s[-1])]
        return dis

    def draw_fit(self, fits):
        plt.figure()
        x = np.arange(0, len(fits))
        plt.plot(x, fits, color='r')
        plt.xlabel('迭代次数')
        plt.ylabel('目标函数值')
        plt.title('ALNS求解TSP')
        plt.show()

    def draw_routes(self, s):
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

        plt.figure()
        plt.scatter(data[:-1, 0], data[:-1, 1], s=75, c='r', alpha=0.5)
        plt.plot(data[:, 0], data[:, 1], 'g')
        for i in range(len(s)):
            plt.annotate(self.cities[int(s[i])][0], xy=(data[i, 0], data[i, 1]), xycoords='data', xytext=(+5, +1),
                         textcoords="offset points")

        plt.show()

    def init_solution(self):
        ind = []
        load_net = np.array(self.load_net)
        max_dis = load_net.max()
        for i in range(self.city_num):
            load_net[i, i] = max_dis + 1000

        pos = np.unravel_index(np.argmin(load_net), load_net.shape)
        ind.append(pos[0])
        ind.append(pos[1])
        load_net[:, pos[0]] = max_dis + 1000
        next_row = pos[1]
        while len(ind) < self.city_num:
            pos = np.unravel_index(np.argmin(load_net[next_row, :]), load_net.shape)
            load_net[:, next_row] = max_dis + 1000
            next_row = pos[1]
            ind.append(next_row)

        return ind


if __name__ == '__main__':
    city = '../data/cities.txt'
    location = '../data/locations'
    load = '../data/load_net'
    data = Data(city, location, load)
    # Solve(1, 2).result([1, 2, 3], [1, 2, 3])
    solve = Solve(data.cities, data.locations, data.load_net)
    ind = solve.init_solution()
    fit = solve.fun(ind)
    print(fit)
    solve.draw_routes(ind)
