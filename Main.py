def main():

    # read from file
    users = []

    with open("users.txt", "r") as file:
        for line in file:
            name, posts, f_list = line.split(" ", 2)
            posts = int(posts)

            friends = f_list.strip()[1:-1].split()

            users.append({
                "name": name,
                "posts": posts,
                "friends": friends
            })









    # print test (prints whole file)
    # for u in users[:100]:
    #     print(f"{u['name']}: {u['posts']} friends → {u['friends']}")





# end of file
if __name__ == "__main__":
    main()