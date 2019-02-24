# -*- coding: utf-8 -*- 
#   Copyright (C) 2008-2019 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import matplotlib

from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import QCheckBox, QIcon, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PyQt4"
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtGui import QCheckBox, QIcon, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PySide"
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtGui import QIcon
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
import numpy as np
import copy, os
from numpy import arange, ceil, floor, linspace, log10
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
import matplotlib as mpl
#import pandas as pd
import matplotlib.font_manager as fm

from .pysdt import*
from .PSI_method import*
from .utils_general import*

#mpl.rcParams['font.family'] = 'sans-serif'

#fontPath = os.path.abspath(os.path.dirname(__file__)+'/../') + '/data/Ubuntu-R.ttf'
#fontPath = '/media/ntfsShared/lin_home/auditory/code/pychoacoustics/pychoacoustics-qt4/development/dev/data/Ubuntu-R.ttf'
#prop = fm.FontProperties(fname=fontPath)
#mpl.rcParams.update({'font.size': 16})


class PSIParSpacePlot(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.prm = prm
     
            
        self.pchs = ["o", "s", "v", "p", "h", "8", "*", "x", "+", "d", ",", "^", "<", ">", "1", "2", "3", "4", "H", "D", ".", "|", "_"]  


        mpl.rcParams['xtick.major.size'] = 6
        mpl.rcParams['xtick.minor.size'] = 4
        mpl.rcParams['xtick.major.width'] = 1
        mpl.rcParams['xtick.minor.width'] = 1
        mpl.rcParams['ytick.major.size'] = 9
        mpl.rcParams['ytick.minor.size'] = 5
        mpl.rcParams['ytick.major.width'] = 0.8
        mpl.rcParams['ytick.minor.width'] = 0.8
        mpl.rcParams['xtick.direction'] = 'out'
        mpl.rcParams['ytick.direction'] = 'out'
        mpl.rcParams['font.size'] = 14
        mpl.rcParams['figure.facecolor'] = 'white'
        mpl.rcParams['lines.color'] = 'black'
        mpl.rcParams['axes.color_cycle'] = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]#['k', 'b', 'g', 'r', 'c', 'm', 'y']

        self.mw = QWidget(self)
        self.vbl = QVBoxLayout(self.mw)
        self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
        self.ax4 = self.fig.add_subplot(221) #stimulus
        self.ax1 = self.fig.add_subplot(222) #midpoint
        self.ax2 = self.fig.add_subplot(223) #slope
        self.ax3 = self.fig.add_subplot(224) #lapse

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
        self.ntb = NavigationToolbar(self.canvas, self.mw)
      

        self.logAxisMidpoint = QCheckBox(self.tr("Stim./Midpoint Log Axis"))
        self.logAxisMidpoint.stateChanged[int].connect(self.toggleMidpointLogAxis)

        self.logAxisSlope = QCheckBox(self.tr("Slope Log Axis"))
        self.logAxisSlope.stateChanged[int].connect(self.toggleSlopeLogAxis)

        self.logAxisLapse = QCheckBox(self.tr("Lapse Log Axis"))
        self.logAxisLapse.stateChanged[int].connect(self.toggleLapseLogAxis)

        self.updateButton = QPushButton(self.tr("Update"), self)
        self.updateButton.setIcon(QIcon.fromTheme("view-refresh", QIcon(":/view-refresh")))
        self.updateButton.clicked.connect(self.onClickUpdateButton)
        
        self.ntbBox = QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.logAxisMidpoint)
        self.ntbBox.addWidget(self.logAxisSlope)
        self.ntbBox.addWidget(self.logAxisLapse)
        self.ntbBox.addWidget(self.updateButton)
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)

        self.getPSIPars()
        if self.stimScaling == "Linear":
            self.logAxisMidpoint.setChecked(False)
            self.plotDataMidpoint()
            self.plotDataStimulus()
        elif self.stimScaling == "Logarithmic":
            self.logAxisMidpoint.setChecked(True)
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()

        if self.slopeSpacing == "Linear":
            self.logAxisSlope.setChecked(False)
            self.plotDataSlope()
        elif self.slopeSpacing == "Logarithmic":
            self.logAxisSlope.setChecked(True)
            self.plotDataSlopeLogAxis()

        if self.lapseSpacing == "Linear":
            self.logAxisLapse.setChecked(False)
            self.plotDataLapse()
        elif self.lapseSpacing == "Logarithmic":
            self.logAxisLapse.setChecked(True)
            self.plotDataLapseLogAxis()

        self.fig.suptitle(self.tr("PSI Parameter Space"))
        self.show()
        self.canvas.draw()

    def getPSIPars(self):

        self.psyFun = self.parent().psyFunChooser.currentText()
        self.loStim = self.parent().currLocale.toDouble(self.parent().loStim.text())[0]
        self.hiStim = self.parent().currLocale.toDouble(self.parent().hiStim.text())[0]
        self.stimGridStep = self.parent().currLocale.toDouble(self.parent().stimGridStep.text())[0]
        self.stimScaling = self.parent().stimScalingChooser.currentText()
        self.loMidPoint = self.parent().currLocale.toDouble(self.parent().loMidPoint.text())[0]
        self.hiMidPoint = self.parent().currLocale.toDouble(self.parent().hiMidPoint.text())[0]
        self.threshGridStep = self.parent().currLocale.toDouble(self.parent().threshGridStep.text())[0]
        self.threshPrior = self.parent().threshPriorChooser.currentText()
        self.threshPriorMu = self.parent().currLocale.toDouble(self.parent().threshPriorMu.text())[0]
        self.threshPriorSTD = self.parent().currLocale.toDouble(self.parent().threshPriorSTD.text())[0]
        self.loSlope = self.parent().currLocale.toDouble(self.parent().loSlope.text())[0]
        self.hiSlope = self.parent().currLocale.toDouble(self.parent().hiSlope.text())[0]
        self.slopeGridStep =  self.parent().currLocale.toDouble(self.parent().slopeGridStep.text())[0]
        self.slopeSpacing = self.parent().slopeSpacingChooser.currentText()
        self.slopePrior = self.parent().slopePriorChooser.currentText()
        self.slopePriorMu = self.parent().currLocale.toDouble(self.parent().slopePriorMu.text())[0]
        self.slopePriorSTD = self.parent().currLocale.toDouble(self.parent().slopePriorSTD.text())[0]
        self.loLapse = self.parent().currLocale.toDouble(self.parent().loLapse.text())[0]
        self.hiLapse = self.parent().currLocale.toDouble(self.parent().hiLapse.text())[0]
        self.lapseGridStep =  self.parent().currLocale.toDouble(self.parent().lapseGridStep.text())[0]
        self.lapseSpacing = self.parent().lapseSpacingChooser.currentText()
        self.lapsePrior = self.parent().lapsePriorChooser.currentText()
        self.lapsePriorMu = self.parent().currLocale.toDouble(self.parent().lapsePriorMu.text())[0]
        self.lapsePriorSTD = self.parent().currLocale.toDouble(self.parent().lapsePriorSTD.text())[0]
        self.nAlternatives = int(self.parent().nAlternativesChooser.currentText())

        self.margLapse = self.parent().margLapseChooser.currentText()
        self.margSlope = self.parent().margSlopeChooser.currentText()
        self.margThresh = self.parent().margThreshChooser.currentText()

        if self.margThresh == "Yes" or self.margSlope == "Yes" or self.margLapse == "Yes":
            ax = np.array([])
            if self.margThresh == "Yes":
                ax = numpy.append(ax, 0)
            if self.margSlope == "Yes":
                ax = numpy.append(ax, 1)
            if self.margLapse == "Yes":
                ax = numpy.append(ax, 2)
            ax = tuple(np.sort(ax))
        else:
            ax = None

        if self.stimScaling == "Linear":
            self.PSI = setupPSI(model=self.psyFun,
                                x0=1,
                                xLim=(self.loStim, self.hiStim),
                                xStep=self.stimGridStep,
                                stimScale=self.stimScaling,
                                alphaLim=(self.loMidPoint, self.hiMidPoint),
                                alphaStep=self.threshGridStep,
                                alphaSpacing="Linear",
                                alphaDist=self.threshPrior,
                                alphaMu=self.threshPriorMu,
                                alphaSTD=self.threshPriorSTD,
                                betaLim=(self.loSlope, self.hiSlope),
                                betaStep=self.slopeGridStep,
                                betaSpacing=self.slopeSpacing,
                                betaDist=self.slopePrior,
                                betaMu=self.slopePriorMu,
                                betaSTD=self.slopePriorSTD,
                                gamma=1/self.nAlternatives,
                                lambdaLim=(self.loLapse, self.hiLapse),
                                lambdaStep=self.lapseGridStep,
                                lambdaSpacing=self.lapseSpacing,
                                lambdaDist=self.lapsePrior,
                                lambdaMu=self.lapsePriorMu,
                                lambdaSTD=self.lapsePriorSTD,
                                marginalize = ax)
        elif self.stimScaling == "Logarithmic":
            self.PSI = setupPSI(model=self.psyFun,
                                x0=1,
                                xLim=(abs(self.loStim), abs(self.hiStim)),
                                xStep=self.stimGridStep,
                                stimScale=self.stimScaling,
                                alphaLim=(abs(self.loMidPoint), abs(self.hiMidPoint)),
                                alphaStep=self.threshGridStep,
                                alphaSpacing="Linear",
                                alphaDist=self.threshPrior,
                                alphaMu=abs(self.threshPriorMu),
                                alphaSTD=self.threshPriorSTD,
                                betaLim=(self.loSlope, self.hiSlope),
                                betaStep=self.slopeGridStep,
                                betaSpacing=self.slopeSpacing,
                                betaDist=self.slopePrior,
                                betaMu=self.slopePriorMu,
                                betaSTD=self.slopePriorSTD,
                                gamma=1/self.nAlternatives,
                                lambdaLim=(self.loLapse, self.hiLapse),
                                lambdaStep=self.lapseGridStep,
                                lambdaSpacing=self.lapseSpacing,
                                lambdaDist=self.lapsePrior,
                                lambdaMu=self.lapsePriorMu,
                                lambdaSTD=self.lapsePriorSTD,
                                marginalize = ax)

    
    def plotDataMidpoint(self):
        self.ax1.clear()
        self.A = setPrior(self.PSI["a"], self.PSI["par"]["alpha"])
        
        if self.stimScaling == "Linear":
            markerline, stemlines, baseline = self.ax1.stem(self.PSI["alpha"], self.A[:,0,0], 'k')
        elif self.stimScaling == "Logarithmic":
            markerline, stemlines, baseline = self.ax1.stem(exp(self.PSI["alpha"]), self.A[:,0,0]/exp(self.PSI["alpha"]), 'k')
            if self.loStim < 0:
                self.ax1.set_xticklabels(list(map(str, -self.ax1.get_xticks())))
                
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

    def plotDataSlope(self):
        self.ax2.clear()
        self.B = setPrior(self.PSI["b"], self.PSI["par"]["beta"])
        if self.PSI["par"]["beta"]["spacing"] == "Linear":
            markerline, stemlines, baseline = self.ax2.stem(self.PSI["beta"], self.B[0,:,0], 'k')
        elif self.PSI["par"]["beta"]["spacing"] == "Logarithmic":
            markerline, stemlines, baseline = self.ax2.stem(self.PSI["beta"], self.B[0,:,0]/self.PSI["beta"], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nBeta = len(self.B[0,:,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataLapse(self):
        self.ax3.clear()
        L = setPrior(self.PSI["l"], self.PSI["par"]["lambda"])
        if self.PSI["par"]["lambda"]["spacing"] == "Linear":
            markerline, stemlines, baseline = self.ax3.stem(self.PSI["lambda"], L[0,0,:], 'k')
        elif self.PSI["par"]["lambda"]["spacing"] == "Logarithmic":
            markerline, stemlines, baseline = self.ax3.stem(self.PSI["lambda"], L[0,0,:]/self.PSI["lambda"], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nLambda = len(L[0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))

    def plotDataStimulus(self):
        self.ax4.clear()

        nStim = len(self.PSI["stims"])
        if self.stimScaling == "Linear":
            markerline, stemlines, baseline = self.ax4.stem(self.PSI["stims"], np.ones(nStim), 'k')
        elif self.stimScaling == "Logarithmic":
            markerline, stemlines, baseline = self.ax4.stem(exp(self.PSI["stims"]), np.ones(nStim), 'k')
            if self.loStim < 0:
                self.ax4.set_xticklabels(list(map(str, -self.ax4.get_xticks())))
            
        plt.setp(markerline, 'markerfacecolor', 'k')
        self.ax4.set_title("Stimulus, #Points " + str(nStim))


    def plotDataMidpointLogAxis(self):
        self.ax1.clear()
        self.A = setPrior(self.PSI["a"], self.PSI["par"]["alpha"])

        if self.stimScaling == "Logarithmic":
            x = self.PSI["alpha"]
            markerline, stemlines, baseline = self.ax1.stem(x, self.A[:,0,0], 'k')
        elif self.stimScaling == "Linear":
            x = log(self.PSI["alpha"])
            markerline, stemlines, baseline = self.ax1.stem(x, self.A[:,0,0]*self.PSI["alpha"], 'k')
      
        setLogTicks(self.ax1, exp(1))   
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

    def plotDataSlopeLogAxis(self):
        self.ax2.clear()
        self.B = setPrior(self.PSI["b"], self.PSI["par"]["beta"])
        if self.PSI["par"]["beta"]["spacing"] == "Logarithmic":
            markerline, stemlines, baseline = self.ax2.stem(log(self.PSI["beta"]), self.B[0,:,0], 'k')
        elif self.PSI["par"]["beta"]["spacing"] == "Linear":
            markerline, stemlines, baseline = self.ax2.stem(log(self.PSI["beta"]), self.B[0,:,0]*self.PSI["beta"], 'k')

        setLogTicks(self.ax2, exp(1))
        plt.setp(markerline, 'markerfacecolor', 'k')
        
        nBeta = len(self.B[0,:,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataLapseLogAxis(self):
        self.ax3.clear()
        L = setPrior(self.PSI["l"], self.PSI["par"]["lambda"])
        if self.PSI["par"]["lambda"]["spacing"] == "Logarithmic":
            markerline, stemlines, baseline = self.ax3.stem(log(self.PSI["lambda"]), L[0,0,:], 'k')
        elif self.PSI["par"]["lambda"]["spacing"] == "Linear":
            markerline, stemlines, baseline = self.ax3.stem(log(self.PSI["lambda"]), L[0,0,:]*self.PSI["lambda"], 'k')

        setLogTicks(self.ax3, exp(1))
        plt.setp(markerline, 'markerfacecolor', 'k')
      
        nLambda = len(L[0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))

    def plotDataStimulusLogAxis(self):
        self.ax4.clear()

        nStim = len(self.PSI["stims"])
        if self.stimScaling == "Logarithmic":
            x = self.PSI["stims"]
        elif self.stimScaling == "Linear":
            x = log(self.PSI["stims"])

            
        markerline, stemlines, baseline = self.ax4.stem(x, np.ones(nStim), 'k')
        setLogTicks(self.ax4, exp(1))
        plt.setp(markerline, 'markerfacecolor', 'k')
        
        self.ax4.set_title("Stimulus, #Points " + str(nStim))

    def onClickUpdateButton(self):
        self.getPSIPars()
        
        if self.logAxisMidpoint.isChecked() == False:
            self.plotDataMidpoint()
            self.plotDataStimulus()
        else:
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()

        if self.logAxisSlope.isChecked() == False:
            self.plotDataSlope()
        else:
            self.plotDataSlopeLogAxis()

        if self.logAxisLapse.isChecked() == False:
            self.plotDataLapse()
        else:
            self.plotDataLapseLogAxis()

        self.canvas.draw()
        
    def toggleMidpointLogAxis(self):
        if self.logAxisMidpoint.isChecked() == True:
            self.plotDataMidpointLogAxis()
            self.plotDataStimulusLogAxis()
        else:
            self.plotDataMidpoint()
            self.plotDataStimulus()
        self.canvas.draw()

    def toggleSlopeLogAxis(self):
        if self.logAxisSlope.isChecked() == True:
            self.plotDataSlopeLogAxis()
        else:
            self.plotDataSlope()
        self.canvas.draw()

    def toggleLapseLogAxis(self):
        if self.logAxisLapse.isChecked() == True:
            self.plotDataLapseLogAxis()
        else:
            self.plotDataLapse()
        self.canvas.draw()
           




