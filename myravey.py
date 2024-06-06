import random

def ant_alg(mass):
    canvas = mass[0]
    canvas.best_edges_delete()
    canvas.edges_mass = canvas.table.check_data(canvas.edges_mass)
    edges = canvas.edges_mass
    num_ants = 10
    iterations = 50
    evaporation_rate = float(mass[1].get())
    alpha = float(mass[2].get())
    beta = float(mass[3].get())
    pheromone_constant = float(mass[4].get())
    ant_colony = AntColony(num_ants, edges, evaporation_rate, pheromone_constant, iterations,
                           alpha, beta)
    ant_colony.run()

    print('Полученный путь: ', ant_colony.best_path)
    print('Длина: ', ant_colony.best_distance)
    canvas.best_way = ant_colony.best_path
    canvas.best_weight = ant_colony.best_distance
    canvas.all_edges_hidden(True)
    canvas.draw_best_way()
    return canvas
class Ant:
    def __init__(self, id, start_node):
        self.id = id
        self.path = [start_node]
        self.visited_nodes = set()
        self.visited_nodes.add(start_node)
        self.total_distance = 0

    def move_to_node(self, node, distance):
        self.path.append(node)
        self.visited_nodes.add(node)
        self.total_distance += distance

class AntColony:
    def __init__(self, num_ants, edges, evaporation_rate, pheromone_constant, iterations,alpha,beta):
        self.num_ants = num_ants
        self.edges = edges
        self.evaporation_rate = evaporation_rate #феромоны испаряются на каждой итерации алгоритма.
        self.pheromone_constant = pheromone_constant # отложение феромона
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.nodes = set()
        self.distances = {}
        self.pheromones = {}
        self.best_path = None
        self.best_distance = float('inf')

        for edge in edges:
            node1, node2, distance = edge
            self.nodes.add(node1)
            self.nodes.add(node2)
            self.distances[(node1, node2)] = distance
            self.distances[(node2, node1)] = distance
            self.pheromones[(node1, node2)] = 1
            self.pheromones[(node2, node1)] = 1

    def prob(self,edges,distance,pheromones):
        sum = 0
        mass = []
        for i in range(len(edges)):
            d = distance[i]
            t = pheromones[i]
            h = d**self.alpha*(1/d)**self.beta
            mass.append(h)
            sum += h
        for i in range(len(mass)):
            mass[i] = mass[i] / sum
        return mass

    def run(self):
        for i in range(self.iterations):
            ants = [Ant(j, random.choice(list(self.nodes))) for j in range(10)]
            for ant in ants:
                while len(ant.visited_nodes) < len(self.nodes):
                    current_node = ant.path[-1]
                    candidate_nodes = [node for node in self.nodes if node not in ant.visited_nodes]
                    if len(candidate_nodes) == 0:
                        break
                    candidate_edges = [(current_node, node) for node in candidate_nodes]
                    candidate_distances = [self.distances[edge] for edge in candidate_edges]
                    candidate_pheromones = [self.pheromones[edge] for edge in candidate_edges]
                    candidate_probabilities = self.prob(candidate_edges,candidate_distances,candidate_pheromones)
                    next_node = random.choices(candidate_nodes, candidate_probabilities)[0]
                    distance = self.distances[(current_node, next_node)]
                    ant.move_to_node(next_node, distance)
                ant.move_to_node(ant.path[0], self.distances[(ant.path[-1], ant.path[0])])
                if ant.total_distance < self.best_distance:
                    self.best_path = ant.path
                    self.best_distance = ant.total_distance
            for edge in self.pheromones:
                self.pheromones[edge] *= (1 - self.evaporation_rate)
            for ant in ants:
                for i in range(len(ant.path) - 1):
                    edge = (ant.path[i], ant.path[i+1])
                    self.pheromones[edge] += self.pheromone_constant / ant.total_distance