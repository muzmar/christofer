# -*- coding: utf-8 -*-

# @author: Florian Niefind, edited and modified based on PEP8
# @contact: nifflor@googlemail.com
# @date: 2014-05-26

from psychopy import visual, core, event, gui, data
import string
import codecs
import random

# ===============================================================================
# global variables: INTERFACE
# ===============================================================================

# PATH = 'C:/Users/Christofer/Google Drive/HiWi-Job/PsychoPy/Composite/1_CF'
PATH = "C:\\pythonProjects\\christofer\\1_cf"
FIXCROSS_SIZE = 40  # size of the fixation cross (the character '+' in Arial)
INSTR_CHAR_SIZE = 18  # character size for instructions
OUTPATH = '{0}/results/'.format(PATH)  # output path for storing the results
AVAILABLE_KEYS = ['lctrl', 'rctrl', 'q']
LANGUAGE = 'DE_K'  # 'DE_K'=German for smaller children; 'DE_G'=German for older children
MATCHING = {'lctrl': 'left', 'rctrl': 'right'}  # matching of buttons to answers
SCREEN_SIZE = [1366, 768]  # what is your screen resolution?
LANG_FONT_MAP = {'DE_K': 'Courier New', 'DE_G': 'Courier New'}  # what font is used for what language?


class Image():  # class that creates ....

    def __init__(self, name, **kwargs):

        # ** if the format of images are different(ie. .png, .jpg, .gif) give the complete name with extension and
        # remove the ".png" from self.path
        # :param name: name of the image
        # :param type: can be "load", "arrow", "questionMark", "questionLoad"
        # :return:

        self.path = '{0}/instructions/{1}/{2}.png'.format(PATH, LANGUAGE, name)
        if 'loc' in kwargs:
            self.loc = kwargs['loc']

    def buffer(self, **kwargs):

        buffer_image = visual.ImageStim(exp_win, image=self.path, units=u'pix')
        if 'factor' in kwargs:
            buffer_image.setSize(kwargs['factor'], '*')
        return buffer_image


# ===============================================================================
# functions
# ===============================================================================


def read_stims(stim_file):
    item_list = []
    trial_order = []  # order of the trials in the experiment (hard-coded in the trial file)
    with codecs.open(stim_file, 'rb', encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if '###' in line:  # its the header
                continue
            elif len(line) == 0:  # last line if an empty one
                break
            line = line.split(';')
            trial_order.append(int(line[14]))  # trial order
            item_list.append(line[0:14])  # write entire rest of the line
    return item_list, trial_order


def match_answer(answer_given, condition):
    # Function to match the answer of the participant with the correct answer.
    # lctrl: left
    # rctrl: right

    return int(MATCHING.get(answer_given, 'escape') == condition)


def run_trials(items, trial_order, practice=False):

    # NOTE: If one wants a random order each time, uncomment the following two lines
    # trial_order = range(len(items)) #NOTE: initial seed is system time, so it is different each time
    # shuffle(trial_order)

    # if practice:
        # item_prefix = 'practice'
    # else:
        # item_prefix = ''

    trial_count = 1

    # loop through trials
    for i in trial_order:

        item = items[i-1]
        mask_index = random.randint(0, 9)

        # new stimuli
        target = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[12]), pos=[-0, 0], units=u'pix')
        stim = visual.ImageStim(exp_win, image='%s/stimuli/%s'%(PATH, item[13]), pos=[0, 0], units=u'pix')

        # prepare mask
        mask = visual.SimpleImageStim(exp_win, image='%s/stimuli/mask/Mask0%s.jpg'%(PATH, mask_index))

        # prepare cue
        if item[5] == 'upper':
            cue = cue_up
        else:
            cue = cue_low

        # pre-stimulus interval
        exp_win.flip()  # flip blank screen
        core.wait(0.5)  # 500 ms

        # fix_cross
        fix_cross.draw()
        exp_win.flip()
        core.wait(0.2)  # 200 ms

        # draw target
        target.draw()
        exp_win.flip()
        core.wait(1.6)  # 1600 ms

        # mask (400 ms)
        mask.draw()
        cue.draw()
        exp_win.flip()
        core.wait(0.4)  # 400 ms

        # blank (1 cycle)
        exp_win.flip()

        # draw to back buffer
        stim.draw()
        cue.draw()
        reminder_screen.draw()
        # present
        exp_win.flip()

        # start reaction time clock and collect answer
        rt_clock.reset()
        ans = event.waitKeys(keyList=AVAILABLE_KEYS)

        # get reaction time
        rt = rt_clock.getTime()
        rt *= 1000  # in ms

        # write out answers
        string_output = [exp_info['Subject'], str(trial_count)]  # initialize output list: subject ID, trial number
        string_output.extend([str(x) for x in item])  # add trial infos
        string_output.extend([str(int(practice)), str(ans[-1]), str(match_answer(ans[-1], item[3])), str(rt)])
        outfile.write(';'.join(string_output) + '\n')  # write to file

        if practice and match_answer(ans[-1], item[3]):
            correct_screen.draw()
            exp_win.flip()
            core.wait(1)
        elif practice:
            incorrect_screen.draw()
            exp_win.flip()
            core.wait(1)

        # check if experiment was aborted
        if len(ans) == 2:
            if ans[-2] == 'lctrl' and ans[-1] == 'q':
                exp_win.close()
                core.quit()

        # check for quit
        if ans[-1] == "q":
            core.quit()

        # quarter messages
        if (trial_count != len(trial_order)) and (not practice) and (trial_count % (len(trial_order)/4)) == 0:
            break_image = visual.ImageStim(exp_win, image='{0}/instructions/{1}/Break_0{2}.png'.
                                                 format(PATH, LANGUAGE, trial_count/(len(trial_order)/4)))
            break_image.setSize(1.3333, '*')
            break_image.draw()
            exp_win.flip()
            event.waitKeys(keyList=['space'])

        trial_count += 1

# ===============================================================================
# prepare psychopy
# ===============================================================================
# gather experiment and subject information
exp_name = 'CompositeFaces'
exp_info = {'Subject': '', 'Subject (repeat)': ''}

# prompt user for subject number
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
if dlg.OK is False:
    core.quit()  # user pressed cancel

# if repetition and original do not match, repeat prompt
while exp_info['Subject'] != exp_info['Subject (repeat)']:
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Please insert matching number in both fields')
    if dlg.OK is False:
        core.quit()  # user pressed cancel

# dictionary with additional info about the experiment
exp_info['date'] = data.getDateStr()  # add a simple timestamp
exp_info['exp_name'] = exp_name


# create a window
exp_win = visual.Window(size=SCREEN_SIZE, monitor="testMonitor", color=(230, 230, 230), fullscr=True,
                        colorSpace='rgb255', units="deg")

# ===============================================================================
# read stimuli
# ===============================================================================
practice_items, practice_trial_order = read_stims('%s/stimuli/Practice_CompositeFaces.txt'%(PATH))

items, trial_order = read_stims('%s/stimuli/Trials_CompositeFaces.txt'%(PATH))

# ===============================================================================
# Other preparations
# ===============================================================================
# width for text wrapping
wrap_width = SCREEN_SIZE[0]-100
font = LANG_FONT_MAP[LANGUAGE]  # font based on language selection

output_file = OUTPATH + exp_info['exp_name'] + '_' + "DE_K" + '_%02i.txt'%(int(exp_info['Subject']))
rt_clock = core.Clock()  # reaction time clock

# fixation cross
fix_cross = visual.TextStim(exp_win, pos=[0, 0], text='+', font='Arial', color=-1, height=FIXCROSS_SIZE,
                            alignHoriz='center', units=u'pix')

# cue upper half
cue_up = visual.SimpleImageStim(exp_win, image='{0}/stimuli/cues/fingers_1.png'.format(PATH), pos=[0, 150], units=u'pix')

# cue lower half
cue_low = visual.SimpleImageStim(exp_win, image='{0}/stimuli/cues/fingers_2.png'.format(PATH), pos=[0, -150],
                                 units=u'pix')

# ------------------------------------------------------------------------------
# read instructions
instructions = []
try:
    for i in range(18):
        if i < 9:
            num = "0" + str(i+1)
        else:
            num = str(i+1)
        image_name = "Intro_CF_" + num
        instructions.append(Image(image_name).buffer(factor=1.33))

    with codecs.open('%s/Reminder.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        rem_text = infile.read()
    with codecs.open('%s/Correct_Screen.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        correct_text = infile.read()
    with codecs.open('%s/Incorrect_Screen.txt'%(PATH), 'rb', encoding='utf-8') as infile:
        incorrect_text = infile.read()
except IOError:
    print 'Error: Language option set to unknown language. Choose DE_K for German (smaller children) ' \
          'or DE_G for German (older children).'
    exp_win.close()
    core.quit()

# task question shown again
reminder_screen = visual.TextStim(exp_win, pos=[0, -300], text=rem_text, font=font, color=-1,
                                  height=INSTR_CHAR_SIZE, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

# feedback screens practice
correct_screen = visual.TextStim(exp_win, pos=[0, 0], text=correct_text, font=font, color=(-1, 1.0, -1),
                                 height=40, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')
incorrect_screen = visual.TextStim(exp_win, pos=[0, 0], text=incorrect_text, font=font, color=(1.0, -1, -1),
                                   height=40, alignHoriz='center', wrapWidth=wrap_width, units=u'pix')

# ===============================================================================
# experiment
# ===============================================================================
# ------------------------------------------------------------------------------
# present instructions
for ii in range(14):
    instructions[ii].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

# ------------------------------------------------------------------------------
# run experiment
with codecs.open(output_file, 'wb', encoding="utf-8") as outfile:

    # write outfile header
    # outfile.write('### Experiment: %s\n### Subject ID: %s\n### Date: %s\n\n' %(exp_info['exp_name'], exp_info['Subject'], exp_info['date']))
    outfile.write('subject_id;trial;trial_id;type;same_or_different;expected_answer;sex;cue;Face_A:_Top_of_face;Face_A:_Bottom_of_face;Face_B:_Top_of_face;Face_B:_Bottom_of_face;Face_A_Original;Face_B_Original;Face_A_Name;Face_B_Name;_;given_answer;correct;reaction_time\n')
    # practice start if no questions
    # Intro_CF_15.draw()
    instructions[14].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

    # run practice trials
    run_trials(practice_items, practice_trial_order, practice=True)

    # practice end
    # Intro_CF_16.draw()
    instructions[15].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])
    
    # exp start screen
    # Intro_CF_17.draw()
    instructions[16].draw()
    exp_win.flip()
    event.waitKeys(keyList=['space'])

    # exp start
    run_trials(items, trial_order)

# Intro_CF_18.draw()
instructions[17].draw()
exp_win.flip()
event.waitKeys()

exp_win.close()
core.quit()
