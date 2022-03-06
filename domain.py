class API:

    def __init__(self, package_name, class_name, class_description):
        self.package_name = package_name
        self.class_name = class_name
        self.class_description = class_description
        self.methods = []
        self.methods_descriptions_pure_text = []
        self.methods_descriptions = []  #the description is segmented into words
        self.methods_descriptions_stemmed = []
        self.methods_matrix = []
        self.methods_idf_vector = []
        self.class_description_matrix = None
        self.class_description_idf_vector = None


    def print_api(self):
        print (self.package_name+'.'+self.class_name,self.class_description)


class Question:

    def __init__(self, id, title, body, score, view_count, accepted_answer_id, answers = []):
        self.id = id
        self.title = title
        self.body = body # not used in training
        self.accepted_answer_id = accepted_answer_id # not used in training
        self.score = score # hard set to 0
        self.view_count = view_count # not used
        self.answers = answers
        self.title_words = None
        self.matrix = None
        self.idf_vector = None
    def __str__(self):
        return self.id, self.title, self.body, self.score, self.answers, self.title_words, self.matrix, self.idf_vector

class Answer:

    def __init__(self, id, parent_id, body, score):
        self.id = id # not used
        self.parent_id = parent_id # not used
        self.body = body
        self.score = score # hard set to 0

    def __repr__(self):
        return self.body

    def __str__(self):
        return self.body


