# Copyright (C) 2019 Cody Sorgenfrey
import c4d
import os

class res(object):
    QUANTIZE_SPLINE_GROUP = 1000
    QUANTIZE_SPLINE_ORDER = 1002
    QUANTIZE_SPLINE_ORDER_XYZ = 1
    QUANTIZE_SPLINE_ORDER_XZY = 2
    QUANTIZE_SPLINE_ORDER_YXZ = 3
    QUANTIZE_SPLINE_ORDER_YZX = 4
    QUANTIZE_SPLINE_ORDER_ZYX = 5
    QUANTIZE_SPLINE_ORDER_ZXY = 6
res = res()


def load_bitmap(path):
    path = os.path.join(os.path.dirname(__file__), path)
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp.InitWith(path)[0] != c4d.IMAGERESULT_OK:
        bmp = None
    return bmp

def compX(endSpacer, points):
    lastIn = points[len(points) - 1]
    if lastIn.x != endSpacer.x:
        lastIn = c4d.Vector(endSpacer.x, lastIn.y, lastIn.z)
        points.append(lastIn)

def compY(endSpacer, points):
    lastIn = points[len(points) - 1]
    if lastIn.y != endSpacer.y:
        lastIn = c4d.Vector(lastIn.x, endSpacer.y, lastIn.z)
        points.append(lastIn)

def compZ(endSpacer, points):
    lastIn = points[len(points) - 1]
    if lastIn.z != endSpacer.z:
        lastIn = c4d.Vector(lastIn.x, lastIn.y, endSpacer.z)
        points.append(lastIn)

class connectiongridData(c4d.plugins.ObjectData):
    PLUGIN_ID = 1053145
    PLUGIN_NAME = 'Quantize Spline'
    PLUGIN_INFO = c4d.OBJECT_GENERATOR | c4d.OBJECT_ISSPLINE | c4d.OBJECT_INPUT
    PLUGIN_DESC = 'Oquantizespline'
    PLUGIN_ICON = load_bitmap('res/icons/quantize spline.tiff')
    PLUGIN_DISKLEVEL = 0
    LAST_FRAME = 0
    INPUT_SPLINE = None
    UPDATE = True

    @classmethod
    def Register(cls):
        return c4d.plugins.RegisterObjectPlugin(
            cls.PLUGIN_ID,
            cls.PLUGIN_NAME,
            cls,
            cls.PLUGIN_DESC,
            cls.PLUGIN_INFO,
            cls.PLUGIN_ICON,
            cls.PLUGIN_DISKLEVEL
        )

    def Init(self, node):
        self.InitAttr(node, int, [res.QUANTIZE_SPLINE_ORDER])

        node[res.QUANTIZE_SPLINE_ORDER] = 1

        doc = c4d.documents.GetActiveDocument()
        self.LAST_FRAME = doc.GetTime().GetFrame(doc.GetFps())
        self.INPUT_SPLINE = None
        self.UPDATE = True

        return True

    def CheckDirty(self, op, doc) :
        frame = doc.GetTime().GetFrame(doc.GetFps())
        if frame != self.LAST_FRAME:
            self.LAST_FRAME = frame
            op.SetDirty(c4d.DIRTYFLAGS_DATA)
        
        if self.UPDATE:
            self.UPDATE = False
            op.SetDirty(c4d.DIRTYFLAGS_DATA)

    def MakeSpline(self, order):
        inPoints = self.INPUT_SPLINE.GetAllPoints()
        outPoints = []

        for x in range(len(inPoints) - 1):
            p1 = inPoints[x]
            p2 = inPoints[x + 1]

            outPoints.append(p1)

            if order == 2:
                compX(p2, outPoints)
                compZ(p2, outPoints)
                compY(p2, outPoints)
            elif order == 3:
                compY(p2, outPoints)
                compX(p2, outPoints)
                compZ(p2, outPoints)
            elif order == 4:
                compY(p2, outPoints)
                compZ(p2, outPoints)
                compX(p2, outPoints)
            elif order == 5:
                compZ(p2, outPoints)
                compY(p2, outPoints)
                compX(p2, outPoints)
            elif order == 6:
                compZ(p2, outPoints)
                compX(p2, outPoints)
                compY(p2, outPoints)
            else:
                compX(p2, outPoints)
                compY(p2, outPoints)
                compZ(p2, outPoints)

            outPoints.append(p2)

        spline = c4d.SplineObject(0, c4d.SPLINETYPE_LINEAR)
        spline.ResizeObject(len(outPoints), 1)
        spline.SetSegment(0, len(outPoints), False)
        spline[c4d.SPLINEOBJECT_INTERPOLATION] = 1 # natural
        spline[c4d.SPLINEOBJECT_SUB] = 8
        
        for x in range(len(outPoints)):
            spline.SetPoint(x, outPoints[x])

        return spline

    def GetContour(self, op, doc, lod, bt):
        order = op[res.QUANTIZE_SPLINE_ORDER]

        if self.INPUT_SPLINE is None: return None

        return self.MakeSpline(order)

    def GetVirtualObjects(self, op, hh):
        inObj = op.GetDown()
        order = op[res.QUANTIZE_SPLINE_ORDER]

        if inObj is None: return None

        hClone = op.GetAndCheckHierarchyClone(hh, inObj, c4d.HIERARCHYCLONEFLAGS_ASSPLINE, False)

        if not hClone['dirty']: return hClone['clone']
        if hClone['clone'] is None: return None

        print hClone['clone'].GetPointCount()

        self.INPUT_SPLINE = hClone['clone']
        self.UPDATE = True

        return self.MakeSpline(order)


if __name__ == '__main__':
    connectiongridData.Register()
