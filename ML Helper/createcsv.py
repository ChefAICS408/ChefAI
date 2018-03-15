import pandas
import numpy as np
import json





if __name__ == "__main__":

    cleaned_json = json.load(open("cleaned_dataset.json"))
    data = pandas.read_csv("epi_r_attributes_removed.csv", header=None)
    data = np.asarray(data)

    headers = data[0]

    new_csv = np.zeros((len(cleaned_json), len(headers)))

    for i in range(len(cleaned_json)):
        ingredients = cleaned_json[i]["ingredients"]
        for step in ingredients:
            for j in range(len(headers)):
                if headers[j] in step:
                    new_csv[i][j] = 1
        print("Recipe " + str(i) + " done.")

    df = pandas.DataFrame(new_csv)
    df.to_csv("new_ingredient_vectors.csv", index=False, header=headers)



