import time
import random
import matplotlib.pyplot as plt

DESCENDING = True  # highest first

def main():
    # read from file
    users = []

    with open("users.txt", "r") as file:
        for line in file:
            name, posts, f_list = line.split(" ", 2)
            posts = int(posts)

            friends = f_list.strip()[1:-1].split()

            # adding data to a dictionary
            users.append({
                "name": name,
                "posts": posts,
                "friends": friends
            })

        # Parameters
        k = 20  # as specified
        # Produce SortSelect.txt (bubble sort then pick kth); returns per-user times
        sort_times = sort_select(users, k=k)
        # Produce QSelect.txt (QuickSelect); returns per-user times
        qsel_times = qselect(users, k=k)

        # Write runtimes.txt with (SortSelTimei, QSelTimei) in user_1..user_N order
        with open("runtimes.txt", "w", encoding="utf-8") as f:
            for i in range(1, len(users) + 1):
                uname = f"user_{i}"
                st = sort_times.get(uname, 0)
                qt = qsel_times.get(uname, 0)
                f.write(f"({st}, {qt})\n")

def user_index(name: str) -> int:
    try:
        return int(name.split("_")[1])
    except Exception:
        return 10**9

def bubble_sort_in_place(arr, key=lambda x: x, reverse=False):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            a = key(arr[j])
            b = key(arr[j + 1])
            if (a > b and not reverse) or (a < b and reverse):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def quickselect(arr, k_index, key=lambda x: x):
    # Returns the element that would be at position k_index (0-based) if arr were sorted ascending by key
    # Uses an iterative QuickSelect (Lomuto partition) to avoid recursion depth issues.
    a = list(arr)
    left, right = 0, len(a) - 1

    def partition(l, r, p_idx):
        pivot_key = key(a[p_idx])
        a[p_idx], a[r] = a[r], a[p_idx]
        store = l
        for i in range(l, r):
            if key(a[i]) < pivot_key:
                a[store], a[i] = a[i], a[store]
                store += 1
        a[store], a[r] = a[r], a[store]
        return store

    while left <= right:
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        if pivot_index == k_index:
            return a[pivot_index]
        elif k_index < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
    return None  # k out of bounds

def sort_select(users, k=20):
    # Maps for quick lookups
    posts_by_user = {u["name"]: u["posts"] for u in users}
    friend_count = {u["name"]: len(u["friends"]) for u in users}
    users_in_order = sorted(users, key=lambda u: user_index(u["name"]))

    sort_times_ns = {}
    with open("SortSelect.txt", "w", encoding="utf-8") as out:
        for u in users_in_order:
            friends = list(u["friends"])
            # Keys for descending rank: use negatives so ascending comparison works
            key_posts = lambda fname: (-posts_by_user.get(fname, 0), user_index(fname)) if DESCENDING \
                                      else (posts_by_user.get(fname, 0), user_index(fname))
            key_fcount = lambda fname: (-friend_count.get(fname, 0), user_index(fname)) if DESCENDING \
                                       else (friend_count.get(fname, 0), user_index(fname))

            # Time bubble sort + pick kth
            start_ns = time.perf_counter_ns()
            # (a) by posts
            friends_by_posts = list(friends)
            bubble_sort_in_place(friends_by_posts, key=key_posts, reverse=False)
            kth_posts = friends_by_posts[k - 1] if 1 <= k <= len(friends_by_posts) else "NA"
            # (b) by number of friends
            friends_by_fcount = list(friends)
            bubble_sort_in_place(friends_by_fcount, key=key_fcount, reverse=False)
            kth_fcount = friends_by_fcount[k - 1] if 1 <= k <= len(friends_by_fcount) else "NA"
            end_ns = time.perf_counter_ns()

            sort_times_ns[u["name"]] = end_ns - start_ns
            out.write(f"{u['name']} {kth_posts} {kth_fcount}\n")

    return sort_times_ns

def qselect(users, k=20):
    posts_by_user = {u["name"]: u["posts"] for u in users}
    friend_count = {u["name"]: len(u["friends"]) for u in users}
    users_in_order = sorted(users, key=lambda u: user_index(u["name"]))

    qsel_times_ns = {}
    with open("QSelect.txt", "w", encoding="utf-8") as out:
        for u in users_in_order:
            friends = list(u["friends"])
            if len(friends) < k or k <= 0:
                qsel_times_ns[u["name"]] = 0
                out.write(f"{u['name']} NA NA\n")
                continue

            # For descending rank, convert to an ascending key by negating the numeric metric
            key_posts = lambda fname: (-posts_by_user.get(fname, 0), user_index(fname)) if DESCENDING \
                                      else (posts_by_user.get(fname, 0), user_index(fname))
            key_fcount = lambda fname: (-friend_count.get(fname, 0), user_index(fname)) if DESCENDING \
                                       else (friend_count.get(fname, 0), user_index(fname))

            # Time QuickSelect for both features
            start_ns = time.perf_counter_ns()
            kth_by_posts = quickselect(friends, k - 1, key=key_posts)
            kth_by_fcount = quickselect(friends, k - 1, key=key_fcount)
            end_ns = time.perf_counter_ns()

            qsel_times_ns[u["name"]] = end_ns - start_ns
            out.write(f"{u['name']} {kth_by_posts} {kth_by_fcount}\n")

    return qsel_times_ns

def plot_runtimes():
    """Read runtimes.txt and plot Sort+Select vs QuickSelect times."""
    sort_times = []
    qsel_times = []

    # Read runtimes.txt
    with open("runtimes.txt", "r") as file:
        for line in file:
            # line format: (SortSelTime, QSelTime)
            line = line.strip("()\n ")
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                sort_times.append(int(parts[0]))
                qsel_times.append(int(parts[1]))

    if not sort_times or not qsel_times:
        print("[WARN] No runtimes found to plot.")
        return

    x_vals = range(1, len(sort_times) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, sort_times, label="Sort + Select (BubbleSort)", marker='o', linewidth=1)
    plt.plot(x_vals, qsel_times, label="QuickSelect", marker='x', linewidth=1)
    plt.title("Algorithm Runtimes per User (k = 20)")
    plt.xlabel("User Index")
    plt.ylabel("Runtime (nanoseconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot
    plt.savefig("runtimes_plot.png")
    plt.close()
    print("[INFO] Saved plot to runtimes_plot.png")

if __name__ == "__main__":
    main()
    plot_runtimes()
    
