#!/usr/bin/env python
# coding:utf-8
"""
  Author:  u"王浩" --<823921498@qq.com>
  Purpose: u"文件夹选择对话框"
  Created: 2014/8/26
"""

import wx
###############################################################################
class DirDialog(wx.Frame):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, -1, u"文件夹选择对话框")
        b = wx.Button(self, -1, u"文件夹选择对话框")
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.filename = None

    # ----------------------------------------------------------------------
    def OnButton(self, event):
        """"""
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print(dlg.GetPath())
            self.filename = dlg.GetPath()
        dlg.Destroy()


###############################################################################
if __name__ == '__main__':
    # frame = wx.App()
    # app = DirDialog()
    # app.Show()
    # frame.MainLoop()
    import os
    start_directory = "E:\\111\\DATA_nii_out\\case_00039"
    os.system("explorer.exe %s" % start_directory)
