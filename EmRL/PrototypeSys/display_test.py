import wx
import run


class Frame(wx.Frame):
    def __init__(self,p,t):
        super().__init__()
        wx.Frame.__init__(self,
                        id=wx.ID_ANY,
                        parent=p,
                        size=(800,600),
                        title=t) 
        # 设置背景图
        image_file = 'D:/桌面/My_TTP/PrototypeSys/flower.jpg'
        to_bmp_image = wx.Image("flower.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        image_width = to_bmp_image.GetWidth()
        image_height = to_bmp_image.GetHeight()

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
        panel1 = wx.Panel(self,-1,size=(800,100),pos=(0,0))
        panel2 = wx.Panel(self,-1,size=(800,300),pos=(0,100))
        panel3 = wx.Panel(self,-1,size=(800,200),pos=(0,400))

    

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
                            size=(230,40),
                            pos=(160, -1),
                            style=wx.ALIGN_CENTER)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font1 = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text1.SetFont(font1)
        # 设置文字背景色
        text1.SetForegroundColour("Black")          # 设定前景色为黑色
        # text1.SetBackgroundColour("White")        # 设置背景色为白色
        
        # 设置文本2
        text2 = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "参数设置：",
                            (260,20),)      # 居中对齐:wx.ALIGN_CENTER。 居右：ALIGN_RIGHT
        # 设置字体格式
        font2 = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text2.SetFont(font2)
        # 设置文字背景色
        text2.SetForegroundColour("Black")        # 设定前景色为黑色

        # 设置文本3
        text_env = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "环境大小：",
                            (370,20),)
        text_env.SetFont(font2)
        # 环境复选框
        candidates1 = [u"小", u"中", u"大"]
        self.combol_env = wx.ComboBox(parent=panel2,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(480, 18),
                              value="",
                              choices=candidates1,
                              style=wx.CB_READONLY,
                              name=u"环境大小")
        # 设置列车数量文本4
        text_train = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "列车数量：",
                            (370,60),)
        text_train.SetFont(font2)
        # 环境复选框
        candidates2 = [u"4", u"5", u"6", u"7", u"8"]
        self.combol_train = wx.ComboBox(parent=panel2,
                              id=-1,
                              size=wx.DefaultSize,
                              pos=(480, 58),
                              value="",
                              choices=candidates2,
                              style=wx.CB_READONLY,
                              name=u"列车数量")
        
        # 设置选择模型文本5
        text_model = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "选择模型：",
                            (260,100),)
        text_model.SetFont(font2)
        # 设置单选框
        sampleList1 = ['SCN', 'ACN']
        self.modelRadioBox = wx.RadioBox(panel2, -1, "", (370, 80), (100,90),
                                sampleList1, 1, wx.RA_SPECIFY_COLS)

        # 设置选择任务文本6
        text_task = wx.StaticText(panel2,
                            wx.ID_ANY,
                            "选择任务：",
                            (260,190),)
        text_task.SetFont(font2)
        # 设置单选框
        sampleList2 = ['train', 'test', '展示结果']
        self.taskRadioBox = wx.RadioBox(panel2, -1, "", (370, 168), (100,120),
                                sampleList2, 1, wx.RA_SPECIFY_COLS)
        # 设置按钮
        start_button = wx.Button(panel3, -1, u"开始", pos=(260, 50))
        show_button = wx.Button(panel3, -1, u"结果展示", pos=(420, 50))

        # 绑定事件
        panel2.Bind(wx.EVT_COMBOBOX, self.setEnv,self.combol_env)
        panel2.Bind(wx.EVT_COMBOBOX, self.setTrain,self.combol_train)
        panel2.Bind(wx.EVT_RADIOBOX, self.choiceModel,self.modelRadioBox)
        panel2.Bind(wx.EVT_RADIOBOX, self.choiceTask,self.taskRadioBox)

        # 设置sizer
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(panel2,0,wx.GROW)
        sizer0.Add(panel1,0.5,wx.EXPAND)
        sizer0.Add(sizer2,2,wx.GROW)
        sizer0.Add(panel3,0.5,wx.GROW)

        # 激活sizer
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)     
        self.Show(True)

    def setEnv(self,event):
        self.env = self.combol_env.GetSelection()
        print("setEnv:",self.env)

    def setTrain(self,event):
        self.num_of_train = self.combol_train.GetValue()
        print("setEnv:",self.num_of_train)

    def choiceModel(self,event):
        # 输出序号idx
        p = self.modelRadioBox.GetSelection()
        # 输出字符
        self.model =  self.modelRadioBox.GetStringSelection()
        print("model:",self.model)
        print("p:",p)

    def choiceTask(self, event):
        self.task = self.taskRadioBox.GetStringSelection()
        print("task:",self.task)

    
    # def start(self, event):
        # import 

if __name__=='__main__':
    app = wx.App()
    # 设置一个窗口

    frame = Frame(None,"演示系统版本1")
    # 创建图标
    icon_img = wx.Icon(name="D:/桌面/My_TTP/EmRL/PrototypeSys/icon_img_1.PNG",type=wx.BITMAP_TYPE_ANY)
    # 设置图标
    frame.SetIcon(icon_img)

    frame.Show()
    app.MainLoop()