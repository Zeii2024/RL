import wx
from matplotlib.backends import backend_wxagg
from matplotlib.figure import Figure


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        self.panel = backend_wxagg.FigureCanvasWxAgg(self, -1, Figure())
        axes = self.panel.figure.gca()
        axes.cla()
        axes.plot([1, 2, 3], [1, 1, 3])

        self.panel.draw()


app = wx.App()
f = TestFrame()
f.Show(True)
app.MainLoop()