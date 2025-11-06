import copy

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



    # print test (prints whole file)
    # for u in users[:100]:
    #     print(f"{u['name']}: {u['posts']} friends → {u['friends']}")

# end of file
if __name__ == "__main__":
    main()