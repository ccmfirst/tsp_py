# coding: UTF-8
import math
import random
import numpy as np
from data.get_data import Data
from data.solve import Solve


# 通过禁忌搜索求解TSP
class TS(Data):
    def __init__(self, city_path, location_path, load_net_path):
        Data.__init__(self, city_path, location_path, load_net_path)
        self.Stop = 1000
        self.candidates = 200
        # self.solve = Solve()

    def run(self):
        solve = Solve(self.cities, self.locations, self.load_net, 'TS')

        # 禁忌列表
        taboo_list = np.zeros((self.city_num, self.city_num))

        # 禁忌长度
        # taboo_len = round(math.pow(self.city_num * (self.city_num - 1) / 2, 0.5))
        taboo_len = 5
        # 邻域解
        candidate_num = np.zeros((self.candidates, self.city_num))

        # 贪婪算法 产生初始解
        s0 = solve.init_solution()

        # 全局最优解
        bsf = np.zeros((len(s0), 1))

        # 初始目标值
        best_dis = 10**10

        # 迭代次数
        p = 0

        # 记录局部最优解
        all_dis = []
        # 记录全局最优解
        global_best = np.zeros((self.Stop, 1))

        while p < self.Stop:
            # 防止进入死循环
            if self.candidates > self.city_num * (self.city_num - 1) / 2:
                break

            dis = solve.fun(s0)     # 求解
            all_dis.append(dis)     # 初始解目标值

            i = 0
            # 记录邻域变幻未知
            a = np.zeros((self.candidates, 2))

            while i < self.candidates:
                m1 = math.ceil((self.city_num-1) * random.random())
                m2 = math.ceil((self.city_num-1) * random.random())

                if m1 != m2:
                    a[i, 0] = max(m1, m2)
                    a[i, 1] = min(m1, m2)
                    if i == 0:
                        isa = 0
                    else:
                        for j in range(0, i - 1):
                            if a[i, 0] == a[j, 0] and a[i, 1] == a[j, 1]:
                                isa = 1
                                break
                            else:
                                isa = 0
                    if isa == 0:
                        i += 1
            # 记录最好的解的的个数
            best_candidate_num = 100
            best_candidate = 10**10 * np.ones((best_candidate_num, 4))
            # 记录邻域解目标值
            fit = np.zeros((self.candidates, 1))

            # 产生邻域解并计算目标值
            for i in range(self.candidates):
                candidate_num[i, :] = s0
                tmp1 = s0[int(a[i, 1])]
                tmp2 = s0[int(a[i, 0])]
                candidate_num[i, int(a[i, 0])] = tmp1
                candidate_num[i, int(a[i, 1])] = tmp2

                fit[i] = solve.fun(candidate_num[i, :])

                if i < best_candidate_num:
                    best_candidate[i, 1] = fit[i]
                    best_candidate[i, 0] = i
                    best_candidate[i, 2] = s0[int(a[i, 0])]
                    best_candidate[i, 3] = s0[int(a[i, 1])]
                else:
                    for j in range(best_candidate_num):
                        if fit[i] < best_candidate[j, 1]:
                            # print(i)
                            best_candidate[j, 1] = fit[i]
                            best_candidate[j, 0] = i
                            best_candidate[j, 2] = s0[int(a[i, 0])]
                            best_candidate[j, 3] = s0[int(a[i, 1])]
                            break

            sorted_nums = sorted(enumerate(best_candidate[:, 1]), key=lambda x: x[1])
            new_best = np.zeros(np.array(best_candidate).shape)
            for index in range(new_best.shape[0]):
                new_best[index, :] = best_candidate[sorted_nums[index][0]]
            best_candidate = new_best
            if best_candidate[0, 1] < best_dis:
                s0 = candidate_num[int(best_candidate[0, 0]), :]
                bsf[:, 0] = s0[0:]
                best_dis = best_candidate[0, 1]
                for m in range(self.city_num):
                    for n in range(self.city_num):
                        if taboo_list[m, n] != 0:
                            taboo_list[m, n] -= 1

                taboo_list[int(best_candidate[0, 2]), int(best_candidate[0, 3])] = taboo_len

            else:
                for i in range(best_candidate_num):

                    if int(taboo_list[int(best_candidate[i, 2]), int(best_candidate[i, 3])]) == 0:
                        s0 = candidate_num[int(best_candidate[i, 0]), :]
                    for m in range(self.city_num):
                        for n in range(self.city_num):
                            if taboo_list[m, n] != 0:
                                taboo_list[m, n] -= 1

                    taboo_list[int(best_candidate[i, 2]), int(best_candidate[i, 3])] = taboo_len
                    break

            global_best[p] = best_dis
            p += 1

        # 绘图
        solve.draw_fit(global_best)
        solve.draw_routes(bsf)

        # 输出最优解
        best = solve.fun(bsf)
        print(global_best[-1], best)


if __name__ == '__main__':
    city = '../data/cities.txt'
    location = '../data/locations'
    load = '../data/load_net'
    ts = TS(city, location, load)
    ts.run()

