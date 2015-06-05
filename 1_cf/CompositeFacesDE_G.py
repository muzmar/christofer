﻿# -*- coding: utf-8 -*-
'''
@author: Florian Niefind
@contact: nifflor@googlemail.com
@date: 2014-05-26
'''

from psychopy import visual, core, event, gui, data
import string, codecs
import random

#===============================================================================
# global variables: INTERFACE
#===============================================================================

PATH = 'C:/Users/Christofer/Google Drive/HiWi-Job/PsychoPy/Composite/1_CF'
FIXCROSS_SIZE = 40 #size of the fixation cross (the character '+' in Arial)
INSTR_CHAR_SIZE = 18 #character size for instructions
OUTPATH = '%s/results/'%(PATH) #output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE_G' #which language is the experiment in: 'DE_K'=German for smaller children; 'DE_G'=German for older children
MATCHING = {'lctrl':'left', 'rctrl':'right'} #matching of buttons to answers
SCREEN_SIZE = [1366, 768] #what is your screen resolution?
LANG_FONT_MAP = {'DE_K':'Courier New', 'DE_G':'Courier New'} #what font is used for what language?


#===============================================================================
# prepare psychopy
#===============================================================================

#create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230,230,230), colorSpace='rgb255', units="deg")

#gather experiment and subject information
exp_name = 'CompositeFaces'
exp_info = {'Subject':'', 'Subject (repeat)':''}

#prompt user for subject number
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
if dlg.OK == False:
    core.quit() #user pressed cancel

#if repetition and original do not match, repeat prompt
while exp_info['Subject'] != exp_info['Subject (repeat)']:
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Please insert matching number in both fields')
    if dlg.OK == False:
        core.quit() #user pressed cancel

#dictionary with additional info about the experiment
exp_info['date'] = data.getDateStr()#add a simple timestamp
exp_info['exp_name'] = exp_name


#===============================================================================
# read stimuli
#===============================================================================

def read_stims(stim_file):
    item_list = []
    trial_order = [] #order of the trials in the experiment (hard-coded in the trial file)
    with codecs.open(stim_file, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line: #its the header
                continue
            elif len(line) == 0: #last line if an empty one
                break
            line = line.split(';')
            trial_order.append(int(line[14])) #trial order
            item_list.append(line[0:14]) #write entire rest of the line
    return item_list, trial_order

practice_items, practice_trial_order = read_stims('%s/stimuli/Practice_CompositeFaces.txt'%(PATH))

items, trial_order = read_stims('%s/stimuli/Trials_CompositeFaces.txt'%(PATH))


#===============================================================================
# Other preparations
#===============================================================================

#width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP[LANGUAGE] #font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + '_' + LANGUAGE + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock() #reaction time clock

#fixation cross
fix_cross = visual.TextStim(exp_win, pos=[0, 0], text = '+', font='Arial', color=-1, height=FIXCROSS_SIZE, alignHoriz='center', units=u'pix')


#cue upper half
cue_up = visual.SimpleImageStim(exp_win, image='%s/stimuli/cues/fingers_1.png'%(PATH),pos=[0,150], units=u'pix')

#cue lower half
cue_low = visual.SimpleImageStim(exp_win, image='%s/stimuli/cues/fingers_2.png'%(PATH),pos=[0,-150], units=u'pix')


#------------------------------------------------------------------------------
#read instructions

try:
    Intro_CF_01 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_01.png'%(PATH, LANGUAGE))
    Intro_CF_02 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_02.png'%(PATH, LANGUAGE))
    Intro_CF_03 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_03.png'%(PATH, LANGUAGE))
    Intro_CF_04 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_04.png'%(PATH, LANGUAGE))
    Intro_CF_05 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_05.png'%(PATH, LANGUAGE))
    Intro_CF_06 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_06.png'%(PATH, LANGUAGE))
    Intro_CF_07 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_07.png'%(PATH, LANGUAGE))
    Intro_CF_08 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_08.png'%(PATH, LANGUAGE))
    Intro_CF_09 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_09.png'%(PATH, LANGUAGE))
    Intro_CF_10 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_10.png'%(PATH, LANGUAGE))
    Intro_CF_11 = visual.SimpleImageStim(exp_win, image='%s/instructions/%s/Intro_CF_11.png'%(PATH, LANGUAGE))
   
  
    with codecs.open('%s/Reminder.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        rem_text = infile.read()
    with codecs.open('%s/Correct_Screen.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        correct_text = infile.read()
    with codecs.open('%s/Incorrect_Screen.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        incorrect_text = infile.read()
except IOError:
    print 'Error: Language option set to unknown language. Choose DE_K for German (smaller children) or DE_G for German (older children).'
    exp_win.close()
    core.quit()

#task question shown again
reminder_screen = visual.TextStim(exp_win, pos=[0, -300], text=rem_text, font=font, color=-1, height=INSTR_CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

#feedback screens practice
correct_screen = visual.TextStim(exp_win, pos=[0, 0], text=correct_text, font=font, color=(-1, 1.0, -1), height=40, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')
incorrect_screen = visual.TextStim(exp_win, pos=[0, 0], text=incorrect_text, font=font, color=(1.0, -1, -1), height=40, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

def match_answer(answer_given, condition):
    '''
    Function to match the answer of the participant with the correct answer.
    lctrl: left
    rctrl: right
    '''
    return int(MATCHING.get(answer_given, 'escape') == condition)

#------------------------------------------------------------------------------
# define trial procedure

def run_trials(items, trial_order, practice = False):

    ### NOTE: If one wants a random order each time, uncomment the following two lines
    #trial_order = range(len(items)) #NOTE: initial seed is system time, so it is different each time
    #shuffle(trial_order)

    #if practice:
        #item_prefix = 'practice'
    #else:
        #item_prefix = ''


    trial_count = 1


    #loop through trials
    for i in trial_order:

        item = items[i-1]
        mask_index = random.randint(0,9)

        #new stimuli
        target = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[12]), pos=[-0,0], units=u'pix')
        stim = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[13]), pos=[0,0], units=u'pix')

        #prepare mask
        mask = visual.SimpleImageStim(exp_win, image='%s/stimuli/mask/Mask0%s.jpg'%(PATH, mask_index))

        #prepare cue
        if item[5] == 'upper':
            cue = cue_up
        else:
            cue = cue_low

        #pre-stimulus interval
        exp_win.flip() #flip blank screen
        core.wait(0.5) #500 ms

        #fix_cross
        fix_cross.draw()
        exp_win.flip()
        core.wait(0.2) #200 ms

        #draw target
        target.draw()
        exp_win.flip()
        core.wait(1.6) #1600 ms

        #mask (400 ms)
        mask.draw()
        cue.draw()
        exp_win.flip()
        core.wait(0.4) #400 ms

        #blank (1 cycle)
        exp_win.flip()

        #draw to back buffer
        stim.draw()
        cue.draw()
        reminder_screen.draw()
        #present
        exp_win.flip()

        #start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        #get reaction time
        rt = rt_clock.getTime()
        rt = rt*1000 #in ms

        #write out answers
        string_output = [exp_info['Subject'], str(trial_count)] #initialize output list: subject ID, trial number (in exp)
        string_output.extend([str(x) for x in item]) #add trial infos
        string_output.extend([str(int(practice)),str(ans[-1]), str(match_answer(ans[-1], item[3])), str(rt)]) #add answer infos
        outfile.write(';'.join(string_output) + '\n') #write to file

        if practice and match_answer(ans[-1], item[3]):
            correct_screen.draw()
            exp_win.flip()
            core.wait(1)
        elif practice:
            incorrect_screen.draw()
            exp_win.flip()
            core.wait(1)

        #check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()

        # quarter messages
        if not practice and trial_count in [40, 80, 120]:
            break_image = visual.SimpleImageStim(exp_win,
                image='{0}/instructions/{1}/Break_0{2}.png'.format(PATH, LANGUAGE, trial_count/40))
            break_image.draw()
            exp_win.flip()
            event.waitKeys(keyList=['space'])

        trial_count += 1


#===============================================================================
# experiment
#===============================================================================

#------------------------------------------------------------------------------
# present instructions
Intro_CF_01.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_02.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_03.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_04.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_05.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_06.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])

Intro_CF_07.draw()
exp_win.flip()
event.waitKeys(keyList=['space'])


#------------------------------------------------------------------------------
# run experiment
with codecs.open(output_file, 'wb', encoding="utf-8") as outfile:

    #write outfile header
    #outfile.write('### Experiment: %s\n### Subject ID: %s\n### Date: %s\n\n' %(exp_info['exp_name'], exp_info['Subject'], exp_info['date']))
    outfile.write('subject_id;trial;trial_id;type;same_or_different;expected_answer;sex;cue;Face_A:_Top_of_face;Face_A:_Bottom_of_face;Face_B:_Top_of_face;Face_B:_Bottom_of_face;Face_A_Original;Face_B_Original;Face_A_Name;Face_B_Name;_;given_answer;correct;reaction_time\n')
    #practice start if no questions
    Intro_CF_08.draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

    #run practice trials
    run_trials(practice_items, practice_trial_order, practice=True)

    #practice end
    Intro_CF_09.draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

    #exp start screen
    Intro_CF_10.draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

    #exp start
    run_trials(items, trial_order)

Intro_CF_11.draw()
exp_win.flip()
event.waitKeys()

exp_win.close()
core.quit()