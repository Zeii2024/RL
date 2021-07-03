import vtkmodules.all as vtk
from vtkmodules.util.vtkImageImportFromArray import *
import SimpleITK as sitk
import numpy as np
import cv2
import wx

# path = 'E:\\111\\DATA_nii\\case_00039\\imaging.nii.gz'  # segmentation volume
# path ='E:\\111\\DATA_nii\\case_00039\\segmentation.nii'

def utils_view_3D(path):
    class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
        def __init__(self, parent=None):
            self.parent = vtk.vtkRenderWindowInteractor()
            if (parent is not None):
                self.parent = parent

            self.AddObserver("KeyPressEvent", self.keyPress)

        def keyPress(self, obj, event):
            key = self.parent.GetKeySym()
            if key == 'Up':
                gradtfun.AddPoint(-100, 1.0)
                gradtfun.AddPoint(10, 1.0)
                gradtfun.AddPoint(20, 1.0)

                volumeProperty.SetGradientOpacity(gradtfun)
                # 下面这一行是关键，实现了actor的更新
                renWin.Render()
            if key == 'Down':
                tfun.AddPoint(1129, 0)
                tfun.AddPoint(1300.0, 0.1)
                tfun.AddPoint(1600.0, 0.2)
                tfun.AddPoint(2000.0, 0.1)
                tfun.AddPoint(2200.0, 0.1)
                tfun.AddPoint(2500.0, 0.1)
                tfun.AddPoint(2800.0, 0.1)
                tfun.AddPoint(3000.0, 0.1)
                # 下面这一行是关键，实现了actor的更新
                renWin.Render()

    def StartInteraction():
        renWin.SetDesiredUpdateRate(10)

    def EndInteraction():
        renWin.SetDesiredUpdateRate(0.001)

    def ClipVolumeRender(obj):
        obj.GetPlanes(planes)
        volumeMapper.SetClippingPlanes(planes)

    ds = sitk.ReadImage(path)
    data = sitk.GetArrayFromImage(ds)

    spacing = ds.GetSpacing()
    srange = [np.min(data), np.max(data)]
    img_arr = vtkImageImportFromArray()
    img_arr.SetArray(data)
    img_arr.SetDataSpacing(spacing)
    origin = (0, 0, 0)
    img_arr.SetDataOrigin(origin)  # 设置vtk数据的坐标系原点
    img_arr.Update()


    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)  # 把一个空的渲染器添加到一个空的窗口上
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)  # 把上面那个窗口加入交互操作
    iren.SetInteractorStyle(KeyPressInteractorStyle(parent=iren))  # 在交互操作里面添加这个自定义的操作例如up,down
    min = srange[0]
    max = srange[1]
    diff = max - min
    inter = 4200 / diff
    shift = -min

    shifter = vtk.vtkImageShiftScale()  # 对偏移和比例参数来对图像数据进行操作 数据转换，之后直接调用shifter
    shifter.SetShift(shift)
    shifter.SetScale(inter)
    shifter.SetOutputScalarTypeToUnsignedShort()
    shifter.SetInputData(img_arr.GetOutput())
    shifter.ReleaseDataFlagOff()

    shifter.Update()

    tfun = vtk.vtkPiecewiseFunction()  # 不透明度传输函数---放在tfun
    tfun.AddPoint(1600, 0)
    tfun.AddPoint(2200.0, 0.3)
    tfun.AddPoint(2500.0, 0.1)
    tfun.AddPoint(3000.0, 0.5)

    gradtfun = vtk.vtkPiecewiseFunction()  # 梯度不透明度函数---放在gradtfun
    gradtfun.AddPoint(10, 0)
    gradtfun.AddPoint(90, 0.5)
    gradtfun.AddPoint(100, 1.0)

    ctfun = vtk.vtkColorTransferFunction()  # 颜色传输函数---放在ctfun
    ctfun.AddRGBPoint(0.0, 0.1, 0.0, 0.0)
    ctfun.AddRGBPoint(1280.0, 0.5, 0.2, 0.3)
    ctfun.AddRGBPoint(2200.0, 0.9, 0.2, 0.3)
    ctfun.AddRGBPoint(3024.0, 0.5, 0.5, 0.5)

    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputData(shifter.GetOutput())
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(ctfun)
    volumeProperty.SetScalarOpacity(tfun)
    volumeProperty.SetGradientOpacity(gradtfun)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()

    newvol = vtk.vtkVolume()
    newvol.SetMapper(volumeMapper)
    newvol.SetProperty(volumeProperty)

    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(shifter.GetOutputPort())

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)

    ren.AddActor(outlineActor)
    ren.AddVolume(newvol)
    ren.SetBackground(0, 0, 0)
    renWin.SetSize(600, 600)

    planes = vtk.vtkPlanes()
    boxWidget = vtk.vtkBoxWidget()
    boxWidget.SetInteractor(iren)
    boxWidget.SetPlaceFactor(1.0)
    boxWidget.PlaceWidget(0, 0, 0, 0, 0, 0)
    boxWidget.InsideOutOn()
    boxWidget.AddObserver("StartInteractionEvent", StartInteraction)
    boxWidget.AddObserver("InteractionEvent", ClipVolumeRender)
    boxWidget.AddObserver("EndInteractionEvent", EndInteraction)

    outlineProperty = boxWidget.GetOutlineProperty()
    outlineProperty.SetRepresentationToWireframe()
    outlineProperty.SetAmbient(1.0)
    outlineProperty.SetAmbientColor(1, 1, 1)
    outlineProperty.SetLineWidth(9)

    selectedOutlineProperty = boxWidget.GetSelectedOutlineProperty()
    selectedOutlineProperty.SetRepresentationToWireframe()
    selectedOutlineProperty.SetAmbient(1.0)
    selectedOutlineProperty.SetAmbientColor(1, 0, 0)
    selectedOutlineProperty.SetLineWidth(3)

    ren.ResetCamera()
    iren.Initialize()
    renWin.Render()
    iren.Start()

def imgToBitmap(data,flag):
    if flag=='rotate':
        data = cv2.flip(data, 0)
        data = cv2.transpose(data)
    data = data.astype(np.uint8)
    dstheight = int(data.shape[0]*0.5)
    dstwidth = int(data.shape[1]*0.5)
    data = cv2.resize(data,(dstwidth,dstheight),0,0)
    data_cv2 = cv2.cvtColor(data,cv2.COLOR_BGR2RGB)
    data_Bitmap = wx.Bitmap.FromBuffer(dstwidth,dstheight,data_cv2)
    return data_Bitmap