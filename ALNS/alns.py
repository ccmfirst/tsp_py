import numpy as np
import copy
from data.get_data import Data
from data.solve import Solve


class ALNS(Data):
    def __init__(self, city_path, location_path, load_net_path, weights, operator, iterations=10000,
                 degree_of_destruction=0.25):
        Data.__init__(self, city_path, location_path, load_net_path)
        self.weights = weights
        self.operator = operator
        self.iterations = iterations
        self.degree_of_destruction = degree_of_destruction
        self.destroyed_num = int(self.city_num * self.degree_of_destruction)

    def copy(self):
        return copy.deepcopy()

    def run(self):
        solve = Solve(self.cities, self.locations, self.load_net)
        solution = solve.init_solution()
        current_fit = solve.fun(solution)
        best_solution = solution.copy()
        best_fit = current_fit
        best_fits = []
        d_weights = [1., 1., 1.]
        # r_weights = [1.]
        for _ in range(self.iterations):

            d_idx = self.roulette(d_weights)
            # r_idx = self.roulette(r_weights)
            x = set(solution)
            if len(x) != self.city_num:
                print(x)
            if d_idx == 0:
                destroyed, gens = self.worst_removal(solution)
            elif d_idx == 1:
                destroyed, gens = self.path_removal(solution)
            else:
                destroyed, gens = self.random_removal(solution)

            new_solution = self.greedy_repair(destroyed, gens)
            fit = solve.fun(new_solution)

            w, solution, current_fit = self.consider_solution(best_fit, current_fit, fit, solution, new_solution)

            d_weights[d_idx] *= self.operator
            d_weights[d_idx] += (1 - self.operator) * w

            if fit <= best_fit:
                best_fit = fit
                best_solution = new_solution.copy()

            best_fits.append(best_fit)

        best = solve.fun(best_solution)
        print(best)

        solve.draw_fit(best_fits)
        solve.draw_routes(best_solution)

    # 最差移除
    def worst_removal(self, solution):
        destroyed = []

        to_city = solution[1:]
        to_city.append(solution[0])
        route_dis = []
        for i in range(self.city_num - 1):
            route_dis.append(self.load_net[solution[i], solution[i + 1]])
        route_dis.append(self.load_net[solution[self.city_num - 1], solution[0]])

        dis_sort = sorted(enumerate(route_dis), key=lambda x: x[0])
        gens = []
        for idx in range(self.destroyed_num):
            gens.append(to_city[dis_sort[-idx - 1][0]])

        for i in solution:
            if i not in gens:
                destroyed.append(i)

        return destroyed, gens

    # 路径移除： 删除一段连续的子路径
    def path_removal(self, solution):
        node = np.random.randint(self.city_num)
        s = solution.copy()
        s.extend(solution)
        gens = s[node: node + self.destroyed_num]
        destroyed = []
        for i in solution:
            # print(i, '\n', gens)
            if i not in gens:
                destroyed.append(i)

        return destroyed, gens

    # 随机移除： 随机删除子路径
    def random_removal(self, solution):
        destroyed = solution.copy()
        gens = []
        for i in range(self.destroyed_num):
            j = np.random.randint(len(destroyed))
            gens.append(destroyed[j])
            del destroyed[j]

        return destroyed, gens

    def greedy_repair(self, destroyed, gens):

        while len(destroyed) < self.city_num:
            nearest = self.load_net[destroyed[0], gens[0]]
            row = 0
            col = 0
            for i in range(len(destroyed)):
                for j in range(len(gens)):
                    dis = self.load_net[destroyed[i], gens[j]]
                    if dis < nearest:
                        nearest = dis
                        row = i + 1
                        col = j
            # print(row, col, len(destroyed))
            destroyed.insert(row, gens[col])
            del gens[col]

        return destroyed

    # 轮盘赌选择destroy和repair方法
    def roulette(self, weights):
        w = sum(weights)
        p = []
        for v in weights:
            p.append(v / w)
        s = np.cumsum(p)

        r = np.random.random()
        for i in range(len(s)):
            if r <= s[i]:
                return i

        return i

    # 判断权重更新方向
    def consider_solution(self, best_fit, current_fit, fit, current, new_solution):
        w = 0
        if fit <= best_fit:
            w = self.weights[0]
            current_fit = fit
            current = new_solution.copy()
        elif fit <= current_fit:
            w = self.weights[1]
            current_fit = fit
            current = new_solution.copy()
        elif fit <= best_fit * 1.1:
            w = self.weights[2]
            current_fit = fit
            current = new_solution.copy()
        else:
            w = self.weights[3]
            # current_fit = current_fit
            # current = current.copy()

        return w, current, current_fit


if __name__ == '__main__':
    city = '../data/cities.txt'
    location = '../data/locations'
    load = '../data/load_net'
    alns = ALNS(city, location, load, [3., 2., 1., 0.5], 0.8, 1000, 0.25)
    alns.run()

