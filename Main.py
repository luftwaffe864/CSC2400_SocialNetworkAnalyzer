import copy
import time
import matplotlib.pyplot as plt  # for the extra credit plot

# This is the command to get the time in nanoseconds, _ms for milliseconds if needed
# start_time_ns = time.perf_counter_ns()
# end_time_ns = time.perf_counter_ns()
# elapsed_time_ns = end_time_ns - start_time_ns

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

    BubbleSort(copy.deepcopy(users))  # (i) bubble sort
    bub_times = BubbleSort_2(copy.deepcopy(users))  # (ii) bubble sort — returns per-user times

    merge_sort(users, key=lambda u: (u["posts"], u["name"]), reverse=False)  # (i) merge sort
    mer_times = merge_sort2(copy.deepcopy(users), ascending=True)  # (ii) merge sort — returns per-user times

    # Write per-user runtimes in user_1..user_100 order
    with open("runtimes.txt", "w") as rt:
        n = len(users)
        for i in range(1, n + 1):
            uname = f"user_{i}"
            bt = bub_times.get(uname, 0)
            mt = mer_times.get(uname, 0)
            rt.write(f"({bt}, {mt})\n")

    # --- EXTRA CREDIT: create plot ---
    plot_runtimes()


############################################################################
# (i) Bubble Sort
def BubbleSort(users):
    with open("userposts_BubSort.txt", "w") as file:
        n = len(users)
        for i in range(n - 1):
            didswap = False

            for j in range(n - 1 - i):
                if users[j]["posts"] > users[j + 1]["posts"]:
                    users[j], users[j + 1] = users[j + 1], users[j]
                    didswap = True

            if not didswap:
                break

        # writing to file
        for user in users:
            file.write(user["name"] + " " + str(user["posts"]) + "\n")

    return None
############################################################################

############################################################################
# (ii) Bubble Sort for Friend Lists
def BubbleSort_2(users):
    # method to call the number of posts for each user in the friends list
    def get_posts(friend_name):
        for u in users:
            if u["name"] == friend_name:
                return u["posts"]
        return None

    bub_times = {}
    with open("userfriendsBubSort.txt", "w") as file:
        for user in users:
            friends = user["friends"]
            k = len(friends)

            start_ns = time.perf_counter_ns()
            for i in range(k - 1):
                didswap = False
                for j in range(k - 1 - i):
                    if get_posts(friends[j]) > get_posts(friends[j + 1]):
                        friends[j], friends[j + 1] = friends[j + 1], friends[j]
                        didswap = True
                if not didswap:
                    break
            end_ns = time.perf_counter_ns()
            bub_times[user["name"]] = end_ns - start_ns

            # writing to file (cleaner format)
            file.write(f"{user['name']} [{' '.join(friends)}]\n")

    return bub_times
############################################################################

############################################################################
# (i) Merge Sort
def merge_sort(arr, key=lambda x: x, reverse=False):
    def _merge_sort(a):
        if len(a) <= 1:
            return a

        mid = len(a) // 2
        left = _merge_sort(a[:mid])     # <-- recurse on helper
        right = _merge_sort(a[mid:])    # <-- recurse on helper

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            keyL, keyR = key(left[i]), key(right[j])
            takeLeft = (keyL <= keyR and not reverse) or (keyL >= keyR and reverse)
            if takeLeft:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1

        if i < len(left): merged.extend(left[i:])
        if j < len(right): merged.extend(right[j:])
        return merged

    sorted_arr = _merge_sort(list(arr))

    with open("userposts_MerSort.txt", "w") as outFile:
        for u in sorted_arr:
            outFile.write(u["name"] + " " + str(u["posts"]) + "\n")

    return sorted_arr
############################################################################

############################################################################
# (ii) Merge Sort for Friend Lists
def merge_sort2(users, ascending=True):
    # allows a faster lookup combining user and posts
    users_posts = {u["name"]: u["posts"] for u in users}

    # Grabs the index from the user for the output order
    def user_index(name: str) -> int:
        try:
            return int(name.split("_")[1])
        except Exception:
            return 10**9

    def msort(arr, key=lambda x: x, reverse=False):
        a = list(arr)
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = msort(a[:mid], key, reverse)
        right = msort(a[mid:], key, reverse)

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            keyL, keyR = key(left[i]), key(right[j])
            takeLeft = (keyL <= keyR and not reverse) or (keyL >= keyR and reverse)
            if takeLeft:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        if i < len(left): merged.extend(left[i:])
        if j < len(right): merged.extend(right[j:])
        return merged

    mer_times = {}
    users_in_order = sorted(users, key=lambda u: user_index(u["name"]))

    with open("userfriends_MerSort.txt", "w") as outFile:
        for u in users_in_order:
            # Sorts the friends list by their posts, and if same number of posts, then go by user number
            friends = list(u["friends"])
            start_ns = time.perf_counter_ns()
            sorted_friends = msort(
                friends,
                key=lambda fname: (users_posts.get(fname, 0), user_index(fname)),
                reverse=not ascending
            )
            end_ns = time.perf_counter_ns()
            mer_times[u["name"]] = end_ns - start_ns

            outFile.write(f"{u['name']} [{' '.join(sorted_friends)}]\n")

    return mer_times
############################################################################

############################################################################
# Extra Credit: Plot Runtimes
def plot_runtimes():
    bub_times = []
    mer_times = []

    # Read runtimes.txt
    with open("runtimes.txt", "r") as file:
        for line in file:
            line = line.strip("()\n ")
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                bub_times.append(int(parts[0]))
                mer_times.append(int(parts[1]))

    # Plot both lines
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(bub_times) + 1), bub_times, label="Bubble Sort", marker='o', linewidth=1)
    plt.plot(range(1, len(mer_times) + 1), mer_times, label="Merge Sort", marker='x', linewidth=1)
    plt.title("Sorting Algorithm Runtimes per User")
    plt.xlabel("User Index")
    plt.ylabel("Runtime (nanoseconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot to file
    plt.savefig("runtimes_plot.png")
    plt.close()
############################################################################

# end of file
if __name__ == "__main__":
    main()
