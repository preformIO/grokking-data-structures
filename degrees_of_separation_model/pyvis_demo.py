from social_graph import RandomSocialGraph
from pyvis.network import Network

def to_pyvis_network(graph):
    net = Network(notebook=True, height="500px", width="100%")
    for user, friends in graph.network.items():
        net.add_node(user, label=str(user), color="#00ff1e")
        for friend in friends:
            net.add_node(friend, label=str(friend), color="#00ff1e")
            net.add_edge(user, friend)
    return net

def main():
    # ---------------------------------------------------------
    # 1. Automated Generation (Using future functionality)
    # ---------------------------------------------------------
    print("--- Automated Graph Generation ---")
    # Instantiating with n_users and n_edges automatically calls randomize_fully_connected() [1].
    # This in turn calls make_minimum_spanning_tree() and add_n_random_friendships() [1].
    try:
        # We request 6 users and 10 edges.
        auto_graph = RandomSocialGraph(n_users=6, n_edges=10)
        print(f"Automated Graph Network dictionary: {auto_graph.network}\n")
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
    net = to_pyvis_network(manual_graph)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")

    # Save and render the interactive HTML file for the automated graph
    output_file = "automated_graph_vis.html"
    net = to_pyvis_network(auto_graph)
    net.show(output_file)
    print(
        f"Interactive graph saved to {output_file}. Open this in your browser to explore!")


if __name__ == "__main__":
    main()
