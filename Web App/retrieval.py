import numpy as np
from sklearn import metrics
from tqdm import tqdm
from glob import glob
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from pyvi import ViTokenizer
from music import Speech_to_Text
from preprocess import crop_music
import time
import os

def load_data_in_a_directory(data_path):
    file_paths = glob(data_path)
    lst_contents = []
    for file_path in tqdm(file_paths):
        with open(file_path,'r',encoding='utf-8') as f:
            lines = f.readlines()
            lines = ' '.join(lines)
            lines = gensim.utils.simple_preprocess(lines)
            lines = ' '.join(lines)
            lines = ViTokenizer.tokenize(lines)
            lst_contents.append(lines)
    count = 0
    x = 0
    while x != len(lst_contents)-1:
        if lst_contents[x] == '':
            lst_contents.pop(x)
            os.remove(file_paths[x])
            file_paths.pop(x)
            count += 1
        x += 1
    print('Remove: {} song does not have lyrices'.format(count))
    return (lst_contents, file_paths)

def run(file_name,data_tfidf_ngram,tfidf_vect_ngram, classes):

    # Buoc 3 Crop music thành 2 đoạn
    crop_time = time.time()
    file_crop = crop_music(file_name)
    print("--- crop time: %s seconds ---" % str(round(time.time() - crop_time,2)))
    rank = []
    label = []

    tfidf_time = 0

    # Voi moi doan:
    query_time = time.time()
    for crop in file_crop:

        # Tach loi tu bai hat
        query = Speech_to_Text(crop)

        tf_time = time.time()

        # Buoc 4 xu ly tf-idf N-gram voi n = 2
        query = gensim.utils.simple_preprocess(query)
        query = ' '.join(query)
        query = ViTokenizer.tokenize(query)
        query_vect_ngram = tfidf_vect_ngram.transform([query])

        # Buoc 5 so sanh cosine
        sim_matrix = metrics.pairwise.cosine_similarity(query_vect_ngram,data_tfidf_ngram)
        sim_matrix = np.reshape(sim_matrix, (-1,))

        idx= np.argsort(-sim_matrix)[:4]
        for i in idx:
            rank.append(sim_matrix[i])
            label.append(classes[i][14:-4])
        print(rank)
        print("--- tfidf time: %s seconds ---" % str(round(time.time() - tf_time,2)))
    print("--- speech to text time: %s seconds ---" % str(round(time.time() - query_time,2)))

    tfidf_time = time.time()
    rank = np.asarray(rank)
    print('Searching......................')
    idx_rank = np.argsort(-rank)
    output = []
    for i in idx_rank[:4]:
        print("Your query is {} with {}%".format(label[i],rank[i]))
        output.append(label[i])
    print("--- query time: %s seconds ---" % str(round(time.time() - tfidf_time,2)))
    return output


# if __name__ == '__main__':
#     start_time = time.time()
#     config = ConfigProto()
#     config.gpu_options.allow_growth = True
#     session = InteractiveSession(config=config)
#     print(run('./music/ALL9.mp3'))
#     print("--- total: %s seconds ---" % str(round(time.time() - start_time,2)))
