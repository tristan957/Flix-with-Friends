def getFriends():
    friends = []
    f = open("friends.txt", "r")
    for line in f:
        if line != "\n":
            line = line.rstrip()
            friends.append(line)
    f.close()
    return friends

def addFriend(name):
    f = open("friends.txt", "a")
    f.write(name + "\n")
    f.close()

def deleteFriend(name):
    friends = getFriends()
    f = open("friends.txt", "w")
    if name in friends:
        friends.remove(name)
        for friend in friends:
            f.write(friend + "\n")
    f.close()
