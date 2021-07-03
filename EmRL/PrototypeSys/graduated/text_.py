import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        panel = wx.Panel(self)

        self.static_text = wx.StaticText(panel, label="静态文本", pos=(10, 10))

        self.text_1 = wx.TextCtrl(panel, value="文本框", pos=(10, 40))
        self.text_2 = wx.TextCtrl(panel, value="密码框", style=wx.TE_PASSWORD, pos=(10, 70))
        self.text_3 = wx.TextCtrl(panel, value="只读文本框", style=wx.TE_READONLY, pos=(10, 100))
        self.text_4 = wx.TextCtrl(panel, value="多行\n文本框", style=wx.TE_MULTILINE, pos=(10, 130))

        self.btn1 = wx.Button(panel, label="修改窗口标题", pos=(200, 10))
        self.btn2 = wx.Button(panel, label="修改静态文本内容", pos=(200, 40))
        self.btn3 = wx.Button(panel, label="修改文本框内容", pos=(200, 70))
        self.btn4 = wx.Button(panel, label="修改只读文本框内容", pos=(200, 100))

        self.Bind(wx.EVT_BUTTON, self.OnButton1, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnButton2, self.btn2)
        self.Bind(wx.EVT_BUTTON, self.OnButton3, self.btn3)
        self.Bind(wx.EVT_BUTTON, self.OnText1, self.btn4)

    def OnButton1(self, event):
        self.Title += 'Hello'
    def OnButton2(self, event):
        self.static_text.Label += 'Hi'
    def OnButton3(self, event):
        self.text_1.Value = 'Good'
        self.text_2.Value = 'GOOD'
        self.text_3.Value = 'Good\nbetter\nbest'
        self.text_4.Value = 'GOOD\nBetter\nBest'
    def OnText1(self, event):
        self.text_3.Value = self.text_1.Value

app = wx.App()
frame = MyFrame(None, title="Multi_Text", size=(500, 300))
frame.Show()
app.MainLoop()