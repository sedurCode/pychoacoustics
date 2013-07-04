# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2012 Samuele Carcagno <sam.carcagno@gmail.com>
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
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QLocale, SIGNAL, Qt, QEvent
from PyQt4.QtGui import QLabel, QComboBox, QLineEdit
import copy, pickle
from numpy import unique


class experimentersDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.tmpPref = {}
        self.tmpPref['experimenter'] = {}
        self.tmpPref['experimenter'] = copy.deepcopy(self.parent().prm['experimenter'])
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)

        self.sizer = QtGui.QGridLayout()
        self.h1Sizer = QtGui.QHBoxLayout()
        self.v1Sizer = QtGui.QVBoxLayout()
        self.v2Sizer = QtGui.QVBoxLayout()

        n = 0
        self.experimenterLabel =  QLabel(self.tr("Experimenter ID:"), self)
        self.sizer.addWidget(self.experimenterLabel, n, 0)
        self.experimenterChooser = QComboBox()
        self.experimenterChooser.addItems(self.tmpPref['experimenter']['experimenter_id'])
        self.sizer.addWidget(self.experimenterChooser, n, 1)
        self.connect(self.experimenterChooser, QtCore.SIGNAL('activated(QString)'), self.onExperimenterChange)
        self.currIdx = self.experimenterChooser.currentIndex()

        n = n+1
        self.experimenterNameLabel =  QLabel(self.tr("Name:"), self)
        self.sizer.addWidget(self.experimenterNameLabel, n, 0)
        self.experimenterNameTF = QLineEdit("")
        self.experimenterNameTF.setText(self.tmpPref['experimenter']['experimenter_name'][0])
        self.sizer.addWidget(self.experimenterNameTF, n, 1)

        n = n+1
        self.experimenterSurnameLabel =  QLabel(self.tr("Surname:"), self)
        self.sizer.addWidget(self.experimenterSurnameLabel, n, 0)
        self.experimenterSurnameTF = QLineEdit("")
        self.experimenterSurnameTF.setText(self.tmpPref['experimenter']['experimenter_surname'][0])
        self.sizer.addWidget(self.experimenterSurnameTF, n, 1)
        
        n = n+1
        self.experimenterEmailLabel =  QLabel(self.tr("e-mail:"), self)
        self.sizer.addWidget(self.experimenterEmailLabel, n, 0)
        self.experimenterEmailTF = QLineEdit("")
        self.experimenterEmailTF.setText(self.tmpPref['experimenter']['experimenter_email'][0])
        self.sizer.addWidget(self.experimenterEmailTF, n, 1)


        n = n+1
        self.experimenterAddressLabel =  QLabel(self.tr("Address (line 1):"), self)
        self.sizer.addWidget(self.experimenterAddressLabel, n, 0)
        self.experimenterAddressTF = QLineEdit("")
        self.experimenterAddressTF.setText(self.tmpPref['experimenter']['experimenter_address'][0])
        self.sizer.addWidget(self.experimenterAddressTF, n, 1)

        n = n+1
        self.experimenterAddressLabel2 =  QLabel(self.tr("Address (line 2):"), self)
        self.sizer.addWidget(self.experimenterAddressLabel2, n, 0)
        self.experimenterAddressTF2 = QLineEdit("")
        self.experimenterAddressTF2.setText(self.tmpPref['experimenter']['experimenter_address2'][0])
        self.sizer.addWidget(self.experimenterAddressTF2, n, 1)


        n = n+1
        self.experimenterTelephoneLabel =  QLabel(self.tr("Telephone:"), self)
        self.sizer.addWidget(self.experimenterTelephoneLabel, n, 0)
        self.experimenterTelephoneTF = QLineEdit("")
        self.experimenterTelephoneTF.setText(self.tmpPref['experimenter']['experimenter_telephone'][0])
        self.sizer.addWidget(self.experimenterTelephoneTF, n, 1)


        n = n+1
        self.experimenterMobileLabel =  QLabel(self.tr("Mobile:"), self)
        self.sizer.addWidget(self.experimenterMobileLabel, n, 0)
        self.experimenterMobileTF = QLineEdit("")
        self.experimenterMobileTF.setText(self.tmpPref['experimenter']['experimenter_mobile'][0])
        self.sizer.addWidget(self.experimenterMobileTF, n, 1)


        #ADD EXPERIMENTER BUTTON
        addExpButton = QtGui.QPushButton(self.tr("Add Experimenter"), self)
        QtCore.QObject.connect(addExpButton,
                               QtCore.SIGNAL('clicked()'), self.onClickAddExpButton)
        self.v2Sizer.addWidget(addExpButton)
        #REMOVE EXPERIMENTER BUTTON
        removeExpButton = QtGui.QPushButton(self.tr("Remove Experimenter"), self)
        QtCore.QObject.connect(removeExpButton,
                               QtCore.SIGNAL('clicked()'), self.onClickRemoveExpButton)
        self.v2Sizer.addWidget(removeExpButton)
        #CHANGE ID BUTTON
        changeIdButton = QtGui.QPushButton(self.tr("Change Identifier"), self)
        QtCore.QObject.connect(changeIdButton,
                               QtCore.SIGNAL('clicked()'), self.onClickChangeIdButton)
        self.v2Sizer.addWidget(changeIdButton)
        #SET AS DEFAULT BUTTON
        setAsDefaultButton = QtGui.QPushButton(self.tr("Set as default"), self)
        QtCore.QObject.connect(setAsDefaultButton,
                               QtCore.SIGNAL('clicked()'), self.onClickSetAsDefaultButton)
        self.v2Sizer.addWidget(setAsDefaultButton)
        self.v2Sizer.addStretch()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        self.connect(buttonBox.button(QtGui.QDialogButtonBox.Apply),
                     QtCore.SIGNAL("clicked()"), self.onClickApplyButton)
        
        self.h1Sizer.addLayout(self.v2Sizer)
        self.sizer.setAlignment(Qt.AlignTop)
        self.h1Sizer.addLayout(self.sizer)
        self.v1Sizer.addLayout(self.h1Sizer)
        self.v1Sizer.addWidget(buttonBox)
        self.setLayout(self.v1Sizer)

    def onClickApplyButton(self):
        self.tryApply(self.currIdx)
        self.permanentApply()
    def permanentApply(self):
        self.parent().prm['experimenter'] = copy.deepcopy(self.tmpPref['experimenter'])
        f = open(self.parent().prm['experimenterPrefFile'], 'wb')
        pickle.dump(self.parent().prm['experimenter'], f)
        f.close()
        for i in range(self.parent().experimenterChooser.count()):
            self.parent().experimenterChooser.removeItem(0)
        self.parent().experimenterChooser.addItems(self.parent().prm['experimenter']['experimenter_id'])
    def tryApply(self, idx):
        self.tmpPref['experimenter']['experimenter_id'][idx] = self.experimenterChooser.itemText(idx)
        self.tmpPref['experimenter']['experimenter_name'][idx] = self.experimenterNameTF.text()
        self.tmpPref['experimenter']['experimenter_surname'][idx] = self.experimenterSurnameTF.text()
        self.tmpPref['experimenter']['experimenter_email'][idx] = self.experimenterEmailTF.text()
        self.tmpPref['experimenter']['experimenter_address'][idx] = self.experimenterAddressTF.text()
        self.tmpPref['experimenter']['experimenter_address2'][idx] = self.experimenterAddressTF2.text()
        self.tmpPref['experimenter']['experimenter_telephone'][idx] = self.experimenterTelephoneTF.text()
        self.tmpPref['experimenter']['experimenter_mobile'][idx] = self.experimenterMobileTF.text()
    def revertChanges(self):
        if len(self.tmpPref['experimenter']['experimenter_id']) != len(self.parent().prm['experimenter']['experimenter_id']): #experimenter was added, reverting
            for i in range(self.experimenterChooser.count()):
                self.experimenterChooser.removeItem(0)
            self.experimenterChooser.addItems(self.parent().prm['experimenter']['experimenter_id'])
        self.tmpPref['experimenter'] = copy.deepcopy(self.parent().prm['experimenter'])
    def onExperimenterChange(self, experimenterSelected):
        self.prevIdx = self.currIdx
        self.currIdx = self.tmpPref['experimenter']['experimenter_id'].index(experimenterSelected)
        self.tryApply(self.prevIdx)
        if self.tmpPref['experimenter'] != self.parent().prm['experimenter']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.revertChanges()
        self.experimenterNameTF.setText(self.prm['experimenter']['experimenter_name'][self.currIdx])
        self.experimenterSurnameTF.setText(self.prm['experimenter']['experimenter_surname'][self.currIdx])
        self.experimenterEmailTF.setText(self.prm['experimenter']['experimenter_email'][self.currIdx])
        self.experimenterAddressTF.setText(self.prm['experimenter']['experimenter_address'][self.currIdx])
        self.experimenterAddressTF2.setText(self.prm['experimenter']['experimenter_address2'][self.currIdx])
        self.experimenterTelephoneTF.setText(self.prm['experimenter']['experimenter_telephone'][self.currIdx])
        self.experimenterMobileTF.setText(self.prm['experimenter']['experimenter_mobile'][self.currIdx])
   
        
       
    def onClickAddExpButton(self):
        self.tryApply(self.currIdx)
        if self.tmpPref['experimenter'] != self.parent().prm['experimenter']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.revertChanges()
        msg = self.tr("Experimenter's Identifier:")
        name, ok = QtGui.QInputDialog.getText(self, self.tr('Input Dialog'), msg)
        if ok:
            self.tmpPref['experimenter']['defaultExperimenter'].append('')
            self.tmpPref['experimenter']['experimenter_id'].append(name)
            self.tmpPref['experimenter']['experimenter_name'].append('')
            self.tmpPref['experimenter']['experimenter_surname'].append('')
            self.tmpPref['experimenter']['experimenter_email'].append('')
            self.tmpPref['experimenter']['experimenter_address'].append('')
            self.tmpPref['experimenter']['experimenter_address2'].append('')
            self.tmpPref['experimenter']['experimenter_telephone'].append('')
            self.tmpPref['experimenter']['experimenter_mobile'].append('')
            self.permanentApply()
            self.currIdx = self.experimenterChooser.count() 
            self.experimenterNameTF.setText(self.tmpPref['experimenter']['experimenter_name'][self.currIdx])
            self.experimenterSurnameTF.setText(self.tmpPref['experimenter']['experimenter_surname'][self.currIdx])
            self.experimenterEmailTF.setText(self.tmpPref['experimenter']['experimenter_email'][self.currIdx])
            self.experimenterAddressTF.setText(self.tmpPref['experimenter']['experimenter_address'][self.currIdx])
            self.experimenterAddressTF2.setText(self.tmpPref['experimenter']['experimenter_address2'][self.currIdx])
            self.experimenterTelephoneTF.setText(self.tmpPref['experimenter']['experimenter_telephone'][self.currIdx])
            self.experimenterMobileTF.setText(self.tmpPref['experimenter']['experimenter_mobile'][self.currIdx])
            self.experimenterChooser.addItem(name)
            self.experimenterChooser.setCurrentIndex(self.currIdx)
    
    def onClickRemoveExpButton(self):
        self.tryApply(self.currIdx)
        if self.tmpPref['experimenter'] != self.parent().prm['experimenter']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.revertChanges()
        if self.experimenterChooser.count() > 1:
            reply = QtGui.QMessageBox.warning(self, self.tr('Message'),
                                              "Remove experimenter? This action cannot be undone!", QtGui.QMessageBox.Yes | 
                                              QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.tmpPref['experimenter']['defaultExperimenter'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_id'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_name'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_surname'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_email'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_address'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_address2'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_telephone'].pop(self.currIdx)
                self.tmpPref['experimenter']['experimenter_mobile'].pop(self.currIdx)
                self.experimenterChooser.removeItem(self.currIdx)
                self.currIdx = self.experimenterChooser.currentIndex()
                self.permanentApply()
                self.experimenterNameTF.setText(self.tmpPref['experimenter']['experimenter_name'][self.currIdx])
                self.experimenterSurnameTF.setText(self.tmpPref['experimenter']['experimenter_surname'][self.currIdx])
                self.experimenterEmailTF.setText(self.tmpPref['experimenter']['experimenter_email'][self.currIdx])
                self.experimenterAddressTF.setText(self.tmpPref['experimenter']['experimenter_address'][self.currIdx])
                self.experimenterAddressTF2.setText(self.tmpPref['experimenter']['experimenter_address2'][self.currIdx])
                self.experimenterTelephoneTF.setText(self.tmpPref['experimenter']['experimenter_telephone'][self.currIdx])
                self.experimenterMobileTF.setText(self.tmpPref['experimenter']['experimenter_mobile'][self.currIdx])
            else:
                QtGui.QMessageBox.warning(self, self.tr('Message'),
                                          self.tr("Only one experimenter left. Experimenter cannot be removed!"), QtGui.QMessageBox.Ok)

    def onClickChangeIdButton(self):
        self.tryApply(self.currIdx)
        if self.tmpPref['experimenter'] != self.parent().prm['experimenter']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.revertChanges()
        msg = self.tr("Experimenter's Identifier:")
        name, ok = QtGui.QInputDialog.getText(self, self.tr('Input Dialog'), msg)
        if ok:
            self.tmpPref['experimenter']['experimenter_id'][self.currIdx] = name
            self.experimenterChooser.setItemText(self.currIdx, name)
            self.permanentApply()
    def onClickSetAsDefaultButton(self):
        idx = self.experimenterChooser.currentIndex()
        print(idx)
        self.tryApply(self.currIdx)
        if self.tmpPref['experimenter'] != self.parent().prm['experimenter']:
            conf = applyChanges(self)
            if conf.exec_():
                self.permanentApply()
            else:
                self.revertChanges()
        
        for i in range(len(self.parent().prm['experimenter']["defaultExperimenter"])):
            if i == idx:
                self.tmpPref['experimenter']["defaultExperimenter"][i] = "\u2713"
            else:
                self.tmpPref['experimenter']["defaultExperimenter"][i] = "\u2012"
        print(self.tmpPref)
        self.permanentApply()

class applyChanges(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        grid = QtGui.QGridLayout()
        n = 0
        label = QtGui.QLabel(self.tr('There are unsaved changes. Apply Changes?'))
        grid.addWidget(label, n, 1)
        n = n+1
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Apply Changes"))


  
  

     