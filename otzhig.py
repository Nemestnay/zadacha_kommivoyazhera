import random
import math

mass_edges = []

#рассчет расстояния между двумя городами
def distance(city1, city2):
    for i in mass_edges:
        if city1 in i and city2 in i:
            return i[2]
    return

#рассчет расстояния путя
def total_distance(cities, order):
    dist = 0
    for i in range(len(order)):
        dist += distance(cities[order[i]], cities[order[(i + 1) % len(order)]])
    return dist

#алгоритм отжига
def alg_otzhig(mass):
    #инициализация переменных, задание первого порядка
    k = 0
    global mass_edges
    canvas = mass[0]
    initial_temp = int(mass[1].get())
    cooling_rate = float(mass[2].get())
    stopping_temp = 10 ** (-8)
    canvas.best_edges_delete()
    canvas.edges_mass = canvas.table.check_data(canvas.edges_mass)
    verticles, mass_edges = canvas.circle_mass, canvas.edges_mass
    cities = []
    for i in range(len(verticles)):
        cities.append(verticles[i][0])

    current_order = list(range(len(cities)))
    random.shuffle(current_order)
    current_temp = initial_temp

    best_order = current_order[:]
    best_dist = total_distance(cities, current_order)

    #пока не достигнута температура остановки
    while current_temp > stopping_temp:
        k+=1
        new_order = current_order[:]
        i, j = random.sample(range(len(cities)), 2)
        new_order[i], new_order[j] = new_order[j], new_order[i]
        #определение энергии текущего расстояния
        current_dist = total_distance(cities, current_order)
        #определение энергии нового расстояния
        new_dist = total_distance(cities, new_order)

        if new_dist < current_dist:
            current_order = new_order[:]
            if new_dist < best_dist:
                best_order = new_order[:]
                best_dist = new_dist
        else:
            delta = new_dist - current_dist
            prob = math.exp(-delta / current_temp)
            if random.random() < prob:
                current_order = new_order[:]

        current_temp *= 1 - cooling_rate

    best_order.append(best_order[0])
    canvas.best_weight = best_dist
    canvas.best_way = best_order
    canvas.all_edges_hidden(True)
    canvas.counter = k
    canvas.draw_best_way()
    return canvas
