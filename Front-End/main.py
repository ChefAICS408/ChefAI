import cluster
import json
import pickle
import numpy as np
import actionverbingr


class ML:


    def __init__(self):
        self.data = json.load(open("cleaned_dataset.json"))
        with open("./static/assets/title.list", "rb") as fp:
            self.titles = pickle.load(fp)
        with open("./static/assets/protein.list", "rb") as fp:
            self.proteins = pickle.load(fp)
        with open("./static/assets/calorie.list", "rb") as fp:
            self.calories = pickle.load(fp)
        with open("./static/assets/sodium.list", "rb") as fp:
            self.sodium = pickle.load(fp)
        with open("./static/assets/fat.list", "rb") as fp:
            self.fat = pickle.load(fp)
        self.all_recipe_start = 0
        self.all_recipe_threshold = 10
        self.ids = np.arange(0, len(self.titles))

        self.sortby = "original"
        self.order = "0"

        self.titleProteins = self.titles
        self.iDsProteins = self.ids

        self.titleFats = self.titles
        self.iDsFats = self.ids

        self.titleSodium = self.titles
        self.iDsSodium = self.ids

        self.titleCalories = self.titles
        self.iDsCalories = self.ids

    def getRecipe(self, page, id, content):
        self.all_recipe_start = self.all_recipe_threshold*(page-1)

        if content == "original":
            #self.all_recipe_start = 0
            return self.data[self.ids[self.all_recipe_threshold*(page-1) + id]]

        if content == "protein":
            return self.data[self.iDsProteins[self.all_recipe_threshold*(page-1) + id]]
        if content == "fat":
            return self.data[self.iDsFats[self.all_recipe_threshold*(page-1) + id]]
        if content == "sodium":
            return self.data[self.iDsSodium[self.all_recipe_threshold*(page-1) + id]]
        if content == "calorie":
            return self.data[self.iDsCalories[self.all_recipe_threshold*(page-1) + id]]


    # def getAllRecipes(self, content, order):

    #     if content == "original":
    #         self.all_recipe_start = 0
    #         return self.titles[self.all_recipe_start: self.all_recipe_start + self.all_recipe_threshold]

    #     # if content == "protein":
    #     #     self.sortDataProtein(order)
    #     #     return self.titleProteins[self.all_recipe_start: self.all_recipe_start + self.all_recipe_threshold]

    #     if content == "fat":
    #         self.sortDataFat(order)
    #         return self.titleFats[self.all_recipe_start: self.all_recipe_start + self.all_recipe_threshold]

    #     if content == "sodium":
    #         self.sortDataSodium(order)
    #         return self.titleSodium[self.all_recipe_start: self.all_recipe_start + self.all_recipe_threshold]

    #     if content == "calorie":
    #         self.sortDataCalories(order)
    #         return self.titleCalories[self.all_recipe_start: self.all_recipe_start + self.all_recipe_threshold]

    #     return self.titles[self.all_recipe_start : self.all_recipe_start + self.all_recipe_threshold]


    # def onClickNext(self):
    #     self.all_recipe_start += self.all_recipe_threshold
    #     if self.all_recipe_start >= len(self.titles):
    #         self.all_recipe_start += self.all_recipe_threshold
    #         # return []
    #     return self.titles[self.all_recipe_start : min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]
    #
    # def onClickPrevios(self):
    #     self.all_recipe_start -= self.all_recipe_threshold
    #     if self.all_recipe_start < 0:
    #         self.all_recipe_start += self.all_recipe_threshold
    #         # return []
    #     result = self.titles[self.all_recipe_start : min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]
    #
    #     return result

    def get10recipes(self, parameter, content, order):

        print(parameter)
        print(content)
        print(order)

        self.all_recipe_start = self.all_recipe_threshold*(parameter-1)

        if content == "original":
            #self.all_recipe_start = 0
            return self.titles[
                 self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

        if content == "protein":
            self.sortDataProtein(order)
            return self.titleProteins[
                 self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

        if content == "fat":
            self.sortDataFat(order)
            return self.titleFats[
                 self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

        if content == "sodium":
            self.sortDataSodium(order)
            return self.titleSodium[
                 self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]

        if content == "calorie":
            self.sortDataCalories(order)
            return self.titleCalories[
                 self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]


        #
        # result = self.titles[
        #          self.all_recipe_start: min((self.all_recipe_start + self.all_recipe_threshold), len(self.titles))]
        # return result


    def onClickSubmit(self, toInclude, toExclude, computer_generated):
        if computer_generated:
            return actionverbingr.computerGenerated(toInclude)
        else:
            i, l = cluster.findRecipe(toInclude, toExclude)
            if i == None:
                return None, l
            else:
                return self.data[i], l



    def sortDataProtein(self, order):

        np_proteins = np.array(self.proteins)
        np_titles = np.array(self.titles)
        np_ids = np.array(self.ids)
        if (order == "0"):
            np_proteins = np.array([float("inf") if v is None else v for v in np_proteins])
        else:
            np_proteins = np.array([-float("inf") if v is None else v for v in np_proteins])

        idx = np.ma.argsort(np_proteins)
        if (order == "1"):
            idx = idx[::-1]

        self.titleProteins = np_titles[idx]
        self.iDsProteins = np_ids[idx]

    def sortDataFat(self, order):

        np_fats = np.array(self.fat)
        np_titles = np.array(self.titles)
        np_ids = np.array(self.ids)
        if (order == "0"):
            np_fats = np.array([float("inf") if v is None else v for v in np_fats])
        else:
            np_fats = np.array([-float("inf") if v is None else v for v in np_fats])

        idx = np.ma.argsort(np_fats)
        if (order == "1"):
            idx = idx[::-1]

        self.titleFats = np_titles[idx]
        self.iDsFats = np_ids[idx]

    def sortDataSodium(self, order):

        np_sodium = np.array(self.sodium)
        np_titles = np.array(self.titles)
        np_ids = np.array(self.ids)
        if (order == "0"):
            np_sodium = np.array([float("inf") if v is None else v for v in np_sodium])
        else:
            np_sodium = np.array([-float("inf") if v is None else v for v in np_sodium])

        idx = np.ma.argsort(np_sodium)
        if (order == "1"):
            idx = idx[::-1]

        self.titleSodium = np_titles[idx]
        self.iDsSodium = np_ids[idx]

    def sortDataCalories(self, order):
        np_calories = np.array(self.calories)
        np_titles = np.array(self.titles)
        np_ids = np.array(self.ids)
        if (order == "0"):
            np_calories = np.array([float("inf") if v is None else v for v in np_calories])
        else:
            np_calories = np.array([-float("inf") if v is None else v for v in np_calories])

        idx = np.ma.argsort(np_calories)
        if (order == "1"):
            idx = idx[::-1]

        self.titleCalories = np_titles[idx]
        self.iDsCalories = np_ids[idx]






