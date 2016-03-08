dict = {"lol":1}

dict["ninja"] = 2

index = {hash("lol"):["lol", {"aID1":1}]}

print index

print index[hash("lol")][1]

index[hash("lol")][1]["aID1"] += 1
index[hash("lol")][1]["aID2"] = 1



print index[hash("lol")][1]
