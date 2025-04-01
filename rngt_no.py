#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## these two lines to avoid a problem when importing gui, see: https://groups.google.com/forum/#!topic/psychopy-users/0wVjYIcXQsk
import pyglet 
pyglet.options['shadow_window'] = False

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import time
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray, round
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys


## global variables
fullscreen=False
quit_button="escape"
key_confirm="return"
key_left="n"   # "lalt"
key_right="m"  # "rctrl"
probe_keys=["1","2","3","4"]
n_trials_training_session=2
ISI = 0.75
sleeptime=0 # 5
stimcolor="white"


## Likert-scale
class LikertScale:
    def __init__(self, win, nposs=4, instruction_text=u"", scale_labels=[]):
        start,end=-.5, .5
        ypad=.05
        instru = visual.TextStim(win=win, ori=0, name='instru',units='norm',
            text=instruction_text,    font='Arial',
            pos=[0, 0.5], height=0.07, wrapWidth=None,
            color='white', colorSpace='rgb', opacity=1,
            depth=0.0)
        self.nposs=nposs
        self.show_arrow=False
        line=visual.Line(win, start=(start, 0), end=(end,0), units='norm', lineColor=stimcolor, lineWidth=5)
        ticks=start+np.arange(0,nposs)*(end-start)/float(nposs-1)
        poss=[visual.Line(win, start=(tick, -ypad), end=(tick,ypad), units='norm', lineColor=stimcolor,
                          lineWidth=3) for tick in ticks]
        lab=[visual.TextStim(win, pos=(ticks[i], -.1), units='norm', text=scale_labels[i], height=.05, color=stimcolor) for i in range(len(scale_labels))]

        self.arrow_v=0.4*np.array([ [0,0], [.2, .2], [.1, .2], [.1, .5], [-.1, .5], [-.1, .2], [-.2, .2], [0, 0]])
        self.arrow_v[:,1]+=ypad+.01
        self.ticks=ticks
        self.arrow=visual.ShapeStim(win, vertices=self.arrow_v, fillColor=stimcolor, units='norm')

        self.init_random()

        self.elements=[line]+poss+lab+[instru]

    def init_random(self):
        ## initialize to either 0 or nposs-1
        initial_pos=np.random.choice([0,self.nposs-1])
        self.set_arrow(initial_pos)
    def init_middle(self):
        ## initialize to either 0 or nposs-1
        initial_pos=int(self.nposs/2)
        self.set_arrow(initial_pos)

    def set_arrow(self, pos):
        self.current_pos=pos
        v=self.arrow_v.copy()
        v[:,0]+=self.ticks[pos]
        self.arrow.setVertices(v)
        self.show_arrow=True

    def arrow_left(self):
        if self.current_pos==0:
            return
        else:
            self.set_arrow(self.current_pos-1)

    def arrow_right(self):
        if self.current_pos==self.nposs-1:
            return
        else:
            self.set_arrow(self.current_pos+1)
    def draw(self):
        for el in self.elements:
            el.draw()
        if self.show_arrow:
            self.arrow.draw()


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'RNGT HDtDCS'  # from the Builder filename that created this script
expInfo = {u'participant': u'', 'session':["training","baseline","stimulation"]}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


## duration for baseline
session_duration=10*60 # in s
num_probes=10

# overwrite in case of real stimulation session
if expInfo["session"]=="stimulation":
    session_duration=20*60 # in s
    num_probes=20

min_probe_interval=30 # in s
max_probe_interval=60 # in s

## randomization
ntrials=int(session_duration/ISI)
probe_times=np.array(np.random.randint( min_probe_interval, max_probe_interval+1, num_probes-1)/ISI, dtype=np.int)
probe_trials=np.cumsum(np.array(probe_times/sum(probe_times)*(ntrials-20/ISI), dtype=np.int))
probe_trials=np.append(probe_trials, ntrials)


# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' %(expInfo['participant'], expInfo["session"], expName, expInfo['date'])
#filename='data/test'
datafile=filename+".csv"

#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file


# Setup the Window
win = visual.Window(size=(800, 600), fullscr=fullscreen, screen=0,      allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )

# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "instruction"
instruction1 = visual.TextStim(win=win, ori=0, name='text',
    text=u'Plasser din venstre pekefinger på den markerte tastaturknappen på venstre siden (Uten å pressen den ned) og plasser din høyre pekefinger på den nedre markerte tastaturknappen på høyre side av tastaturet (Igjen, uten å presse knappen ned).\nVennligst hold denne posisjonen gjennom hele eksperimentet.\n\nI dette eksperimentet vil du høre en tone som vil spille i en fast rytme.\nBasert på instruksene du har fått i starten av dette eksperimentet, prøv å trykk på tastene i en tilfeldig rekkefølge til takten av tonene.\n\nPrøv å trykk tastene synkront med tonene så presist som du klarer.\nDu kan kun trykke ned EN av tastene om gangen.\n\nTrykk hvilken som helst tast for å fortsette.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

instruction1b = visual.TextStim(win=win, ori=0, name='text',
    text=u'Prøv å hold deg så konsentrert om oppgaven som bare mulig gjennom hele eksperimentet, men det er ikke uvanlig at tankene dine noen ganger kan begynne å vandre.\n\nPå grunn av dette vil du noen ganger gjennom eksperimentet bli avbrutt av noen spørsmål på skjermen. Bruk venstre og høyretastene for å svare hvor oppmerksomheten/tankene dine var rett før spørsmålet dukket opp på skjermen.\n\nDu får velge mellom svar fra «Helt klart ON TASK» til «Helt klart OFF TASK», altså om tankene dine var rettet mot oppgaven (ON TASK) eller mot noe annet (OFF TASK). Bruk tastene for å flytte markøren til det alternativet du vil svare og trykk OK.\n\nTrykk hvilken som helst tast for å fortsette.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

instruction1c = visual.TextStim(win=win, ori=0, name='text',
    text=u'Hvis du svarer «ON TASK», gjelder dette når du har holdt fokus/tankene dine på oppgaven (Hvilken taster du skal trykke på, hvilken du har tastet på, og i hvilken takt).\n\nHvis du svarer «OFF TASK», gjelder dette når fokuset/tankene dine har vært andre plasser (Dagdrømming, minner, framtidsplaner, venner ect..).\n\nTrykk hvilken som helst tast for å fortsette.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

instruction1d= visual.TextStim(win=win, ori=0, name='text',
#    text=u'Importantly, mind-wandering can occur either because you INTENTIONALLY decided to think about things that are unrelated to the task, OR because your thoughts UNINTENTIONALLY drifted away to task-unrelated thoughts, despite your best intentions to focus on the task. \n\nTherefore, if you want to answer MIND WANDERING, you have to choose if it was “INTENTIONALLY” or “UNINTENTIONALLY”.\n\nNote that there is no right or wrong answer and that there will not be any consequences related to your answers, so please just be honest when answering those questions.\n\nPress any button to continue.',    font='Arial',
    text=u'Det er viktig å påpeke at det finnes ikke et riktig eller galt svar og ingen konsekvenser vil følge av svarene dine, så bare svar så ærlig som mulig.\n\nTrykk hvilken som helst tast for å fortsette.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

#instruction1e = visual.TextStim(win=win, ori=0, name='text',
#    text=u'Following the question regarding attention you will get a second question about how certain you are that you assessed your focus of attention correctly during the first question. \n\nOut of the answer options ranging from "very uncertain" to "very certain", choose the one that fits best.\n\nPress any button to continue.',    font='Arial',
#    pos=[0, 0], height=0.07, wrapWidth=None,
#    color='white', colorSpace='rgb', opacity=1,
#    depth=0.0)

instruction1f = visual.TextStim(win=win, ori=0, name='text',
    text=u'Det vil være et kryss på skjermen foran deg i eksperimentet, vennligst prøv å hold blikket ditt rettet mot dette krysset gjennom hele eksperimentet.\n\nHvis du har noen spørsmål angående eksperimentet vennligst spør eksperimentatoren nå.\nHvis ikke, trykk hvilken som helst tast for å starte eksperimentet',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

training_session_starts=visual.TextStim(win=win, ori=0, name='text',
    text=u'Eksperimentet starter med en øvelsesrunde\n\nTrykk hvilken som helst tast for å starte.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
training_repeat=visual.TextStim(win=win, ori=0, name='text',
    text=u'Vil du ta en øvelsesrunde til?\n\nTrykk på høyre knapp for JA, venstre for NEI.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

real_experiment_starts=visual.TextStim(win=win, ori=0, name='text',
    text=u'Nå starter det ekte eksperimentet\n\Har du noen spørsmål, vennligst spør nå\nHvis ikke, trykk hvilken som helst tast for å starte.',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


task_stimulus=visual.TextStim(win=win, ori=0, name='text',
    text=u'+',    font='Arial',
    pos=[0, 0], height=0.15, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

thankyou=visual.TextStim(win=win, ori=0, name='text',
    text=u'Ferdig! Takk skal du ha!',    font='Arial',
    pos=[0, 0], height=0.15, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


def waitforkey():
    while 1:
        keys=event.getKeys()
        if quit_button in keys:
            sys.exit()
        elif len(keys)>0:
            break

def show_probe(probe):
    #probe.init_random()
    probe.show_arrow=False
    while(1):
        probe.draw()
        win.flip()
        keys=event.getKeys()
        if len(set(keys) & set(probe_keys))>0:
            k=int(list(set(keys) & set(probe_keys))[-1])-1
            probe.set_arrow(k)
            probe.draw()
            win.flip()
            time.sleep(1.0)
            probe.show_arrow=False
            break
        elif quit_button in keys:
            sys.exit()
    return probe.current_pos


with open(datafile, "w") as f:
    f.write("# %s\n"%(str(expInfo)))
    f.write("subj,trial,time,stimulus,response\n")

probe=LikertScale(win, 4,
    instruction_text=u"Hvor var oppmerksomheten din (tankene dine) rettet like før dette spørsmålet?",
    scale_labels=[u"Helt klart \n ON TASK", "", "", u"Helt klart \n OFF TASK"])

task_clock = core.Clock()
trial_clock = core.Clock()
metronome_sound = sound.Sound('A', secs=0.075 )
metronome_sound.setVolume(1)
#metronome_sound.play()


# first instructions
instruction1.draw()
win.flip()
time.sleep(sleeptime)
event.getKeys()
waitforkey()


# first instructions part B
instruction1b.draw()
win.flip()
time.sleep(sleeptime)
event.getKeys()
waitforkey()

# first instructions part C
instruction1c.draw()
win.flip()
time.sleep(sleeptime)
event.getKeys()
waitforkey()

# first instructions part E
#instruction1e.draw()
#win.flip()
#time.sleep(sleeptime)
#event.getKeys()
#waitforkey()

# first instructions part D
instruction1d.draw()
win.flip()
time.sleep(sleeptime)
event.getKeys()
waitforkey()



# first instructions part F
instruction1f.draw()
win.flip()
time.sleep(sleeptime)
event.getKeys()
waitforkey()
##############################################3
## Training
##############################################3

if expInfo["session"]=="training":
    training_session_starts.draw()
    win.flip()
    time.sleep(2)
    event.getKeys()
    waitforkey()

    repeat_training=True
    while repeat_training==True:
        # stimulus shown during auditory beeps
        task_stimulus.draw()
        win.flip()

        time.sleep(0.5)
        event.getKeys()

        task_clock.reset()
        for trial in range(n_trials_training_session):
            trial_clock.reset()
            metronome_sound.play()
            while 1:
                current_time=trial_clock.getTime()
                keys=event.getKeys()
                if quit_button in keys:
                    sys.exit()
                if current_time>ISI:
                    #print current_time
                    break

        response=show_probe(probe)

        ## ask for repeating the training
        training_repeat.draw()
        win.flip()
        time.sleep(sleeptime)
        event.getKeys()

        while 1:
            keys=event.getKeys()
            if key_left in keys:
                repeat_training=False
                break
            elif key_right in keys:
                repeat_training=True
                break
            elif quit_button in keys:
                sys.exit()





##############################################3
## Experiment starts
##############################################3

if expInfo["session"] in ["baseline", "stimulation"]:
    real_experiment_starts.draw()
    win.flip()
    time.sleep(sleeptime)
    event.getKeys()
    waitforkey()


    # stimulus shown during auditory beeps
    task_stimulus.draw()
    win.flip()

    time.sleep(0.5)
    f=open(datafile, "a")

    # official session start
    task_clock.reset()

    for trial in range(ntrials):
        trial_clock.reset()

        if trial not in probe_trials:
            metronome_sound.play()
            logtext="{subj},{trial},{time},{type},{response}\n".format( \
                trial=trial,\
                subj=expInfo['participant'], \
                type="stimulus", response="", \
                time="%.10f"%(task_clock.getTime()))
            f.write(logtext)
            f.flush()
            while 1:
                current_time=trial_clock.getTime()
                keys=event.getKeys()
                if quit_button in keys:
                    sys.exit()
                if len(keys)>0:
                    logtext="{subj},{trial},{time},{type},{response}\n".format( \
                        trial=trial,\
                        subj=expInfo['participant'], \
                        type="tap", response=keys[0], \
                        time="%.10f"%(task_clock.getTime()))
                    f.write(logtext)
                    f.flush()

                if current_time>ISI:
                    break
        else:
            response=show_probe(probe)
            logtext="{subj},{trial},{time},{type},{response}\n".format(\
                    trial=trial,\
                    subj=expInfo['participant'], \
                    type="probe1", response=response, \
                    time="%.10f"%(task_clock.getTime()))
            f.write(logtext)
            f.flush()


            task_stimulus.draw()
            win.flip()
            time.sleep(ISI)

    f.close()

thankyou.draw()
win.flip()
time.sleep(2)
waitforkey()
