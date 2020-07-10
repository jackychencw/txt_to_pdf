import os
import wx
import time
import wx.lib.agw.multidirdialog as MDD
from converter import txtToPdf

wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"

files = []
########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "pdf转换器")
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        
        # create the buttons and bindings
        openFileDlgBtn = wx.Button(self.panel, label="打开文件")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)

        
        
        saveFileDlgBtn = wx.Button(self.panel, label="转换")
        saveFileDlgBtn.Bind(wx.EVT_BUTTON, self.onSaveFile)
        
        self.gauge = wx.Gauge(self.panel, range = 20, size = (250, 25), style =  wx.GA_HORIZONTAL)
        
        # put the buttons in a sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(openFileDlgBtn, 0, wx.ALL|wx.CENTER, 5)
        self.sizer.Add(saveFileDlgBtn, 0, wx.ALL|wx.CENTER, 5)
        self.sizer.Add(self.gauge, 0, wx.ALL|wx.CENTER, 5)
        self.panel.SetSizer(self.sizer)
        
        
    #----------------------------------------------------------------------
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        del files[:]
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard="txt files (*.txt)|*.txt",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print("You chose the following file(s):")
            for path in paths:
                files.append(path)
        dlg.Destroy()
        
    #----------------------------------------------------------------------
    def onSaveFile(self, event):
        """
        Create and show the Save FileDialog
        """
        r = len(files)
        self.gauge.SetRange(r)
        self.gauge.SetValue(0)
        i = 0
        for file in files:
            print("Processing " + file)
            i += 1
            time.sleep(1)
            txtToPdf(file)
            self.gauge.SetValue(i)
        
            # txtToPdf(file)
        # dlg = wx.FileDialog(
        #     self, message="Save file as ...", 
        #     defaultDir=self.currentDirectory, 
        #     defaultFile="", wildcard="pdf files (*.pdf)|*.pdf", style=wx.FD_SAVE
        #     )
        # if dlg.ShowModal() == wx.ID_OK:
        #     path = dlg.GetPath()
        #     print("You chose the following filename: %s" % path)
        # dlg.Destroy()
        
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()