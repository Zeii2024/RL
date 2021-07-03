import wx

class TextEntryDialog(wx.Dialog):

    def __init__(self, parent=None, title='Title', caption='Caption', size=(500, 200)):
        '''
        #~ dialog = TextEntryDialog(parent=None, title=title,caption=caption,size=size)
        #~ dialog = TextEntryDialog()
        '''
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(TextEntryDialog, self).__init__(parent, -1, title=title, style=style)
        self.text = wx.StaticText(self, -1, caption)
        self.input = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.input.SetInitialSize(size)
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text, 0, wx.ALL, 5)
        self.sizer.Add(self.input, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.buttons, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(self.sizer)
        self.Center()

    def SetValue(self, value):
        self.input.SetValue(value)

    def GetValue(self):
        return self.input.GetValue()


def wxinputbox(Initialstring='Initial String', title='Title', caption='Caption', size=(500, 200)):
    '''
    #~ >>>stringvalue=wxinputbox(Initialstring='Initial String',title='Title',caption='Caption',size=(500,200)):
    #~ >>> stringvalue=wxinputbox()
    '''
    app = wx.App()
    # ~ dialog = TextEntryDialog(None, title=title,caption=caption,size=size)
    dialog = TextEntryDialog(size=(150,30))
    dialog.SetValue(Initialstring)
    if dialog.ShowModal() == wx.ID_OK:
        stringvalue = dialog.GetValue()
    else:
        stringvalue = ''
        dialog.Destroy()
        app.MainLoop()
    return stringvalue


if __name__ == '__main__':
    # ~ #使用wx的输入对话框
    stringvalue = wxinputbox()
    print(stringvalue)

# ~ if __name__ == '__main__':
# ~ app = wx.PySimpleApp()
# ~ #使用wx自带的输入对话框
# ~ dialog = wx.TextEntryDialog(None, 'Rules:', 'Edit rules',
# ~ style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
# ~ dialog.SetInitialSize((500,200))
# ~ if dialog.ShowModal() == wx.ID_OK:
# ~ print 'OK'
# ~ dialog.Destroy()
# ~ app.MainLoop()