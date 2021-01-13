import numpy as np
from sklearn import metrics
from tqdm import tqdm
from glob import glob
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from pyvi import ViTokenizer
import random

# Load Data
file_paths = glob('./static/data/*.txt')
data = []
for file_path in tqdm(file_paths):
    with open(file_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines = ' '.join(lines)
        lines = gensim.utils.simple_preprocess(lines)
        lines = ' '.join(lines)
        lines = ViTokenizer.tokenize(lines)
        data.append(lines)
count = 0
x = 0
while x != len(data)-1:
    if data[x] == '':
        data.pop(x)
        os.remove(file_paths[x])
        file_paths.pop(x)
        count += 1
    x += 1
# print('Remove: {} song does not have lyrices'.format(count))
# print('Total database: {}'.format(len(data)))

# Buoc 2 tinh' TF_IDF kết hợp 2 từ liên tiếp nhau
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', max_features=5000, ngram_range=(2, 3))
tfidf_vect_ngram.fit(data)
data_tfidf_ngram = tfidf_vect_ngram.transform(data)

querys = []
for file_path in tqdm(file_paths):
    with open(file_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
        lines = ' '.join(lines[random.randint(0,8):random.randint(12,20)])
        querys.append(lines)

totalTrue = 0
for x in range(len(querys)):

    # Buoc 4 xu ly tf-idf N-gram voi n = 2
    query = gensim.utils.simple_preprocess(querys[x])
    query = ' '.join(query)
    query = ViTokenizer.tokenize(query)
    query_vect_ngram = tfidf_vect_ngram.transform([query])

    # Buoc 5 so sanh cosine
    sim_matrix = metrics.pairwise.cosine_similarity(query_vect_ngram,data_tfidf_ngram)
    sim_matrix = np.reshape(sim_matrix, (-1,))

    idx = np.argsort(-sim_matrix)[0]
    if (idx == x):
        totalTrue += 1

# print('Total True: ', totalTrue)
# print('Total Data: ', len(file_paths))
print('Accuracy for TF_IDF N_GRAMS: ', totalTrue/len(file_paths))
