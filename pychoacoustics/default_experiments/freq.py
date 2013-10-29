# -*- coding: utf-8 -*-

"""
This experiment can be used to measure pure-tone frequency-discrimination
thresholds.

The available fields are:

- Frequency (Hz) :
    Signal frequency in Hz
- Difference (%) :
    Frequency difference (for constant procedures),
    or starting frequency difference (for adaptive procedures),
    between the standard and comparison stimuli. The difference
    is measured as a percentage of the standard frequency in Hz.
- Level (dB SPL) :
    Signal level in dB SPL
- Duration (ms) :
    Signal duration (excluding ramps), in ms
- Ramps (ms) :
    Duration of each ramp, in ms

The available choosers are:

- Ear: [``Right``, ``Left``, ``Both``]
    The ear to which the signal will be presented

"""

from ..sndlib import*
from ..pyqtver import*
if pyqtversion == 4:
    from PyQt4.QtGui import QApplication
elif pyqtversion == 5:
    from PyQt5.QtWidgets import QApplication

                                                                              
def initialize_freq(prm):
    exp_name = "Frequency Discrimination Demo"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Adaptive",
                                        "Weighted Up/Down",
                                        "Constant m-Intervals n-Alternatives"]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasIntervalLights"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Geometric","", QApplication.UnicodeUTF8)
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "freq"
    return prm

def select_default_parameters_freq(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    
    fieldLabel.append("Frequency (Hz)")
    field.append(1000)

    fieldLabel.append("Difference (%)")
    field.append(20)
    
    fieldLabel.append("Level (dB SPL)")
    field.append(50)
    
    fieldLabel.append("Duration (ms)")
    field.append(180)
    
    fieldLabel.append("Ramps (ms)")
    field.append(10)

    
    chooserOptions.append(["Right",
                           "Left",
                           "Both"])
    chooserLabel.append("Ear:")
    chooser.append("Right")
   
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

    
def doTrial_freq(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
        parent.writeResultsHeader('log')

    frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
    level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
    phase = 0
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
    
    correctFrequency = frequency + (frequency*parent.prm['adaptiveDifference'])/100
    stimulusCorrect = pureTone(correctFrequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])

      
            
    stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)
