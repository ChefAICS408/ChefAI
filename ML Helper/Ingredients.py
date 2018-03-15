import pandas
import numpy as np
import pickle



def parseIngredients():

    file = open("epi_r_attributes_removed.csv", "r")
    arr = pandas.read_csv(file, nrows=1, header=None)

    arr = np.asarray(arr)
    arr = arr[0][11:]
    print(arr)

    f = open("./assets/parsed_ingredients.txt", "w")
    for i in arr:
        i = i.replace(" ", "_").replace("/", "_").replace("-", "_")
        f.write(i + "\n")
    f.close()

    f = open("./assets/parsed_ingredients.list", "wb")
    pickle.dump(arr, f)
    f.close()

def cleanCSV():
    file = open("epi_r_1.csv", "r")
    arr = pandas.read_csv(file, header=None)

    arr = np.asarray(arr)
    arr = arr[:, 11:]
    print(arr.shape)

    f = open("ToRemove.csv", "r")
    toremove = pandas.read_csv(f, header=None)
    toremove = np.asarray(toremove)

    newarr = []

    for i in range(len(arr)):
        temp = []
        for j in toremove[0]:
            print(i)
            temp.append(arr[i][int(j)])
        newarr.append(temp)

    df = pandas.DataFrame(newarr)
    df.to_csv("epi_r_attributes_removed.csv", index=False, header=False)



cleanCSV()
parseIngredients()

