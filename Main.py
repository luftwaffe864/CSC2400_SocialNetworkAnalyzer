import copy
import time

#This is the command to get the time in nanoseconds, _ms for milliseconds if needed
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

    BubbleSort(copy.deepcopy(users)) # calls (i) bubble sort
    BubbleSort_2(copy.deepcopy(users)) # calls (ii) bubble sort

    merge_sort(users, key=lambda u: (u["posts"], u ["name"]), reverse=False) # calls (i) merge sort

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
# (ii) Bubble Sort
def BubbleSort_2(users):
    # method to call the number of posts for each user in the friends list
    def get_posts(friend_name):
        for u in users:
            if u["name"] == friend_name:
                return u["posts"]
        return None

    with open("userfriendsBubSort.txt", "w") as file:
        for user in users:
            friends = user["friends"]
            k = len(friends)

            for i in range(k - 1):
                didswap = False

                for j in range(k - 1 - i):
                    if get_posts(friends[j]) > get_posts(friends[j + 1]):
                        friends[j], friends[j + 1] = friends[j + 1], friends[j]
                        didswap = True

                if not didswap:
                    break

            # writing to file
            file.write(user["name"]+ " [")
            for friend in friends:
                file.write(f"{friend}, ")
            file.write(f"] \n")

    return None
############################################################################

############################################################################
# (i) Merge Sort
def merge_sort(arr, key=lambda x: x, reverse=False):
    def _merge_sort(a):
        if len(a) <= 1:
            return a
    
        mid = len(a) // 2
        left = merge_sort(a[:mid], key, reverse)
        right = merge_sort(a[mid:], key, reverse)
    
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
    # print test (prints whole file)
    # for u in users[:100]:
    #     print(f"{u['name']}: {u['posts']} friends → {u['friends']}")

############################################################################

############################################################################
def merge_sort2(users, ascending=True):
    # allows a faster lookup combining user and posts
    users_posts = {u["name"]: u["posts"] for u in users}

    # Grabs the index from the user for the output order
    def user_index(name: str) -> int:
        try:
            return int(name.split("_")[1])
        except Exc:
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

    users_in_order = sorted(users, key=lambda u: user_index(u["name"]))

    with open("userfriends_MerSort.txt", "w") as outFile:
        for u in users_in_order:
            # Sorts the friends list by their posts, and if same number of posts, then go by user number
            friends = list(u["friends"])
            sorted_friends = msort(friends, key=lambda fname: (posts_by_user.get(fname, 0), fname),
                                  reverse=not ascending)
            outFile.write(f"{u['name']} [{' '.join(sorted_friends)}]\n")
            
# end of file
if __name__ == "__main__":
    main()
