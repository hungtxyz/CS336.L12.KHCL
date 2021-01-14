import os
import time
from multiprocessing import Process
from tqdm import tqdm
from glob import glob
import gensim
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

from models import Task
from retrieval import run

class AudioProcessor(Process):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def load_data_in_a_directory(sefl, data_path):
        file_paths = glob(data_path)
        lst_contents = []
        for file_path in tqdm(file_paths):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines = ' '.join(lines)
                lines = gensim.utils.simple_preprocess(lines)
                lines = ' '.join(lines)
                lines = ViTokenizer.tokenize(lines)
                lst_contents.append(lines)
        count = 0
        x = 0
        while x != len(lst_contents) - 1:
            if lst_contents[x] == '':
                lst_contents.pop(x)
                os.remove(file_paths[x])
                file_paths.pop(x)
                count += 1
            x += 1
        print('Remove: {} song does not have lyrices'.format(count))
        return (lst_contents, file_paths)

    def run(self) -> None:
        # tf-idf here

        ## apply new data
        data, classes = self.load_data_in_a_directory('./data/*.txt')
        print('Total database: {}'.format(len(data)))
        # Buoc 2 tinh' TF_IDF kết hợp 2 từ liên tiếp nhau
        tfidf_vect_ngram = TfidfVectorizer(analyzer='word', max_features=5000, ngram_range=(2, 3))
        tfidf_vect_ngram.fit(data)
        # print("debug mode---------------------"+str(data))
        data_tfidf_ngram = tfidf_vect_ngram.transform(data)

        while True:
            tasks = Task.query.filter_by(status=False).all()

            if len(tasks) == 0:
                print("No task")
                time.sleep(3)
                continue

            for task in tasks:

                print(f"Task {task.id} is processing ...")

    #audio process hể

                ##  status = result - string
                # name example q_2audit.mp3
                songs_name = run('./q_'+str(task.id)+"audio.mp3",data_tfidf_ngram,classes,tfidf_vect_ngram)[0]

                # TODO: GET TOP 1 : index 0



                # time.sleep(20) # Fake process

                print(f"Task {task.id} is done")
                task.result = songs_name
                task.status = True
                self.db.session.commit()


                os.remove('./q_'+str(task.id)+"audio.mp3")

