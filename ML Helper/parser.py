import json
import pickle
import nltk
import pandas
import numpy as np


def CleanJsonAndEPI(data):

    file = open("epi_r.csv", "r")
    arr = pandas.read_csv(file, header=None)
    arr = np.asarray(arr)

    j = 0
    toRemove_data = []
    toRemove_arr = []
    for i in range(len(arr) - 1):
        try:
            if (i + j >= len(data)):
                break
            if (data[i]["title"]) != arr[i + 1 - j][0]:
                print(i + j)
                toRemove_data.append(i)
                j += 1
        except KeyError:
            print("ERROR " + str(i))
            toRemove_data.append(i)
            toRemove_arr.append(i + 1 - j)
    print()
    '''
    print("TESTING")
    for i in range(len(data)):
        if data[i]["title"] != arr[i + 1][0]:
            print("ERROR")
    print("END TESTING")
    '''

    for i in range(len(toRemove_data)):
        data.pop(toRemove_data[i] - i)

    arr = np.delete(arr, toRemove_arr, 0)

    with open('cleaned_dataset.json', 'w') as fp:
        json.dump(data, fp)

    df = pandas.DataFrame(arr)
    df.to_csv("epi_r_1.csv", index=False, header=False)

    print(toRemove_data)
    print(toRemove_arr)
    print()
    print(len(data))
    print(len(arr))




if __name__ == "__main__":
    print("START")
    data = json.load(open("cleaned_dataset.json"))
    print("DONE READING DATA\n")


    # DATA
    # [directions] - List of steps
    # [fat] - Fat content in decimal
    # [date] - Date in datetime format
    # [categories] - List of categories
    # [calories] - Decimal value
    # [desc] - Description string
    # [protein] - Protein content decimal value
    # [rating] - Recipe rating decimal value
    # [title] - Title string
    # [ingredients] - List of ingredients with amount
    # [sodium] - Sodium content decimal value

    '''
    # CREATING DIRECTIONS ======================= #
    directions = []
    f = open("./assets/directions.txt", "w")
    for i in range(len(data)):
        try:
            directions.append(data[i]["directions"])
            f.write(str(data[i]["directions"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/directions.list", "wb") as fp:  # Pickling
        pickle.dump(directions, fp)
    print("DONE CREATING directions\n")



    # CREATING INGREDIENTS ======================= #
    ingredients = []
    f = open("./assets/ingredients.txt", "w")
    for i in range(len(data)):
        try:
            ingredients.append(data[i]["ingredients"])
            f.write(str(data[i]["ingredients"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/ingredients.list", "wb") as fp:  # Pickling
        pickle.dump(ingredients, fp)
    print("DONE CREATING ingredients\n")



    # CREATING FATS ======================= #
    fats = []
    f = open("./assets/fat.txt", "w")
    for i in range(len(data)):
        try:
            fats.append(data[i]["fat"])
            f.write(str(data[i]["fat"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/fat.list", "wb") as fp:  # Pickling
        pickle.dump(fats, fp)
    print("DONE CREATING fats\n")


    # CREATING PROTEINS ======================= #
    proteins = []
    f = open("./assets/protein.txt", "w")
    for i in range(len(data)):
        try:
            proteins.append(data[i]["protein"])
            f.write(str(data[i]["protein"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/protein.list", "wb") as fp:  # Pickling
        pickle.dump(proteins, fp)
    print("DONE CREATING proteins\n")



    # CREATING Titles ======================= #
    titles = []
    f = open("./assets/title.txt", "w")
    for i in range(len(data)):
        try:
            titles.append(data[i]["title"])
            f.write(str(data[i]["title"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/title.list", "wb") as fp:  # Pickling
        pickle.dump(titles, fp)
    print("DONE CREATING titles\n")
    

    # CREATING FATS ======================= #
    fats = []
    f = open("./assets/calorie.txt", "w")
    for i in range(len(data)):
        try:
            fats.append(data[i]["calories"])
            f.write(str(data[i]["calories"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/calorie.list", "wb") as fp:  # Pickling
        pickle.dump(fats, fp)
    print("DONE CREATING calorie\n")

    # CREATING FATS ======================= #
    fats = []
    f = open("./assets/sodium.txt", "w")
    for i in range(len(data)):
        try:
            fats.append(data[i]["sodium"])
            f.write(str(data[i]["sodium"]) + "\n")
        except KeyError:
            print(i)
    f.close()
    with open("./assets/sodium.list", "wb") as fp:  # Pickling
        pickle.dump(fats, fp)
    print("DONE CREATING sodium\n")
    '''
