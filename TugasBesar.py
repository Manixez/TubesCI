import random

# --- DATASET P04 ---
CAPACITY = 524
WEIGHTS = [
    442, 252, 252, 252, 252, 252, 252, 252, 127, 127, 127, 127, 127,
    106, 106, 106, 106, 85, 84, 46, 37, 37, 12, 12, 12, 10, 10, 10,
    10, 10, 10, 9, 9
]

def first_fit_decoder(permutation, weights, capacity):
    bins = []
    for idx in permutation:
        weight = weights[idx]
        placed = False
        for b in bins:
            if sum(b) + weight <= capacity:
                b.append(weight)
                placed = True
                break
        if not placed:
            bins.append([weight])
    return bins # Mengembalikan list isi bin untuk visualisasi

def calculate_fitness(individual, weights, capacity):
    bins = first_fit_decoder(individual, weights, capacity)
    return 1.0 / len(bins)

def initialize_population(pop_size, num_items):
    print(f"\n[STEP 1] Inisialisasi: Membuat {pop_size} individu acak...")
    population = []
    indices = list(range(num_items))
    for i in range(pop_size):
        individual = indices[:]
        random.shuffle(individual)
        population.append(individual)
    return population

def tournament_selection(population, fitnesses, k=3, verbose=False):
    selected_indices = random.sample(range(len(population)), k)
    best_idx = max(selected_indices, key=lambda i: fitnesses[i])
    if verbose:
        print(f"  - Turnamen: Memilih dari indeks {selected_indices}, Pemenang: Indeks {best_idx}")
    return population[best_idx]

def order_crossover(p1, p2, verbose=False):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[a:b] = p1[a:b]
    
    p2_remaining = [item for item in p2 if item not in child]
    pointer = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = p2_remaining[pointer]
            pointer += 1
    
    if verbose:
        print(f"  - Crossover OX: Titik potong [{a}:{b}]")
        print(f"    P1: {p1[:5]}... | P2: {p2[:5]}... -> Child: {child[:5]}...")
    return child

def mutate(individual, mutation_rate, verbose=False):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        if verbose:
            print(f"  - Mutasi: Swap indeks {idx1} dan {idx2}")
    return individual

def run_genetic_algorithm(weights, capacity, pop_size=10, generations=5, mutation_rate=0.2):
    num_items = len(weights)
    population = initialize_population(pop_size, num_items)
    
    print("\n" + "="*50)
    print("MEMULAI PROSES EVOLUSI")
    print("="*50)

    for gen in range(generations):
        verbose_gen = (gen == 0) # Hanya cetak detail di generasi pertama
        
        # 1. Evaluasi Fitness
        fitnesses = [calculate_fitness(ind, weights, capacity) for ind in population]
        best_f = max(fitnesses)
        best_bins = int(1/best_f)
        
        print(f"\n>>> GENERASI {gen} | Best Fitness: {best_f:.4f} ({best_bins} Bins)")
        
        if verbose_gen:
            print("[STEP 2] Seleksi, Crossover, & Mutasi (Detail Generasi Awal):")
        
        # 2. Reproduksi
        new_population = []
        for i in range(pop_size // 2):
            # Seleksi
            p1 = tournament_selection(population, fitnesses, verbose=verbose_gen)
            p2 = tournament_selection(population, fitnesses, verbose=verbose_gen)
            
            # Crossover
            c1 = order_crossover(p1, p2, verbose=verbose_gen)
            c2 = order_crossover(p2, p1, verbose=verbose_gen)
            
            # Mutasi
            new_population.append(mutate(c1, mutation_rate, verbose=verbose_gen))
            new_population.append(mutate(c2, mutation_rate, verbose=verbose_gen))
        
        population = new_population

    # Hasil Akhir
    final_fitnesses = [calculate_fitness(ind, weights, capacity) for ind in population]
    best_idx = final_fitnesses.index(max(final_fitnesses))
    best_ind = population[best_idx]
    final_bins_structure = first_fit_decoder(best_ind, weights, capacity)

    print("\n" + "="*60)
    print("HASIL AKHIR OPTIMASI (BIN PACKING)")
    print("="*60)
    print(f"Total Bin yang Dibutuhkan: {len(final_bins_structure)}")
    print("-"*60)

    for i, contents in enumerate(final_bins_structure):
        total_weight = sum(contents)
        free_space = capacity - total_weight
        print(f"Bin {i+1:02d} | Isi: {contents}")
        print(f"       | Total: {total_weight}/{capacity} (Sisa: {free_space})")
        print("-"*60)

    print("\nProses evolusi selesai, 33 dari 33 objek berhasil ditempatkan pada bin. Solusi terbaik ditemukan dengan jumlah bin:", len(final_bins_structure))

if __name__ == "__main__":
    run_genetic_algorithm(WEIGHTS, CAPACITY, pop_size=6, generations=5)