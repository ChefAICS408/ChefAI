import numpy as np
import pandas
import pickle
import random
import math


def scoreVector(vector, z):
    if len(vector) == 0 or len(vector) == 1:
        return 0
    score = 0
    for i in range(len(vector)):
        for j in range(i + 1, len(vector)):
            score += z[vector[i]][vector[j]]

    return score / math.sqrt(len(vector))

def findIngredientSubset(orig_vector, to_consider, z, depth):

    if depth == 15:
        print("HEREREEREEE")
        return scoreVector(to_consider, z), to_consider

    score1, set1 = findIngredientSubset(orig_vector, to_consider, z, depth+1)
    to_consider_1 = to_consider + [orig_vector[depth]]
    score2, set2 = findIngredientSubset(orig_vector, to_consider_1, z, depth+1)

    new_score = max([score1, score2])
    print("score = " + str(new_score))
    if new_score == score1:
        return new_score, set1
    else:
        return new_score, set2


if __name__ == "__main__":
    data = pandas.read_csv("new_ingredient_vectors.csv", header=None)
    data = np.asarray(data)

    headers = data[0]

    data = data[1:, :]
    data = np.asarray(data, dtype=float)
    print(headers)
    print(data)
    print(data.shape)
    data = np.transpose(data)
    print(data.shape)

    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

    with open("./assets/firsts.list", "rb") as fp:  # Unpickling
        firsts = pickle.load(fp)

    z = np.dot(data, data.T)
    print(z)

    test_ingredients = []
    for i in range(15):
        test_ingredients.append(random.randint(0, len(z) - 1))


    max_score, final_ingredietns = findIngredientSubset(test_ingredients, [], z, 0)
    print("Test INGREDIENTS")
    for i in test_ingredients:
        print(headers[i])
    print("FINAL INGREDIENTS")
    for i in final_ingredietns:
        print(headers[i])

    step_data = pandas.read_csv("step_ingredient_probs.csv", header=None)
    step_data = np.asarray(step_data)
    step_data = step_data[1:, :]
    step_data = np.asarray(step_data, dtype=float)
    print(step_data)


    steps = []

    for i in final_ingredietns:
        steps.append(np.argmax(step_data[:,i]))

    #for i in range(len(headers)):
    #    steps.append(np.argmax(data[:,i]))

    print(steps)

    first_idx = np.argmax(firsts[steps])
    print("First = " + verbs[steps[first_idx]])

    for i in range(len(steps)):
        print(verbs[steps[i]] + " -> " + headers[final_ingredietns[i]])







