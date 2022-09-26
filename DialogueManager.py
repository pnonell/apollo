from os import path
import time
from youtubesearchpython import SearchVideos
import pafy
import os
import pickle
import random
import pandas as pd
import numpy as np
import nltk
import pylast
import copy
import spacy
from sklearn.feature_extraction.text import CountVectorizer

# os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

# import vlc

nlp = spacy.load('en_core_web_sm')

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
        self.waitForMessage = True
        self.message = ''

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
        self.controller.waitingForAnswer = False
        while self.waitForMessage:
            time.sleep(0.1)

        self.waitForMessage = True
        if not sen:
            # input
            self.curr_sen = self.message  # input('You: ')
        else:
            self.curr_sen = sen

        self.curr_vec = None
        # self.controller.answerMessage = ""

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
        answers = ['That\'s awesome! May I ask what your name is?',
                   'What would you like me to call you?',
                   'I would like to know you a little more, what is your name?']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'That\'s awesome! May I ask what your name is?')

    def ask_for_consent(self, mood=None):
        answers = ['In order to personalize the recommendations, would it be ok if we store some information? ',
                   'We want to make the best experience as possible, can I ask store some information about this '
                   'conversation? ',
                   'I want to  ask your permission to store some information, Is it ok? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans

    # print(self.agent + 'Hello my friend!! '
    #                'In order to personalize the recommendations, would it be ok if we store some information?')

    def pass_with_no_consent(self, mood=None):
        answers = ['It\'s totally fine! we can continue without storing your data! ',
                   'No problem!! I\'ll try to do as good as I can without storing your data. ',
                   'Ok, I\'m the God of music. I can give you all the information without storing your data!!']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'It\'s totally fine! we can continue without storing your data!')

    def ask_for_yes_no(self, mood=None, append=None):
        answers = ['Is it a yes or no?',
                   'May I interpret your answer as a yes or no?',
                   'So? Yes or No?']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'Is it a yes or no?')

    def suggest_period(self, period, new=True):
        if new:
            answers = [f'Do you want to know about {period} period in the history of music?',
                       f'Are you in the mood to learn something about {period} period?',
                       f'Would you like to discover {period} period?']
            ans = answers[random.randint(0, len(answers) - 1)]
            return ans
            # print(self.agent + f'Do you want to know about {period} period in the history of music?')
        else:
            answers = [f'We already went through {period} period. Do you want to know more?',
                       f'Now we know general information about {period}, would you want to know a bit more?',
                       f'We already talked about {period}, but I know more information. Do you like to know it?']
            ans = answers[random.randint(0, len(answers) - 1)]
            return ans
            # print(self.agent + f'We already went through {period} period. Do you want to know more?')

    def say_something_nice(self, user=None):
        if not user:
            answers = ['I\'m really happy to talk to you! ',
                       'It is a pleasure for me to talk to you!! ',
                       'I really love talking with you! ']
            ans = answers[random.randint(0, len(answers) - 1)]
            return ans
            # print(self.agent + 'I\'m really happy to talk to you!')
        else:
            answers = [f'Nice to meet you, {user}! Let\'s start! ',
                       f'It is a pleasure to meet you, {user}. We can start now!! ',
                       f'{user} ?! It is a great name!! Let\'s start!! ']
            ans = answers[random.randint(0, len(answers) - 1)]
            return ans
        #  print(self.agent + f'Nice to meet you, {user}! Let\'s start!')

    def say_name_wasnt_clear_repeat(self):
        answers = ['Sorry! I\'m almost 5000 years old! Couldn\'t  hear! Can you repeat your name? ',
                   'I may be becoming a bit like Beethoven and I couldn\'t hear you well. What did you say your name '
                   'was? ',
                   'I have not understood you correctly, can you repeat your name? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'Sorry! I\'m almost 5000 years old! Couldn\'t  hear! Can you repeat your name?')

    def say_welcome_back(self, name):
        answers = [f'Welcome back! {name}! ',
                   f'Nice to see you again {name}!! ',
                   'Oh!! Look who is back!! ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + f'Welcome back! {name}')

    def ask_if_want_to_know_composer(self, period):
        answers = [f'Let\'s talk about one of major composer of {period} period. yes? ',
                   f'I think it\'s time to know a little bit about the most important composers of {period} period! '
                   f'Fine?',
                   f'If you like {period},  I bet you want to know something about one of the major composers, right? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + f'Let\'s talk about one of major composer of {period} period. huh?')

    def suggest_composer(self, composer):
        answers = [f'{composer} is one of the bests of his time! Any question about him? ',
                   f'I can suggest {composer}. Any question about him? ',
                   f'One of my favourite composers is {composer}. Any question about him? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + f'Would you like to know about {composer}?')

    def try_another_period(self):
        answers = ['OK. Let\'s talk about another period! ',
                   'We have already talked about this period, but there are more. Would you like to discover another '
                   'one?',
                   'I think it\'s a perfect time to talk about another period!! ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'OK. Let\'s talk about another period!')

    def say_that_was_all_for_now(self):
        answers = ['I think it is enough for today... ',
                   'We have spent a very good time for today. ',
                   'I\'m a bit tired now… ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'I think it is enough for today...')

    def continue_with_period(self):
        answers = ['I\'m glad you are interested in this period! ',
                   'I knew you would like this period. ',
                   'It seems you are interested in this period!! ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'I\'m glad you are interested in this period!')

    def try_another_composer(self):
        answers = ['OK. I can find you another composer! or anything else? ',
                   'There are hundreds of composer, let\'s try another one or something else? ',
                   'I think we should try with another composer. or anything else? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + 'OK. I can find you another composer!')

    def ask_if_want_to_know_a_song(self, composer):
        answers = [f'May I recommend you a song from {composer}? ',
                   f'Would you want to know one of the best compositions of {composer}? ',
                   f'I want to show you a very good composition of {composer}! What do you think? ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + f'May I recommend you a song from {composer}?')

    def suggest_song(self, song):
        answers = [f'Check out {song}. I really like this one! I can play this song if you want! ',
                   f'{song}. Oh yeah!! This is one of the best. I can play this song if you want!!! ',
                   f'Try {song}. I really love it. I can play this song if you want! ']
        ans = answers[random.randint(0, len(answers) - 1)]
        return ans
        # print(self.agent + f'Check out {song}. I really like this one!')

    def ask_if_play(self):

        return f'Do you want to hear it? '

    def say_bio(self, bio):

        return f'{bio}. any other question? '

    def say_no_understand(self):

        return f'I can\'t understand what you want! '

    def say_to_stop_you(self):

        return f'I hope you are enjoying! let me know if you want to stop the song. '

    def say_goodbye(self, user):

        return f'It was great talking to you, {user}! Visit me again! Bye bye '


class DialogueManager(Preprocessor):
    def __init__(self, controller):
        super().__init__()
        self.curr_da = None
        self.profile = None
        self.curr_period = None
        self.curr_composer = None
        self.curr_song = None
        self.controller = controller
        self.mouth = Generator()
        self.data = pd.read_pickle('composers.pkl')
        self.player = None

        try:
            with open('dialogue_act.model', 'rb') as file:
                self.da_tagger = pickle.load(file)

        except Exception:
            raise FileNotFoundError('Dialogue act model not found!')

        try:
            with open('questions.model', 'rb') as file:
                self.q_tagger = pickle.load(file)
        except Exception:
            raise FileNotFoundError('Question tagger model not found!')

    def load_profile(self, name):
        try:
            with open(f'users/{name}.pkl', 'rb') as file:
                self.profile = pickle.load(file)

            self.controller.answerMessage += self.mouth.say_welcome_back(name)

        except FileNotFoundError:
            self.profile = copy.deepcopy(profile)
            self.profile['user'] = name

            with open(f'users/{name}.pkl', 'wb') as file:
                pickle.dump(self.profile, file)

    def tag_da(self):
        self.digest()
        self.curr_da = self.da_tagger.predict(self.curr_vec)

    def tag_q(self):
        self.digest(q=True)

        return self.q_tagger.predict(self.curr_vec)

    def greet(self):
        while True:
            if self.profile is None:
                self.controller.answerMessage += self.mouth.ask_for_consent()

                self.listen()
                self.tag_da()

                if self.curr_da == 'accept':
                    self.controller.answerMessage += self.mouth.ask_name()
                    self.load_profile(name=self.look_for_name())

                    return

                elif self.curr_da == 'reject':
                    self.controller.answerMessage += self.mouth.pass_with_no_consent()
                    self.load_profile(name='temp')

                    return

                else:
                    self.controller.answerMessage += self.mouth.ask_for_yes_no()

    def suggest(self):
        if self.curr_da == 'farewell':
            return

        while True:
            self.pick_frame()

            self.recommend_period()

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                self.controller.answerMessage += self.mouth.continue_with_period()
            else:
                self.controller.answerMessage += self.mouth.try_another_period()
                continue

            self.controller.answerMessage += self.mouth.ask_if_want_to_know_composer(period=self.curr_period)

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                self.recommend_composer()
                self.controller.answerMessage += self.mouth.suggest_composer(self.curr_composer)
                while True:
                    self.listen()
                    self.tag_da()
                    if self.curr_da == 'imperative':
                        bio = self.data[self.data['composer'] == self.curr_composer]['Bio'].values[0]
                        self.controller.answerMessage += self.mouth.say_bio(bio=bio)
                    elif self.curr_da == 'wh-question':
                        q_type = self.tag_q()
                        if q_type == 'LOC':
                            bio = self.data[self.data['composer'] == self.curr_composer]['Born In'].values[0]
                            self.controller.answerMessage += self.mouth.say_bio(bio=bio)

                        else:
                            self.controller.answerMessage += self.mouth.say_no_understand()
                    else:
                        break

                # self.controller.answerMessage += self.mouth.suggest_composer(composer=self.curr_composer)

                self.controller.answerMessage += self.mouth.ask_if_want_to_know_a_song(composer=self.curr_composer)
                self.listen()
                self.tag_da()

                if self.curr_da == 'accept':
                    self.recommend_song()
                    self.controller.answerMessage += self.mouth.suggest_song(song=self.curr_song)

                    self.listen()
                    self.tag_da()
                    if self.curr_da == 'imperative':
                        #self.play_song()
                        self.controller.answerMessage += self.mouth.say_to_stop_you()
                        self.listen()
                        self.tag_da()
                        if self.curr_da == 'imperative':
                            self.player.stop()

            self.controller.answerMessage += self.mouth.try_another_composer()

            self.listen()
            self.tag_da()

            if self.curr_da == 'accept':
                continue
            elif self.curr_da == 'farewell':
                self.controller.answerMessage += self.mouth.say_goodbye(user=self.profile['user'])
            else:
                self.controller.answerMessage += self.mouth.say_that_was_all_for_now()
                return

    def look_for_name(self):
        while True:
            self.listen()

            if len(self.curr_sen.split()) == 1:
                self.controller.answerMessage += self.mouth.say_something_nice(user=self.curr_sen)
                return self.curr_sen

            named_ents = nlp(self.curr_sen).ents

            if not named_ents:
                self.controller.answerMessage += self.mouth.say_name_wasnt_clear_repeat()
                continue

            for ent in named_ents:
                if ent.label_ == 'PERSON':
                    self.controller.answerMessage += self.mouth.say_something_nice(user=str(ent))
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
            self.controller.answerMessage += self.mouth.suggest_period(period=self.curr_period, new=False)
        else:
            self.controller.answerMessage += self.mouth.suggest_period(period=self.curr_period)
            self.profile['frames'][self.curr_period]['Suggested'] = True

    def recommend_composer(self):
        sug_composers = self.data['composer'].isin(self.profile['frames'][self.curr_period]['Suggested Composers'])
        composers = self.data[(~sug_composers) & (self.data['Period'] == self.curr_period)].sample(n=1)['composer']
        self.curr_composer = composers.values[0]

    def recommend_song(self):
        sug_songs = self.profile['frames'][self.curr_period]['Suggested Songs']
        songs = self.data[self.data['composer'] == self.curr_composer]['songs'].values[0]

        print(sug_songs)

        songs = [str(s).split(' - ')[1] for s in songs if s not in sug_songs]
        self.curr_song = np.random.choice(songs, 1)[0]

    def play_song(self):
        url = SearchVideos(f'{self.curr_composer} {self.curr_song}', offset=1, mode="json", max_results=1).links[0]
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        instance = vlc.Instance()
        self.player = instance.media_player_new()
        media = instance.media_new(playurl)
        media.get_mrl()
        self.player.set_media(media)
        self.player.play()

    def close(self):
        self.controller.answerMessage += self.mouth.say_goodbye(user=self.profile['user'])

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
                active = False

            else:
                self.controller.answerMessage = 'Be more clear please! I\'m from ancient Greece and my English is a ' \
                                                'bit rusty!'


if __name__ == '__main__':
    df = pd.read_pickle('composers.pkl')

    df.loc[
        (df.composer == 'Nicolas Gombert'), 'Bio'] = 'Nicolas Gombert was a Franco-Flemish composer of the ' \
                                                     'Renaissance.' \
                                                     ' He was one of the most famous and influential composers ' \
                                                     'between Josquin des Prez and Palestrina, ' \
                                                     'and best represents the fully developed, complex polyphonic ' \
                                                     'style of this period in music history.'
    # df.to_pickle('composers.pkl')

#     # from Controller import ApolloController
#     # d = DialogueManager(ApolloController)
#     # d.main()
#     # d.data = d.data[(~d.data['composer'].str.contains('Field'))]
#     # with open('composers.pkl', 'wb') as file:
#     #     pickle.dump(d.data)
#     # print(d.data[(~d.data['composer'].str.contains('Field'))])
#     # d.main()
#
#     df = pd.read_pickle('composers.pkl')
#     # df = df[(df['composer'].str.contains('Field'))]
#     # print(df[df['composer'] == 'John Field (composer)'])
#     df.to_csv('comp.csv')
