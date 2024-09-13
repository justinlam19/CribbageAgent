import csv, pickle

with open("python/dealer.pkl", "rb") as f:
    t = pickle.load(f)
    with open("python/dealer.csv", "w+") as c:
        w = csv.writer(c)
        w.writerows(t)

with open("python/nondealer.pkl", "rb") as f:
    t = pickle.load(f)
    with open("python/nondealer.csv", "w+") as c:
        w = csv.writer(c)
        w.writerows(t)
