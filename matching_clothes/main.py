import os
import pickle
import indicoio
import requests # pip install requests
import json     # pip install json
import matplotlib.pyplot as plt
from operator import itemgetter
from PIL import Image
from indicoio.custom import Collection
indicoio.config.api_key = 'ae25a46523d9ac6a76b2a687ab477b16'

styles_list = ["Casual", "Bohemian", "Business", "Elegant", "Romantic", "Vintage", "Eclectic", "Rocker", "Sexy", "Denim", "Outdoor", "90s"]

def generate_training_data(fname):
    """
    Read in text file and generate training data.
    Each line looks like the following:

    1050: [1, 2, 3, 4, 5]
    1349: [1, 2, 3, 4, 5]
    4160: [1, 2, 3]
    ...

    First we split on the colon of each row, where the first
    half is the image filename and the second half is its
    associated labels.
    """
    with open(fname, "rb") as f:
        for line in f:
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
    collection = Collection("clothes_collection_2")

    # Clear any previous changes

    '''
    try:
        collection.clear()
    except:
        pass
    '''
    train = generate_training_data("clothes_match_labeled_data_2.txt")

    total = 0
    for samples in train:
        print("Adding {num} samples to collection".format(num=len(samples)))
        collection.add_data(samples)
        total += len(samples)
        print("Added {total} samples to collection thus far".format(total=total))

    collection.train()
    collection.wait()

    f = open('store1.pckl','wb')
    pickle.dump(collection,f)
    f.close()

if __name__ == "__main__":

    #main()

    sort_key = itemgetter(1)

    f = open('store1.pckl','rb')
    collect = pickle.load(f)
    f.close()

    img_dict = "test_shirts/9915.jpg"
    input_path = os.path.abspath(img_dict)
    styletype, stylenumber = what_style(input_path)
    print("Style: {}".format(styletype))

    predicted_number = sorted(collect.predict(img_dict).items(), key=sort_key)[-1][0][5]
    print("Predicted Number: {}".format(predicted_number))

    output_path = "training_pants/{image}.jpg".format(
        image= predicted_number
    )
    output_path = os.path.abspath(output_path)

    im = Image.open(output_path)
    im2 = Image.open(input_path)

    make_img(im,im2)

    '''
    print(sorted(collect.predict("test_shirts/12770.jpg").items(), key=sort_key))
    print(sorted(collect.predict("test_shirts/13668.jpg").items(), key=sort_key))
    print(sorted(collect.predict("test_shirts/14195.jpg").items(), key=sort_key))
    print(sorted(collect.predict("test_shirts/11896765.jpg").items(), key=sort_key))
    '''
