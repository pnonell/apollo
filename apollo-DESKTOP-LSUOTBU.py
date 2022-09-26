from os import path
import pickle

import pandas as pd
import numpy as np
import nltk
import copy
import spacy
from sklearn.feature_extraction.text import CountVectorizer

nlp = spacy.load('en_core_web_sm')

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

profile = {
    'user': None,
    'frames': {
        'Medieval': {
            'Suggested': False,
            'Liked': None,
            'Familiar': None,
            'Suggested Composers': [],
            'Suggested Songs': []
        },
        'Baroque': {
            'Suggested': False,
            'Liked': None,
            'Familiar': None,
            'Suggested Composers': [],
            'Suggested Songs': []
        },
        'Renaissance': {
            'Suggested': False,
            'Liked': None,
            'Familiar': None,
            'Suggested Composers': [],
            'Suggested Songs': []
        },
        'Classical': {
            'Suggested': False,
            'Liked': None,
            'Familiar': None,
            'Suggested Composers': [],
            'Suggested Songs': []
        },
        'Romantic': {
            'Suggested': False,
            'Liked': None,
            'Familiar': None,
            'Suggested Composers': [],
            'Suggested Songs': []
        }
    }
}


class Preprocessor:
    def __init__(self):
        self.sentences = []
        self.curr_sen = None
        self.curr_vec = None

        if path.isfile('q_vectorizer.pkl'):
            with open('q_vectorizer.pkl', 'rb') as pkl:
                self.q_vectorizer = pickle.load(pkl)
        else:
            self.q_vectorizer = None

        if path.isfile('da_vectorizer.pkl'):
            with open('da_vectorizer.pkl', 'rb') as file:
                self.da_vectorizer = pickle.load(file)
        else:
            self.da_vectorizer = None

    def clean(self):
        self.curr_sen = self.curr_sen.lower()

    @property
    def tokens(self):

        return nltk.word_tokenize(self.curr_sen)

    def tag_pos(self):
        self.curr_sen = ' '.join([f'{i[0]}-{i[1]}' for i in nltk.pos_tag(self.tokens)])

    def listen(self, sen=None):
        if not sen:
            self.curr_sen = input('You: ')
        else:
            self.curr_sen = sen

        self.curr_vec = None

    def digest(self, q=False):
        self.clean()
        self.memorize()
        self.tag_pos()
        self.embed(q=q)

    def create_embeder(self, corpus=None, q=False):
        if corpus is not None:
            for sen in corpus:
                self.listen(sen)
                self.clean()
                self.tag_pos()
                self.memorize()
        if q:
            self.q_vectorizer = CountVectorizer().fit(self.sentences)
        else:
            self.da_vectorizer = CountVectorizer().fit(self.sentences)

    def save_embeder(self, q=False):
        if q:
            with open(f'q_vectorizer.pkl', 'wb') as file:
                pickle.dump(self.da_vectorizer, file=file)
        else:
            with open(f'da_vectorizer.pkl', 'wb') as file:
                pickle.dump(self.da_vectorizer, file=file)

    def embed(self, q=False):
        if q:
            self.curr_vec = self.q_vectorizer.transform([self.curr_sen])[0]
        else:
            self.curr_vec = self.da_vectorizer.transform([self.curr_sen])[0]

    def memorize(self):
        self.sentences.append(self.curr_sen)


# p = Preprocessor()
# p.create_embeder(corpus=da['sentence'])
# p.save_embeder()
# p.fetch('Why you are?')
# p.clean()
# p.tag_pos()
# p.embed()
# print(p.curr_sen)


class Generator:
    agent = 'Apollo: '

    def ask_name(self, mood=None):
        print(self.agent + self.agent + 'That\'s awesome! May I ask what your name is?')

    def ask_for_consent(self, mood=None):
        print(self.agent + 'Hello my friend!! '
                           'In order to personalize the recommendations, would it be ok if we store some information?')

    def pass_with_no_consent(self, mood=None):
        print(self.agent + 'It\'s totally fine! we can continue without storing your data!')

    def ask_for_yes_no(self, mood=None, append=None):
        print(self.agent + 'Is it a yes or no?')

    def suggest_period(self, period, new=True):
        if new:
            print(self.agent + f'Do you want to know about {period} period in the history of music?')
        else:
            print(self.agent + f'We already went through {period} period. Do you want to know more?')

    def say_something_nice(self, user=None):
        if not user:
            print(self.agent + 'I\'m really happy to talk to you!')
        else:
            print(self.agent + f'Nice to meet you, {user}! Let\'s start!')

    def say_name_wasnt_clear_repeat(self):
        print(self.agent + 'Sorry! I\'m almost 5000 years old! Couldn\'t  hear! Can you repeat your name?')

    def say_welcome_back(self, name):
        print(self.agent + f'Welcome back! {name}')

    def ask_if_want_to_know_composer(self, period):
        print(self.agent + f'Let\'s talk about one of major composer of {period} period. huh?')

    def suggest_composer(self, composer):
        print(self.agent + f'Would you like to know about {composer}?')

    def try_another_period(self):
        print(self.agent + 'OK. Let\'s talk about another period!')

    def say_that_was_all_for_now(self):
        print(self.agent + 'I think it is enough for today...')

    def continue_with_period(self):
        print(self.agent + 'I\'m glad you are interested in this period!')

    def try_another_composer(self):
        print(self.agent + 'OK. I can find you another composer!')

    def ask_if_want_to_know_a_song(self, composer):
        print(self.agent + f'May I recommend you a song from {composer}?')

    def suggest_song(self, song):
        print(self.agent + f'Check out {song}. I really like this one!')


class DialogueManager(Preprocessor):
    def __init__(self):
        super().__init__()
        self.curr_da = None
        self.profile = None
        self.curr_period = None
        self.curr_composer = None
        self.curr_song = None
        self.mouth = Generator()
        self.data = pd.read_pickle('composers.pkl')

        try:
            with open('dialogue_act.model', 'rb') as file:
                self.da_tagger = pickle.load(file)
        except Exception:
            raise FileNotFoundError('Dialogue act model not found!')

    def load_profile(self, name):
        try:
            with open(f'users/{name}.pkl', 'rb') as file:
                self.profile = pickle.load(file)

            self.mouth.say_welcome_back(name)

        except FileNotFoundError:
            self.profile = copy.deepcopy(profile)
            self.profile['user'] = name

    def tag_da(self):
        self.digest()
        self.curr_da = self.da_tagger.predict(self.curr_vec)

    def greet(self):
        while True:
            if self.profile is None:
                self.mouth.ask_for_consent()
                self.listen()
                self.tag_da()

                if self.curr_da == 'accept':
                    self.mouth.ask_name()
                    self.load_profile(name=self.look_for_name())

                    return

                elif self.curr_da == 'reject':
                    self.mouth.pass_with_no_consent()
                    self.load_profile(name='temp')

                    return

                else:
                    self.mouth.ask_for_yes_no()

    def suggest(self):
        if self.curr_da == 'farewell':
            return

        while True:
            self.pick_frame()

            self.recommend_period()

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                self.mouth.continue_with_period()
            else:
                self.mouth.try_another_period()
                continue

            self.mouth.ask_if_want_to_know_composer(period=self.curr_period)

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                self.recommend_composer()
                self.mouth.suggest_composer(composer=self.curr_composer)

                self.mouth.ask_if_want_to_know_a_song(composer=self.curr_composer)
                self.listen()
                self.tag_da()

                if self.curr_da == 'accept':
                    self.recommend_song()
                    self.mouth.suggest_song(song=self.curr_song)

            self.mouth.try_another_composer()

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                continue
            else:
                self.mouth.say_that_was_all_for_now()
                return

    def look_for_name(self):
        while True:
            self.listen()

            if len(self.curr_sen.split()) == 1:
                self.mouth.say_something_nice(user=self.curr_sen)
                return self.curr_sen

            named_ents = nlp(self.curr_sen).ents

            if not named_ents:
                self.mouth.say_name_wasnt_clear_repeat()
                continue

            for ent in named_ents:
                if ent.label_ == 'PERSON':
                    self.mouth.say_something_nice(user=str(ent))
                    return str(ent)

    def pick_frame(self):
        avail_frames = [k for k, v in self.profile['frames'].items() if not v['Suggested']]
        suggested_frames = [k for k, v in self.profile['frames'].items() if v['Suggested']]

        if not avail_frames:
            self.curr_period = np.random.choice(suggested_frames, size=1)[0]
        else:
            self.curr_period = np.random.choice(avail_frames, size=1)[0]

    def recommend_period(self):
        if self.profile['frames'][self.curr_period]['Suggested']:
            self.mouth.suggest_period(period=self.curr_period, new=False)
        else:
            self.mouth.suggest_period(period=self.curr_period)
            self.profile['frames'][self.curr_period]['Suggested'] = True

    def recommend_composer(self):
        sug_composers = self.data['composer'].isin(self.profile['frames'][self.curr_period]['Suggested Composers'])
        composers = self.data[(~sug_composers) & (self.data['Period'] == self.curr_period)].sample(n=1)['composer']
        self.curr_composer = composers.values[0]

    def recommend_song(self):
        sug_songs = self.profile['frames'][self.curr_period]['Suggested Songs']
        songs = self.data[self.data['composer'] == self.curr_composer]['songs'].values[0]
        songs = [str(s).split(' - ')[1] for s in songs if s not in sug_songs]
        self.curr_song = np.random.choice(songs, 1)[0]

    def main(self):
        print('Greet Apollo to wake him up :)')
        active = True

        while active:
            self.listen()
            self.tag_da()

            if self.curr_da == 'greeting':
                self.greet()
                self.suggest()
                # self.close()

            else:
                print(self.curr_sen)
                print('Be more clear with him! He is from ancient Greece and his English is a bit rusty!')


if __name__ == '__main__':
    d = DialogueManager()
    d.main()
