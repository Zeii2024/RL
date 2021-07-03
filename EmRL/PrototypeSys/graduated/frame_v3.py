import wx
import time
from utils.utils_view_3d import utils_view_3D

Version = "v1.0"
ReleaseDate = "2020-11-03"

ID_PREDATA_1 = 191
ID_RESAMPLED_1 = 192
ID_visualization_2 = 193
ID_visualization_1 = 194
ID_imgSeg_cnn = 195
ID_imgSeg_fcn = 196
ID_FILE_OPEN_HOME = 100
ID_FILE_OPEN_ITEM = 197
ID_FILE_QUIT_ITEM = 198
ID_OPEN = 199
ID_EXIT = 200
ID_ABOUT = 201
ID_MR = 100

class MainFrame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(800,500))

        self.filename = None

        self.panel_init = None
        self.panel_visualization = None
        self.panel_reSampled = None
        self.panel_preData = None
        self.panel_segment = None

        self.setStatusBar()
        self.setMenuBar()
        self.initUI()

    # 设置菜单栏
    def setMenuBar(self):
        menuBar = wx.MenuBar()

        otherMenu = wx.Menu()
        homeItem = wx.MenuItem(otherMenu, ID_FILE_OPEN_HOME, "主页", kind=wx.ITEM_NORMAL)
        newItem = wx.MenuItem(otherMenu, ID_FILE_OPEN_ITEM, "打开文件", kind=wx.ITEM_NORMAL)
        delItem = wx.MenuItem(otherMenu, ID_FILE_QUIT_ITEM, "关闭系统", kind=wx.ITEM_NORMAL)
        otherMenu.Append(homeItem)
        otherMenu.Append(newItem)
        otherMenu.Append(delItem)
        menuBar.Append(otherMenu,'主页')
        self.Bind(wx.EVT_MENU,self.reInitUI,id=ID_FILE_OPEN_HOME)
        self.Bind(wx.EVT_MENU,self.openFile,id=ID_FILE_OPEN_ITEM)
        self.Bind(wx.EVT_MENU,self.OnMenuExit,id=ID_FILE_QUIT_ITEM)

        visualizaMenu = wx.Menu()
        vis1Item = wx.MenuItem(visualizaMenu,ID_visualization_1,"可视化")
        visualizaMenu.Append(vis1Item)
        menuBar.Append(visualizaMenu,'数据可视化')
        self.Bind(wx.EVT_MENU, self.visualization, id=ID_visualization_1)

        reSampledMenu = wx.Menu()
        reSampledItem = wx.MenuItem(reSampledMenu,ID_RESAMPLED_1,"数据重采样")
        reSampledMenu.Append(reSampledItem)
        menuBar.Append(reSampledMenu,'数据重采样')
        self.Bind(wx.EVT_MENU,self.OnReSampled,id=ID_RESAMPLED_1)

        preDataMenu = wx.Menu()
        preDataItem = wx.MenuItem(preDataMenu,ID_PREDATA_1,"数据预处理")
        preDataMenu.Append(preDataItem)
        menuBar.Append(preDataMenu,'数据预处理')
        self.Bind(wx.EVT_MENU,self.OnPreData,id=ID_PREDATA_1)

        imgSegMenu = wx.Menu()
        fcnItem = wx.MenuItem(imgSegMenu, ID_imgSeg_fcn, "Attention", kind=wx.ITEM_NORMAL)
        cnnItem = wx.MenuItem(imgSegMenu, ID_imgSeg_cnn, "GRU", kind=wx.ITEM_NORMAL)
        imgSegMenu.Append(fcnItem)
        imgSegMenu.Append(cnnItem)
        menuBar.Append(imgSegMenu, '图像分割')

        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu,ID_ABOUT,"关于(&A)")
        helpMenu.Append(aboutItem)
        menuBar.Append(helpMenu, '帮助(&H)')
        self.Bind(wx.EVT_MENU, self.OnMenuAbout, id=ID_ABOUT)

        self.SetMenuBar(menuBar)

    # 其它
    def openFile(self, event):
        # file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open .jpg file", wildcard="jpg files (*.jpg)|*.jpg",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.SetTitle('title:'+'--' + self.filename)
            self.sb.SetStatusText("成功打开文件！",1)
        dlg.Destroy()

    # 初始界面，加载数据
    def initUI(self):
        if self.panel_visualization:
            self.panel_visualization.Destroy()

        self.panel_init = wx.Panel(self,pos=(0, 0), size=(800, 500))
        self.buttonLoad = wx.Button(self.panel_init, -1, u"导入", pos=(10, 10))
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.buttonLoad)

        self.buttonView = wx.Button(self.panel_init, -1, u"显示", pos=(10, 40))
        self.Bind(wx.EVT_BUTTON, self.OnView, self.buttonView)

        self.onlyRead_text = wx.TextCtrl(self.panel_init, value="待读入...", style=wx.TE_READONLY, pos=(100, 10), size=(300, 25))
        self.static_text = wx.StaticText(self.panel_init, label="CT图像信息", pos=(100, 50), size=(500, 500))
    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.onlyRead_text.Label = self.filename
            self.sb.SetStatusText("成功导入文件！", 1)
        dlg.Destroy()
    def OnView(self, event):
        if self.filename == None:
            self.static_text.Label = "请导入数据！"
        else:
            import nibabel as nib
            img = nib.load(self.filename)
            self.static_text.Label = "CT图像信息："
            self.static_text.Label += '\n\ndata shape\t: ' + str(img.shape)
            self.static_text.Label += '\nsizeof_hdr\t: ' + str(img.header['sizeof_hdr'])
            self.static_text.Label += '\ndim_info\t: ' + str(img.header['dim_info'])
            self.static_text.Label += '\ndim\t\t: ' + str(img.header['dim'])
            self.static_text.Label += '\ndatatype\t: ' + str(img.header['datatype'])
            self.static_text.Label += '\nbitpix\t\t: ' + str(img.header['bitpix'])
            self.static_text.Label += '\nslice_start\t: ' + str(img.header['slice_start'])
            self.static_text.Label += '\npixdim\t\t: ' + str(img.header['pixdim'])
            self.static_text.Label += '\nvox_offset\t: ' + str(img.header['vox_offset'])
            self.static_text.Label += '\nslice_end\t: ' + str(img.header['slice_end'])
            self.static_text.Label += '\nsrow_x\t\t: ' + str(img.header['srow_x'])
            self.static_text.Label += '\nsrow_y\t\t: ' + str(img.header['srow_y'])
            self.static_text.Label += '\nsrow_z\t\t: ' + str(img.header['srow_z'])
            print('over...')
            utils_view_3D(self.filename)
    def reInitUI(self,event):
        self.initUI()

    # 数据可视化
    def visualization(self,event):
        if self.panel_init:
            self.filename = None
            self.panel_init.Destroy()

        self.filename_visualization = None

        self.panel_visualization = wx.Panel(self,pos=(0, 0), size=(150, 800))
        self._background = wx.Image("background.jpg", type=wx.BITMAP_TYPE_ANY, )
        self._background = self._background.Rescale(150, 150)  # 改变图像大小
        wx.StaticBitmap(self.panel_visualization, -1, wx.Bitmap(self._background))  # 显示图像

        self._caidan1 = wx.Button(self.panel_visualization, label=u'导入数据', pos=(0, 150), size=(150, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan1)
        self._caidan2 = wx.Button(self.panel_visualization, label=u'三视图映像', pos=(0, 180), size=(150, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan2)
        self._caidan3 = wx.Button(self.panel_visualization, label=u'三维可视化', pos=(0, 210), size=(150, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan3)

    def Onclick_visualization(self,event):
        if event.GetEventObject() == self._caidan1:
            dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename_visualization = dlg.GetPath()
                self.sb.SetStatusText("成功导入文件！", 1)
            dlg.Destroy()
        elif event.GetEventObject() == self._caidan2:
            print("点击了三视图映像！")
        else:
            if self.filename_visualization == None:
                wx.MessageBox('请导入数据！')
            else:
                utils_view_3D(self.filename_visualization)


    # 数据重采样
    def OnReSampled(self,event):
        print("在这里进行数据重采样！")

    # 数据预处理
    def OnPreData(self, event):
        print("在这里进行数据预处理！")

    # 图像分割
    def segment(self):
        pass

    # 状态栏
    def setStatusBar(self):
        self.sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-1,-2])
        self.SetStatusText("Ready",1)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d %H:%M:%S',t)
        self.SetStatusText(st,0)

    # 系统信息
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
        self.sizer.Add(wx.StaticText(self, -1, "CT图像分割系统"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sizer.Add(wx.StaticText(self, -1, "^_^ (c) 2020"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
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