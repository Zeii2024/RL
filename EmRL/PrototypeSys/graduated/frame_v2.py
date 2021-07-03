import wx
import time

Version = "v4.0"
ReleaseDate = "2021-03-03"

ID_PREDATA_1 = 191
ID_RESAMPLED_1 = 192
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
        wx.Frame.__init__(self,parent,id,title,size=(1200,900))
        # 参数表
        self.params = {'env': 1,
                        'num_of_train': 4,
                        'model': 0,
                        'task': 0}

        self.splitter = wx.SplitterWindow(self)
        self.setStatusBar()
        self.setMenuBar()
        self.initUI()
        

    def setMenuBar(self):
        menuBar = wx.MenuBar()

        otherMenu = wx.Menu()
        newItem = wx.MenuItem(otherMenu, ID_FILE_OPEN_ITEM, "打开文件", kind=wx.ITEM_NORMAL)
        delItem = wx.MenuItem(otherMenu, ID_FILE_QUIT_ITEM, "关闭系统", kind=wx.ITEM_NORMAL)
        otherMenu.Append(newItem)
        otherMenu.Append(delItem)
        menuBar.Append(otherMenu,'文件')
        self.Bind(wx.EVT_MENU,self.openFile,id=ID_FILE_OPEN_ITEM)
        self.Bind(wx.EVT_MENU,self.OnMenuExit,id=ID_FILE_QUIT_ITEM)

        visualizaMenu = wx.Menu()
        vis1Item = wx.MenuItem(visualizaMenu,ID_visualization_1,"数据展示")
        vis2Item = wx.MenuItem(visualizaMenu,ID_visualization_2,"数据处理")
        visualizaMenu.Append(vis1Item)
        visualizaMenu.Append(vis2Item)
        menuBar.Append(visualizaMenu,'编辑')
        self.Bind(wx.EVT_MENU, self.testEvent1, id=ID_visualization_1)
        self.Bind(wx.EVT_MENU, self.testEvent2, id=ID_visualization_2)

        reSampledMenu = wx.Menu()
        reSampledItem = wx.MenuItem(reSampledMenu,ID_RESAMPLED_1,"打开或关闭可视化")
        reSampledMenu.Append(reSampledItem)
        menuBar.Append(reSampledMenu,'视图')
        self.Bind(wx.EVT_MENU,self.OnReSampled,id=ID_RESAMPLED_1)

        preDataMenu = wx.Menu()
        preDataItem = wx.MenuItem(preDataMenu,ID_PREDATA_1,"截图")
        preDataMenu.Append(preDataItem)
        menuBar.Append(preDataMenu,'工具')
        self.Bind(wx.EVT_MENU,self.OnPreData,id=ID_PREDATA_1)

        '''
        imgSegMenu = wx.Menu()
        fcnItem = wx.MenuItem(imgSegMenu, ID_imgSeg_fcn, "Attention", kind=wx.ITEM_NORMAL)
        cnnItem = wx.MenuItem(imgSegMenu, ID_imgSeg_cnn, "GRU", kind=wx.ITEM_NORMAL)
        imgSegMenu.Append(fcnItem)
        imgSegMenu.Append(cnnItem)
        menuBar.Append(imgSegMenu, '图像分割')
        '''
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
            self.sb.SetStatusText("成功打开文件！",1)
        dlg.Destroy()

    def OnPreData(self,event):
        print("在这里进行数据预处理！")

    def OnReSampled(self,event):
        print("在这里进行数据重采样！")

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

        panel = wx.Panel(self.splitter)
        panel1 = wx.Panel(self.splitter,-1,size=(260,480),pos=(20,20),style=wx.BORDER_SUNKEN)
        panel2 = wx.Panel(self.splitter,-1,size=(800,750),pos=(300,20),style=wx.BORDER_SUNKEN)
        # panel3 = wx.Panel(self.splitter,-1,size=(260,40),pos=(20,450))
        
        '''
        self.filename = None

        self.buttonLoad = wx.Button(panel,-1,u"导入",pos=(10, 10))
        self.Bind(wx.EVT_BUTTON,self.OnLoad,self.buttonLoad)

        self.buttonView = wx.Button(panel,-1,u"显示",pos=(100, 540))
        self.Bind(wx.EVT_BUTTON,self.OnView,self.buttonView)

        self.onlyRead_text = wx.TextCtrl(panel, value="待读入...", style=wx.TE_READONLY, pos=(100, 10),size=(300,25))
        self.static_text = wx.StaticText(panel, label="CT图像信息", pos=(100, 50),size=(500,500))
        '''
        # 设置文本2
        text2 = wx.StaticText(panel1,
                            wx.ID_ANY,
                            "参数设置：",
                            (20,20),)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font2 = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text2.SetFont(font2)
        # 设置文字背景色
        text2.SetForegroundColour("Black")        # 设定前景色为黑色

        # 设置展示文字
        text_show = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "展示区",
                            (330,360),)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font_show = wx.Font(28, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text_show.SetFont(font_show)
        # 设置文字背景色
        text_show.SetForegroundColour("Gray")        # 设定前景色为黑色
        
        # 设置文本3
        text_env = wx.StaticText(panel1,
                            wx.ID_ANY,
                            "环境大小：",
                            (20,60),)
        text_env.SetFont(font2)
        # 环境复选框
        candidates1 = [u"小", u"中", u"大"]
        self.combol_env = wx.ComboBox(parent=panel1,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(140, 60),
                              value="",
                              choices=candidates1,
                              style=wx.CB_READONLY,
                              name=u"环境大小")
        # 设置列车数量文本4
        text_train = wx.StaticText(panel1,
                            wx.ID_ANY,
                            "列车数量：",
                            (20,120),)
        text_train.SetFont(font2)
        # 环境复选框
        candidates2 = [u"4", u"5", u"6", u"7", u"8"]
        self.combol_train = wx.ComboBox(parent=panel1,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(140, 120),
                              value="",
                              choices=candidates2,
                              style=wx.CB_READONLY,
                              name=u"列车数量")
        
        # 设置选择模型文本5
        text_model = wx.StaticText(panel1,
                            wx.ID_ANY,
                            "选择模型：",
                            (20,200),)
        text_model.SetFont(font2)
        # 设置单选框
        sampleList1 = ['SCN', 'ACN']
        self.modelRadioBox = wx.RadioBox(panel1, -1, "", (140, 180), (100,90),
                                sampleList1, 1, wx.RA_SPECIFY_COLS)

        # 设置选择任务文本6
        text_task = wx.StaticText(panel1,
                            wx.ID_ANY,
                            "选择任务：",
                            (20,300),)
        text_task.SetFont(font2)
        # 设置单选框
        sampleList2 = ['train', 'test', '展示结果']
        self.taskRadioBox = wx.RadioBox(panel1, -1, "", (140, 280), (100,120),
                                sampleList2, 1, wx.RA_SPECIFY_COLS)
        # 设置按钮\/
        self.close_button = wx.Button(panel1, -1, u"关闭", pos=(20, 430))
        self.start_button = wx.Button(panel1, -1, u"开始", pos=(140, 430))

        # 绑定事件
        # self.Bind(wx.EVT_MENU,self.close,menuExit) # exit
        # self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout) # about
        panel1.Bind(wx.EVT_COMBOBOX, self.setEnv,self.combol_env)
        panel1.Bind(wx.EVT_COMBOBOX, self.setTrain,self.combol_train)
        panel1.Bind(wx.EVT_RADIOBOX, self.choiceModel,self.modelRadioBox)
        panel1.Bind(wx.EVT_RADIOBOX, self.choiceTask,self.taskRadioBox)

        panel1.Bind(wx.EVT_BUTTON,self.start, self.start_button)
        panel1.Bind(wx.EVT_BUTTON,self.close, self.close_button)

    def OnLoad(self,event):
        dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.onlyRead_text.Label = self.filename
            self.sb.SetStatusText("成功导入文件！", 1)
        dlg.Destroy()

    def OnView(self,event):
        if self.filename == None:
            self.static_text.Label = "请导入数据！"
        else:
            import nibabel as nib
            img = nib.load(self.filename)
            self.static_text.Label = "CT图像信息："
            self.static_text.Label += '\n\ndata shape\t: '+str(img.shape)
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

    def OnClick(self,event):
        print("Onclick")

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

    def setEnv(self,event):
        env = self.combol_env.GetSelection()
        self.params['env'] = env
        # print("setEnv:",env)

    def setTrain(self,event):
        num_of_train = self.combol_train.GetValue()
        self.params['num_of_train'] = num_of_train
        # print("setEnv:",num_of_train)

    def choiceModel(self,event):
        # 输出序号idx
        model = self.modelRadioBox.GetSelection()
        # 输出字符
        # self.model =  self.modelRadioBox.GetStringSelection()
        # print("model:",self.model)
        self.params['model'] = model
        # print("p:",model)

    def choiceTask(self, event):
        # 输出序号idx
        task = self.taskRadioBox.GetSelection()
        # 输出字符
        #self.task = self.taskRadioBox.GetStringSelection()
        self.params['task'] = task
        # print("task:",task)

    def start(self, event):
        # TODO 把参数整合，传入配置文件
        # 读取配置文件到运行程序
        print("params:",self.params)
        if self.params['task'] == 0:
            # train
            import PSD_run
            print("run")
            PSD_run.run() 
        elif self.params['task'] == 1:
            # test
            import PSD_run
            print("run")
            PSD_run.run() 
        else:
            print("show results")

    def close(self,event):
        self.Close(True)

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
        self.version = " v2"
        self.title = "列车调度演示系统"+self.version
        frame = MainFrame(None,-1,self.title)
        frame.Show(True)

        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()