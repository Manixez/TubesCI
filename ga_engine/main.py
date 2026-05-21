from typing import Any, Dict, Tuple
import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from ga_engine.ga.crossover import uniform_crossover
from ga_engine.ga.fitness import evaluate_schedule
from ga_engine.ga.genetic_algorithm import GAConfig, run_ga
from ga_engine.ga.mutation import mutate_random_reset
from ga_engine.ga.population import create_individual
from ga_engine.models.input_model import InputModel
from ga_engine.models.result_model import ResultModel
from ga_engine.models.schedule_model import PenaltyWeights
from ga_engine.services.schedule_generator import (
    build_problem,
    decode_schedule,
    schedule_rows,
)
from ga_engine.services.schedule_validator import capacity_warning, validate_input_model
from ga_engine.services.summary_generator import summarize_guards


def _build_ga_config(input_model: InputModel) -> Tuple[GAConfig, float]:
    ga = input_model.ga or {}
    config = GAConfig(
        population_size=int(ga.get("populationSize", ga.get("population_size", 120)) or 120),
        generations=int(ga.get("generations", 200) or 200),
        tournament_size=int(ga.get("tournamentSize", ga.get("tournament_size", 3)) or 3),
        crossover_rate=float(ga.get("crossoverRate", ga.get("crossover_rate", 0.9)) or 0.9),
        mutation_rate=float(ga.get("mutationRate", ga.get("mutation_rate", 0.3)) or 0.3),
        elite_count=int(ga.get("eliteCount", ga.get("elite_count", 2)) or 2),
        seed=int(ga.get("seed", 12042026) or 12042026),
    )
    gene_mutation_rate = float(
        ga.get("geneMutationRate", ga.get("gene_mutation_rate", 0.02)) or 0.02
    )
    return config, gene_mutation_rate


def generate_schedule_from_payload(payload: Dict[str, Any]) -> ResultModel:
    input_model = InputModel.from_dict(payload)
    errors = validate_input_model(input_model)
    if errors:
        raise ValueError("; ".join(errors))

    problem = build_problem(input_model)
    warnings = []
    warning_text = capacity_warning(problem)
    if warning_text:
        warnings.append(warning_text)

    config, gene_mutation_rate = _build_ga_config(input_model)
    weights = PenaltyWeights()

    def create_fn(rng):
        return create_individual(problem, rng)

    def fitness_fn(genome):
        return evaluate_schedule(genome, problem, weights)[0]

    def mutate_fn(genome, rng):
        return mutate_random_reset(
            genome,
            rng,
            guard_count=len(problem.guards),
            gene_mutation_rate=gene_mutation_rate,
        )

    result = run_ga(
        config=config,
        create_individual=create_fn,
        fitness_fn=fitness_fn,
        crossover_fn=uniform_crossover,
        mutate_fn=mutate_fn,
    )

    schedule = decode_schedule(result.best_genome, problem)
    fitness, metrics = evaluate_schedule(result.best_genome, problem, weights)
    summaries = summarize_guards(schedule, problem)
    rows = schedule_rows(schedule, problem)

    return ResultModel(
        schedule=rows,
        guard_summary=summaries,
        warnings=warnings,
        fitness_score=fitness,
        metrics=metrics,
    )


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.stderr.write("Input JSON required on stdin.\n")
        return 1

    try:
        payload = json.loads(raw)
        result = generate_schedule_from_payload(payload)
    except Exception as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    sys.stdout.write(json.dumps(result.to_dict()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
