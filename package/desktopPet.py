import sys, os, math, time
import numpy as np
import random as rd

from PyQt5 import QtCore, QtWidgets, QtGui

class mainFrame(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(mainFrame, self).__init__(parent);
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint);
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);

        self.cowSize = QtCore.QSize(200*1.21, 200);
        self.setFixedSize(self.cowSize*1.2);
        self.screenGeo = QtWidgets.QDesktopWidget().screenGeometry();
        self.availGeo  = QtWidgets.QDesktopWidget().availableGeometry();
        randW = rd.random()*0.6 + 0.2;
        randH = rd.random()*0.4 + 0.3;
        self.currLoc = [self.screenGeo.width()*randW, \
                        self.screenGeo.height()*randH];
        self.move(self.currLoc[0], self.currLoc[1]);
        self.keyPool = [QtCore.Qt.Key_Left, QtCore.Qt.Key_Right,
                        QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,
                        QtCore.Qt.Key_S, QtCore.Qt.Key_P,
                        QtCore.Qt.Key_I, QtCore.Qt.Key_N];
        self.pressedKeys = {QtCore.Qt.Key_Left:  False,
                            QtCore.Qt.Key_Right: False,
                            QtCore.Qt.Key_Up:    False,
                            QtCore.Qt.Key_Down:  False,
                            QtCore.Qt.Key_S: False,
                            QtCore.Qt.Key_P: False,
                            QtCore.Qt.Key_I: False,
                            QtCore.Qt.Key_N: False,};
        self.lrDirection = "";
        self.udDirection = "";
        self.movieTracker = "";
        self.movieCounter = -400;
        self.lrDirIdleMove = "";
        self.udDirIdleMove = "";

        self.nextAct = {};
        self.nextAct["IdleLeft"] = {"IdleLeft": 0.5,
                                    "Moo1Left": 0.2,
                                    "Moo2Left": 0.1,
                                    "DownLeft": 0.1,
                                    "move"    : 0.1};
        self.nextAct["Moo1Left"] = {"IdleLeft": 0.5,
                                    "Moo1Left": 0.2,
                                    "Moo2Left": 0.1,
                                    "DownLeft": 0.1,
                                    "move":     0.1};
        self.nextAct["Moo2Left"] = {"IdleLeft": 0.5,
                                    "Moo1Left": 0.2,
                                    "Moo2Left": 0.1,
                                    "DownLeft": 0.1,
                                    "move":     0.1};
        self.nextAct["DownLeft"] = {"DownMunchLeft": 1.0};
        self.nextAct["UpLeft"]   = {"UpMunchLeft":   1.0};
        self.nextAct["DownMunchLeft"] = {"DownMunchLeft": 0.6,
                                         "UpLeft":        0.4};
        self.nextAct["UpMunchLeft"]   = {"UpMunchLeft":   0.7,
                                         "DownLeft":      0.1,
                                         "IdleLeft":      0.1,
                                         "Moo1Left":      0.1};
        self.nextAct["IdleRight"] = {"IdleRight": 0.5,
                                     "Moo1Right": 0.2,
                                     "Moo2Right": 0.1,
                                     "DownRight": 0.1,
                                     "move":      0.1};
        self.nextAct["Moo1Right"] = {"IdleRight": 0.5,
                                     "Moo1Right": 0.2,
                                     "Moo2Right": 0.1,
                                     "DownRight": 0.1,
                                     "move":      0.1};
        self.nextAct["Moo2Right"] = {"IdleRight": 0.5,
                                     "Moo1Right": 0.2,
                                     "Moo2Right": 0.1,
                                     "DownRight": 0.1,
                                     "move":      0.1};
        self.nextAct["DownRight"] = {"DownMunchRight": 1.0};
        self.nextAct["UpRight"]   = {"UpMunchRight":   1.0};
        self.nextAct["DownMunchRight"] = {"DownMunchRight": 0.6,
                                          "UpRight":        0.4};
        self.nextAct["UpMunchRight"]   = {"UpMunchRight":   0.7,
                                          "DownRight":      0.1,
                                          "IdleRight":      0.1,
                                          "Moo1Right":      0.1};
        self.nextAct["move"] = {"move":      0.6,
                                "IdleLeft":  0.2,
                                "IdleRight": 0.2}
        self.changeDirProbIdleMove = 0.3;
 
        for name, nextAction in self.nextAct.items():
            norm = 0;
            for action, prob in nextAction.items():
                norm = norm + prob;
            if abs(norm - 1.0) > pow(10, -6):
                print("BUG: nextAct probabilities are not entered correctly for");
                print(name);
                self.close();
                sys.exit(0);
        self.initUI();
    def initUI(self):
        gifPath = os.getcwd() + "/figures/cowIdleLeft.gif";
        self.cow = QtGui.QMovie(gifPath, QtCore.QByteArray(), self);
        self.cow.setScaledSize(self.cowSize);
        self.cow.setCacheMode(QtGui.QMovie.CacheAll);
        #self.cow.setSpeed(100);
        self.cowScreen = QtWidgets.QLabel();
        self.cowScreen.setAlignment(QtCore.Qt.AlignCenter);
        self.cowScreen.setMovie(self.cow);

        layout = QtWidgets.QVBoxLayout();
        layout.addWidget(self.cowScreen);
        self.setLayout(layout);

        self.liveTimer = QtCore.QTimer(self);
        self.liveTimer.timeout.connect(self.liveAction);
        self.liveTimer.start(20);
        
        self.button = QtWidgets.QPushButton(self);
        self.button.setText("");
        self.button.setGeometry(QtCore.QRect(18, 22, self.cowSize.width(), \
                                                     self.cowSize.height()));
        self.button.setStyleSheet("background-color: transparent;");
        self.button.clicked.connect(self.buttonClick);
 
        self.show();
    def runCow(self):
        self.cow.stop();
        gifPath = os.getcwd() + "/figures/cow" + self.movieTracker + ".gif";
        if "move" in self.movieTracker:
            if "left" in self.lrDirection: 
                gifPath = os.getcwd() + "/figures/cowWalkLeft.gif";
            elif "right" in self.lrDirection:
                gifPath = os.getcwd() + "/figures/cowWalkRight.gif";
        self.cow.setFileName(gifPath);
        self.cow.start();
        self.cow.loopCount();
        self.cowScreen.setMovie(self.cow);
    def keyPressEvent(self, event):
        key = event.key();
        if key in self.keyPool:
            self.pressedKeys[key] = True;
    def keyReleaseEvent(self, event):
        key = event.key();
        if key in self.keyPool:
            self.pressedKeys[key] = False;
    def liveAction(self):
        self.movieCounter = min(10000, self.movieCounter+1);
        movementSpeed = 1.0;
        movieCNegCap = -400;            #should be < movieCIdleRefreshRate
        movieCIdleRefreshRate = -200;   #should be < 0
        movieCThres = 100;              #should be > 0
        if self.movieCounter >= movieCThres:
            movementSpeed = (100+self.movieCounter-movieCThres)/50.0;
        #key processing
        keyLeft  = self.pressedKeys[QtCore.Qt.Key_Left];
        keyRight = self.pressedKeys[QtCore.Qt.Key_Right];
        keyUp    = self.pressedKeys[QtCore.Qt.Key_Up];
        keyDown  = self.pressedKeys[QtCore.Qt.Key_Down];
        keyPressedSPIN = self.pressedKeys[QtCore.Qt.Key_S] or \
                         self.pressedKeys[QtCore.Qt.Key_P] or \
                         self.pressedKeys[QtCore.Qt.Key_I] or \
                         self.pressedKeys[QtCore.Qt.Key_N];
        keyPressedN = keyLeft or keyRight or keyUp or keyDown or\
                      keyPressedSPIN;
        if keyLeft == True and keyRight == True:
            if "both" not in self.lrDirection:
                if self.lrDirection == "right":
                    self.lrDirection = "left_both";
                elif self.lrDirection == "left":
                    self.lrDirection = "right_both";
        elif keyLeft == True:
            self.lrDirection = "left";
        elif keyRight == True:
            self.lrDirection = "right";
        else:
            if "both" in self.lrDirection:
                self.lrDirection = self.lrDirection[:-5];
        if keyUp == True and keyDown == True:
            if "both" not in self.udDirection:
                if self.udDirection == "down":
                    self.udDirection = "up_both";
                elif self.udDirection == "up":
                    self.udDirection = "down_both";
        elif keyUp == True:
            self.udDirection = "up";
        elif keyDown == True: 
            self.udDirection = "down";       
        else:
            self.udDirection = "";
        #idle processing + action
        if keyPressedN == False:
            if "move" in self.movieTracker:
                movementSpeed = 0.5;
                if self.lrDirIdleMove != "" and self.udDirIdleMove != "":
                    movementSpeed = movementSpeed/np.sqrt(2);
                if "left" in self.lrDirIdleMove:
                    self.currLoc[0] -= movementSpeed; 
                elif "right" in self.lrDirIdleMove:
                    self.currLoc[0] += movementSpeed;
                if "up" in self.udDirIdleMove:
                    self.currLoc[1] -= movementSpeed;
                elif "down" in self.udDirIdleMove:
                    self.currLoc[1] += movementSpeed;
                if self.movieCounter == 0:
                    self.movieCounter = movieCIdleRefreshRate;
                    self.idleMode();
            elif self.movieCounter > 0:
                self.movieCounter = movieCNegCap;
            elif self.movieCounter < movieCIdleRefreshRate or\
                 "Walk" in self.movieTracker or \
                 "Float" in self.movieTracker:
                self.lrDirIdleMove = "";
                self.udDirIdleMove = "";
                if "left" in self.lrDirection:
                    if self.movieTracker != "IdleLeft":
                        self.movieTracker = "IdleLeft";
                        self.runCow();
                elif "right" in self.lrDirection:
                    if self.movieTracker != "IdleRight":
                        self.movieTracker = "IdleRight";
                        self.runCow();
            else:
                self.lrDirIdleMove = "";
                self.udDirIdleMove = "";
                if self.movieCounter == 0:
                    self.movieCounter = movieCIdleRefreshRate;
                    self.idleMode();
        #key action
        if keyPressedSPIN == True:
            self.lrDirIdleMove = "";
            self.udDirIdleMove = "";
            self.movieCounter = movieCNegCap;
            if self.lrDirection == "left":
                if self.movieTracker != "ZRotatingLeft":
                    self.movieTracker = "ZRotatingLeft";
                    self.runCow();
            elif self.lrDirection == "right":
                if self.movieTracker != "ZRotatingRight":
                    self.movieTracker = "ZRotatingRight";
                    self.runCow();
        else:
            if keyLeft == True or keyRight == True:
                self.lrDirIdleMove = "";
                self.udDirIdleMove = "";
                if self.udDirection != "":
                    movementSpeed = movementSpeed/np.sqrt(2);
                if self.movieCounter < movieCThres:
                    if "left" in self.lrDirection:
                        self.currLoc[0] -= movementSpeed;
                        if self.movieTracker != "WalkLeft":
                            self.movieTracker = "WalkLeft";
                            self.runCow();
                    elif "right" in self.lrDirection:
                        self.currLoc[0] += movementSpeed;
                        if self.movieTracker != "WalkRight":
                            self.movieTracker = "WalkRight";
                            self.runCow();
                elif self.movieCounter >= movieCThres:
                    if "left" in self.lrDirection:
                        self.currLoc[0] -= movementSpeed;
                        if self.movieTracker != "FloatLeft":
                            self.movieTracker = "FloatLeft";
                            self.runCow();
                    elif "right" in self.lrDirection:
                        self.currLoc[0] += movementSpeed;
                        if self.movieTracker != "FloatRight":
                            self.movieTracker = "FloatRight";
                            self.runCow();
            if keyUp == True or keyDown == True:
                self.lrDirIdleMove = "";
                self.udDirIdleMove = "";
                if self.movieCounter < movieCThres:
                    if "left" in self.lrDirection:
                        if self.movieTracker != "WalkLeft":
                            self.movieTracker = "WalkLeft";
                            self.runCow();
                    elif "right" in self.lrDirection:
                        if self.movieTracker != "WalkRight":
                            self.movieTracker = "WalkRight";
                            self.runCow();
                elif self.movieCounter >= movieCThres:
                    if "left" in self.lrDirection:
                        if self.movieTracker != "FloatLeft":
                            self.movieTracker = "FloatLeft";
                            self.runCow();
                    elif "right" in self.lrDirection:
                        if self.movieTracker != "FloatRight":
                            self.movieTracker = "FloatRight";
                            self.runCow();
                if "up" in self.udDirection:
                    self.currLoc[1] -= movementSpeed;
                elif "down" in self.udDirection:
                    self.currLoc[1] += movementSpeed;
        self.currLoc[0] = self.currLoc[0]%self.screenGeo.width();
        self.currLoc[1] = max(self.availGeo.y(),\
                              self.currLoc[1]%\
                              (self.screenGeo.height()-self.cowSize.height()/2));
        self.move(self.currLoc[0]-self.cowSize.width()/2, self.currLoc[1]);
        if self.lrDirection == "":
            if rd.random() < 0.5:
                self.lrDirection = "left";
            else:
                self.lrDirection = "right";
    def idleMode(self):
        rand = rd.random();
        probCum = 0;
        for action, prob in self.nextAct[self.movieTracker].items():
            probCum += prob;
            if rand < probCum:
                if action == "move":
                    self.idleMoveMode();
                elif self.movieTracker != action:
                    self.movieTracker = action;
                    self.runCow();
                    if "Munch" not in self.movieTracker:
                        if "Down" in self.movieTracker or \
                           "Up" in self.movieTracker:
                            self.movieCounter = -20;
                    if "Moo1" in self.movieTracker:
                        self.movieCounter = -150;
                break;
    def idleMoveMode(self):
        self.movieTracker = "move";
        randChangeDir = rd.random();
        if (self.lrDirIdleMove == "" and self.udDirIdleMove == "") or\
           (randChangeDir < self.changeDirProbIdleMove):
            self.lrDirIdleMoveOld = np.copy(self.lrDirIdleMove);
            self.udDirIdleMoveOld = np.copy(self.udDirIdleMove);
            self.lrDirIdleMove = "";
            self.udDirIdleMove = "";
            rand = rd.random();        
            if rand < 1.0/8:
                self.udDirIdleMove = "up";
            elif rand < 2.0/8:
                self.lrDirIdleMove = "right";
                self.udDirIdleMove = "up";
            elif rand < 3.0/8:
                self.lrDirIdleMove = "right";
            elif rand < 4.0/8:
                self.lrDirIdleMove = "right";
                self.udDirIdleMove = "down";
            elif rand < 5.0/8:
                self.udDirIdleMove = "down";
            elif rand < 6.0/8:
                self.lrDirIdleMove = "left";
                self.udDirIdleMove = "down";
            elif rand < 7.0/8:
                self.lrDirIdleMove = "left";
            elif rand < 8.0/8:
                self.lrDirIdleMove = "left";
                self.udDirIdleMove = "up";
            if self.lrDirIdleMove != "":
                self.lrDirection = np.copy(self.lrDirIdleMove);
            if self.lrDirIdleMove != self.lrDirIdleMoveOld or\
               self.udDirIdleMove != self.udDirIdleMoveOld:
                self.runCow();
    def buttonClick(self):
        self.liveTimer.stop();
        if self.lrDirection == "left":
            self.movieTracker = "ZDisappearingLeft";
            self.runCow();
        elif self.lrDirection == "right":
            self.movieTracker = "ZDisappearingRight";
            self.runCow();
        self.exitTimer = QtCore.QTimer(self);
        self.exitTimer.timeout.connect(self.exitAction);
        self.exitTimer.start(350);
    def exitAction(self):
        self.cow.stop();
        self.close();

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv);
    sphericalCow = mainFrame(None);
    print("\n    Click on the cow to exit.");
    print("    Use the direction keys to control the cow.");
    print("   (note: the cow violates parity because the creator was lazy.)");
    print("");
    sys.exit(app.exec_());



 









 
