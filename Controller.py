from PySide2 import QtCore, QtGui, QtQml
import View
from View import ApolloView
from PySide2.QtCore import *
import speech_recognition as sr
from punctuator import Punctuator
import random
import pyttsx3
import asyncio
import threading
import logging
import time
from functools import partial
from DialogueManager import DialogueManager as DM
from playsound import playsound


class ApolloController(QtCore.QObject):
    dataReady = QtCore.Signal(name='dataReady')
    stateChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(ApolloController, self).__init__(parent)
        self._model = ApolloView()
        self.r = sr.Recognizer()
        self.p = Punctuator('model.pcl')
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        self.engine.setProperty('voice', en_voice_id)
        self._volume = "high"
        self.userMessage = ''
        self.d = DM(self)
        self.t = threading.Thread(target=self.d.main, args=())
        self.t.start()
        self.waitingForAnswer = True
        self.answerMessage = ''
        with sr.Microphone() as self.source:
            self.r.adjust_for_ambient_noise(self.source)
        self.showMessage("Hi, I'm Apollo!", True)

    #       self.volumeChanged.emit(1)

    @QtCore.Property(QtCore.QObject)
    def model(self):
        return self._model

    # @QtCore.Property(str)
    # def volume(self):
    #     return self._volume

    # @volume.setter
    # def setVolume(self, volume):
    #     if volume == self._volume:
    #         return
    #     self._volume = volume
    #   #  self.volumeChanged.emit()

    def speak_thread(self, msg):
        print("speaking")
        self.engine.say(msg)
        self.engine.runAndWait()
        self.answerMessage = ""

    def showMessage(self, msg, agent):
        t = msg
        a = agent
        self.model.insertRows(t, a)

        if agent:
            # speak msg
            print(msg)
            thr = threading.Thread(target=self.speak_thread, args=(msg,))
            thr.start()

    def speak(self, msg):
        self.engine.say(msg)
        self.engine.runAndWait()

    @Slot()
    def startRecording(self):

        self.timer1 = QtCore.QTimer(interval=10)
        self.timer1.setSingleShot(True)
        self.timer1.timeout.connect(self.changeButton)
        self.timer1.start()

    def changeButton(self):
        # with sr.Microphone() as self.source:
        #     self.r.adjust_for_ambient_noise(self.source)
        print("Speak (5 sec)...")
        self.stateChanged.emit(2)

        self.timer2 = QtCore.QTimer(interval=10)
        self.timer2.setSingleShot(True)
        self.timer2.timeout.connect(self.getRecording)
        self.timer2.start()

    def getRecording(self):
        with sr.Microphone() as self.source:
            #     self.r.adjust_for_ambient_noise(source)
            #     print("Speak (5 sec)...")
            playsound('record_start.mp3')
            self.data = self.r.record(self.source, duration=3)

            print("Stop")

            self.stateChanged.emit(3)

            self.timer3 = QtCore.QTimer(interval=10)
            self.timer3.setSingleShot(True)
            self.timer3.timeout.connect(self.processText)
            self.timer3.start()

    def processText(self):
        playsound('record_end.mp3')

        try:
            text = self.r.recognize_google(self.data, language='en')
            text = self.p.punctuate(text)
            # time.sleep(2)
            # text = "testing"
            self.userMessage = text

            self.showMessage(text, False)
            self.stateChanged.emit(4)

            self.timer = QtCore.QTimer(interval=1000)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.handleMessage)
            self.timer.start()
        except Exception:
            self.showMessage("Sorry I didn't get what you said.", True)

    def handleMessage(self):
        # dialogue manager
        self.d.message = self.userMessage
        self.d.waitForMessage = False

        # answer generator
        while self.waitingForAnswer:
            time.sleep(0.1)
        self.waitingForAnswer = True
        self.showMessage(self.answerMessage, True)
        self.stateChanged.emit(1)

        # provisional random answers
        # answers = ["Do you like Renaissence music?", "Bach was born in 1685 in Germany", "I can show you a lot of
        # options", "I don't like Reggeaton", "Sure", "Ludwig van Beethoven (16 December 1770 – 26 March 1827) was a
        # German pianist and composer of the transitional period between the late Classical and early Romantic eras.
        # He is often regarded as one of the most brilliant, prolific and influential composers of all time."]
        # ans = answers[random.randint(0, len(answers)-1)]
        # self.showMessage(ans, True)
