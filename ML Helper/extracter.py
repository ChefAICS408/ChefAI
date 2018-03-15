import pickle

if __name__ == "__main__":

    verb_file = open("verbs.txt", "r")
    verbs_string = verb_file.readline()
    verbs = verbs_string.split(" - ")
    verbs = [x.lower() for x in verbs]
    print(verbs)
    verb_file.close()

    with open("./assets/directions.list", "rb") as fp:  # Unpickling
        data = pickle.load(fp)

    with open("./assets/parsed_ingredients.list", "rb") as fp:
        parsed_ingredients = pickle.load(fp)

    parsed_directions = []

    verbs_hash = {}

    i = 0
    for rec in data[:10]:
        new_directions = []
        for step in rec:
            sub_steps = step.split(".")
            for sub_step in sub_steps:
                sub_step_cleaned = sub_step.lower()
                sub_step_cleaned = sub_step_cleaned.replace(",", "")
                sub_step_words = sub_step_cleaned.split(" ")
                j = 0
                for word in sub_step_words:
                    if word in verbs:
                        new_directions.append(word)
                    elif word in parsed_ingredients:
                        new_directions.append(word)
                        print("found noun")

                    try:
                        verbs_hash[word] += 1
                    except KeyError:
                        verbs_hash[word] = 1
                        continue
        parsed_directions.append(new_directions)
        # print(i)
        i += 1


    print(parsed_directions)
    '''
    f = open("parsed_directions.txt", "w")
    for i in range(len(parsed_directions)):
        f.write(str(parsed_directions[i]) + "\n")
    f.close()
    with open("parsed_directions.list", "wb") as fp:  # Pickling
        pickle.dump(parsed_directions, fp)
    print("DONE CREATING parsed_directions\n")
    '''

    print(data[0])
