import random
from typing import List, Tuple

# =========================================================
# DATASET P04
# =========================================================
BIN_CAPACITY = 524

WEIGHTS = [
    442,
    252, 252, 252, 252, 252, 252, 252,
    127, 127, 127, 127, 127,
    106, 106, 106, 106,
    85, 84, 46, 37, 37,
    12, 12, 12,
    10, 10, 10, 10, 10, 10,
    9, 9
]

KNOWN_ASSIGNMENT_7_BINS = [
    1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7,
    1, 6, 7, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5
]

# =========================================================
# PARAMETER GA
# =========================================================
SEED = 42
POP_SIZE = 30
GENERATIONS = 80
TOURNAMENT_SIZE = 3
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.2
ELITE_COUNT = 2
VERBOSE = True


# =========================================================
# UTILITAS PRINT
# =========================================================
def log(message: str):
    if VERBOSE:
        print(message)


# =========================================================
# REPRESENTASI
# Kromosom = permutasi indeks item
# Contoh: [3, 0, 2, 1, ...]
# =========================================================
def create_chromosome(n_items: int) -> List[int]:
    chromosome = list(range(n_items))
    random.shuffle(chromosome)
    log(f"[create_chromosome] Kromosom baru dibuat: {chromosome}")
    return chromosome


def initialize_population(pop_size: int, n_items: int) -> List[List[int]]:
    log("\n=== INISIALISASI POPULASI ===")
    population = []
    for i in range(pop_size):
        chrom = create_chromosome(n_items)
        population.append(chrom)
        log(f"[initialize_population] Individu-{i+1} selesai dibuat.")
    return population


# =========================================================
# DECODER
# Mengubah urutan item menjadi penempatan ke bin memakai First Fit
# =========================================================
def decode_chromosome(chromosome: List[int], weights: List[int], capacity: int) -> Tuple[List[List[int]], List[int]]:
    log("\n[decode_chromosome] Mulai decoding kromosom...")
    bins = []               # isi indeks item per bin
    remaining = []          # sisa kapasitas per bin

    for gene in chromosome:
        weight = weights[gene]
        placed = False

        for b in range(len(bins)):
            if remaining[b] >= weight:
                bins[b].append(gene)
                remaining[b] -= weight
                log(f"  Item idx={gene}, berat={weight} -> masuk Bin-{b+1}, sisa={remaining[b]}")
                placed = True
                break

        if not placed:
            bins.append([gene])
            remaining.append(capacity - weight)
            log(f"  Item idx={gene}, berat={weight} -> buat Bin-{len(bins)}, sisa={remaining[-1]}")

    return bins, remaining


# =========================================================
# FITNESS
# Tujuan utama: jumlah bin sekecil mungkin
# Tambahan: semakin kecil sisa total, semakin baik
# =========================================================
def fitness(chromosome: List[int], weights: List[int], capacity: int) -> Tuple[int, int]:
    bins, remaining = decode_chromosome(chromosome, weights, capacity)
    bin_count = len(bins)
    total_remaining = sum(remaining)

    log(f"[fitness] Jumlah bin = {bin_count}, total sisa kapasitas = {total_remaining}")
    return bin_count, total_remaining


def evaluate_population(population: List[List[int]], weights: List[int], capacity: int):
    log("\n=== EVALUASI POPULASI ===")
    scored = []
    for i, chrom in enumerate(population):
        log(f"\n[evaluate_population] Evaluasi Individu-{i+1}")
        fit = fitness(chrom, weights, capacity)
        scored.append((chrom, fit))
    scored.sort(key=lambda x: (x[1][0], x[1][1]))  # minimasi bin, lalu minimasi sisa
    return scored


# =========================================================
# SELEKSI
# Tournament Selection
# =========================================================
def tournament_selection(scored_population, tournament_size: int) -> List[int]:
    log("\n[tournament_selection] Mulai seleksi tournament...")
    candidates = random.sample(scored_population, tournament_size)
    log("  Kandidat tournament:")
    for i, (_, fit) in enumerate(candidates):
        log(f"    Kandidat-{i+1}: fitness={fit}")
    winner = min(candidates, key=lambda x: (x[1][0], x[1][1]))
    log(f"  Pemenang tournament: fitness={winner[1]}")
    return winner[0][:]


# =========================================================
# CROSSOVER
# Order Crossover (OX)
# Cocok untuk representasi permutasi
# =========================================================
def order_crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    log("\n[order_crossover] Mulai crossover...")
    n = len(parent1)
    c1, c2 = sorted(random.sample(range(n), 2))
    log(f"  Titik crossover: {c1} - {c2}")

    child1 = [-1] * n
    child2 = [-1] * n

    # Salin segmen tengah
    child1[c1:c2+1] = parent1[c1:c2+1]
    child2[c1:c2+1] = parent2[c1:c2+1]

    # Isi sisanya dengan urutan parent lain
    fill_pos1 = (c2 + 1) % n
    fill_pos2 = (c2 + 1) % n

    p2_idx = (c2 + 1) % n
    while -1 in child1:
        gene = parent2[p2_idx]
        if gene not in child1:
            child1[fill_pos1] = gene
            fill_pos1 = (fill_pos1 + 1) % n
        p2_idx = (p2_idx + 1) % n

    p1_idx = (c2 + 1) % n
    while -1 in child2:
        gene = parent1[p1_idx]
        if gene not in child2:
            child2[fill_pos2] = gene
            fill_pos2 = (fill_pos2 + 1) % n
        p1_idx = (p1_idx + 1) % n

    log(f"  Parent1: {parent1}")
    log(f"  Parent2: {parent2}")
    log(f"  Child1 : {child1}")
    log(f"  Child2 : {child2}")

    return child1, child2


# =========================================================
# MUTASI
# Swap Mutation: tukar 2 posisi
# =========================================================
def mutate_swap(chromosome: List[int]) -> List[int]:
    log("\n[mutate_swap] Mulai mutasi swap...")
    mutated = chromosome[:]
    i, j = random.sample(range(len(mutated)), 2)
    log(f"  Posisi yang ditukar: {i} <-> {j}")
    mutated[i], mutated[j] = mutated[j], mutated[i]
    log(f"  Sebelum: {chromosome}")
    log(f"  Sesudah: {mutated}")
    return mutated


# =========================================================
# PEMBENTUKAN GENERASI BARU
# Dengan elitism
# =========================================================
def create_new_population(scored_population, pop_size: int) -> List[List[int]]:
    log("\n=== MEMBENTUK GENERASI BARU ===")
    new_population = []

    # Elitism
    elites = [chrom[:] for chrom, _ in scored_population[:ELITE_COUNT]]
    new_population.extend(elites)
    log(f"[create_new_population] Elitism: {ELITE_COUNT} individu terbaik dipertahankan.")

    while len(new_population) < pop_size:
        parent1 = tournament_selection(scored_population, TOURNAMENT_SIZE)
        parent2 = tournament_selection(scored_population, TOURNAMENT_SIZE)

        if random.random() < CROSSOVER_RATE:
            child1, child2 = order_crossover(parent1, parent2)
        else:
            log("\n[create_new_population] Crossover tidak dilakukan, anak = copy parent.")
            child1, child2 = parent1[:], parent2[:]

        if random.random() < MUTATION_RATE:
            child1 = mutate_swap(child1)

        if random.random() < MUTATION_RATE:
            child2 = mutate_swap(child2)

        new_population.append(child1)
        if len(new_population) < pop_size:
            new_population.append(child2)

    return new_population


# =========================================================
# KONVERSI HASIL KE FORMAT ASSIGNMENT BIN
# assignment[i] = nomor bin dari item ke-i
# =========================================================
def bins_to_assignment(bins: List[List[int]], n_items: int) -> List[int]:
    assignment = [0] * n_items
    for bin_idx, bin_items in enumerate(bins, start=1):
        for item_idx in bin_items:
            assignment[item_idx] = bin_idx
    return assignment


# =========================================================
# TAMPILKAN SOLUSI
# =========================================================
def print_solution(chromosome: List[int], weights: List[int], capacity: int):
    log("\n=== SOLUSI TERBAIK ===")
    bins, remaining = decode_chromosome(chromosome, weights, capacity)
    assignment = bins_to_assignment(bins, len(weights))

    print("\nHASIL AKHIR")
    print("-" * 50)
    print(f"Jumlah bin yang dipakai : {len(bins)}")
    print(f"Assignment per item     : {assignment}")
    print()

    for i, bin_items in enumerate(bins):
        bin_weights = [weights[idx] for idx in bin_items]
        print(f"Bin-{i+1}: item_idx={bin_items}")
        print(f"       berat={bin_weights}")
        print(f"       total={sum(bin_weights)} / {capacity}, sisa={remaining[i]}")
        print()

    print("Urutan kromosom terbaik:")
    print(chromosome)


# =========================================================
# CEK SOLUSI REFERENSI 7 BIN
# =========================================================
def verify_known_solution(weights: List[int], assignment: List[int], capacity: int):
    log("\n=== VERIFIKASI SOLUSI REFERENSI 7 BIN ===")
    max_bin = max(assignment)
    sums = [0] * max_bin
    for i, bin_no in enumerate(assignment):
        sums[bin_no - 1] += weights[i]

    for i, total in enumerate(sums, start=1):
        print(f"Bin-{i}: total={total} / {capacity}")
    print(f"Jumlah bin referensi = {max_bin}")


# =========================================================
# MAIN GA
# =========================================================
def genetic_algorithm(weights: List[int], capacity: int):
    log("\n==============================")
    log(" GENETIC ALGORITHM DIMULAI ")
    log("==============================")

    random.seed(SEED)
    log(f"\n[genetic_algorithm] Random seed = {SEED}")
    log(f"[genetic_algorithm] Jumlah item = {len(weights)}")
    log(f"[genetic_algorithm] Kapasitas bin = {capacity}")

    population = initialize_population(POP_SIZE, len(weights))
    best_global = None
    best_fitness_global = (10**9, 10**9)

    for gen in range(GENERATIONS):
        log(f"\n\n########################################")
        log(f" GENERASI {gen + 1}")
        log(f"########################################")

        scored_population = evaluate_population(population, weights, capacity)
        best_chrom, best_fit = scored_population[0]

        print(f"\n[Generasi {gen+1}] Best fitness = bins:{best_fit[0]}, sisa:{best_fit[1]}")

        if best_fit < best_fitness_global:
            best_global = best_chrom[:]
            best_fitness_global = best_fit
            print(f"[Generasi {gen+1}] Ditemukan best global baru: {best_fitness_global}")

        # Kalau sudah mencapai 7 bin, bisa berhenti lebih cepat
        if best_fit[0] == 7:
            print(f"\n[STOP] Solusi 7 bin ditemukan pada generasi {gen+1}")
            break

        population = create_new_population(scored_population, POP_SIZE)

    print_solution(best_global, weights, capacity)
    return best_global, best_fitness_global


# =========================================================
# PROGRAM UTAMA
# =========================================================
if __name__ == "__main__":
    print("PROGRAM BIN PACKING DENGAN GENETIC ALGORITHM")
    print("=" * 60)

    verify_known_solution(WEIGHTS, KNOWN_ASSIGNMENT_7_BINS, BIN_CAPACITY)

    best_chromosome, best_fit = genetic_algorithm(WEIGHTS, BIN_CAPACITY)

    print("\nRINGKASAN")
    print("=" * 60)
    print(f"Fitness terbaik: jumlah bin={best_fit[0]}, total sisa={best_fit[1]}")
    if best_fit[0] == 7:
        print("GA berhasil menemukan solusi 7 bin.")
    else:
        print("GA belum menemukan 7 bin pada run ini.")