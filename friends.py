def getFriends():
    friendsList = []

    f = open("friends.txt", "r")

    for line in f:
        if line != "\n":
            line = line.rstrip()
            friendsList.append(line)
    return friendsList

def addFriend(name):
    f = open("friends.txt", "a")
    f.write(name + "\n")


# def deleteFriend():
