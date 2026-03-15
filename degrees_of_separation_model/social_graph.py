import random


class RandomSocialGraph:
    def __init__(self, n_users=0, n_edges=0, model=None):
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
            
        if n_users and n_edges:
            # switch statement for future graph generation models (e.g. preferential attachment)
            switch = {
                "naive": self.randomize_minimally_connected,
                "minimally_connected": self.randomize_minimally_connected,
                "watts_strogatz": self.randomize_watts_strogatz,
                "barabasi_albert": self.randomize_barabasi_albert,
            }
            if model in switch:
                switch[model](n_edges)
            else:
                self.randomize_minimally_connected(n_edges)

    def add_user(self, user):
        if user not in self.network:
            self.network[user] = set()
        else:
            raise ValueError(f"User {user} already exists in the network.")

    def add_friendship(self, user1, user2):
        # For an undirected graph (mutual friendship)
        if user1 in self.network and user2 in self.network:
            if user2 in self.network[user1]:
                raise ValueError(
                    f"Users {user1} and {user2} are already friends.")

            self.network[user1].add(user2)
            self.network[user2].add(user1)

        else:
            missing_users = []
            if user1 not in self.network:
                missing_users.add(user1)
            if user2 not in self.network:
                missing_users.add(user2)

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
        # Check if we can add n_edges without exceeding the maximum possible edges in the graph
        max_edges = len(self.network) * (len(self.network) - 1) // 2
        num_edgs_in_graph = sum(len(friends)
                                for friends in self.network.values()) // 2
        total_edges = n_edges + num_edgs_in_graph
        if total_edges > max_edges:
            raise ValueError(
                f"Cannot add {n_edges} edges. "
                f"Maximum possible edges for {len(self.network)} users is {max_edges}, """
                f"and the graph already has {num_edgs_in_graph} edges. "
                f"(total_edges = n_edges + existing edges = {total_edges})."
            )

        # Make a list of all possible user pairs that are not currently friends
        possible_friendships = set()
        users = self.network.keys()
        for u in list(users):
            # only consider pairs (u, v) where v is not already a friend of u and v != u
            for v in list(users - self.network[u] - {u}):
                # Sort the pair (u, v) to avoid duplicates like (u, v) and (v, u)
                possible_friendships.add(tuple(sorted((u, v))))
                
        # Randomly select n_edges pairs from the possible friendships and add them to the graph
        edges_to_add = random.sample(list(possible_friendships), n_edges)
        for u, v in edges_to_add:
            self.add_friendship(u, v)

    def randomize_minimally_connected(self, n_edges):
        self.make_minimum_spanning_tree()
        self.add_n_random_friendships(n_edges - len(self.network) + 1)

    def randomize_watts_strogatz(self, n_edges):
        
        pass
    
    def randomize_barabasi_albert(self, n_edges):
        pass

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
