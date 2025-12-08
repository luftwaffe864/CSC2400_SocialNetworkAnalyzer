# Checkpoint3
##########
# Credit Statement:
# We only worked within our group
# The author(s) acknowledge the utilization of ChatGPT, a language model developed by OpenAI, in the preparation of this assignment.
# ChatGPT was employed in the following manners within this assignment: The ways specified in the assignment such as, how to read/generate files with python.
##########
INF = 10**9  # a large "infinity" value


def read_users_file(filename: str = "users.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = len(lines)  # should be 100
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    next_node = [[None] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dist[i][i] = 0

    for line in lines:
        clean = line.replace("[", "").replace("]", "")
        parts = clean.split()
        user_label = parts[0]
        u = int(user_label.split("_")[1])  # turn "user_1" into 1

        friend_labels = parts[2:]
        for friend_label in friend_labels:
            v = int(friend_label.split("_")[1])
            if dist[u][v] > 1:
                dist[u][v] = 1
                dist[v][u] = 1
                next_node[u][v] = v
                next_node[v][u] = u

    return n, dist, next_node


def floyd_warshall(n, dist, next_node):
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if dist[i][k] == INF:
                continue
            for j in range(1, n + 1):
                if dist[k][j] == INF:
                    continue
                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist
                    next_node[i][j] = next_node[i][k]


def reconstruct_path(i, j, next_node):
    if next_node[i][j] is None:
        return None  # no path

    path = [i]
    while i != j:
        i = next_node[i][j]
        if i is None:
            return None
        path.append(i)
    return path


def write_path_lengths(n, dist, filename: str = "path_lengths.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                if dist[i][j] >= INF:
                    f.write("-1\n")
                else:
                    f.write(f"{dist[i][j]}\n")


def write_connections(n, next_node, filename: str = "connections.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                path = reconstruct_path(i, j, next_node)
                if path is None:
                    f.write("no_connection\n")
                else:
                    # Convert indices back to labels like "user_1"
                    labels = [f"user_{v}" for v in path]
                    f.write(" ".join(labels) + "\n")


def main():
    n, dist, next_node = read_users_file("users.txt")

    floyd_warshall(n, dist, next_node)

    write_path_lengths(n, dist, "path_lengths.txt")

    write_connections(n, next_node, "connections.txt")


if __name__ == "__main__":
    main()
