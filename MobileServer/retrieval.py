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

# For GPU Configure
# from spleeter.separator import Separator
# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

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

def cosine_similarity(x,y):
    return np.dot(x,y) / (np.sqrt(np.dot(x,x)) * np.sqrt(np.dot(y,y)))

def run(file_name, data_tfidf_ngram,classes,tfidf_vect_ngram):
    # # Buoc 1: Load data
    # data, classes = load_data_in_a_directory('./data/*.txt')
    # print('Total database: {}'.format(len(data)))
    # # Buoc 2 tinh' TF_IDF kết hợp 2 từ liên tiếp nhau
    # tfidf_vect_ngram = TfidfVectorizer(analyzer='word', max_features=5000, ngram_range=(2, 3))
    # tfidf_vect_ngram.fit(data)
    # # print("debug mode---------------------"+str(data))
    # data_tfidf_ngram = tfidf_vect_ngram.transform(data)

    # Buoc 3 Crop music thành 2 đoạn
    # file_crop = crop_music(file_name)
    rank = []
    label = []

    # # Voi moi doan:
    # for crop in file_crop:
        # Tach loi tu bai hat
    query = Speech_to_Text(file_name)
    #query = "Giống như mây - gió, khi gió theo mây thì mây hóa mưa Và nếu cả hai như một giấc ngủ thì em không còn bên trong đó nữa."
    # Buoc 4 xu ly tf-idf N-gram voi n = 2
    print("debug mode---------------------"+query)
    query = gensim.utils.simple_preprocess(query)
    query = ' '.join(query)
    query = ViTokenizer.tokenize(query)
    query_vect_ngram = tfidf_vect_ngram.transform([query])

    # Buoc 5 so sanh cosine
    sim_matrix = metrics.pairwise.cosine_similarity(query_vect_ngram,data_tfidf_ngram)
    sim_matrix = np.reshape(sim_matrix, (-1,))

    idx = np.argsort(-sim_matrix)[:5]
    for i in idx:
        rank.append(sim_matrix[i])
        label.append(classes[i][7:-4])

    rank = np.asarray(rank)
    print('Searching......................')
    idx_rank = np.argsort(-rank)
    print(rank)
    output = []
    for i in idx_rank[:5]:
        print("Your query is {} with {}%".format(label[i],rank[i]))
        output.append(label[i])
    return output

# if __name__ == '__main__':
#     start_time = time.time()
#     # config = ConfigProto()
#     # config.gpu_options.allow_growth = True
#     # session = InteractiveSession(config=config)
#     print(run('./music/Em Vu Quy.mp3'))
#     print("--- %s seconds ---" % str(round(time.time() - start_time,2)))
