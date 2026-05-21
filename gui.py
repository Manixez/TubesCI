import threading
from typing import List
import tkinter as tk
from tkinter import ttk, messagebox

from ga_core import GAConfig, run_ga
from shift_scheduling import (
    PenaltyWeights,
    ShiftProblem,
    create_individual,
    decode_schedule,
    evaluate_schedule,
    mutate_random_reset,
    schedule_rows,
    summarize_guards,
    uniform_crossover,
)


class ShiftSchedulerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sistem Rekomendasi Penjadwalan Shift Satpam - GA")

        self.input_frame = ttk.Frame(root, padding=10)
        self.input_frame.pack(fill=tk.X)

        self.output_frame = ttk.Frame(root, padding=10)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self._build_inputs()
        self._build_outputs()

    def _build_inputs(self) -> None:
        self.var_building_count = tk.IntVar(value=3)
        self.var_building_names = tk.StringVar(value="Gedung A, Gedung B, Gedung C")
        self.var_guard_count = tk.IntVar(value=12)
        self.var_guard_names = tk.StringVar(value="S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12")
        self.var_guards_per_shift = tk.IntVar(value=2)
        self.var_min_days_off = tk.IntVar(value=2)

        self.var_pop_size = tk.IntVar(value=120)
        self.var_generations = tk.IntVar(value=200)
        self.var_tournament = tk.IntVar(value=3)
        self.var_crossover = tk.DoubleVar(value=0.9)
        self.var_mutation = tk.DoubleVar(value=0.3)
        self.var_elite = tk.IntVar(value=2)
        self.var_gene_mutation = tk.DoubleVar(value=0.02)
        self.var_seed = tk.IntVar(value=12042026)

        row = 0
        ttk.Label(self.input_frame, text="Jumlah gedung").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_building_count, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Nama gedung (pisah koma)").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_building_names, width=40).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Jumlah satpam").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_guard_count, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Nama satpam (pisah koma)").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_guard_names, width=40).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Satpam per shift").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_guards_per_shift, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Hari libur min (per satpam)").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_min_days_off, width=10).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Pop size").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_pop_size, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Generasi").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_generations, width=10).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Tournament size").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_tournament, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Elite count").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_elite, width=10).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Crossover rate").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_crossover, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Mutation rate").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_mutation, width=10).grid(row=row, column=3, sticky=tk.W)

        row += 1
        ttk.Label(self.input_frame, text="Gene mutation rate").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_gene_mutation, width=10).grid(row=row, column=1, sticky=tk.W)
        ttk.Label(self.input_frame, text="Seed").grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.input_frame, textvariable=self.var_seed, width=10).grid(row=row, column=3, sticky=tk.W)

        row += 1
        self.run_button = ttk.Button(self.input_frame, text="Generate Jadwal", command=self._on_generate)
        self.run_button.grid(row=row, column=0, pady=8, sticky=tk.W)
        self.status_label = ttk.Label(self.input_frame, text="Siap")
        self.status_label.grid(row=row, column=1, columnspan=3, sticky=tk.W)

    def _build_outputs(self) -> None:
        self.warning_label = ttk.Label(self.output_frame, text="", foreground="#a00")
        self.warning_label.pack(anchor=tk.W, pady=(0, 6))

        self.metrics_label = ttk.Label(self.output_frame, text="")
        self.metrics_label.pack(anchor=tk.W, pady=(0, 6))

        schedule_frame = ttk.LabelFrame(self.output_frame, text="Jadwal Rekomendasi")
        schedule_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=4)

        schedule_scroll = ttk.Scrollbar(schedule_frame, orient=tk.VERTICAL)
        self.schedule_tree = ttk.Treeview(
            schedule_frame,
            show="headings",
            height=10,
            yscrollcommand=schedule_scroll.set,
        )
        schedule_scroll.config(command=self.schedule_tree.yview)
        schedule_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.schedule_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        summary_frame = ttk.LabelFrame(self.output_frame, text="Ringkasan Satpam")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=4)

        summary_scroll = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL)
        self.summary_tree = ttk.Treeview(
            summary_frame,
            show="headings",
            height=8,
            yscrollcommand=summary_scroll.set,
        )
        summary_scroll.config(command=self.summary_tree.yview)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def _normalize_names(self, raw: str, count: int, prefix: str) -> List[str]:
        raw = raw.strip()
        if not raw:
            if prefix == "S":
                return [f"S{str(i + 1).zfill(2)}" for i in range(count)]
            return [f"{prefix} {i + 1}" for i in range(count)]
        names = [part.strip() for part in raw.split(",") if part.strip()]
        if len(names) < count:
            for i in range(len(names), count):
                if prefix == "S":
                    names.append(f"S{str(i + 1).zfill(2)}")
                else:
                    names.append(f"{prefix} {i + 1}")
        elif len(names) > count:
            names = names[:count]
        return names

    def _build_problem(self) -> ShiftProblem:
        building_count = self.var_building_count.get()
        guard_count = self.var_guard_count.get()
        guards_per_shift = self.var_guards_per_shift.get()
        min_days_off = self.var_min_days_off.get()

        if building_count <= 0 or guard_count <= 0 or guards_per_shift <= 0:
            raise ValueError("Jumlah gedung, satpam, dan satpam per shift harus > 0")
        if min_days_off < 0 or min_days_off > 6:
            raise ValueError("Hari libur min harus di antara 0 sampai 6")

        buildings = self._normalize_names(self.var_building_names.get(), building_count, "Gedung")
        guards = self._normalize_names(self.var_guard_names.get(), guard_count, "S")

        return ShiftProblem(
            buildings=buildings,
            guards=guards,
            guards_per_shift=guards_per_shift,
            min_days_off=min_days_off,
        )

    def _update_warning(self, problem: ShiftProblem) -> None:
        total_required = (
            len(problem.days)
            * len(problem.shifts)
            * len(problem.buildings)
            * problem.guards_per_shift
        )
        max_per_guard = len(problem.days) - problem.min_days_off
        max_capacity = max_per_guard * len(problem.guards)

        warning = ""
        if max_capacity < total_required:
            warning = (
                "Jumlah satpam tidak mencukupi untuk memenuhi seluruh shift secara adil. "
                "Tambah satpam atau kurangi gedung/shift/hari libur."
            )
        self.warning_label.config(text=warning)

    def _on_generate(self) -> None:
        try:
            problem = self._build_problem()
        except ValueError as exc:
            messagebox.showerror("Input tidak valid", str(exc))
            return

        self._update_warning(problem)

        config = GAConfig(
            population_size=self.var_pop_size.get(),
            generations=self.var_generations.get(),
            tournament_size=self.var_tournament.get(),
            crossover_rate=self.var_crossover.get(),
            mutation_rate=self.var_mutation.get(),
            elite_count=self.var_elite.get(),
            seed=self.var_seed.get(),
        )

        gene_mutation_rate = self.var_gene_mutation.get()
        weights = PenaltyWeights()

        self.run_button.config(state=tk.DISABLED)
        self.status_label.config(text="Menjalankan GA...")

        thread = threading.Thread(
            target=self._run_ga_thread,
            args=(problem, config, weights, gene_mutation_rate),
            daemon=True,
        )
        thread.start()

    def _run_ga_thread(
        self,
        problem: ShiftProblem,
        config: GAConfig,
        weights: PenaltyWeights,
        gene_mutation_rate: float,
    ) -> None:
        def create_fn(rng):
            return create_individual(problem, rng)

        def fitness_fn(genome):
            return evaluate_schedule(genome, problem, weights)[0]

        def mutate_fn(genome, rng):
            return mutate_random_reset(
                genome, rng, guard_count=len(problem.guards), gene_mutation_rate=gene_mutation_rate
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

        self.root.after(
            0,
            lambda: self._update_output(problem, rows, summaries, metrics, fitness),
        )

    def _update_output(
        self,
        problem: ShiftProblem,
        rows: List[List[str]],
        summaries: List[dict],
        metrics,
        fitness: float,
    ) -> None:
        self._render_schedule_table(problem, rows)
        self._render_summary_table(summaries)

        metrics_text = (
            f"Fitness: {fitness:.2f} | "
            f"Kurang satpam/shift: {metrics.missing_guards} | "
            f"Double shift/hari: {metrics.double_shift_days} | "
            f"Kekurangan libur: {metrics.day_off_shortage} | "
            f"Stdev beban: {metrics.workload_stdev:.2f} | "
            f"Repeat gedung: {metrics.building_repeat_excess:.2f}"
        )
        self.metrics_label.config(text=metrics_text)

        self.status_label.config(text="Selesai")
        self.run_button.config(state=tk.NORMAL)

    def _render_schedule_table(self, problem: ShiftProblem, rows: List[List[str]]) -> None:
        columns = ["Hari", "Gedung", "Shift"] + [
            f"Satpam {i + 1}" for i in range(problem.guards_per_shift)
        ]
        self.schedule_tree.config(columns=columns)
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=120, anchor=tk.W)

        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        for row in rows:
            self.schedule_tree.insert("", tk.END, values=row)

    def _render_summary_table(self, summaries: List[dict]) -> None:
        columns = ["Satpam", "Total Shift", "Gedung", "Keterangan"]
        self.summary_tree.config(columns=columns)
        for col in columns:
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, width=140, anchor=tk.W)

        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)

        for summary in summaries:
            self.summary_tree.insert(
                "",
                tk.END,
                values=(
                    summary["name"],
                    summary["total_shifts"],
                    summary["buildings"],
                    summary["label"],
                ),
            )


def main() -> None:
    root = tk.Tk()
    app = ShiftSchedulerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
