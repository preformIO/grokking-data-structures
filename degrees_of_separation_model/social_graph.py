import random


class RandomSocialGraph:
    def __init__(self, n_users=0, n_edges=0, m0=5, beta=0.5, model='naive'):
        # The graph: { "User": ["Friend1", "Friend2"] }
        self.network = dict()  # equivalent to {}

        # Add specified number of nodes to the graph
        for i in range(n_users):
            self.add_user(i)

        # Add specified number of edges
        if n_edges < (n_users-1):
            raise ValueError(
                f"n_edges must be > n_users - 1 in order for graph to be fully connected.\n"
                f"    {n_users = }, {n_edges = }"
            )
        # https://brainly.com/question/37683068
        if n_edges > (n_users) * (n_users-1) // 2:
            raise ValueError(
                f"n_edges cannot be > n_users*(n_users-1)/2.\n"
                f"    {n_users = }, {n_edges = }"
            )

        # Model reference: https://medium.com/data-science/what-are-small-world-network-models-87bbcfe0e038
        if n_users and n_edges:
            if model == "naive" or model == "minimally_connected" or model == "erdos_renyi":
                self.randomize_erdos_renyi(n_edges)
            elif model == "watts_strogatz":
                self.randomize_watts_strogatz(n_edges, beta)
            elif model == "barabasi_albert":
                self.randomize_barabasi_albert(n_edges, m0)
            else:
                raise ValueError(
                    f"Invalid model type: '{model}'. "
                    f"Choose from 'naive', 'minimally_connected', 'erdos_renyi', "
                    f"'watts_strogatz', or 'barabasi_albert'."
                )

    def add_user(self, user):
        if user not in self.network:
            self.network[user] = set()
        else:
            raise ValueError(f"User '{user}' already exists in the network.")

    def add_friendship(self, user1, user2):
        # For an undirected graph (mutual friendship)
        if user1 in self.network and user2 in self.network:
            if user2 in self.network[user1]:
                raise ValueError(
                    f"Users '{user1}' and '{user2}' are already friends.")

            self.network[user1].add(user2)
            self.network[user2].add(user1)

        else:
            missing_users = []
            if user1 not in self.network:
                missing_users.append(user1)
            if user2 not in self.network:
                missing_users.append(user2)

            raise ValueError(
                f"Cannot find user(s) in the network: {missing_users}")

    def make_minimum_spanning_tree(self):
        # If the graph has edges already, raise an error
        if any(len(friends) > 0 for friends in self.network.values()):
            raise ValueError(
                "Graph must have no edges to create a minimum spanning tree.")

        # Start with a set of all users and an empty set for connected users
        all_users = set(self.network.keys())
        connected_users = set()

        # Add one random user to the connected set and remove from the all_users set
        initial_user = random.choice(list(all_users))
        connected_users.add(initial_user)
        all_users.remove(initial_user)

        # While there are still unconnected users, connect them to the connected set
        while all_users:
            # Randomly select one user from the connected set and one unconnected user
            u = random.choice(list(connected_users))
            v = random.choice(list(all_users))

            # Connect the two users
            self.add_friendship(u, v)

            # Move the newly connected user to the connected set
            all_users.remove(v)
            connected_users.add(v)

    def add_n_random_friendships(self, n_edges):
        # Check if we can add n_edges without exceeding the maximum 
        # possible edges in the graph
        max_edges = len(self.network) * (len(self.network) - 1) // 2
        num_edges_in_graph = sum(
                len(friends) for friends in self.network.values()
            ) // 2
        total_edges = n_edges + num_edges_in_graph
        if total_edges > max_edges:
            raise ValueError(
                f"Cannot add {n_edges} edges. "
                f"Maximum possible edges for {len(self.network)} users is {max_edges}, "
                f"and the graph already has {num_edges_in_graph} edges. "
                f"(total_edges = n_edges + existing edges = {total_edges})."
            )

        # Make a list of all possible user pairs that are not currently friends
        possible_friendships = set()
        users = self.network.keys()
        for u in list(users):
            # only consider pairs (u, v) where v is not already a friend 
            # of u and v != u
            for v in list(users - self.network[u] - {u}):
                # Sort the pair (u, v) to avoid duplicates like (u, v) and (v, u)
                possible_friendships.add(tuple(sorted((u, v))))

        # Randomly select n_edges pairs from the possible friendships and 
        # add them to the graph
        edges_to_add = random.sample(list(possible_friendships), n_edges)
        for u, v in edges_to_add:
            self.add_friendship(u, v)

    def randomize_erdos_renyi(self, n_edges):
        self.make_minimum_spanning_tree()
        self.add_n_random_friendships(n_edges - (len(self.network) - 1))

    def create_ring_lattice(self, k):
        """
        Helper function to create a regular ring lattice.
        Each user is connected to k nearest neighbors (k/2 on each side).
        """
        users = list(self.network.keys())
        n = len(users)

        for i in range(n):
            # Connect to k/2 neighbors on the right (undirected handles the left automatically)
            for j in range(1, (k // 2) + 1):
                neighbor_index = (i + j) % n

                # Use the existing class method to add the friendship safely
                if users[neighbor_index] not in self.network[users[i]]:
                    self.add_friendship(users[i], users[neighbor_index])

    def randomize_watts_strogatz(self, n_edges, beta):
        """
        Implements the Watts-Strogatz small-world graph model.
        """
        users = list(self.network.keys())
        n_users = len(users)

        # Derive the mean degree (k) based on the exact number of requested edges
        # (Since total edges in a regular lattice = n * k / 2)
        k = (2 * n_edges) // n_users

        # 1. Build the foundational structured ring lattice
        self.create_ring_lattice(k)

        # Gather all current edges to consider them for rewiring
        existing_edges = set()
        for u in users:
            for v in self.network[u]:
                existing_edges.add(tuple(sorted((u, v))))

        # 2. The rewiring process
        for u, v in existing_edges:
            if random.random() < beta:
                # Disconnect the existing local tie
                self.network[u].remove(v)
                self.network[v].remove(u)

                # Find a new random target that prevents self-loops and duplicate edges
                possible_targets = [
                    w for w in users
                    if w != u and w not in self.network[u]
                ]

                if possible_targets:
                    new_target = random.choice(possible_targets)
                    self.add_friendship(u, new_target)

        # Top off any missing edges due to integer division when calculating 'k'
        current_edges = sum(len(friends)
                            for friends in self.network.values()) // 2
        if current_edges < n_edges:
            self.add_n_random_friendships(n_edges - current_edges)

    def randomize_barabasi_albert(self, n_edges, m0):
        """
        Implements the Barabási-Albert scale-free network model.
        m0: The size of the initial fully-connected seed network.
        """
        users = list(self.network.keys())
        n_users = len(users)

        if n_users < m0:
            raise ValueError(
                "Total users must be greater than the seed size (m0).")

        # 'm' is the number of edges each new node will form.
        # We estimate 'm' to get as close to n_edges as possible.
        m = n_edges // (n_users - m0) if (n_users - m0) > 0 else 1
        if m < 1:
            m = 1
        if m > m0:
            m = m0  # In standard BA models, m <= m0

        # 1. Growth: Initialize the seed network of m0 nodes
        # We will make them a fully-connected clique to start.
        seed_users = users[:m0]
        for i in range(m0):
            for j in range(i + 1, m0):
                self.add_friendship(seed_users[i], seed_users[j])

        # degree_list acts as a "roulette wheel" for preferential attachment.
        # Every time a node gains an edge, it is added to this list again.
        degree_list = []
        for u in seed_users:
            degree_list.extend([u] * len(self.network[u]))

        # 2. Preferential Attachment: Add the remaining nodes sequentially
        for i in range(m0, n_users):
            new_user = users[i]
            targets = set()

            # Pick m distinct targets preferentially
            while len(targets) < m and len(targets) < len(self.network):
                # Because high-degree nodes appear in degree_list more often,
                # random.choice naturally simulates preferential attachment.
                target = random.choice(degree_list)

                # Avoid self-loops and duplicate edges
                if target != new_user and target not in targets:
                    targets.add(target)

            # Register the friendships and update our degree tracker
            for target in targets:
                self.add_friendship(new_user, target)
                degree_list.extend([new_user, target])

        # Ensure we exactly hit n_edges (since m integer division is an approximation)
        current_edges = sum(len(friends)
                            for friends in self.network.values()) // 2
        if current_edges < n_edges:
            self.add_n_random_friendships(n_edges - current_edges)


if __name__ == "__main__":
    graph = RandomSocialGraph()

    print(f"{graph = }")
    print(f"{graph.network = }")

    graph.add_user("david")
    graph.add_user("Harrison")

    print(f"{graph.network = }")

    graph.add_user("Isabel")
    graph.add_user("Lily")
    graph.add_user("Bob")
    graph.add_user("Rafael")
    graph.add_user("Jude")

    graph.add_friendship('david', 'Isabel')
    graph.add_friendship('david', 'Lily')
    graph.add_friendship('david', 'Harrison')
    graph.add_friendship('Harrison', 'Rafael')
    graph.add_friendship('Harrison', 'Jude')

    print(f"{graph.network = }")

    # Test errors
    try:
        graph.add_friendship('Ford', 'Charlie')
    except Exception as e:
        print(e)
    try:
        print(f"{ 1/0 = }")
    except Exception as e:
        print(e)

    graph_2 = RandomSocialGraph(15, 14)
    print(f"{graph_2 = }")
    print(f"{graph_2.network = }")

    graph_3 = RandomSocialGraph(15, 105)
    print(f"{graph_3 = }")
    print(f"{graph_3.network = }")

    try:
        graph_4 = RandomSocialGraph(15, 13)
    except Exception as e:
        print(e)

    try:
        graph_5 = RandomSocialGraph(15, 2_000_000)
    except Exception as e:
        print(e)
