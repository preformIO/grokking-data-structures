class RandomSocialGraph:
    def __init__(self, n_users=0, n_edges=0):
        # The graph: { "User": ["Friend1", "Friend2"] }
        self.network = dict() # equivalent to {}

        # Add specified number of nodes to the graph
        for i in range(n_users):
            self.add_user(i)

        # Add specified number of edges
        if n_edges < (n_users-1):
            raise ValueError(
                f"n_edges must be > n_users - 1 in order for graph to be fully connected.\n"
                f"    {n_users = }, {n_edges = }"
            )
        if n_edges > (n_users) * (n_users-1) // 2: # https://brainly.com/question/37683068
            raise ValueError(
                f"n_edges cannot be > n_users*(n_users-1)/2.\n"
                f"    {n_users = }, {n_edges = }"
            )
        self.randomize_fully_connected(n_edges)

    def add_user(self, user):
        if user not in self.network:
            self.network[user] = set()

    def add_friendship(self, user1, user2):
        # For an undirected graph (mutual friendship)
        if user1 in self.network and user2 in self.network:
            self.network[user1].add(user2)
            self.network[user2].add(user1)

        else:
            missing_users = []
            if user1 not in self.network:
                missing_users.add(user1)
            if user2 not in self.network:
                missing_users.add(user2)
            
            raise ValueError(f"Cannot find user(s) in the network: {missing_users}")
        
    def make_minimum_spanning_tree(self):
        pass

    def add_n_random_friendships(self, n_edges):
        pass

    def randomize_fully_connected(self, n_edges):
        self.make_minimum_spanning_tree()
        self.add_n_random_friendships(n_edges - len(self.network) + 1)

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
