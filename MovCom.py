#!/usr/bin/python2

# Importing required modules
import sys, os, json, urllib, time, csv, re
from PyQt4 import QtGui, QtCore

from MovCom_UI import Ui_MovCom

class getReviewsThread(QtCore.QThread):
    def __init__(self, movies, directory):
        '''
            Make a new thread instance with specified
            movies list. This list will later be used by other instance functions
        '''
        QtCore.QThread.__init__(self)
        self.movies = movies    # movies is a list
        self.path = directory + 'MovCom.csv'
        self.final_lst = list()
        try:
            with open(self.path, 'rb') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if row[0] == 'TITLE':
                        pass
                    else:
                        if float(row[1]) == -1 and float(row[2]) == -1 :
                            continue

                        self.final_lst.append( ( (float(row[1]), float(row[2]) ), row[0]) )
        except IOError:
            pass
        except:
            QtGui.QMessageBox.critical(None, "Error", "Some error in getReviewsThread. Have to exit")
            exit()

    def __del__(self):
        self.quit()

    def getMovieRating(self, movie):
        try:
            movie = urllib.urlencode({'t' : movie})

            response = urllib.urlopen('http://www.omdbapi.com/?' + movie + '&y=&plot=short&r=json&tomatoes=true').read()
            jres = json.loads(response)
            return jres
        except IOError:
            QtGui.QMessageBox.critical(None, "Error", "Net connection is not good. Try again later. Have to exit")
            time.sleep(3)
            exit()

    def run(self):
        for movie in self.movies:
            jres = self.getMovieRating(movie)
            self.emit(QtCore.SIGNAL("add_movie(QString)"), movie)
            if jres['Response'] == 'True':
                if jres['imdbRating'] != 'N/A':
                    v1 = float(jres['imdbRating'])
                else:
                    v1 = -1

                if jres['tomatoMeter'] != 'N/A':
                    v2 = float(jres['tomatoMeter'])
                else:
                    v2 = -1

                if ( (v1, v2), jres['Title'] ) not in self.final_lst:
                    #print ((v1, v2), jres['Title'])
                    self.final_lst.append( ( (v1, v2), jres['Title']) )
                self.sleep(1)
            else:
                v1 , v2 = -1, -1
                if ( (v1, v2), movie ) not in self.final_lst:
                    self.final_lst.append( ( (v1, v2), movie) )

        self.final_lst.sort(reverse = True)

        try:
            with open(self.path, 'wb') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(['TITLE', 'IMDB_RATING', 'TOMATO_METER'])
                for val in self.final_lst:
                    spamwriter.writerow([val[1], val[0][0], val[0][1]])
        except:
            QtGui.QMessageBox.critical(None, "Error", "Error in writing final result to the file")
            exit()




# Extending QFileDialog class because I want to be able to select multiple folders and Files
class FileDialog(QtGui.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtGui.QFileDialog.ExistingFiles)

    # Creating our own accept function..this is the most important part
    def accept(self):
        QtGui.QDialog.accept(self)

class Window(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_MovCom()
        self.ui.setupUi(self)
        self.lst = list()
        self.ui.button_com.setEnabled(False)
        self.ui.button_update.setEnabled(False)
        self.ui.progressBar.setValue(0)

        # Here we connect signals with slots
        QtCore.QObject.connect(self.ui.button_select, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.button_com, QtCore.SIGNAL("clicked()"), self.make_comparison)
        QtCore.QObject.connect(self.ui.button_update, QtCore.SIGNAL("clicked()"), self.update_list)
        QtCore.QObject.connect(self.ui.list_window, QtCore.SIGNAL("textChanged()"), self.enable_save)

    def file_dialog(self):
        dlg = FileDialog()
        if dlg.exec_() == QtGui.QDialog.Accepted:
            # First we convert the QStringList
            self.lst = [str(x) for x in dlg.selectedFiles()]

            ret = str(self.ui.list_window.toPlainText())
            cmp_path = re.findall("(.+/)", self.lst[0])[0]
            self.directory = cmp_path
            self.lst = list()

            for fl in dlg.selectedFiles():
                fl = str(fl).strip()

                if(len(fl) > 0):
                    self.lst.append(fl[len(cmp_path):])
                    ret = ret + fl[len(cmp_path):] + '\n'


            self.ui.list_window.setText(ret)
            self.ui.progressBar.setMaximum(len(self.lst))
            self.ui.button_com.setEnabled(True)
            self.ui.button_update.setEnabled(False)



    def make_comparison(self):
        print self.lst
        if len(self.lst) > 0:
            response = False
            YES = 'Yes'
            NO  = 'No'

            msg = QtGui.QMessageBox(self)
            msg.setText('Do you want to make any changes to the movie list?')
            msg.setWindowTitle('MovCom')
            msg.setIcon(QtGui.QMessageBox.Question)
            msg.addButton(YES, QtGui.QMessageBox.YesRole)
            msg.addButton(NO, QtGui.QMessageBox.NoRole)
            msg.setDetailedText('This program will search the final list given by you. Please make sure the movie title is correct otherwise you may not get right results.')
            msg.exec_()

            response = msg.clickedButton().text()

            # This means that we have to finally make the comparisons based on each file
            if response == NO:
                OK = 'OK'
                wrng = QtGui.QMessageBox(self)
                wrng.setText('Fair warning: Please ensure that net connection is alright.')
                wrng.setWindowTitle('MovCom')
                wrng.setIcon(QtGui.QMessageBox.Information)
                wrng.addButton(OK, QtGui.QMessageBox.AcceptRole)
                wrng.exec_()

                self.ui.progressBar.setMaximum(len(self.lst))
                self.mov_thread = getReviewsThread(self.lst, self.directory)
                QtCore.QObject.connect(self.mov_thread, QtCore.SIGNAL("add_movie(QString)"), self.add_movie)
                QtCore.QObject.connect(self.mov_thread, QtCore.SIGNAL("finished()"), self.done)
                self.mov_thread.start()

                self.ui.button_quit.clicked.connect(self.mov_thread.terminate)
                self.ui.button_com.setEnabled(False)
                self.ui.button_select.setEnabled(False)
                self.ui.button_update.setEnabled(False)

        else:
            QtGui.QMessageBox.critical(None, "No movies", "You didn't enter any movies.", QtGui.QMessageBox.Ok)
            return

    def add_movie(self, movie):
        self.ui.list_fetched.addItem(movie)
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

    def update_list(self):
        del self.lst[:]
        for x in self.ui.list_window.toPlainText().split('\n'):
            ss = str(x).strip()
            if len(ss) > 0:
                self.lst.append(str(ss))
        QtGui.QMessageBox.information(None, "Updated", "Movie list has been updated", QtGui.QMessageBox.Ok)

    def enable_save(self):
        self.ui.button_update.setEnabled(True)

    def done(self):
        self.ui.button_select.setEnabled(True)
        self.ui.button_com.setEnabled(False)
        self.ui.button_update.setEnabled(False)
        self.ui.list_window.setText("")
        QtGui.QMessageBox.information(None, "Done!", "Done fetching posts!")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
