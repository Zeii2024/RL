import wx
import time
###状态栏的实现###
class MainFrame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(500,300))
        self.setStatusBar()
        self.initUI()

    def initUI(self):
        self.buttonOK = wx.Button(self,-1,u"ok",(20,20),(60,30))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.buttonOK)

        self.buttonCancel = wx.Button(self,-1,u"cancel",(20,80),(60,30))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.buttonCancel)

    def setStatusBar(self):
        sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-1,-2])
        self.SetStatusText("Ready",0)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000,wx.TIMER_CONTINUOUS)
        self.Notify()

    def OnClick(self,event):
        if event.GetEventObject() == self.buttonOK:
            print(event.GetEventObject().GetLabel())
        elif event.GetEventObject() == self.buttonCancel:
            print(event.GetEventObject().GetLabel())
        else:
            print("No button is clicked!")

    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d  %H:%M:%S',t)
        self.SetStatusText(st,1)

class App(wx.App):
    def __init__(self):
        super(self.__class__,self).__init__()

    def OnInit(self):
        self.version = " 第四课"
        self.title = "wxPython初级教程"+self.version
        frame = MainFrame(None,-1,self.title)
        frame.Show(True)

        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()