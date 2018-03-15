import pickle
import numpy as np
import pandas
import json

def createVerbNoun():

    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

    cleaned_json = json.load(open("cleaned_dataset.json"))
    data = pandas.read_csv("epi_r_attributes_removed.csv", header=None)
    data = np.asarray(data)

    headers = data[0]

    new_csv = np.zeros((len(verbs), len(headers)))


    for i in range(len(cleaned_json)):
        directions = cleaned_json[i]["directions"]
        for step in directions:
            substeps = step.split(".")
            for sub_step in substeps:
                sub_step_cleaned = sub_step.lower()
                sub_step_cleaned = sub_step_cleaned.replace(",", "")

                sub_step_words = sub_step_cleaned.split(" ")

                to_look = ""
                j = 0
                while j < len(sub_step_words):
                    if sub_step_words[j] in verbs:
                        temp = j
                        to_look = ""
                        k = j + 1
                        while k < len(sub_step_words):
                            if sub_step_words[k] in verbs:
                                j = k - 1
                                break
                            to_look += sub_step_words[k] + " "
                            k += 1
                        j = k - 1
                        for l in range(len(headers)):
                            if headers[l] in to_look:
                                new_csv[verbs.index(sub_step_words[temp])][l] += 1
                    j += 1

        print("Recipe " + str(i) + " done.")


    new_csv += 1
    print(new_csv)
    print(new_csv.shape)

    df = pandas.DataFrame(new_csv)
    df.to_csv("step_ingredient_probs.csv", index=False, header=headers)


def createFirstVerb():

    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

    cleaned_json = json.load(open("cleaned_dataset.json"))
    data = pandas.read_csv("epi_r_attributes_removed.csv", header=None)
    data = np.asarray(data)

    headers = data[0]
    data = data[1:, :]
    data = np.asarray(data, dtype=int)


    new_csv = np.zeros((len(verbs), len(headers)))
    firsts = np.zeros(len(verbs))

    for i in range(len(cleaned_json)):
        directions = cleaned_json[i]["directions"]
        for step in directions:
            sub_step_cleaned = step.lower()
            sub_step_cleaned = sub_step_cleaned.replace(",", "").replace(".", "")

            sub_step_words = sub_step_cleaned.split(" ")
            stop = False
            for word in sub_step_words:
                if word in verbs:
                    idx = verbs.index(word)
                    ingrs = np.where(data[i] == 1)[0]
                    new_csv[idx][ingrs] += 1
                    stop = True
                    break
            if stop:
                break

        print("Recipe " + str(i) + " done.")

    new_csv += 1
    print(new_csv)

    df = pandas.DataFrame(new_csv)
    df.to_csv("first_verb_probs.csv", index=False, header=headers)



def createNextVerb():
    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

    cleaned_json = json.load(open("cleaned_dataset.json"))
    data = pandas.read_csv("epi_r_attributes_removed.csv", header=None)
    data = np.asarray(data)

    headers = data[0]

    new_csv = np.zeros((len(verbs), len(headers), len(verbs)))


    for i in range(len(cleaned_json)):
        directions = cleaned_json[i]["directions"]
        for step in directions:
            substeps = step.split(".")
            for sub_step in substeps:
                sub_step_cleaned = sub_step.lower()
                sub_step_cleaned = sub_step_cleaned.replace(",", "")

                sub_step_words = sub_step_cleaned.split(" ")

                to_look = ""
                j = 0
                while j < len(sub_step_words):
                    if sub_step_words[j] in verbs:
                        temp = j
                        to_look = ""
                        k = j + 1
                        while k < len(sub_step_words):
                            nextVerb = ""
                            if sub_step_words[k] in verbs:
                                nextVerb = sub_step_words[k]
                                j = k - 1
                                break
                            to_look += sub_step_words[k] + " "
                            k += 1
                        j = k - 1
                        if nextVerb != "":
                            for l in range(len(headers)):
                                if headers[l] in to_look:
                                    new_csv[verbs.index(sub_step_words[temp])][l][verbs.index(nextVerb)] += 1
                    j += 1

        print("Recipe " + str(i) + " done.")

    new_csv += 1
    temp1 = np.reshape(new_csv, (len(verbs) * len(headers) * len(verbs)))
    print(temp1.shape)

    df = pandas.DataFrame(temp1)
    df.to_csv("next_verb_probs.csv", index=False, header=False)

    temp2 = pandas.read_csv("next_verb_probs.csv", header=None)
    temp2 = np.asarray(temp2)
    temp2 = np.reshape(temp2, (len(verbs), len(headers), len(verbs)))

    print(np.array_equal(new_csv, temp2))





createVerbNoun()
createFirstVerb()
createNextVerb()