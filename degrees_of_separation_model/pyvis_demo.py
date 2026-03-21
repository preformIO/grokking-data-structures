from social_graph import RandomSocialGraph
from pyvis.network import Network


def random_social_graph_to_pyvis_network(graph):
    net = Network(notebook=True, height="500px", width="100%")
    for user, friends in graph.network.items():
        net.add_node(user, label=str(user), color="orange")
        for friend in friends:
            net.add_node(friend, label=str(friend), color="orange")
            net.add_edge(user, friend)
    return net


def main():
    # This demo script showcases both automated and manual graph generation 
    # using the RandomSocialGraph class.

    # Defaults
    n = 100  # Number of users
    e = 150  # Number of friendships (edges)

    # ---------------------------------------------------------
    # 1.a. Automated Generation (Naive Random Graph)
    # ---------------------------------------------------------
    print("--- Automated Graph Generation (Naive Random Graph) ---")
    # Instantiating with n_users and n_edges automatically calls 
    # randomize_minimally_connected() [1].
    # This in turn calls make_minimum_spanning_tree() 
    # and add_n_random_friendships() [1].
    try:
        auto_graph_naive = RandomSocialGraph(
            n_users=n, n_edges=e, model="naive")
        print(
            f"Automated Graph Network dictionary: {auto_graph_naive.network}\n")
    except Exception as e:
        print(f"Automated generation error: {e}\n")

    # ---------------------------------------------------------
    # 1.b. Automated Generation (Watts-Strogatz Small-World Graph)
    # ---------------------------------------------------------
    print("--- Automated Graph Generation (Watts-Strogatz Small-World Graph) ---")
    try:
        auto_graph_watts_strogatz = RandomSocialGraph(
            n_users=n, n_edges=e, model="watts_strogatz")
        print(
            f"Automated Graph Network dictionary: {auto_graph_watts_strogatz.network}\n")
    except Exception as e:
        print(f"Automated generation error: {e}\n")

    # ----------------------------------------------------------
    # 1.c. Automated Generation (Barabási-Albert Scale-Free Graph)
    # ---------------------------------------------------------
    print("--- Automated Graph Generation (Barabási-Albert Scale-Free Graph) ---")
    try:
        auto_graph_barabasi_albert = RandomSocialGraph(
            n_users=n, n_edges=e, model="barabasi_albert")
        print(
            f"Automated Graph Network dictionary: {auto_graph_barabasi_albert.network}\n")
    except Exception as e:
        print(f"Automated generation error: {e}\n")

    # ---------------------------------------------------------
    # 2. Manual Graph Population
    # ---------------------------------------------------------
    print("--- Manual Graph Generation ---")
    manual_graph = RandomSocialGraph()

    # Adding users to the network [1]
    users = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    for user in users:
        manual_graph.add_user(user)

    # Adding mutual friendships (undirected edges) [1]
    manual_graph.add_friendship("Alice", "Bob")
    manual_graph.add_friendship("Alice", "Charlie")
    manual_graph.add_friendship("Bob", "Diana")
    manual_graph.add_friendship("Charlie", "Eve")
    manual_graph.add_friendship("Diana", "Eve")

    print(f"Manual Graph Network dictionary: {manual_graph.network}\n")

    # ---------------------------------------------------------
    # 3. Viewing in vscode.dev using PyVis
    # ---------------------------------------------------------
    print("--- Generating PyVis Interactive Visualization ---")

    # Save and render the interactive HTML file for the manual graph
    output_file = "manual_graph_vis.html"
    net = random_social_graph_to_pyvis_network(manual_graph)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")

    # Save and render the interactive HTML file for the automated graph (naive approach)
    output_file = "automated_graph_naive_vis.html"
    net = random_social_graph_to_pyvis_network(auto_graph_naive)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")

    # Save and render the interactive HTML file for the automated graph (Watts-Strogatz)
    output_file = "automated_graph_watts_strogatz_vis.html"
    net = random_social_graph_to_pyvis_network(auto_graph_watts_strogatz)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")

    # Save and render the interactive HTML file for the automated graph (Barabási-Albert)
    output_file = "automated_graph_barabasi_albert_vis.html"
    net = random_social_graph_to_pyvis_network(auto_graph_barabasi_albert)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")


if __name__ == "__main__":
    main()
