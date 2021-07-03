# Box布局器
'''使用步骤：
1.创建BoxSizer对象
2.将控件添加到布局管理器中，由布局管理器管理控件布局（但布局管理器不是一个容器）
本例中
1.创建一个垂直方向的box布局管理器-vbox
2.写一个静态文本框，并将其添加到vbox
3.创建一个水平方向的box布局管理器-hbox
4.写两个button，并将button添加到hbox
5.将hbox添加到vbox中
6.将vbox添加到这个面板中
'''

import wx


# 自定义窗口类MyFrame
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Box布局器", size=(300, 120))
        self.Centre()  # 设置窗口居中
        panel = wx.Panel(parent=self)

        # 创建垂直方向box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 创建一个静态文本
        self.statictext = wx.StaticText(parent=panel, label='Button1单击')
        # 添加静态文本到vbox布局管理器中，指定文本框在整个面板中所占权重为2，标志为固定大小填充，顶部有边框，水平居中，边框宽度为10
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=10)
        # 设置两个button按钮并绑定点击事件
        b1 = wx.Button(parent=panel, id=10, label='button1')
        b2 = wx.Button(parent=panel, id=11, label='button2')
        self.Bind(wx.EVT_BUTTON, self.on_click, id=10, id2=20)

        # 创建水平方向box布局管理器（默认水平方向）
        hbox = wx.BoxSizer()
        # 将两个button添加到hbox布局管理器中
        hbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, border=5)
        hbox.Add(b2, 0, wx.EXPAND | wx.BOTTOM, border=5)

        # 将hbox添加到vbox
        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        # 整个界面为一个面板，面板中设置一个垂直方向的布局管理器（根布局管理器）
        panel.SetSizer(vbox)

    '''将两个button放到一个水平方向布局管理器，然后将水平方向布局管理器放到垂直方向布局管理器中 
    添加控件到其父容器是通过parent属性，这里button和statictext的父容器都是面板，与布局管理器的添加是没有关系的
    布局管理器添加是通过Add()方法添加，这个添加只是说将某个控件纳入布局管理器管理
    不是添加到容器中，注意布局管理器不是一个容器'''

    def on_click(self):
        pass


# 自定义应用程序对象
class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True

    def OnExit(self):
        print('应用程序退出')
        return 0


if __name__ == '__main__':
    app = App()  # 调用上面函数
    app.MainLoop()  # 进入主事件循环