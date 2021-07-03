import wx

# 一般GUI程序的最外层框架使用wx.Frame
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, -1, title='StaticBoxSizer Test')
        # 新建一个panel，作为主面板
        self.panel = wx.Panel(self, size=(250, 50))
        # 新建两个按钮，用于弹出消息和关闭程序
        self.btn_hello = wx.Button(self.panel, label='Hello World')
        self.btn_exit = wx.Button(self.panel, label='Exit')
        # 给按钮事件绑定按钮事件方法，不同的控件都有对应的事件，可查阅API文档DOCS
        self.btn_hello.Bind(wx.EVT_BUTTON, self.on_helloworld)
        self.btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)

        # 新建一个sizer用于界面布局，界面布局最好不使用pos参数写死，不然以后不好维护
        self.box_sizer = wx.BoxSizer()
        self.box_sizer.Add(self.btn_hello, 0, wx.ALL, 10)
        self.box_sizer.Add(self.btn_exit, 0, wx.ALL, 10)
        self.panel.SetSizer(self.box_sizer)

        # 界面设计好后，如果使用到了sizer布局控件，一般需要使用Layout重新绘制界面
        self.box_sizer.Layout()
        self.panel.Layout()
        self.Layout()

        # Fit方法使框架自适应内部控件
        self.Fit()

    # 事件方法，的第二个参数evt或者event一定不要忘了，不然这个方法会报错
    # 类中可能有很多个方法，事件方法建议约定一个容易识别的命名方式，比如我这里是以“on_”开头
    def on_helloworld(self, event):
        """弹出消息：Welcome to WxPython!"""
        # 新建一个消息弹窗，用于显示消息
        wx.MessageBox('Welcome to WxPython!')

    def on_exit(self, evt):
        """退出程序"""
        wx.Exit()


if __name__ == '__main__':
    app = wx.App()
    myframe = MyFrame()
    myframe.Show()
    app.MainLoop()