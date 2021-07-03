import os
import wx
import time
from utils.utils_view_3d import utils_view_3D
from utils.utils_reSampled import utils_getReSampled
from utils.utils_reSampled import utils_delFullBlack
from utils.utils_statistic import utils_numOfTumor
from utils.utils_preData import utils_retCopy,utils_flippedHorizontally,utils_flippedVertical,utils_rotation,utils_cropScale

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
        self.Centre()
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
        attItem = wx.MenuItem(imgSegMenu, ID_imgSeg_fcn, "Attention", kind=wx.ITEM_NORMAL)
        gruItem = wx.MenuItem(imgSegMenu, ID_imgSeg_cnn, "GRU", kind=wx.ITEM_NORMAL)
        imgSegMenu.Append(attItem)
        imgSegMenu.Append(gruItem)
        menuBar.Append(imgSegMenu, '图像分割')
        self.Bind(wx.EVT_MENU, self.segment_attItem,attItem)
        self.Bind(wx.EVT_MENU, self.segment_gruItem,gruItem)

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
        if self.panel_reSampled:
            self.panel_reSampled.Destroy()
        if self.panel_preData:
            self.panel_preData.Destroy()
        if self.panel_segment:
            self.panel_segment.Destroy()

        self.panel_init = wx.Panel(self,pos=(0, 0), size=(800, 500))
        self.buttonLoad = wx.Button(self.panel_init, -1, u"导入", pos=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.buttonLoad)

        self.buttonView = wx.Button(self.panel_init, -1, u"信息", pos=(50, 60))
        self.Bind(wx.EVT_BUTTON, self.OnView, self.buttonView)

        self.onlyRead_text = wx.TextCtrl(self.panel_init, value="待读入...", style=wx.TE_READONLY, pos=(140, 30), size=(300, 25))
        self.static_text = wx.StaticText(self.panel_init, label="CT图像信息", pos=(140, 70), size=(500, 500))
    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.onlyRead_text.Label = self.filename
            self.sb.SetStatusText("成功导入文件！", 0)
        dlg.Destroy()
    def OnView(self, event):
        if self.filename == None:
            self.static_text.Label = "请导入数据！"
        else:
            import nibabel as nib
            img = nib.load(self.filename)
            self.static_text.Label = "_____CT图像信息：____"
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
            # utils_view_3D(self.filename)
    def reInitUI(self,event):
        self.initUI()


    # 数据可视化
    def visualization(self,event):
        if self.panel_init:
            self.filename = None
            self.panel_init.Destroy()
        if self.panel_reSampled:
            self.panel_reSampled.Destroy()
        if self.panel_preData:
            self.panel_preData.Destroy()
        if self.panel_segment:
            self.panel_segment.Destroy()

        self.filename_visualization = None
        self.panel_visualization = wx.Panel(self, pos=(0, 0), size=(800, 500))

        self._caidan1 = wx.Button(self.panel_visualization, label=u'导入数据', pos=(30, 20), size=(80, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan1)
        self._caidan2 = wx.Button(self.panel_visualization, label=u'三视图映像', pos=(30, 70), size=(80, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan2)
        self._caidan3 = wx.Button(self.panel_visualization, label=u'三维可视化', pos=(30, 120), size=(80, 30))
        self.panel_visualization.Bind(wx.EVT_BUTTON, self.Onclick_visualization, self._caidan3)

        self._background = wx.Image("background.jpg", type=wx.BITMAP_TYPE_ANY)
        self._background = self._background.Rescale(348, 348)  # 改变图像大小
        wx.StaticBitmap(self.panel_visualization, -1, wx.Bitmap(self._background),pos=(130,20))  # 显示图像
    def Onclick_visualization(self,event):
        if event.GetEventObject() == self._caidan1:
            dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename_visualization = dlg.GetPath()
                self.sb.SetStatusText("成功导入文件！", 0)
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
        self.path_input = None
        self.path_output = None
        self.gapSpace = "3.22,1.62,1.62"

        if self.panel_init:
            self.filename = None
            self.panel_init.Destroy()
        if self.panel_visualization:
            self.panel_visualization.Destroy()
        if self.panel_preData:
            self.panel_preData.Destroy()
        if self.panel_segment:
            self.panel_segment.Destroy()

        self.filename_reSampled = None
        self.panel_reSampled = wx.Panel(self, size=(800, 500))

        self._reSampled_caidan1 = wx.Button(self.panel_reSampled, label=u'输入路径', pos=(80, 20), size=(150, 30))
        self._reSampled_onlyRead_text_input_path = wx.TextCtrl(self.panel_reSampled, value="待读入...",style=wx.TE_READONLY, pos=(240, 22), size=(300, 25))
        self._reSampled_caidan1_look = wx.Button(self.panel_reSampled, label=u'查看', pos=(550, 20), size=(80, 30))
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled, self._reSampled_caidan1)
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled_look, self._reSampled_caidan1_look)

        self._reSampled_caidan2 = wx.Button(self.panel_reSampled, label=u'输出路径', pos=(80, 50), size=(150, 30))
        self._reSampled_onlyRead_text_output_path = wx.TextCtrl(self.panel_reSampled, value="待读入...",style=wx.TE_READONLY, pos=(240, 52), size=(300, 25))
        self._reSampled_caidan2_look = wx.Button(self.panel_reSampled, label=u'查看', pos=(550, 50), size=(80, 30))
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled, self._reSampled_caidan2)
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled_look, self._reSampled_caidan2_look)

        self._reSampled_caidan3 = wx.Button(self.panel_reSampled, label=u'体素间距', pos=(80, 80), size=(150, 30))
        self._reSampled_onlyRead_text_exe = wx.TextCtrl(self.panel_reSampled, value="待读入...   默认为: 3.22,1.62,1.62",style=wx.TE_READONLY, pos=(240, 82), size=(300, 25))
        self._reSampled_caidan3_exe = wx.Button(self.panel_reSampled, label=u'执行', pos=(550, 80), size=(80, 30))
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled, self._reSampled_caidan3)
        self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled_look, self._reSampled_caidan3_exe)

        self._reSampled_static_text = wx.StaticText(self.panel_reSampled, pos=(260, 120), size=(500, 100))
    def Onclick_reSampled(self,event):
        if event.GetEventObject() == self._reSampled_caidan1:
            dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.path_input = dlg.GetPath()
                self._reSampled_onlyRead_text_input_path.Label = self.path_input
            dlg.Destroy()
        if event.GetEventObject() == self._reSampled_caidan2:
            dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.path_output = dlg.GetPath()
                self._reSampled_onlyRead_text_output_path.Label = self.path_output
            dlg.Destroy()
        if event.GetEventObject() == self._reSampled_caidan3:
            dlg = wx.TextEntryDialog(None, "请在下面文本框中输入体素间距（Z,X,Y）:", "体素间距", "3.22,1.62,1.62")
            if dlg.ShowModal() == wx.ID_OK:
                self.gapSpace = dlg.GetValue()
                self._reSampled_onlyRead_text_exe.Label = self.gapSpace
            dlg.Destroy()
    def Onclick_reSampled_look(self, event):
        self._case = None

        if event.GetEventObject() == self._reSampled_caidan1_look:
            if not self.path_input:
                wx.MessageBox('输入路径为空！')
            else:
                os.system("explorer.exe %s" % self.path_input)
        if event.GetEventObject() == self._reSampled_caidan2_look:
            if not self.path_output:
                wx.MessageBox("输出路径为空！")
            else:
                os.system("explorer.exe %s" % self.path_output)
        if event.GetEventObject() == self._reSampled_caidan3_exe:
            if not self.path_input or not self.path_output:
                wx.MessageBox('路径信息不全！')
            else:
                self._case = utils_getReSampled(self.path_input,self.path_output,self.gapSpace)
                self._num_tumor,self._num_kidney,self._num_black = utils_numOfTumor(self.path_output+"\\"+self._case)
                self._reSampled_static_text.Label = "\n________重采样得到：________" + "\n\n肿瘤切片数目为：\t" + str(self._num_tumor) + "\n\n正常组织切片数目为：\t" + str(self._num_kidney) + "\n\n全黑切片数目为：\t"+str(self._num_black)
                wx.MessageBox("案例：" + str(self._case)+" 重采样完毕！")
                self._reSampled_delBlack = wx.Button(self.panel_reSampled, label=u'去除黑片', pos=(550, 260), size=(80, 30))
                self.panel_reSampled.Bind(wx.EVT_BUTTON, self.Onclick_reSampled_delBlack, self._reSampled_delBlack)
    def Onclick_reSampled_delBlack(self,event):
        if not self.path_output:
            wx.MessageBox("路径信息不全！")
        else:
            if self._case:
                utils_delFullBlack(self.path_output,self._case)
                self._num_black = 0
                self._reSampled_static_text.Label = "\n________重采样得到：________" + "\n\n肿瘤切片数目为：\t" + str(self._num_tumor) + "\n\n正常组织切片数目为：\t" + str(self._num_kidney) + "\n\n全黑切片数目为：\t" + str(self._num_black)
                wx.MessageBox("去除黑片成功！")
            else:
                pass


    # 数据预处理
    def OnPreData(self, event):
        self._pic_input = None
        self._pic_output = None

        self._ret_pic = None
        self._ret_gt = None

        self._flag = [False,False,False,False]
        self._func = [utils_flippedHorizontally,utils_flippedVertical,utils_rotation,utils_cropScale]

        if self.panel_init:
            self.filename = None
            self.panel_init.Destroy()
        if self.panel_visualization:
            self.panel_visualization.Destroy()
        if self.panel_reSampled:
            self.panel_reSampled.Destroy()
        if self.panel_segment:
            self.panel_segment.Destroy()

        self.filename_preData = None
        self.panel_preData = wx.Panel(self, pos=(0, 0), size=(800, 500))

        self._preData_caidan1 = wx.Button(self.panel_preData, label=u'输入', pos=(100, 300), size=(150, 30))
        self.panel_preData.Bind(wx.EVT_BUTTON, self.Onclick_preData, self._preData_caidan1)
        self._preData_caidan2 = wx.Button(self.panel_preData, label=u'输出', pos=(500, 300), size=(150, 30))
        self.panel_preData.Bind(wx.EVT_BUTTON, self.Onclick_preData, self._preData_caidan2)
        self._preData_caidan3 = wx.Button(self.panel_preData, label=u'查看标签', pos=(500, 340), size=(150, 30))
        self.panel_preData.Bind(wx.EVT_BUTTON, self.Onclick_preData, self._preData_caidan3)

        self._preData_background = wx.Image("./utils/utils_background.jpg", type=wx.BITMAP_TYPE_ANY).Rescale(256, 256).ConvertToBitmap()
        self._preData_background = wx.StaticBitmap(self.panel_preData, -1, self._preData_background,pos=(50,30))  # 显示图像
        self._pic_output = wx.Image("./utils/utils_background.jpg", type=wx.BITMAP_TYPE_ANY).Rescale(256, 256).ConvertToBitmap()
        self._pic_output = wx.StaticBitmap(self.panel_preData, -1, self._pic_output, pos=(450, 30))  # 显示图像

        self._preData_static_text = wx.StaticText(self.panel_preData,label="[处理方式] ",pos=(350, 50))
        self._cb_flippedHorizontal = wx.CheckBox(self.panel_preData,label="水平翻转",pos=(350,80))
        self.panel_preData.Bind(wx.EVT_CHECKBOX,self.Onclick_preData_cb,self._cb_flippedHorizontal)
        self._cb_flippedVertical = wx.CheckBox(self.panel_preData, label="垂直翻转", pos=(350, 110))
        self.panel_preData.Bind(wx.EVT_CHECKBOX, self.Onclick_preData_cb, self._cb_flippedVertical)
        self._cb_rotation = wx.CheckBox(self.panel_preData, label="旋转45°", pos=(350, 140))
        self.panel_preData.Bind(wx.EVT_CHECKBOX, self.Onclick_preData_cb, self._cb_rotation)
        self._cb_cropScale = wx.CheckBox(self.panel_preData, label="缩放", pos=(350, 170))
        self.panel_preData.Bind(wx.EVT_CHECKBOX, self.Onclick_preData_cb, self._cb_cropScale)
    def Onclick_preData(self,event):
        if event.GetEventObject() == self._preData_caidan1:
            dlg = wx.FileDialog(self, "Open .jpg file", wildcard="jpg files (*.jpg)|*.jpg",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self._pic_input = dlg.GetPath()
                self.sb.SetStatusText(self._pic_input, 0)

                pic = wx.Image(self._pic_input, wx.BITMAP_TYPE_JPEG).Rescale(256, 256).ConvertToBitmap()
                self._preData_background.SetBitmap(wx.Bitmap(pic))

                self._ret_pic = utils_retCopy(self._pic_input)
                self._ret_gt = str(self._ret_pic).replace("Images", "GT")

            dlg.Destroy()
        if event.GetEventObject() == self._preData_caidan2:
            if not self._pic_input:
                wx.MessageBox("请输入要处理的图片！")
            else:
                self._ret_pic = utils_retCopy(self._pic_input)
                self._ret_gt = str(self._ret_pic).replace("Images", "GT")

                for i,fx in enumerate(self._flag):
                    if fx:
                        self._func[i](self._ret_pic)
                        self._func[i](self._ret_gt)

                self._pic_output = wx.Image(self._ret_pic, type=wx.BITMAP_TYPE_ANY).Rescale(256, 256).ConvertToBitmap()
                self._pic_output = wx.StaticBitmap(self.panel_preData, -1, self._pic_output, pos=(450, 30))  # 显示图像
        if event.GetEventObject() == self._preData_caidan3:
            if not self._ret_gt:
                wx.MessageBox("请输入待预处理的图片！")
            else:
                self._pic_output = wx.Image(self._ret_gt, type=wx.BITMAP_TYPE_ANY).Rescale(256, 256).ConvertToBitmap()
                self._pic_output = wx.StaticBitmap(self.panel_preData, -1, self._pic_output, pos=(450, 30))  # 显示图像
    def Onclick_preData_cb(self,event):
        e = event.GetEventObject()
        if e == self._cb_flippedHorizontal:
            isChecked_hor = e.GetValue()
            if isChecked_hor:
                self._flag[0] = True
            else:
                self._flag[0] = False
        if e == self._cb_flippedVertical:
            isChecked_ver = e.GetValue()
            if isChecked_ver:
                self._flag[1] = True
            else:
                self._flag[1] = False
        if e == self._cb_rotation:
            isChecked_rot = e.GetValue()
            if isChecked_rot:
                self._flag[2] = True
            else:
                self._flag[2] = False
        if e == self._cb_cropScale:
            isChecked_cro = e.GetValue()
            if isChecked_cro:
                self._flag[3] = True
            else:
                self._flag[3] = False

    # 图像分割
    def segment_attItem(self,event):
        print("点击了图像分割_attItem！")
        if self.panel_init:
            self.filename = None
            self.panel_init.Destroy()
        if self.panel_visualization:
            self.panel_visualization.Destroy()
        if self.panel_reSampled:
            self.panel_reSampled.Destroy()
        if self.panel_preData:
            self.panel_preData.Destroy()

        self.fileName_segment = None
        self.modelName_segment = None
        self.panel_segment = wx.Panel(self, pos=(0, 0), size=(800, 500))

        self._st = wx.StaticText(self.panel_segment,label="选择网络模型：",pos=(32,10))

        self._net_select = ["基础框架", "注意力模块", "GRU模块", "综合框架"]
        self._net_cb = wx.ComboBox(self.panel_segment, pos=(30, 30), choices=self._net_select, style=wx.CB_READONLY)
        self._net_cb.Bind(wx.EVT_COMBOBOX, self.OnSelect_segment)

        self._button1_segment = wx.Button(self.panel_segment, label=u'导入数据', pos=(30, 80), size=(90, 30))
        self.panel_segment.Bind(wx.EVT_BUTTON, self.Onclick_segment, self._button1_segment)

        self._button2_segment = wx.Button(self.panel_segment, label=u'加载模型', pos=(30, 130), size=(90, 30))
        self.panel_segment.Bind(wx.EVT_BUTTON, self.Onclick_segment, self._button2_segment)
        self._button3_segment = wx.Button(self.panel_segment, label=u'得到结果', pos=(30, 180), size=(90, 30))
        self.panel_segment.Bind(wx.EVT_BUTTON, self.Onclick_segment, self._button3_segment)

        self._background_segment = wx.Image("background.jpg", type=wx.BITMAP_TYPE_ANY)
        self._background_segment = self._background_segment.Rescale(348, 348)  # 改变图像大小
        wx.StaticBitmap(self.panel_segment, -1, wx.Bitmap(self._background_segment),pos=(180,20))  # 显示图像
    def Onclick_segment(self,event):
        if event.GetEventObject() == self._button1_segment:
            dlg = wx.FileDialog(self, "Open .nii.gz file", wildcard="nii files (*.nii.gz)|*.nii.gz",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.fileName_segment = dlg.GetPath()
                self.sb.SetStatusText("成功导入"+self.fileName_segment, 0)
            dlg.Destroy()
        elif event.GetEventObject() == self._button2_segment:
            print("加载模型！")
            dlg = wx.FileDialog(self, "Open .pth file", wildcard="nii files (*.pth)|*.pth",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.modelName_segment = dlg.GetPath()
                self.sb.SetStatusText("成功加载"+self.modelName_segment, 0)
            dlg.Destroy()
        else:
            if self.fileName_segment == None:
                wx.MessageBox('请导入数据！')
            else:
                print("得到图像分割结果！")
    def OnSelect_segment(self,event):
        i = event.GetString()
        print("选择了",i)

    def segment_gruItem(self,event):
        print("点击了图像分割_gruItem！")
        # if self.panel_init:
        #     self.filename = None
        #     self.panel_init.Destroy()
        # if self.panel_visualization:
        #     self.panel_visualization.Destroy()
        # if self.panel_reSampled:
        #     self.panel_reSampled.Destroy()
        # if self.panel_preData:
        #     self.panel_preData.Destroy()

        # self.panel_preData = wx.Panel(self, pos=(0, 0), size=(800, 500))


    # 状态栏
    def setStatusBar(self):
        self.sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-2,-1])
        self.SetStatusText("Ready",0)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d %H:%M:%S',t)
        self.SetStatusText(st,1)


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
        self.sizer.Add(wx.StaticText(self, -1, "Version：v4"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
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