import random
import numpy as np

# Ma trận khoảng cách giữa các thành phố (ví dụ: 5 thành phố)
distance_matrix = [
    [0, 2, 3, 5, 7],
    [2, 0, 4, 6, 3],
    [3, 4, 0, 7, 5],
    [5, 6, 7, 0, 4],
    [7, 3, 5, 4, 0]
]

# Số lượng thành phố
num_cities = len(distance_matrix)

# Tính tổng khoảng cách của một đường đi
def calculate_distance(path):
    total_distance = 0
    for i in range(len(path)):
        total_distance += distance_matrix[path[i]][path[(i + 1) % len(path)]]
    return total_distance

# Tính fitness (nghịch đảo tổng khoảng cách)
def fitness(path):
    return 1 /  (1 + calculate_distance(path))

# Tạo một chromosome ngẫu nhiên (bắt đầu từ 0, quay lại 0)
def create_chromosome():
    # Tạo danh sách các đỉnh trừ đỉnh 0
    other_cities = list(range(1, num_cities))
    random.shuffle(other_cities)
    # Thêm đỉnh 0 vào đầu và cuối
    return [0] + other_cities + [0]

# Khởi tạo quần thể
def initialize_population(pop_size):
    return [create_chromosome() for _ in range(pop_size)]

# Chọn lọc (Tournament Selection)
def tournament_selection(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

# Lai ghép (Order Crossover - OX) với cố định đỉnh 0
def order_crossover(parent1, parent2):
    size = len(parent1) - 1  # Bỏ đỉnh 0 ở cuối
    # Chọn hai điểm cắt ngẫu nhiên (trừ vị trí đầu và cuối)
    start, end = sorted(random.sample(range(1, size-1), 2))
    
    # Lấy đoạn từ parent1 (không bao gồm đỉnh 0 ở cuối)
    child = [-1] * size
    child[0] = 0  # Cố định đỉnh 0 ở đầu
    for i in range(start, end + 1):
        child[i] = parent1[i]
    
    # Điền các thành phố còn lại từ parent2
    parent2_idx = 1  # Bỏ đỉnh 0 đầu tiên của parent2
    child_idx = 1
    while child_idx < size:
        if child_idx == start:
            child_idx = end + 1
            continue
        if parent2[parent2_idx] not in child:
            child[child_idx] = parent2[parent2_idx]
            child_idx += 1
        parent2_idx += 1
    
    # Thêm đỉnh 0 vào cuối
    child.append(0)
    return child

# Đột biến (Swap Mutation) chỉ trên các đỉnh không phải 0
def mutate(chromosome, mutation_rate=0.01):
    if random.random() < mutation_rate:
        # Chọn hai vị trí ngẫu nhiên từ 1 đến len-2 (tránh đỉnh 0 đầu và cuối)
        i, j = random.sample(range(1, len(chromosome)-1), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

# Thuật toán di truyền chính
def genetic_algorithm(pop_size=100, num_generations=100, mutation_rate=0.01, elitism_size=2):
    # Khởi tạo quần thể
    population = initialize_population(pop_size)
    
    for generation in range(num_generations):
        # Đánh giá fitness và tìm chromosome tốt nhất
        best_chromosome = max(population, key=fitness)
        best_distance = calculate_distance(best_chromosome)
        
        # In tiến trình
        if generation % 10 == 0:
            print(f"Generation {generation}: Best Distance = {best_distance:.2f}, Path = {best_chromosome}")
        
        # Tạo quần thể mới
        new_population = []
        
        # Elitism: Giữ lại chromosome tốt nhất
        new_population.extend(sorted(population, key=fitness, reverse=True)[:elitism_size])
        
        # Tạo các chromosome con
        while len(new_population) < pop_size:
            # Chọn cha mẹ
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            
            # Lai ghép
            child = order_crossover(parent1, parent2)
            
            # Đột biến
            child = mutate(child, mutation_rate)
            
            new_population.append(child)
        
        # Cập nhật quần thể
        population = new_population
    
    # Tìm chromosome tốt nhất cuối cùng
    best_chromosome = max(population, key=fitness)
    best_distance = calculate_distance(best_chromosome)
    return best_chromosome, best_distance

# Chạy thuật toán
random.seed(42)  # Để kết quả có thể tái tạo
best_path, best_distance = genetic_algorithm(pop_size=100, num_generations=100, mutation_rate=0.01)
print(f"\nFinal Best Path: {best_path}")
print(f"Final Best Distance: {best_distance:.2f}")


#Test chạy với số số lượng thành phố lớn hơn 
def generate_distance_matrix(n, min_distance=1, max_distance=20):
    matrix = [[0 if i == j else None for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = random.randint(min_distance, max_distance)
            matrix[i][j] = distance
            matrix[j][i] = distance  # Đảm bảo đối xứng
    
    return matrix

# Ví dụ sinh ma trận 6 thành phố
num_cities = 15
distance_matrix = generate_distance_matrix(num_cities)
for row in distance_matrix:
    print(row)


# Chạy thuật toán
random.seed(42)  # Để kết quả có thể tái tạo
best_path, best_distance = genetic_algorithm(pop_size=100, num_generations=100, mutation_rate=0.01)
print(f"\nFinal Best Path: {best_path}")
print(f"Final Best Distance: {best_distance:.2f}")
