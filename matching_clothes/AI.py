import os
import pickle
import indicoio
import json
import requests # pip install requests
import json     # pip install json
import matplotlib.pyplot as plt
from firebase import firebase
from operator import itemgetter
from PIL import Image
from indicoio.custom import Collection
from time import sleep
from google.cloud import firestore
indicoio.config.api_key = 'ae25a46523d9ac6a76b2a687ab477b16'

styles_list = ["Casual", "Bohemian", "Business", "Elegant", "Romantic", "Vintage", "Eclectic", "Rocker", "Sexy", "Denim", "Outdoor", "90s"]

def generate_training_data(fname):
    with open(fname, "rb") as f:
        for line in f:
            print(line)
            shirt, targets = line.decode().split(":")
            shirt_path = "training_shirts/{image}.jpg".format(
                image=shirt.strip()
            )
            shirt_path = os.path.abspath(shirt_path)

            # parse out the list of targets
            target_list = targets.strip()[1:-1].split(",")
            labels = map(lambda target: "label" + target.strip(), target_list)
            yield [ (shirt_path, label) for label in labels]
    raise StopIteration

def generate_selection_data(fname):
    with open(fname, "rb") as f:
        for line in f:
            print(line)
            shirt, targets = line.decode().split(":")
            shirt_path = "model_with_shirts/{image}.jpg".format(
                image=shirt.strip()
            )
            shirt_path = os.path.abspath(shirt_path)

            # parse out the list of targets
            target_list = targets.strip()[1:-1].split(",")
            labels = map(lambda target: "label" + target.strip(), target_list)
            yield [ (shirt_path, label) for label in labels]
    raise StopIteration


def make_img(im,im2):
    fig = plt.figure()
    plt.xticks([])
    plt.yticks([])
    fig.add_subplot(1, 1, 1)
    plt.imshow(im)
    fig.add_subplot(2, 1, 1)
    plt.imshow(im2)
    plt.axis('off')
    plt.show()

def what_style(file):
    # url name
    url = "https://fashion.recoqnitics.com/analyze"
    accessKey = "18f38db58e2375790160"
    secretKey = "f2c08046086c40ba811d5ff5fd46d26d9c0a4d78"

    # access_key and secret_key
    data = {'access_key': accessKey,
            'secret_key': secretKey}

    filename = {'filename': open(file, 'rb')}
    r = requests.post(url, files=filename, data=data)
    content = json.loads(r.content.decode('utf-8'))

    content_values = list(content.values())
    style = content_values[0]['styles'][0]['styleName']

    return (style, styles_list.index(style))

def main():

    #　Train Recommendation Model
    collection = Collection("clothes_collection")

    train = generate_training_data("clothes_match_labeled_data_2.txt")

    total = 0
    for samples in train:
        print("Adding {num} samples to collection".format(num=len(samples)))
        collection.add_data(samples)
        total += len(samples)
        print("Added {total} samples to collection thus far".format(total=total))

    collection.train()
    collection.wait()

    return_list = main2()
    f = open('store1.pckl','wb')
    pickle.dump((collection,return_list),f)
    f.close()

def main2():
    # Output selection list
    train = generate_selection_data("model_with_shirts.txt")
    model_with_shirts_list = []
    style_list = []
    return_list = []
    total = 0

    sort_key = itemgetter(1)
    f = open('store1.pckl', 'rb')
    collect = pickle.load(f)
    f.close()

    for samples in train:
        print("Adding {num} samples to collection".format(num=len(samples)))
        model_with_shirts_list.append(samples)
        total += len(samples)
        print("Added {total} samples to collection thus far".format(total=total))

    for i in model_with_shirts_list:
        print(i[0][0])
        head, tail = os.path.split(i[0][0])

        dict = { 'URL': tail, 'Style':what_style(i[0][0])[0], 'Pant': sorted(collect.predict(i[0][0]).items(), key=sort_key)[-1][0][5] }
        return_list.append(dict)

        if (model_with_shirts_list.index(i)+1)%10 == 0:
            sleep(65)

    print(return_list)
    return(return_list)




if __name__ == "__main__":

    #main()


    sort_key = itemgetter(1)

    f = open('store1.pckl','rb')
    collect, return_list = pickle.load(f)
    f.close()

    return_list = sorted(return_list, key = lambda k: k['Style'])


    firebase = firebase.FirebaseApplication('https://aihackerthon.firebaseio.com', authentication=None)
    result = firebase.post('/SomethingLeong', return_list)
    print(result)


    '''
    img_dir = "model_with_shirts/" + return_list[0]['URL']
    input_path = os.path.abspath(img_dir)

    predicted_number = return_list[0]['Pant']
    print("Predicted Pant: {}".format(predicted_number))

    output_path = "training_pants/{image}.jpg".format(
        image= predicted_number
    )
    output_path = os.path.abspath(output_path)

    im = Image.open(output_path)
    im2 = Image.open(input_path)

    make_img(im,im2)
    '''