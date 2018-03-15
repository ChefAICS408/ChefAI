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
    data = np.transpose(data)
    print(data.shape)

    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

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

    first_verb = pandas.read_csv("first_verb_probs.csv", header=None)
    first_verb = np.asarray(first_verb)
    first_verb = first_verb[1:, :]
    first_verb = np.asarray(first_verb, dtype=float)
    #print(first_verb)
    print(first_verb.shape)

    next_ingr = pandas.read_csv("step_ingredient_probs.csv", header=None)
    next_ingr = np.asarray(next_ingr)
    next_ingr = next_ingr[1:, :]
    next_ingr = np.asarray(next_ingr, dtype=float)
    #print(next_ingr)
    print(next_ingr.shape)


    next_verb = pandas.read_csv("next_verb_probs.csv", header=None)
    next_verb = np.asarray(next_verb)
    next_verb = np.reshape(next_verb, (len(verbs), len(headers), len(verbs)))
    next_verb = np.asarray(next_verb, dtype=float)
    #print(next_verb)
    print(next_verb.shape)

    max_first = -1
    max_first_idx = -1
    for i in range(len(verbs)):
        v_sum = sum(first_verb[i])
        p_v = float(v_sum) / np.sum(first_verb)
        p_i = 1
        for j in final_ingredietns:
            p_i *= float(first_verb[i][j]) / v_sum
        if max_first < (p_v * p_i):
            max_first = p_v * p_i
            max_first_idx = i
    print(verbs[max_first_idx])


    prev_verb = max_first_idx


    while len(final_ingredietns) > 0:
        # Find Ingredient and then next verb
        max_ingr = -1
        max_ingr_idx = -1
        for i in final_ingredietns:
            i_sum = np.sum(next_ingr[:,i])
            p_i = float(i_sum) / np.sum(next_ingr)
            p_v_i = float(next_ingr[prev_verb][i]) / i_sum

            if max_ingr < p_i * p_v_i:
                max_ingr = p_i * p_v_i
                max_ingr_idx = i
        print(headers[max_ingr_idx])
        print()

        final_ingredietns.remove(max_ingr_idx)

        # Find next verb based on prev verb and ingr
        max_next_verb = -1
        max_next_verb_idx = -1
        for i in range(len(verbs)):
            v_sum = np.sum(next_verb[:,:,i])
            p_v = float(v_sum) / np.sum(next_verb)
            p_v_i = float(next_verb[prev_verb][max_ingr_idx][i]) / v_sum
            if max_next_verb < (p_v_i * p_v):
                max_next_verb = (p_v_i * p_v)
                max_next_verb_idx = i
        print(verbs[max_next_verb_idx])

        prev_verb = max_next_verb_idx






















