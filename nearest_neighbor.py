import random

def nearest_neighbor(canvas):
    canvas.best_edges_delete()
    canvas.edges_mass = canvas.table.check_data(canvas.edges_mass)
    vertices, edges = canvas.circle_mass, canvas.edges_mass
    visited = []
    current_vertex = random.choice(vertices)
    visited.append(current_vertex[0])
    while len(visited) < len(vertices):
        next_vertex = None
        min_distance = float("inf")
        for edge in edges:
            if current_vertex[0] == edge[0] and edge[1] not in visited:
                if edge[2] < min_distance:
                    min_distance = edge[2]
                    next_vertex = edge[1]
            elif current_vertex[0] == edge[1] and edge[0] not in visited:
                if edge[2] < min_distance:
                    min_distance = edge[2]
                    next_vertex = edge[0]
        visited.append(next_vertex)
        for vertex in vertices:
            if vertex[0] == next_vertex:
                current_vertex = vertex
                break
    visited.append(visited[0])
    total_weight = 0
    for i in range(len(visited) - 1):
        for edge in edges:
            if visited[i] == edge[0] and visited[i+1] == edge[1]:
                total_weight += edge[2]
            elif visited[i] == edge[1] and visited[i+1] == edge[0]:
                total_weight += edge[2]

    print("Полученный путь:",visited,"длина пути:", total_weight)
    canvas.best_way = visited
    canvas.best_weight = total_weight
    canvas.all_edges_hidden(True)
    canvas.draw_best_way()
    return canvas
