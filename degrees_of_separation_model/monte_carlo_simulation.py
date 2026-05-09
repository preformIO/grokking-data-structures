import csv
import math
from pathlib import Path
import time

from pyvis_demo import save_graph_visualization
from social_graph import RandomSocialGraph


# Monte Carlo constants
NUM_GRAPHS = 1000
NUM_NODES = 100
NUM_EDGES = 150
M0 = 5
W = 10
MODEL = "barabasi_albert"


def pearson_correlation(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0

    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)

    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    sum_sq_x = sum((x - mean_x) ** 2 for x in xs)
    sum_sq_y = sum((y - mean_y) ** 2 for y in ys)

    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    if denominator == 0:
        return 0.0

    return numerator / denominator


def run_monte_carlo_simulation(num_graphs=NUM_GRAPHS, num_nodes=NUM_NODES):
    rows = []
    mean_separation_values = []
    degree_stdev_values = []
    sample_graph = None

    last_update_time = time.time()
    for graph_index in range(1, num_graphs + 1):
        graph = RandomSocialGraph(
            n_users=num_nodes,
            n_edges=NUM_EDGES,
            m0=M0,
            w=W,
            model=MODEL,
        )

        if sample_graph is None:
            sample_graph = graph

        graph_stats = graph.get_graph_stats()
        mean_degree_connection = graph.degree_mean()
        degree_distribution = graph.degree_distribution()

        average_degree_of_separation = graph_stats["average_degree_of_separation"]
        stdev_degree_of_connection = graph_stats[
            "standard_deviation_of_degrees_of_connection"
        ]

        mean_separation_values.append(average_degree_of_separation)
        degree_stdev_values.append(stdev_degree_of_connection)

        rows.append(
            {
                "graph_id": graph_index,
                "model": MODEL,
                "n_nodes": num_nodes,
                "n_edges_target": NUM_EDGES,
                "m0": M0,
                "w": W,
                "average_degree_of_separation": average_degree_of_separation,
                "mean_degree_of_connection": mean_degree_connection,
                "standard_deviation_of_degrees_of_connection": stdev_degree_of_connection,
                "degree_distribution": str(degree_distribution),
            }
        )
        
        # Print progress every 2 seconds
        current_time = time.time()
        if current_time - last_update_time >= 2:
            print(f"Processed {graph_index}/{num_graphs} graphs...")
            last_update_time = current_time

    correlation = pearson_correlation(mean_separation_values, degree_stdev_values)

    return rows, correlation, sample_graph


def write_results_csv(rows, correlation, output_csv_path):
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "graph_id",
        "model",
        "n_nodes",
        "n_edges_target",
        "m0",
        "w",
        "average_degree_of_separation",
        "mean_degree_of_connection",
        "standard_deviation_of_degrees_of_connection",
        "degree_distribution",
        "pearson_correlation_mean_separation_vs_degree_stdev",
    ]

    with output_csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_with_correlation = dict(row)
            row_with_correlation[
                "pearson_correlation_mean_separation_vs_degree_stdev"
            ] = correlation
            writer.writerow(row_with_correlation)


def main():
    script_dir = Path(__file__).resolve().parent
    output_csv_path = script_dir / f"monte_carlo_{W}_simulation_results.csv"
    sample_graph_html_path = script_dir / f"monte_carlo_{W}_sample_graph_vis.html"

    rows, correlation, sample_graph = run_monte_carlo_simulation()
    write_results_csv(rows, correlation, output_csv_path)

    if sample_graph is not None:
        save_graph_visualization(sample_graph, str(sample_graph_html_path))

    print(f"Simulation completed for {NUM_GRAPHS} graphs.")
    print(f"Nodes per graph: {NUM_NODES}")
    print(f"Model: {MODEL} (m0={M0}, w={W})")
    print(f"Results CSV: {output_csv_path}")
    print(f"Sample graph HTML: {sample_graph_html_path}")
    print(
        "Pearson correlation (average degree of separation vs. degree stdev): "
        f"{correlation:.6f}"
    )


if __name__ == "__main__":
    main()
