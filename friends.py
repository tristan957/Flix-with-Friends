def getFriends():
    friendsList = []

    f = open("friends.txt", "r")

    for line in f:
        if line != "\n":
            line = line.rstrip()
            friendsList.append(line)
    return friendsList

#def addFriend():

#def deleteFriend():
