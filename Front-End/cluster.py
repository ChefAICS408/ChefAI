from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import pandas
import pickle
from sklearn.decomposition import PCA
import random
from scipy import spatial


def perf_pca(data):
    pca = PCA(n_components=220)
    data = pca.fit_transform(data)
    addi = 0
    for i in range(len(pca.explained_variance_ratio_)):
        addi += pca.explained_variance_ratio_[i]
        print(str(i) + ": " + str(addi))
    return data


def perf_kmeans(data):
    k_values = range(2, 10)
    for k in k_values:
        model = KMeans(n_clusters=k)
        print("FITTING NOW")
        z = model.fit_predict(data)

        print(z)
        with open("cluster_predicions.list", "wb") as fp:  # Pickling
            pickle.dump(z, fp)

        # np.append(data, z, axis=1)

        print("k = " + str(k) + " - Score = " + str(silhouette_score(data, z)))


def findClosestVector(vector, data, clusters):
    max_close = -1
    min_dist = 0

    toLook = np.where(vector == 1)[0]

    final = np.arange(0, len(data))

    temp_look = []

    for i in toLook:
        temp_look = []
        similar = clusters[i]
        for j in similar:
            temp_look = set(temp_look).union(set(np.where(data[final, j] == 1)[0]))
        final = list(temp_look)

    print(temp_look)

    for i in range(len(data)):
        # temp_dist = (1 - spatial.distance.cosine(vector, data[i]))
        temp_dist = vector @ data[i].T
        if min_dist < temp_dist:
            max_close = i
            min_dist = temp_dist

    print(min_dist)
    return max_close



def scoreVector(vector, z):
    if len(vector) == 0 or len(vector) == 1:
        return 0
    score = 0
    for i in range(len(vector)):
        for j in range(i + 1, len(vector)):
            score += z[vector[i]][vector[j]]
            print(str(vector[i]) + " + " + str(vector[j]) + " = " + str(z[vector[i]][vector[j]]))

    return score / (float(len(vector)) - 1)




def findIngredientSubset(orig_vector, to_consider, z, depth):

    if depth == 5:
        score = scoreVector(to_consider, z)
        print("score = " + str(score) + " vec = " + str(to_consider))
        return score, to_consider

    score1, set1 = findIngredientSubset(orig_vector, to_consider, z, depth+1)
    to_consider_1 = to_consider + [orig_vector[depth]]
    score2, set2 = findIngredientSubset(orig_vector, to_consider_1, z, depth+1)

    new_score = max([score1, score2])
    if new_score == score1:
        return new_score, set1
    else:
        return new_score, set2



def findClosestRecipe(final, data):

    to_consier = []

    for i in range(len(data)):
        correct = True
        for j in final:
            if data[i][j] != 1:
                correct = False
                break
        if correct:
            to_consier.append(i)

    print(to_consier)
    return to_consier[0]





def findRecipe(to_include):

    data = pandas.read_csv("static/assets/new_ingredient_vectors.csv", header=None)
    data = np.asarray(data)

    headers = data[0]

    data = data[1:,:]
    data = np.asarray(data, dtype=int)
    print(headers)
    print(data)

    n_samples, n_features = data.shape
    print(data.shape)

    data = np.transpose(data)
    print(data.shape)

    # data = perf_pca(data)

    # perf_kmeans(data)

    z = np.dot(data, data.T)

    print(z)

    clusters = {}

    for i in range(len(z)):
        if i not in clusters.keys():
            clusters[i] = []
        for j in range(len(z[0])):
            if z[i][j] > 20:
                clusters[i].append(j)


    #random.seed()           # 1101 is interesting
    # test_ingredients = [1, 5, 100, 24, 16, 244, 167, 190, 200, 87]
    test_ingredients = []
    #for i in range(5):
    #    test_ingredients.append(random.randint(0, len(z) - 1))

    test_ingredients = []
    for i in to_include:
        test_ingredients.append(list(headers).index(i))

    print(test_ingredients)

    final_ingredietns = []
    '''
    for i in range(len(test_ingredients)):
        for j in range(len(test_ingredients)):
            if test_ingredients[j] in clusters[test_ingredients[i]] and test_ingredients[j] not in final_ingredietns:
                final_ingredietns.append(test_ingredients[j])
        print("Temp for " + str(test_ingredients[i]) + " - " + str(final_ingredietns))
    '''
    max_score = 0

    '''
    for i in range(len(test_ingredients)):
        print("Considering " + str(headers[test_ingredients[i]]) + " as first")
        temp = [test_ingredients[i]]
        temp_score = 0
        j = 0
        while True:
            if j >= len(temp):
                break
            toLook = clusters[temp[j]]
            for k in range(len(test_ingredients)):
                if k == i:
                    continue
                if (test_ingredients[k] in toLook) and (test_ingredients[k] not in temp):
                    temp.append(test_ingredients[k])
                    temp_score += z[test_ingredients[i]][test_ingredients[k]]
            j += 1
        print("Final Temp for " + str(test_ingredients[i]) + " - " + str(temp))
        if temp_score > max_score:
            max_score = temp_score
            final_ingredietns = []
            for i in temp:
                final_ingredietns.append(i)

    '''

    max_score = 0
    final_ingredietns = []

    max_score, final_ingredietns = findIngredientSubset(test_ingredients, [], z, 0)


    print("MAXSCORE = " + str(max_score))
    print("TEST INGREDIENTS")
    for i in test_ingredients:
        print(headers[i])

    print()
    print("FINAL INGREDIENTS")
    for i in final_ingredietns:
        print(headers[i])



    new_vector = np.zeros(len(data))

    #print(new_vector.shape)

    for i in final_ingredietns:
        new_vector[i] = 1
        #toLook = clusters[i]
        #for j in toLook:
            #new_vector[j] += 0.5
            #new_vector[j] = 1

    with open("./static/assets/title.list", "rb") as fp:
        titles = pickle.load(fp)
    with open("./static/assets/ingredients.list", "rb") as fp:
        ingr = pickle.load(fp)


    recipe = findClosestRecipe(final_ingredietns, data.T)

    #recipe = findClosestVector(new_vector, data.T, clusters)
    indx = recipe
    print(recipe)

    itpingr = ingr[recipe]
    recipe = titles[recipe]
    print(recipe)
    print(itpingr)

    return indx








