import sys, os
from random import random

from PyQt5.QtCore import Qt, QSize, QByteArray, QTimer, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QMovie

def exePath():
    try:
        return sys._MEIPASS;
    except Exception:
        return os.path.abspath(".");

class mainFrame(QWidget):
    def __init__(self, parent=None):
        super(mainFrame, self).__init__(parent);
        self.setWindowFlags(Qt.FramelessWindowHint);
        self.setAttribute(Qt.WA_TranslucentBackground);
        self.cowSize = QSize(int(200*1.21), int(200));
        self.setFixedSize(self.cowSize*1.2);
        self.screenGeo = QDesktopWidget().screenGeometry();
        self.availGeo  = QDesktopWidget().availableGeometry();
        randW = random()*0.6 + 0.2;
        randH = random()*0.4 + 0.3;
        self.currLoc = [self.screenGeo.width()*randW, \
                        self.screenGeo.height()*randH];
        self.move(int(self.currLoc[0]), int(self.currLoc[1]));
        self.keyPool = [Qt.Key_Left, Qt.Key_Right,
                        Qt.Key_Up, Qt.Key_Down,
                        Qt.Key_S, Qt.Key_P,
                        Qt.Key_I, Qt.Key_N];
        self.pressedKeys = {Qt.Key_Left:  False,
                            Qt.Key_Right: False,
                            Qt.Key_Up:    False,
                            Qt.Key_Down:  False,
                            Qt.Key_S: False,
                            Qt.Key_P: False,
                            Qt.Key_I: False,
                            Qt.Key_N: False,};
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
        gifPath = exePath() + "/figures/cowIdleLeft.gif";
        self.cow = QMovie(gifPath, QByteArray(), self);
        self.cow.setScaledSize(self.cowSize);
        self.cow.setCacheMode(QMovie.CacheAll);
        #self.cow.setSpeed(100);
        self.cowScreen = QLabel();
        self.cowScreen.setAlignment(Qt.AlignCenter);
        self.cowScreen.setMovie(self.cow);

        layout = QVBoxLayout();
        layout.addWidget(self.cowScreen);
        self.setLayout(layout);

        self.liveTimer = QTimer(self);
        self.liveTimer.timeout.connect(self.liveAction);
        self.liveTimer.start(20);
        
        self.button = QPushButton(self);
        self.button.setText("");
        self.button.setGeometry(QRect(18, 22, self.cowSize.width(), \
                                              self.cowSize.height()));
        self.button.setStyleSheet("background-color: transparent;");
        self.button.clicked.connect(self.buttonClick);
 
        self.show();
    def runCow(self):
        self.cow.stop();
        gifPath = exePath() + "/figures/cow" + self.movieTracker + ".gif";
        if "move" in self.movieTracker:
            if "left" in self.lrDirection: 
                gifPath = exePath() + "/figures/cowWalkLeft.gif";
            elif "right" in self.lrDirection:
                gifPath = exePath() + "/figures/cowWalkRight.gif";
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
        keyLeft  = self.pressedKeys[Qt.Key_Left];
        keyRight = self.pressedKeys[Qt.Key_Right];
        keyUp    = self.pressedKeys[Qt.Key_Up];
        keyDown  = self.pressedKeys[Qt.Key_Down];
        keyPressedSPIN = self.pressedKeys[Qt.Key_S] or \
                         self.pressedKeys[Qt.Key_P] or \
                         self.pressedKeys[Qt.Key_I] or \
                         self.pressedKeys[Qt.Key_N];
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
                    movementSpeed = movementSpeed/1.414;
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
                    movementSpeed = movementSpeed/1.414;
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
        self.move(int(self.currLoc[0]-self.cowSize.width()/2),\
                  int(self.currLoc[1]));
        if self.lrDirection == "":
            if random() < 0.5:
                self.lrDirection = "left";
            else:
                self.lrDirection = "right";
    def idleMode(self):
        rand = random();
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
        randChangeDir = random();
        if (self.lrDirIdleMove == "" and self.udDirIdleMove == "") or\
           (randChangeDir < self.changeDirProbIdleMove):
            self.lrDirIdleMoveOld = self.lrDirIdleMove + "";
            self.udDirIdleMoveOld = self.udDirIdleMove + "";
            self.lrDirIdleMove = "";
            self.udDirIdleMove = "";
            rand = random();        
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
                self.lrDirection = self.lrDirIdleMove + "";
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
        self.exitTimer = QTimer(self);
        self.exitTimer.timeout.connect(self.exitAction);
        self.exitTimer.start(350);
    def exitAction(self):
        self.cow.stop();
        self.close();

if __name__ == "__main__":
    app = QApplication(sys.argv);
    sphericalCow = mainFrame(None);
    print("\n    Click on the cow to exit.");
    print("    Use the direction keys to control the cow.");
    print("   (note: the cow violates parity because the creator was lazy.)");
    print("");
    sys.exit(app.exec_());



 









 
