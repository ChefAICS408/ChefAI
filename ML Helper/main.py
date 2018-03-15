import json
import pickle
import numpy as np


class ML:

    def __init__(self):
        self.data = json.load(open("cleaned_dataset.json"))
        with open("./assets/title.list", "rb") as fp:
            self.titles = pickle.load(fp)
        with open("./assets/protein.list", "rb") as fp:
            self.proteins = pickle.load(fp)
        self.all_recipe_start = 0
        self.all_recipe_threshold = 10
        self.ids = np.arange(0, len(self.titles))

    def getRecipe(self, id):
        return self.data[self.ids[self.all_recipe_start + id]]

    def getAllRecipes(self):
        return self.titles[self.all_recipe_start : self.all_recipe_start + self.all_recipe_threshold]


    def onClickNext(self):
        self.all_recipe_start += self.all_recipe_threshold
        if self.all_recipe_start >= len(self.titles):
            return []
        return self.titles[self.all_recipe_start : min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

    def onClickPrevios(self):
        self.all_recipe_start -= self.all_recipe_threshold
        if self.all_recipe_start < 0:
            return []
        result = self.titles[self.all_recipe_start : min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

        return result

    def sortData(self):

        np_proteins = np.array(self.proteins)
        np_titles = np.array(self.titles)
        np_ids = np.array(self.ids)
        np_proteins = np.array([-float("inf") if v is None else v for v in np_proteins])

        idx = np.ma.argsort(np_proteins)
        np_proteins = np_proteins[idx]
        np_titles = np_titles[idx]
        np_ids = np_ids[idx]

        print(np_proteins)
        print(np_titles)
        print(np_ids)