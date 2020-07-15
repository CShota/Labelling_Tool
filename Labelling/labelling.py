# -*- coding: utf-8 -*-
import re
from maya import cmds
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI
#-------------------------------------------------------
# Base 
#-------------------------------------------------------
def baseWindow():
    mainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(mainWindow), QtWidgets.QWidget)
#-------------------------------------------------------
# Main
#-------------------------------------------------------  
class Gui(QtWidgets.QDialog):
    def __init__(self, parent=baseWindow()):
        super(Gui, self).__init__(parent)
        self.design()
    #---------------------------------------------------
    # Design
    #---------------------------------------------------
    def design(self):    
        # Component
        self.setWindowTitle('Labelling Tool')
        self.setFixedSize(240, 100)
        backLabel = QtWidgets.QLabel()
        backLayout = QtWidgets.QHBoxLayout(self)
        backLayout.addWidget(backLabel)
        searchLabel = QtWidgets.QLabel(' Erase the string', self)
        selectBox = QtWidgets.QComboBox(self)
        selectBox.addItems(["Center", "Left", "Right", "None"])
        searchLine = QtWidgets.QLineEdit(self)
        # Layout
        searchLabel.setGeometry(20, 20, 100, 20)
        selectBox.setGeometry(155, 20, 65, 20)
        searchLine.setGeometry(95, 60, 125, 20)
        # Color
        self.setStyleSheet("background:qlineargradient(x1:0, y1:0, x2:1, y2:1,"
        "stop:0.3 #3494e6, stop:1.0 #ec6ead);")
        backLabel.setStyleSheet("background:rgba(158, 200, 226, 0.4);color:#f5f5f5")
        searchLabel.setStyleSheet("background:rgba(158, 244, 226, 0);color:#f5f5f5")
        selectBox.setStyleSheet("background:rgba(158, 200, 226, 0);color:#f5f5f5;"
        "border-style:solid;border-width:0px;border-color:#f5f5f5;border-radius:0px")
        searchLine.setStyleSheet("background:rgba(158, 200, 226, 0.2);color:#000000;"
        "border-style:solid;border-width:0.5px;border-color:#f5f5f5;border-radius:4px")
        # Instance
        self.searchLine = searchLine
        self.selectBox = selectBox
        # Connect
        searchLine.returnPressed.connect(self.setLabel)
    #---------------------------------------------------
    # processing
    #---------------------------------------------------
    def setLabel(self):
            cmds.undoInfo(openChunk=True)
            searchText = self.searchLine.text()
            selectItem = self.selectBox.currentText()
            selection = cmds.ls(sl=True, type='joint')
            for i in range(len(selection)):
                labelName = re.sub(searchText, '', selection[i])
                cmds.setAttr('{}.{}'.format(selection[i], 'type'), 18)
                cmds.setAttr('{}.{}'.format(selection[i], 'otherType'), 
                labelName, type = 'string')
                if selectItem == 'Center':
                    cmds.setAttr('{}.{}'.format(selection[i], 'side'), 0)
                
                elif selectItem == 'Left':
                    cmds.setAttr('{}.{}'.format(selection[i], 'side'), 1)
                
                elif selectItem == 'Right':
                    cmds.setAttr('{}.{}'.format(selection[i], 'side'), 2) 
                
                elif selectItem == 'None':
                    cmds.setAttr('{}.{}'.format(selection[i], 'side'), 3)
            
            cmds.undoInfo(closeChunk=True)
#-------------------------------------------------------
# Show
#-------------------------------------------------------
if __name__ == '__main__':

    G = Gui()
    G.show()