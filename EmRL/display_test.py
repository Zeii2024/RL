import wx
import PSD_run


class Frame(wx.Frame):
    def __init__(self,p,t):
        super().__init__()
        width = 600
        height = 600
        wx.Frame.__init__(self,
                        id=wx.ID_ANY,
                        parent=p,
                        size=(width,height),
                        title=t) 
        
        splitter = wx.SplitterWindow(self)
        # 设置背景图
        image_file = 'D:/桌面/My_TTP/EmRL/PrototypeSys/flower.jpg'
        to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        image_width = to_bmp_image.GetWidth()
        image_height = to_bmp_image.GetHeight()

        # 参数表
        self.params = {'env': 1,
                        'num_of_train': 4,
                        'model': 0,
                        'task': 0}
        # 设置菜单
        filemenu = wx.Menu()
        # 向菜单里添加open,about,exit选项
        # wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", \
            " Information about this program")    # (ID, 项目名称, 状态栏信息)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", \
            " Terminate the program")    # (ID, 项目名称, 状态栏信息)
        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")    # 在菜单栏中添加filemenu菜单
        self.SetMenuBar(menuBar)    # 在frame中添加菜单栏
        
        # 创建底部的状态栏
        self.CreateStatusBar()    # 创建位于窗口的底部的状态栏
        
        

        # 设置面板
        panel1 = wx.Panel(splitter,-1,size=(width,100),pos=(0,0),style=wx.BORDER_SUNKEN)
        panel2 = wx.Panel(splitter,-1,size=(width,300),pos=(0,100),style=wx.BORDER_SUNKEN)
        panel3 = wx.Panel(splitter,-1,size=(width,80),pos=(0,400),style=wx.BORDER_SUNKEN)

    

        # 给panel添加背景图
        # bitmap1 = wx.StaticBitmap(panel1, -1, to_bmp_image, (0, 0))
        # bitmap2 = wx.StaticBitmap(panel2, -1, to_bmp_image, (0, 0))
        # bitmap3 = wx.StaticBitmap(panel3, -1, to_bmp_image, (0, 0))
        #panel1.SetBackgroundColour("#007FFF")     # 蓝色
        #panel3.SetBackgroundColour("#00FF7F")     # 绿色
        # 设置文本1
        text1 = wx.StaticText(parent=panel1,
                            id=wx.ID_ANY,
                            label="列车调度演示系统",
                            size=(160,40),
                            pos=(140, 20),
                            style=wx.ALIGN_CENTER)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font1 = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text1.SetFont(font1)
        # 设置文字背景色
        text1.SetForegroundColour("Black")        # 设定前景色为黑色
        # text1.SetBackgroundColour("White")        # 设置背景色为白色
        
        # 设置文本2
        text2 = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "参数设置：",
                            (180,20),)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font2 = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text2.SetFont(font2)
        # 设置文字背景色
        text2.SetForegroundColour("Black")        # 设定前景色为黑色

        # 设置文本3
        text_env = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "环境大小：",
                            (290,20),)
        text_env.SetFont(font2)
        # 环境复选框
        candidates1 = [u"小", u"中", u"大"]
        self.combol_env = wx.ComboBox(parent=panel2,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(400, 18),
                              value="",
                              choices=candidates1,
                              style=wx.CB_READONLY,
                              name=u"环境大小")
        # 设置列车数量文本4
        text_train = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "列车数量：",
                            (290,60),)
        text_train.SetFont(font2)
        # 环境复选框
        candidates2 = [u"4", u"5", u"6", u"7", u"8"]
        self.combol_train = wx.ComboBox(parent=panel2,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(400, 58),
                              value="",
                              choices=candidates2,
                              style=wx.CB_READONLY,
                              name=u"列车数量")
        
        # 设置选择模型文本5
        text_model = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "选择模型：",
                            (180,100),)
        text_model.SetFont(font2)
        # 设置单选框
        sampleList1 = ['SCN', 'ACN']
        self.modelRadioBox = wx.RadioBox(panel2, -1, "", (290, 80), (100,90),
                                sampleList1, 1, wx.RA_SPECIFY_COLS)

        # 设置选择任务文本6
        text_task = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "选择任务：",
                            (180,190),)
        text_task.SetFont(font2)
        # 设置单选框
        sampleList2 = ['train', 'test', '展示结果']
        self.taskRadioBox = wx.RadioBox(panel2, -1, "", (290, 168), (100,120),
                                sampleList2, 1, wx.RA_SPECIFY_COLS)
        # 设置按钮
        self.close_button = wx.Button(panel3, -1, u"关闭", pos=(180, 20))
        self.start_button = wx.Button(panel3, -1, u"开始", pos=(340, 20))

        # 绑定事件
        self.Bind(wx.EVT_MENU,self.close,menuExit) # exit
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout) # about
        panel2.Bind(wx.EVT_COMBOBOX, self.setEnv,self.combol_env)
        panel2.Bind(wx.EVT_COMBOBOX, self.setTrain,self.combol_train)
        panel2.Bind(wx.EVT_RADIOBOX, self.choiceModel,self.modelRadioBox)
        panel2.Bind(wx.EVT_RADIOBOX, self.choiceTask,self.taskRadioBox)

        panel3.Bind(wx.EVT_BUTTON,self.start, self.start_button)
        panel3.Bind(wx.EVT_BUTTON,self.close, self.close_button)

        # 设置sizer
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        #sizer2.Add(panel2,0,wx.GROW)
        sizer0.Add(panel1,1,wx.EXPAND)
        sizer0.Add(panel2,0,wx.EXPAND)
        sizer0.Add(panel3,0,wx.EXPAND)

        # 激活sizer
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)     
        self.Show(True)

    # 设置菜单栏
    def OnAbout(self, event):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self, "列车调度演示系统", \
            "About", wx.OK)    # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()    # 显示对话框
        dlg.Destroy()    # 当结束之后关闭对话框

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

if __name__=='__main__':
    app = wx.App()
    # 设置一个窗口

    frame = Frame(None,"演示系统")
    # 创建图标
    #icon_img = wx.Icon(name="icon_img_1.png",type=wx.BITMAP_TYPE_ANY)
    # 设置图标
    #frame.SetIcon(icon_img)

    frame.Show()
    app.MainLoop()