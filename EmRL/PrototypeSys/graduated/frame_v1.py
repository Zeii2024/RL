import wx
import time

Version = "v1.0"
ReleaseDate = "2020-11-03"

ID_visualization_2 = 193
ID_visualization_1 = 194
ID_imgSeg_cnn = 195
ID_imgSeg_fcn = 196
ID_FILE_OPEN_ITEM = 197
ID_FILE_QUIT_ITEM = 198
ID_OPEN = 199
ID_EXIT = 200
ID_ABOUT = 201
ID_MR = 100

class MainFrame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(800,500))

        self.setStatusBar()
        self.setMenuBar()
        self.initUI()

    def setMenuBar(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        newItem = wx.MenuItem(fileMenu, ID_FILE_OPEN_ITEM, "打开", kind=wx.ITEM_NORMAL)
        delItem = wx.MenuItem(fileMenu, ID_FILE_QUIT_ITEM, "关闭", kind=wx.ITEM_NORMAL)
        fileMenu.Append(newItem)
        fileMenu.Append(delItem)
        menuBar.Append(fileMenu,'文件')
        self.Bind(wx.EVT_MENU,self.openFile,id=ID_FILE_OPEN_ITEM)
        self.Bind(wx.EVT_MENU,self.OnMenuExit,id=ID_FILE_QUIT_ITEM)

        imgSegMenu = wx.Menu()
        fcnItem = wx.MenuItem(imgSegMenu,ID_imgSeg_fcn,"3D FCN",kind=wx.ITEM_NORMAL)
        cnnItem = wx.MenuItem(imgSegMenu,ID_imgSeg_cnn,"3D CNN",kind=wx.ITEM_NORMAL)
        imgSegMenu.Append(fcnItem)
        imgSegMenu.Append(cnnItem)
        menuBar.Append(imgSegMenu,'图像分割')

        visualizaMenu = wx.Menu()
        vis1Item = wx.MenuItem(visualizaMenu,ID_visualization_1,"三维图像可视化")
        vis2Item = wx.MenuItem(visualizaMenu,ID_visualization_2,"三维图像交互")
        visualizaMenu.Append(vis1Item)
        visualizaMenu.Append(vis2Item)
        menuBar.Append(visualizaMenu,'三维图像可视化')
        self.Bind(wx.EVT_MENU, self.testEvent1, id=ID_visualization_1)
        self.Bind(wx.EVT_MENU, self.testEvent2, id=ID_visualization_2)

        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu,ID_ABOUT,"关于(&A)")
        helpMenu.Append(aboutItem)
        menuBar.Append(helpMenu, '帮助(&H)')
        self.Bind(wx.EVT_MENU, self.OnMenuAbout, id=ID_ABOUT)

        self.SetMenuBar(menuBar)

    def openFile(self, event):
        # file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open .jpg file", wildcard="jpg files (*.jpg)|*.jpg",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.SetTitle('title:'+'--' + self.filename)
            self.sb.SetStatusText("成功打开文件！",0)
        dlg.Destroy()

    def testEvent1(self,event):
        print("点击了子菜单1！")

    def testEvent2(self,event):
        print("点击了子菜单2！")

    def setStatusBar(self):
        self.sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-1,-2])
        self.SetStatusText("Ready",1)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def initUI(self):
        self.buttonOK = wx.Button(self,-1,u"ok",(20,20),(60,30))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.buttonOK)

        self.buttonCancel = wx.Button(self,-1,u"cancel",(20,80),(60,30))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.buttonCancel)

    def OnClick(self,event):
        if event.GetEventObject() == self.buttonOK:
            print(event.GetEventObject().GetLabel())
        elif event.GetEventObject() == self.buttonCancel:
            print(event.GetEventObject().GetLabel())
        else:
            print("No button is clicked!")

    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d %H:%M:%S',t)
        self.SetStatusText(st,0)

    def OnMenuExit(self,event):
        print("点击了退出菜单项！")
        self.Close()

    def OnMenuAbout(self,event):
        dig = AboutDialog(None,-1)
        dig.ShowModal()
        dig.Destroy()

    def OnCloseWindow(self,event):
        self.Destroy()

class AboutDialog(wx.Dialog):
    def __init__(self,parent,id):
        wx.Dialog.__init__(self,parent,id,'About Me',size=(200,200))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, "CT图像分割系统^_^"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sizer.Add(wx.StaticText(self, -1, "(c) 2020"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sizer.Add(wx.StaticText(self, -1, "Version：v1"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sizer.Add(wx.StaticText(self, -1, "Author：王宗宇"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sizer.Add(wx.Button(self,wx.ID_OK),0,wx.ALIGN_CENTER|wx.BOTTOM,border=20)
        self.SetSizer(self.sizer)

class App(wx.App):
    def __init__(self):
        super(self.__class__,self).__init__()

    def OnInit(self):
        self.version = " v1"
        self.title = "肾部肿瘤CT图像分割系统"+self.version
        frame = MainFrame(None,-1,self.title)
        frame.Show(True)

        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()