import nmslib

import pandas as pd
import spacy


class QA(object):
    def __init__(self, data):
        self.nlp = spacy.load('en')
        self.questions = data.question.tolist()
        self.answers = data.answer.tolist()

    def to_vectors(self, texts):
        """Convert texts into their vectors"""
        result = []
        for item in texts:
            result.append(self.nlp(item).vector)

        return result

    def build_nmslib_index(self):
        """build nmslib index with vectors of question texts"""
        self.index = {}
        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        self.index.addDataPointBatch(self.to_vectors(self.questions))
        self.index.createIndex({'post': 2}, print_progress=True)

    def search(self, text, max_distance=0.2):
        """
        K-Nearest-Neighbour search over indexed taxonomy data and distance threshold parameter
        to get most similar one.
        Args:
            text: (str) sample question text
            max_distance: (float) maximum allowed distance for neighbours

        Returns:
            result: (tuple) index and distance for found item

        """
        result = {}
        vector = self.nlp(text).vector

        if vector is not None:
            ids, distances = self.index.knnQuery(vector)

            if ids is not None and distances is not None:
                best_indices_mask = (distances == distances.min()) & (distances < max_distance)
                if best_indices_mask.sum() != 0:
                    result = {'index': ids[best_indices_mask][0], 'distance': distances[best_indices_mask][0]}

        return result

    def query(self, question, max_distance=0.2):
        search_result = self.search(question, max_distance)
        index, distance = search_result.get('index', -1), search_result.get('distance', -1)
        result = "N/A"
        if index != -1:
            result = self.answers[index]

        return result


def init_qa(data_path):
    data = pd.read_csv(data_path, index_col=0)
    qa_model = QA(data)
    qa_model.build_nmslib_index()

    return qa_model
