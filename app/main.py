"""
SketchCraft 2026 - Modernized 3D CAD & Modeling Application
Rebuilding SketchUp with modernized aesthetics, preserved functionality, and exact visual fidelity.
"""

import sys
import os
import math
import argparse
from PyQt6.QtCore import Qt, QPoint, QPointF, QRectF, QSize, QTimer
from PyQt6.QtGui import (
    QAction, QColor, QFont, QIcon, QKeySequence, QLinearGradient,
    QPainter, QPainterPath, QPen, QBrush, QPixmap, QPolygonF
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QLabel, QLineEdit, QComboBox, QSplitter, QScrollArea,
    QFrame, QSlider, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QMenu, QMenuBar, QStatusBar,
    QToolButton, QSizePolicy, QGridLayout
)

# -----------------------------------------------------------------------------
# Modern Fluent Design Styling
# -----------------------------------------------------------------------------
STYLE_SHEET = """
QMainWindow {
    background-color: #F8FAFC;
}
QMenuBar {
    background-color: #FFFFFF;
    color: #1E293B;
    font-size: 12px;
    border-bottom: 1px solid #E2E8F0;
    padding: 1px 4px;
}
QMenuBar::item {
    background-color: transparent;
    padding: 3px 8px;
    border-radius: 3px;
}
QMenuBar::item:selected {
    background-color: #F1F5F9;
    color: #0284C7;
}
QMenu {
    background-color: #FFFFFF;
    color: #1E293B;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 5px 22px 5px 10px;
    border-radius: 4px;
    font-size: 12px;
}
QMenu::item:selected {
    background-color: #E0F2FE;
    color: #0369A1;
}
QToolBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    border-top: none;
    border-left: none;
    border-right: none;
    spacing: 1px;
    padding: 2px 4px;
}
QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 2px;
    color: #334155;
}
QToolButton:hover {
    background-color: #F1F5F9;
    border-color: #CBD5E1;
}
QToolButton:checked {
    background-color: #E0F2FE;
    border-color: #38BDF8;
}
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 11px;
    color: #1E293B;
    min-height: 20px;
}
QStatusBar {
    background-color: #F8FAFC;
    color: #1E293B;
    border-top: 1px solid #E2E8F0;
    font-size: 12px;
    padding: 2px 8px;
}
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 3px;
    padding: 2px 4px;
    font-size: 11px;
    color: #0F172A;
}
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    gridline-color: #E2E8F0;
    color: #1E293B;
    font-size: 11px;
}
QHeaderView::section {
    background-color: #F8FAFC;
    color: #475569;
    padding: 3px 6px;
    border: 1px solid #E2E8F0;
    font-size: 11px;
    font-weight: 500;
}
"""

# -----------------------------------------------------------------------------
# Vector Icon Renderer Matching picture-1.png
# -----------------------------------------------------------------------------
def make_icon(name, size=22):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pad = 3.5
    s = float(size)
    
    if name == "select":
        p.setBrush(QBrush(QColor("#FFFFFF")))
        p.setPen(QPen(QColor("#0F172A"), 1.8))
        path = QPainterPath()
        path.moveTo(pad, pad)
        path.lineTo(pad, s - 5)
        path.lineTo(pad + 4.5, s - 8.5)
        path.lineTo(pad + 9, s - 4)
        path.lineTo(pad + 11.5, s - 6)
        path.lineTo(pad + 7, s - 10.5)
        path.lineTo(pad + 12.5, s - 10.5)
        path.closeSubpath()
        p.drawPath(path)
        
    elif name == "eraser":
        p.setPen(QPen(QColor("#BE123C"), 1.4))
        p.setBrush(QBrush(QColor("#FDA4AF")))
        path = QPainterPath()
        path.moveTo(pad + 3, pad)
        path.lineTo(s - pad, pad + 6)
        path.lineTo(s - pad - 5, s - pad)
        path.lineTo(pad, s - pad - 6)
        path.closeSubpath()
        p.drawPath(path)
        p.setPen(QPen(QColor("#64748B"), 1.2))
        p.drawLine(QPointF(pad + 4, pad + 8), QPointF(s - pad - 2, pad + 13))
        
    elif name == "line":
        p.setPen(QPen(QColor("#B45309"), 2.0))
        p.drawLine(QPointF(pad, s - pad), QPointF(s - pad - 3, pad + 3))
        p.setPen(QPen(QColor("#DC2626"), 2.5))
        p.drawPoint(QPointF(pad, s - pad))
        p.setPen(QPen(QColor("#F59E0B"), 3.5))
        p.drawPoint(QPointF(s - pad - 1, pad + 1))
        
    elif name == "freehand":
        p.setPen(QPen(QColor("#0284C7"), 1.8))
        path = QPainterPath()
        path.moveTo(pad, s - pad - 2)
        path.cubicTo(pad + 4, pad, s - pad - 4, s - pad, s - pad, pad + 2)
        p.drawPath(path)
        
    elif name == "arc":
        p.setPen(QPen(QColor("#DC2626"), 2.0))
        p.drawArc(QRectF(pad, pad + 2, s - 2*pad, s - 2*pad), 30 * 16, 120 * 16)
        p.setPen(QPen(QColor("#0F172A"), 1.5))
        p.drawPoint(QPointF(pad + 2, s - pad))
        p.drawPoint(QPointF(s - pad - 2, s - pad))
        
    elif name == "arc3":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.drawArc(QRectF(pad, pad, s - 2*pad, s - 2*pad), 40 * 16, 160 * 16)
        
    elif name == "pie":
        p.setPen(QPen(QColor("#DC2626"), 1.6))
        p.setBrush(QBrush(QColor(220, 38, 38, 40)))
        p.drawPie(QRectF(pad, pad, s - 2*pad, s - 2*pad), 45 * 16, 90 * 16)
        
    elif name == "rect":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.setBrush(QBrush(QColor(220, 38, 38, 30)))
        p.drawRect(QRectF(pad, pad + 3, s - 2*pad, s - 2*pad - 4))
        
    elif name == "rect_rot":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        poly = QPolygonF([
            QPointF(pad, s - pad - 2),
            QPointF(pad + 8, pad + 2),
            QPointF(s - pad, pad + 6),
            QPointF(s - pad - 8, s - pad + 2)
        ])
        p.drawPolygon(poly)
        
    elif name == "circle":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.setBrush(QBrush(QColor(220, 38, 38, 30)))
        p.drawEllipse(QRectF(pad, pad, s - 2*pad, s - 2*pad))
        
    elif name == "polygon":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        pts = []
        for i in range(6):
            ang = math.radians(60 * i)
            pts.append(QPointF(s/2 + (s/2 - pad) * math.cos(ang), s/2 + (s/2 - pad) * math.sin(ang)))
        p.drawPolygon(QPolygonF(pts))
        
    elif name == "pushpull":
        p.setPen(QPen(QColor("#0F172A"), 1.4))
        p.setBrush(QBrush(QColor("#E2E8F0")))
        p.drawPolygon([
            QPointF(s/2, pad + 4),
            QPointF(s - pad, pad + 8),
            QPointF(s/2, pad + 12),
            QPointF(pad, pad + 8)
        ])
        p.drawLine(QPointF(pad, pad + 8), QPointF(pad, s - pad))
        p.drawLine(QPointF(s/2, pad + 12), QPointF(s/2, s - pad + 3))
        p.drawLine(QPointF(s - pad, pad + 8), QPointF(s - pad, s - pad))
        p.drawLine(QPointF(pad, s - pad), QPointF(s/2, s - pad + 3))
        p.drawLine(QPointF(s/2, s - pad + 3), QPointF(s - pad, s - pad))
        p.setPen(QPen(QColor("#DC2626"), 2.2))
        p.drawLine(QPointF(s/2, pad + 7), QPointF(s/2, pad - 1))
        p.drawLine(QPointF(s/2, pad - 1), QPointF(s/2 - 2.5, pad + 2))
        p.drawLine(QPointF(s/2, pad - 1), QPointF(s/2 + 2.5, pad + 2))
        
    elif name == "move":
        p.setPen(QPen(QColor("#DC2626"), 2.0))
        cx, cy = s/2, s/2
        p.drawLine(QPointF(cx, pad), QPointF(cx, s - pad))
        p.drawLine(QPointF(pad, cy), QPointF(s - pad, cy))
        p.drawLine(QPointF(cx, pad), QPointF(cx - 2.5, pad + 3))
        p.drawLine(QPointF(cx, pad), QPointF(cx + 2.5, pad + 3))
        p.drawLine(QPointF(cx, s - pad), QPointF(cx - 2.5, s - pad - 3))
        p.drawLine(QPointF(cx, s - pad), QPointF(cx + 2.5, s - pad - 3))
        p.drawLine(QPointF(pad, cy), QPointF(pad + 3, cy - 2.5))
        p.drawLine(QPointF(pad, cy), QPointF(pad + 3, cy + 2.5))
        p.drawLine(QPointF(s - pad, cy), QPointF(s - pad - 3, cy - 2.5))
        p.drawLine(QPointF(s - pad, cy), QPointF(s - pad - 3, cy + 2.5))
        
    elif name == "rotate":
        p.setPen(QPen(QColor("#DC2626"), 2.0))
        p.drawArc(QRectF(pad, pad, s - 2*pad, s - 2*pad), 40 * 16, 280 * 16)
        p.drawLine(QPointF(s - pad, s/2), QPointF(s - pad + 3, s/2 - 3.5))
        p.drawLine(QPointF(s - pad, s/2), QPointF(s - pad - 3, s/2 - 3.5))
        
    elif name == "scale":
        p.setPen(QPen(QColor("#0F172A"), 1.4))
        p.drawRect(QRectF(pad + 2, pad + 2, s - 2*pad - 4, s - 2*pad - 4))
        p.setBrush(QBrush(QColor("#2563EB")))
        p.setPen(Qt.PenStyle.NoPen)
        for hx in (pad + 1, s - pad - 3):
            for hy in (pad + 1, s - pad - 3):
                p.drawRect(QRectF(hx, hy, 3.5, 3.5))
                
    elif name == "offset":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.drawRect(QRectF(pad, pad, s - 2*pad, s - 2*pad))
        p.setPen(QPen(QColor("#2563EB"), 1.6))
        p.drawRect(QRectF(pad + 3.5, pad + 3.5, s - 2*pad - 7, s - 2*pad - 7))
        
    elif name == "tape":
        p.setBrush(QBrush(QColor("#FBBF24")))
        p.setPen(QPen(QColor("#B45309"), 1.2))
        p.drawRoundedRect(QRectF(pad, pad + 3, s - 2*pad, s - 2*pad - 2), 2, 2)
        p.setPen(QPen(QColor("#0F172A"), 1.5))
        p.drawLine(QPointF(s - pad, s - pad + 1), QPointF(s - pad + 3, s - pad + 1))
        
    elif name == "protractor":
        p.setPen(QPen(QColor("#2563EB"), 1.8))
        p.drawArc(QRectF(pad, pad, s - 2*pad, s - 2*pad), 0, 180 * 16)
        p.drawLine(QPointF(pad, s/2), QPointF(s - pad, s/2))
        
    elif name == "axes_tool":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.drawLine(QPointF(pad + 3, s - pad - 3), QPointF(s - pad, s - pad - 3))
        p.setPen(QPen(QColor("#2563EB"), 1.8))
        p.drawLine(QPointF(pad + 3, s - pad - 3), QPointF(pad + 3, pad))
        p.setPen(QPen(QColor("#16A34A"), 1.8))
        p.drawLine(QPointF(pad + 3, s - pad - 3), QPointF(pad + 9, pad + 4))
        
    elif name == "dimension":
        p.setPen(QPen(QColor("#0F172A"), 1.4))
        p.drawLine(QPointF(pad, pad + 2), QPointF(pad, s - pad))
        p.drawLine(QPointF(s - pad, pad + 2), QPointF(s - pad, s - pad))
        p.drawLine(QPointF(pad, s/2), QPointF(s - pad, s/2))
        
    elif name == "text_tool":
        p.setPen(QPen(QColor("#0284C7"), 2.0))
        p.drawText(QRectF(pad, pad, s - 2*pad, s - 2*pad), Qt.AlignmentFlag.AlignCenter, "A")
        
    elif name == "text3d":
        p.setPen(QPen(QColor("#DC2626"), 1.8))
        p.drawText(QRectF(pad, pad, s - 2*pad, s - 2*pad), Qt.AlignmentFlag.AlignCenter, "3D")
        
    elif name == "paint":
        p.setBrush(QBrush(QColor("#3B82F6")))
        p.setPen(QPen(QColor("#1D4ED8"), 1.4))
        p.drawPolygon([
            QPointF(pad + 3, pad + 3),
            QPointF(s - pad - 3, pad + 1),
            QPointF(s - pad - 5, s - pad - 1),
            QPointF(pad + 1, s - pad - 1)
        ])
        p.setPen(QPen(QColor("#3B82F6"), 2.2))
        p.drawLine(QPointF(s - pad - 1, pad + 2), QPointF(s - pad + 2, s - pad))
        
    elif name == "orbit":
        p.setPen(QPen(QColor("#16A34A"), 2.2))
        p.drawArc(QRectF(pad, pad + 2, s - 2*pad, s - 2*pad - 4), 30 * 16, 120 * 16)
        p.setPen(QPen(QColor("#DC2626"), 2.2))
        p.drawArc(QRectF(pad, pad + 2, s - 2*pad, s - 2*pad - 4), 210 * 16, 120 * 16)
        
    elif name == "pan":
        p.setPen(QPen(QColor("#0284C7"), 1.8))
        p.setBrush(QBrush(QColor("#E0F2FE")))
        p.drawRoundedRect(QRectF(pad + 1, pad + 3, s - 2*pad - 2, s - 2*pad), 3, 3)
        p.drawLine(QPointF(pad + 4, pad + 3), QPointF(pad + 4, pad))
        p.drawLine(QPointF(pad + 7, pad + 3), QPointF(pad + 7, pad - 1))
        p.drawLine(QPointF(pad + 10, pad + 3), QPointF(pad + 10, pad))
        
    elif name == "zoom":
        p.setPen(QPen(QColor("#0284C7"), 2.0))
        p.drawEllipse(QRectF(pad, pad, s - 2*pad - 4, s - 2*pad - 4))
        p.drawLine(QPointF(s - pad - 5, s - pad - 5), QPointF(s - pad, s - pad))
        
    elif name == "zoom_extents":
        p.setPen(QPen(QColor("#0284C7"), 1.8))
        p.drawEllipse(QRectF(pad + 2, pad + 2, s - 2*pad - 4, s - 2*pad - 4))
        p.setPen(QPen(QColor("#DC2626"), 1.6))
        p.drawLine(QPointF(pad, pad), QPointF(pad + 4, pad))
        p.drawLine(QPointF(pad, pad), QPointF(pad, pad + 4))
        p.drawLine(QPointF(s - pad, pad), QPointF(s - pad - 4, pad))
        p.drawLine(QPointF(s - pad, pad), QPointF(s - pad, pad + 4))
        p.drawLine(QPointF(pad, s - pad), QPointF(pad + 4, s - pad))
        p.drawLine(QPointF(pad, s - pad), QPointF(pad, s - pad - 4))
        p.drawLine(QPointF(s - pad, s - pad), QPointF(s - pad - 4, s - pad))
        p.drawLine(QPointF(s - pad, s - pad), QPointF(s - pad, s - pad - 4))
        
    elif name == "view_iso":
        p.setPen(QPen(QColor("#0F172A"), 1.6))
        p.setBrush(QBrush(QColor("#E2E8F0")))
        p.drawPolygon([
            QPointF(s/2, pad),
            QPointF(s - pad, pad + 5),
            QPointF(s/2, pad + 9),
            QPointF(pad, pad + 5)
        ])
        p.drawRect(QRectF(pad, pad + 5, s - 2*pad, s - 2*pad - 5))
        
    elif name == "view_top":
        p.setPen(QPen(QColor("#0F172A"), 1.6))
        p.setBrush(QBrush(QColor("#CBD5E1")))
        p.drawRect(QRectF(pad + 2, pad + 2, s - 2*pad - 4, s - 2*pad - 4))
        p.drawLine(QPointF(pad + 2, pad + 2), QPointF(s - pad - 2, s - pad - 2))
        
    elif name == "view_front":
        p.setPen(QPen(QColor("#0F172A"), 1.6))
        p.setBrush(QBrush(QColor("#E2E8F0")))
        p.drawPolygon([
            QPointF(pad + 2, pad + 7),
            QPointF(s/2, pad + 2),
            QPointF(s - pad - 2, pad + 7)
        ])
        p.drawRect(QRectF(pad + 2, pad + 7, s - 2*pad - 4, s - 2*pad - 7))
        
    elif name == "style_wireframe":
        p.setPen(QPen(QColor("#0F172A"), 1.6))
        p.drawRect(QRectF(pad, pad + 3, s - 2*pad, s - 2*pad - 3))
        p.drawLine(QPointF(pad, pad + 3), QPointF(s - pad, s - pad))
        
    elif name == "style_shaded":
        p.setBrush(QBrush(QColor("#93C5FD")))
        p.setPen(QPen(QColor("#1E3A8A"), 1.4))
        p.drawPolygon([
            QPointF(pad, pad + 4),
            QPointF(s/2, pad),
            QPointF(s - pad, pad + 4),
            QPointF(s - pad, s - pad),
            QPointF(pad, s - pad)
        ])
        
    elif name == "style_xray":
        p.setBrush(QBrush(QColor(147, 197, 253, 100)))
        p.setPen(QPen(QColor("#2563EB"), 1.4, Qt.PenStyle.DashLine))
        p.drawRect(QRectF(pad, pad, s - 2*pad, s - 2*pad))
        
    elif name == "shadows":
        p.setBrush(QBrush(QColor("#F59E0B")))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(pad, pad, 9, 9))
        p.setPen(QPen(QColor("#64748B"), 2.2))
        p.drawLine(QPointF(pad + 4, s - pad - 1), QPointF(s - pad, s - pad - 1))
        
    elif name == "warehouse":
        p.setBrush(QBrush(QColor("#0284C7")))
        p.drawRect(QRectF(pad, pad + 3, s - 2*pad, s - 2*pad - 3))
        p.setPen(QPen(QColor("#FFFFFF"), 1.6))
        p.drawLine(QPointF(s/2, pad + 5), QPointF(s/2, s - pad - 2))
        p.drawLine(QPointF(s/2 - 3, s - pad - 5), QPointF(s/2, s - pad - 2))
        p.drawLine(QPointF(s/2 + 3, s - pad - 5), QPointF(s/2, s - pad - 2))
        
    else:
        p.setPen(QPen(QColor("#64748B"), 1.6))
        p.drawRect(QRectF(pad, pad, s - 2*pad, s - 2*pad))
        
    p.end()
    return QIcon(pix)


# -----------------------------------------------------------------------------
# 3D Viewport with Exact Vertical Blue Axis & Calibrated Perspective
# -----------------------------------------------------------------------------
class Viewport3D(QWidget):
    """
    3D Viewport reproducing the camera angle, sky, ground, coordinate axes,
    and scale human figure from SketchUp 2026.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # In SketchUp, camera target is exactly along the Z axis (0, 0, Z),
        # which guarantees the Blue Z-axis is 100% perpendicular vertical!
        self.yaw = -36.0
        self.pitch = 22.0
        self.distance = 9.2
        self.target = [0.0, 0.0, 0.85]
        
        # Modeling states
        self.active_tool = "select"
        self.is_dragging = False
        self.last_mouse_pos = QPoint()
        self.draw_start_point = None
        self.current_cursor_point = None
        
        # Display modes
        self.show_shadows = True
        self.shadow_time = 14.5
        self.display_mode = "shaded"
        self.current_material_color = QColor("#93C5FD")
        
        # Scene objects (Empty by default matching picture-1.png)
        self.objects = []
        
        self.update()

    def set_tool(self, tool_name):
        self.active_tool = tool_name
        self.draw_start_point = None
        self.update()

    def set_display_mode(self, mode):
        self.display_mode = mode
        self.update()

    def set_shadows(self, enabled):
        self.show_shadows = enabled
        self.update()

    def set_shadow_time(self, hour):
        self.shadow_time = hour
        self.update()

    def reset_view(self, view_name="iso"):
        if view_name == "iso":
            self.yaw = -36.0
            self.pitch = 22.0
        elif view_name == "top":
            self.yaw = 0.0
            self.pitch = 89.9
        elif view_name == "front":
            self.yaw = 0.0
            self.pitch = 0.0
        elif view_name == "right":
            self.yaw = 90.0
            self.pitch = 0.0
        elif view_name == "back":
            self.yaw = 180.0
            self.pitch = 0.0
        elif view_name == "left":
            self.yaw = -90.0
            self.pitch = 0.0
        self.update()

    def project_3d(self, x, y, z):
        w = self.width()
        h = self.height()
        
        # Origin (0,0,0) sits at ~27.8% from the left, ~71.2% from the top
        cx = w * 0.278
        cy = h * 0.712
        
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)
        
        # Relative to target
        rx = x - self.target[0]
        ry = y - self.target[1]
        rz = z - self.target[2]
        
        # Yaw rotation around Z
        x1 = rx * math.cos(rad_yaw) - ry * math.sin(rad_yaw)
        y1 = rx * math.sin(rad_yaw) + ry * math.cos(rad_yaw)
        z1 = rz
        
        # Pitch rotation around X
        x2 = x1
        y2 = y1 * math.cos(rad_pitch) - z1 * math.sin(rad_pitch)
        z2 = y1 * math.sin(rad_pitch) + z1 * math.cos(rad_pitch)
        
        depth = y2 + self.distance
        if depth <= 0.2:
            depth = 0.2
            
        scale = (h * 1.5) / depth
        
        screen_x = cx + x2 * scale
        screen_y = cy - z2 * scale
        
        return QPointF(screen_x, screen_y), depth

    def unproject_ground(self, screen_x, screen_y):
        w = self.width()
        h = self.height()
        cx = w * 0.278
        cy = h * 0.712
        scale = h * 1.5
        
        dx = (screen_x - cx) / scale
        dz = -(screen_y - cy) / scale
        
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)
        
        rx, ry, rz = dx, 1.0, dz
        rx2 = rx
        ry2 = ry * math.cos(-rad_pitch) - rz * math.sin(-rad_pitch)
        rz2 = ry * math.sin(-rad_pitch) + rz * math.cos(-rad_pitch)
        
        rx3 = rx2 * math.cos(-rad_yaw) - ry2 * math.sin(-rad_yaw)
        ry3 = rx2 * math.sin(-rad_yaw) + ry2 * math.cos(-rad_yaw)
        rz3 = rz2
        
        cam_p2 = [0, -self.distance * math.cos(-rad_pitch), -self.distance * math.sin(-rad_pitch)]
        cam_world = [
            cam_p2[0] * math.cos(-rad_yaw) - cam_p2[1] * math.sin(-rad_yaw) + self.target[0],
            cam_p2[0] * math.sin(-rad_yaw) + cam_p2[1] * math.cos(-rad_yaw) + self.target[1],
            cam_p2[2] + self.target[2]
        ]
        
        if abs(rz3) < 1e-4:
            return 0.0, 0.0
        t = -cam_world[2] / rz3
        if t < 0:
            return 0.0, 0.0
            
        gx = cam_world[0] + rx3 * t
        gy = cam_world[1] + ry3 * t
        return gx, gy

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Horizon height: 30% from top
        horizon_y = h * 0.30
        
        # Sky: Sky blue
        sky_grad = QLinearGradient(0, 0, 0, horizon_y)
        sky_grad.setColorAt(0.0, QColor("#8ED0F9"))
        sky_grad.setColorAt(1.0, QColor("#BBE4FA"))
        p.fillRect(0, 0, w, int(horizon_y), sky_grad)
        
        # Ground: Neutral warm gray
        ground_grad = QLinearGradient(0, horizon_y, 0, h)
        ground_grad.setColorAt(0.0, QColor("#C7C7C7"))
        ground_grad.setColorAt(1.0, QColor("#BEBEBE"))
        p.fillRect(0, int(horizon_y), w, h - int(horizon_y), ground_grad)
        
        # Horizon line
        p.setPen(QPen(QColor("#A8A8A8"), 1.0))
        p.drawLine(0, int(horizon_y), w, int(horizon_y))
        
        # Draw 3D Axes
        self._draw_axes(p)
        
        # Draw Sun Shadows
        if self.show_shadows:
            self._draw_shadows(p)
            
        # Draw 2D Billboard Scale Woman Figure (matching picture-1.png)
        self._draw_scale_woman(p)
        
        # Draw 3D Objects
        self._draw_objects(p)
        
        # Draw Active Feedback
        self._draw_drawing_feedback(p)
        
        p.end()

    def _draw_axes(self, p):
        axis_len = 16.0
        origin_pt, _ = self.project_3d(0, 0, 0)
        
        # Negative dashed axes
        dashed_pen = QPen(Qt.PenStyle.DotLine)
        dashed_pen.setWidthF(1.0)
        
        # -X (Red negative)
        dashed_pen.setColor(QColor("#DC2626"))
        p.setPen(dashed_pen)
        pt_neg_x, _ = self.project_3d(-axis_len, 0, 0)
        p.drawLine(origin_pt, pt_neg_x)
        
        # -Y (Green negative)
        dashed_pen.setColor(QColor("#16A34A"))
        p.setPen(dashed_pen)
        pt_neg_y, _ = self.project_3d(0, -axis_len, 0)
        p.drawLine(origin_pt, pt_neg_y)
        
        # -Z (Blue negative)
        dashed_pen.setColor(QColor("#2563EB"))
        p.setPen(dashed_pen)
        pt_neg_z, _ = self.project_3d(0, 0, -axis_len)
        p.drawLine(origin_pt, pt_neg_z)
        
        # Positive solid axes
        solid_pen = QPen(Qt.PenStyle.SolidLine)
        solid_pen.setWidthF(1.2)
        
        # +Z Axis (Blue: perfectly vertical)
        solid_pen.setColor(QColor("#1D4ED8"))
        p.setPen(solid_pen)
        pt_pos_z, _ = self.project_3d(0, 0, axis_len)
        p.drawLine(origin_pt, pt_pos_z)
        
        # +Y Axis (Green: up-right)
        solid_pen.setColor(QColor("#15803D"))
        p.setPen(solid_pen)
        pt_pos_y, _ = self.project_3d(0, axis_len, 0)
        p.drawLine(origin_pt, pt_pos_y)
        
        # +X Axis (Red: down-right)
        solid_pen.setColor(QColor("#DC2626"))
        p.setPen(solid_pen)
        pt_pos_x, _ = self.project_3d(axis_len, 0, 0)
        p.drawLine(origin_pt, pt_pos_x)

    def _draw_scale_woman(self, p):
        """Draw the iconic SketchUp 2D billboard woman figure as in picture-1.png."""
        # She stands at (-0.35, 0.15, 0.0), slightly left of the vertical blue axis
        feet_pt, _ = self.project_3d(-0.35, 0.15, 0.0)
        head_pt, _ = self.project_3d(-0.35, 0.15, 1.68)
        
        h = feet_pt.y() - head_pt.y()
        if h <= 15:
            return
            
        w = h * 0.32
        x = feet_pt.x() - w / 2.0
        y = head_pt.y()
        
        # Ground shadow
        p.setBrush(QBrush(QColor(0, 0, 0, 55)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(feet_pt.x() - w * 0.45, feet_pt.y() - h * 0.03, w * 0.9, h * 0.06))
        
        # Hair (Dark brownish-black, parted down middle framing face)
        p.setBrush(QBrush(QColor("#1C1917")))
        p.setPen(QPen(QColor("#0C0A09"), 1.2))
        hair_path = QPainterPath()
        hair_path.moveTo(x + w * 0.30, y + h * 0.12)
        hair_path.cubicTo(x + w * 0.28, y, x + w * 0.72, y, x + w * 0.70, y + h * 0.12)
        hair_path.lineTo(x + w * 0.74, y + h * 0.22)
        hair_path.lineTo(x + w * 0.64, y + h * 0.20)
        hair_path.lineTo(x + w * 0.60, y + h * 0.10)
        hair_path.lineTo(x + w * 0.40, y + h * 0.10)
        hair_path.lineTo(x + w * 0.36, y + h * 0.20)
        hair_path.lineTo(x + w * 0.26, y + h * 0.22)
        hair_path.closeSubpath()
        p.drawPath(hair_path)
        
        # Face / Neck
        p.setBrush(QBrush(QColor("#FCD34D")))
        p.setPen(QPen(QColor("#B45309"), 1.0))
        face_rect = QRectF(x + w * 0.38, y + h * 0.05, w * 0.24, h * 0.09)
        p.drawRoundedRect(face_rect, 3, 3)
        
        # Sleeveless Charcoal / Navy Dress
        p.setBrush(QBrush(QColor("#1E293B")))
        p.setPen(QPen(QColor("#0F172A"), 1.2))
        dress_path = QPainterPath()
        dress_path.moveTo(x + w * 0.32, y + h * 0.14)
        dress_path.lineTo(x + w * 0.68, y + h * 0.14)
        dress_path.lineTo(x + w * 0.82, y + h * 0.74)
        dress_path.lineTo(x + w * 0.18, y + h * 0.74)
        dress_path.closeSubpath()
        p.drawPath(dress_path)
        
        # Portfolio folder in hands
        p.setBrush(QBrush(QColor("#F1F5F9")))
        p.setPen(QPen(QColor("#64748B"), 1.2))
        folder_rect = QRectF(x + w * 0.34, y + h * 0.32, w * 0.32, h * 0.15)
        p.drawRoundedRect(folder_rect, 2, 2)
        
        # Arms
        p.setBrush(QBrush(QColor("#FCD34D")))
        p.setPen(QPen(QColor("#B45309"), 1.0))
        p.drawRect(QRectF(x + w * 0.22, y + h * 0.16, w * 0.12, h * 0.22))
        p.drawRect(QRectF(x + w * 0.66, y + h * 0.16, w * 0.12, h * 0.22))
        
        # Legs
        p.drawRect(QRectF(x + w * 0.36, y + h * 0.74, w * 0.10, h * 0.19))
        p.drawRect(QRectF(x + w * 0.54, y + h * 0.74, w * 0.10, h * 0.19))
        
        # Black heels
        p.setBrush(QBrush(QColor("#0F172A")))
        p.setPen(QPen(QColor("#000000"), 1.0))
        p.drawRect(QRectF(x + w * 0.32, y + h * 0.93, w * 0.15, h * 0.05))
        p.drawRect(QRectF(x + w * 0.52, y + h * 0.93, w * 0.15, h * 0.05))

    def _draw_shadows(self, p):
        hour_rad = math.radians((self.shadow_time - 12.0) * 15.0)
        sun_dx = math.sin(hour_rad) * 1.5
        sun_dy = -math.cos(hour_rad) * 1.2
        
        p.setBrush(QBrush(QColor(0, 0, 0, 40)))
        p.setPen(Qt.PenStyle.NoPen)
        
        for obj in self.objects:
            if obj["type"] == "box":
                x, y, dx, dy, dz = obj["x"], obj["y"], obj["dx"], obj["dy"], obj["dz"]
                p0, _ = self.project_3d(x, y, 0)
                p1, _ = self.project_3d(x + dx, y, 0)
                s1, _ = self.project_3d(x + dx + sun_dx * dz, y + dy + sun_dy * dz, 0)
                s3, _ = self.project_3d(x + sun_dx * dz, y + dy + sun_dy * dz, 0)
                p3, _ = self.project_3d(x, y + dy, 0)
                p.drawPolygon(QPolygonF([p0, p1, s1, s3, p3]))

    def _draw_objects(self, p):
        for obj in self.objects:
            if obj["type"] == "box":
                self._draw_box(p, obj)

    def _draw_box(self, p, box):
        x, y, z = box["x"], box["y"], box["z"]
        dx, dy, dz = box["dx"], box["dy"], box["dz"]
        
        v0, d0 = self.project_3d(x, y, z)
        v1, d1 = self.project_3d(x + dx, y, z)
        v2, d2 = self.project_3d(x + dx, y + dy, z)
        v3, d3 = self.project_3d(x, y + dy, z)
        v4, d4 = self.project_3d(x, y, z + dz)
        v5, d5 = self.project_3d(x + dx, y, z + dz)
        v6, d6 = self.project_3d(x + dx, y + dy, z + dz)
        v7, d7 = self.project_3d(x, y + dy, z + dz)
        
        faces = [
            {"pts": [v4, v5, v6, v7], "depth": (d4 + d5 + d6 + d7)/4.0, "shade": 1.15},
            {"pts": [v0, v1, v5, v4], "depth": (d0 + d1 + d5 + d4)/4.0, "shade": 0.95},
            {"pts": [v1, v2, v6, v5], "depth": (d1 + d2 + d6 + d5)/4.0, "shade": 0.85},
            {"pts": [v2, v3, v7, v6], "depth": (d2 + d3 + d7 + d6)/4.0, "shade": 0.75},
            {"pts": [v3, v0, v4, v7], "depth": (d3 + d0 + d4 + d7)/4.0, "shade": 0.90},
            {"pts": [v0, v3, v2, v1], "depth": (d0 + d3 + d2 + d1)/4.0, "shade": 0.65},
        ]
        faces.sort(key=lambda f: f["depth"], reverse=True)
        
        base_color = box["color"]
        edge_pen = QPen(QColor("#0F172A"), 1.2)
        
        for f in faces:
            poly = QPolygonF(f["pts"])
            if self.display_mode == "wireframe":
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(edge_pen)
                p.drawPolygon(poly)
            elif self.display_mode == "hidden_line":
                p.setBrush(QBrush(QColor("#FFFFFF")))
                p.setPen(edge_pen)
                p.drawPolygon(poly)
            else:
                shade = f["shade"]
                r = min(255, int(base_color.red() * shade))
                g = min(255, int(base_color.green() * shade))
                b = min(255, int(base_color.blue() * shade))
                p.setBrush(QBrush(QColor(r, g, b)))
                p.setPen(edge_pen)
                p.drawPolygon(poly)

    def _draw_drawing_feedback(self, p):
        if self.active_tool == "rect" and self.draw_start_point and self.current_cursor_point:
            sx, sy = self.draw_start_point
            cx, cy = self.current_cursor_point
            p0, _ = self.project_3d(sx, sy, 0)
            p1, _ = self.project_3d(cx, sy, 0)
            p2, _ = self.project_3d(cx, cy, 0)
            p3, _ = self.project_3d(sx, cy, 0)
            p.setBrush(QBrush(QColor(147, 197, 253, 90)))
            p.setPen(QPen(QColor("#0284C7"), 1.8, Qt.PenStyle.DashLine))
            p.drawPolygon(QPolygonF([p0, p1, p2, p3]))
            
        elif self.active_tool == "line" and self.draw_start_point and self.current_cursor_point:
            sx, sy = self.draw_start_point
            cx, cy = self.current_cursor_point
            p0, _ = self.project_3d(sx, sy, 0)
            p1, _ = self.project_3d(cx, cy, 0)
            p.setPen(QPen(QColor("#DC2626"), 2.0))
            p.drawLine(p0, p1)

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
        self.is_dragging = True
        
        if event.button() == Qt.MouseButton.LeftButton:
            gx, gy = self.unproject_ground(event.pos().x(), event.pos().y())
            if self.active_tool in ("rect", "line"):
                self.draw_start_point = (gx, gy)
                self.current_cursor_point = (gx, gy)
            elif self.active_tool == "eraser":
                self.objects = [b for b in self.objects if not (b["x"] <= gx <= b["x"] + b["dx"] and b["y"] <= gy <= b["y"] + b["dy"])]
                self.update()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.last_mouse_pos = event.pos()
        
        if (event.buttons() & Qt.MouseButton.MiddleButton) or (self.is_dragging and self.active_tool == "orbit"):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier or self.active_tool == "pan":
                factor = 0.01 * (self.distance / 5.0)
                self.target[0] -= delta.x() * factor
                self.target[1] += delta.y() * factor
            else:
                self.yaw += delta.x() * 0.4
                self.pitch += delta.y() * 0.4
                self.pitch = max(-89.9, min(89.9, self.pitch))
            self.update()
            return
            
        if self.draw_start_point:
            gx, gy = self.unproject_ground(event.pos().x(), event.pos().y())
            self.current_cursor_point = (gx, gy)
            dx = abs(gx - self.draw_start_point[0])
            dy = abs(gy - self.draw_start_point[1])
            window = self.window()
            if hasattr(window, "update_measurements"):
                window.update_measurements(f"{dx:.2f}m; {dy:.2f}m")
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        if event.button() == Qt.MouseButton.LeftButton:
            if self.active_tool == "rect" and self.draw_start_point and self.current_cursor_point:
                sx, sy = self.draw_start_point
                cx, cy = self.current_cursor_point
                min_x, max_x = min(sx, cx), max(sx, cx)
                min_y, max_y = min(sy, cy), max(sy, cy)
                dx = max_x - min_x
                dy = max_y - min_y
                if dx > 0.1 and dy > 0.1:
                    box_id = len(self.objects)
                    self.objects.append({
                        "id": box_id,
                        "type": "box",
                        "x": min_x, "y": min_y, "z": 0.0,
                        "dx": dx, "dy": dy, "dz": 1.4,
                        "color": self.current_material_color
                    })
                self.draw_start_point = None
                self.current_cursor_point = None
                self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.distance *= 0.90
        else:
            self.distance *= 1.10
        self.distance = max(0.5, min(100.0, self.distance))
        self.update()


# -----------------------------------------------------------------------------
# Collapsible Accordion Section
# -----------------------------------------------------------------------------
class AccordionSection(QWidget):
    def __init__(self, title, content_widget, is_expanded=True, parent=None):
        super().__init__(parent)
        self.is_expanded = is_expanded
        self.content_widget = content_widget
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header_bar = QWidget()
        hb_layout = QHBoxLayout(header_bar)
        hb_layout.setContentsMargins(4, 3, 4, 3)
        hb_layout.setSpacing(4)
        header_bar.setStyleSheet("""
            QWidget {
                background-color: #F1F5F9;
                border: 1px solid #CBD5E1;
                border-radius: 2px;
            }
        """)
        
        self.header_btn = QToolButton(header_bar)
        self.header_btn.setStyleSheet("border: none; font-weight: 500; font-size: 11px; color: #1E293B; text-align: left;")
        self.header_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.title_text = title
        self._update_header_text()
        self.header_btn.clicked.connect(self.toggle)
        hb_layout.addWidget(self.header_btn)
        
        x_btn = QToolButton(header_bar)
        x_btn.setText("×")
        x_btn.setStyleSheet("border: none; font-size: 12px; color: #64748B; font-weight: bold;")
        hb_layout.addWidget(x_btn)
        
        layout.addWidget(header_bar)
        
        # Content frame
        self.content_frame = QFrame(self)
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-left: 1px solid #CBD5E1;
                border-right: 1px solid #CBD5E1;
                border-bottom: 1px solid #CBD5E1;
                padding: 4px;
            }
        """)
        cf_layout = QVBoxLayout(self.content_frame)
        cf_layout.setContentsMargins(6, 6, 6, 6)
        cf_layout.addWidget(self.content_widget)
        layout.addWidget(self.content_frame)
        
        self.content_frame.setVisible(self.is_expanded)

    def _update_header_text(self):
        arrow = "∨ " if self.is_expanded else "› "
        self.header_btn.setText(arrow + self.title_text)

    def toggle(self):
        self.is_expanded = not self.is_expanded
        self.content_frame.setVisible(self.is_expanded)
        self._update_header_text()


# -----------------------------------------------------------------------------
# Main Application Window
# -----------------------------------------------------------------------------
class SketchCraftWindow(QMainWindow):
    def __init__(self, screenshot_path=None):
        super().__init__()
        self.screenshot_path = screenshot_path
        self.setWindowTitle("Sem nome* - SketchUp 2026")
        self.resize(1920, 1040)
        
        self.setStyleSheet(STYLE_SHEET)
        
        # Central Viewport
        self.viewport = Viewport3D(self)
        
        # Create UI
        self._create_menus()
        self._create_toolbars()
        self._create_right_tray()
        self._create_status_bar()
        
        # Central layout
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Mini vertical toolbar on the left (Zoom +/-)
        left_tb = QToolBar("Navegação Lateral", self)
        left_tb.setOrientation(Qt.Orientation.Vertical)
        left_tb.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; padding: 2px;")
        
        z_in = left_tb.addAction(make_icon("zoom", 18), "Zoom Mais")
        z_in.triggered.connect(lambda: self.viewport.wheelEvent(type("E", (), {"angleDelta": lambda: type("D", (), {"y": lambda: 120})()})()))
        
        z_out = left_tb.addAction(make_icon("zoom_extents", 18), "Zoom Menos")
        z_out.triggered.connect(lambda: self.viewport.wheelEvent(type("E", (), {"angleDelta": lambda: type("D", (), {"y": lambda: -120})()})()))
        
        main_layout.addWidget(left_tb)
        
        splitter = QSplitter(Qt.Orientation.Horizontal, main_widget)
        splitter.addWidget(self.viewport)
        splitter.addWidget(self.tray_widget)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([1560, 340])
        
        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)
        
        if self.screenshot_path:
            QTimer.singleShot(900, self._capture_screenshot)

    def _capture_screenshot(self):
        print(f"Capturing screenshot to {self.screenshot_path}...")
        os.makedirs(os.path.dirname(os.path.abspath(self.screenshot_path)), exist_ok=True)
        pix = self.grab()
        pix.save(self.screenshot_path, "PNG")
        print("Screenshot captured successfully!")
        QApplication.quit()

    def _create_menus(self):
        mb = self.menuBar()
        def add(m, txt, sc=None, slot=None):
            a = m.addAction(txt)
            if sc: a.setShortcut(sc)
            if slot: a.triggered.connect(slot)
            return a
            
        m_arq = mb.addMenu("Arquivo")
        add(m_arq, "Novo", QKeySequence.StandardKey.New)
        add(m_arq, "Abrir...", QKeySequence.StandardKey.Open)
        add(m_arq, "Salvar", QKeySequence.StandardKey.Save)
        add(m_arq, "Salvar como...", QKeySequence.StandardKey.SaveAs)
        m_arq.addSeparator()
        add(m_arq, "Importar...")
        add(m_arq, "Exportar...")
        m_arq.addSeparator()
        add(m_arq, "Imprimir...", QKeySequence.StandardKey.Print)
        m_arq.addSeparator()
        add(m_arq, "Sair", QKeySequence.StandardKey.Quit, self.close)
        
        m_edt = mb.addMenu("Editar")
        add(m_edt, "Desfazer", QKeySequence.StandardKey.Undo)
        add(m_edt, "Refazer", QKeySequence.StandardKey.Redo)
        m_edt.addSeparator()
        add(m_edt, "Recortar", QKeySequence.StandardKey.Cut)
        add(m_edt, "Copiar", QKeySequence.StandardKey.Copy)
        add(m_edt, "Colar", QKeySequence.StandardKey.Paste)
        add(m_edt, "Excluir", QKeySequence.StandardKey.Delete)
        m_edt.addSeparator()
        add(m_edt, "Selecionar tudo", QKeySequence.StandardKey.SelectAll)
        
        m_vis = mb.addMenu("Visualizar")
        add(m_vis, "Barras de ferramentas...")
        add(m_vis, "Bandeja padrão")
        m_vis.addSeparator()
        add(m_vis, "Eixos")
        add(m_vis, "Sombras", slot=lambda: self.viewport.set_shadows(not self.viewport.show_shadows))
        
        m_cam = mb.addMenu("Câmera")
        add(m_cam, "Extensão da câmera (Zoom Extents)", slot=lambda: self.viewport.reset_view("iso"))
        m_views = m_cam.addMenu("Exibições padrão")
        add(m_views, "Isométrica", slot=lambda: self.viewport.reset_view("iso"))
        add(m_views, "Alto (Top)", slot=lambda: self.viewport.reset_view("top"))
        add(m_views, "Frente (Front)", slot=lambda: self.viewport.reset_view("front"))
        add(m_views, "Direita (Right)", slot=lambda: self.viewport.reset_view("right"))
        add(m_views, "Trás (Back)", slot=lambda: self.viewport.reset_view("back"))
        add(m_views, "Esquerda (Left)", slot=lambda: self.viewport.reset_view("left"))
        
        m_des = mb.addMenu("Desenho")
        add(m_des, "Linhas", slot=lambda: self.set_active_tool("line"))
        add(m_des, "Retângulo", slot=lambda: self.set_active_tool("rect"))
        add(m_des, "Círculo", slot=lambda: self.set_active_tool("circle"))
        add(m_des, "Arco", slot=lambda: self.set_active_tool("arc"))
        
        m_fer = mb.addMenu("Ferramentas")
        add(m_fer, "Selecionar", slot=lambda: self.set_active_tool("select"))
        add(m_fer, "Borracha", slot=lambda: self.set_active_tool("eraser"))
        add(m_fer, "Pintura", slot=lambda: self.set_active_tool("paint"))
        add(m_fer, "Empurrar/Puxar", slot=lambda: self.set_active_tool("pushpull"))
        add(m_fer, "Mover", slot=lambda: self.set_active_tool("move"))
        add(m_fer, "Girar", slot=lambda: self.set_active_tool("rotate"))
        add(m_fer, "Escala", slot=lambda: self.set_active_tool("scale"))
        add(m_fer, "Fita métrica", slot=lambda: self.set_active_tool("tape"))
        
        mb.addMenu("Janela")
        mb.addMenu("Extensões")
        mb.addMenu("Ajuda")

    def _create_toolbars(self):
        # Toolbar 1: Standard & Views & Styles
        tb1 = QToolBar("Padrão", self)
        tb1.setIconSize(QSize(20, 20))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tb1)
        
        for name, icon_id in [
            ("Novo", "rect"), ("Abrir", "view_top"), ("Salvar", "view_iso"),
            ("Recortar", "eraser"), ("Copiar", "rect"), ("Colar", "select"),
            ("Desfazer", "rotate"), ("Refazer", "rotate")
        ]:
            tb1.addAction(make_icon(icon_id), name)
            
        tb1.addSeparator()
        
        for tid, iid, tip in [
            ("move", "move", "Mover (M)"),
            ("pushpull", "pushpull", "Empurrar/Puxar (P)"),
            ("rotate", "rotate", "Girar (Q)"),
            ("scale", "scale", "Escala (S)"),
            ("offset", "offset", "Equidistância (F)"),
            ("tape", "tape", "Fita Métrica (T)"),
            ("protractor", "protractor", "Transferidor"),
            ("axes", "axes_tool", "Eixos"),
            ("dimension", "dimension", "Dimensões"),
            ("text", "text_tool", "Texto"),
            ("text3d", "text3d", "Texto 3D"),
        ]:
            b = QToolButton(self)
            b.setIcon(make_icon(iid))
            b.setToolTip(tip)
            b.clicked.connect(lambda ch, t=tid: self.set_active_tool(t))
            tb1.addWidget(b)
            
        tb1.addSeparator()
        
        cb = QComboBox(self)
        cb.addItems(["✓ Sem etiquetas", "  Paredes", "  Mobiliário", "  Telhado"])
        cb.setFixedWidth(130)
        tb1.addWidget(cb)
        
        tb1.addSeparator()
        
        for vname, tip in [
            ("iso", "Isométrica"), ("top", "Alto (Top)"), ("front", "Frente"),
            ("right", "Direita"), ("back", "Trás"), ("left", "Esquerda")
        ]:
            b = QToolButton(self)
            b.setIcon(make_icon(f"view_{vname}" if vname in ("iso", "top", "front") else "view_iso"))
            b.setToolTip(tip)
            b.clicked.connect(lambda ch, v=vname: self.viewport.reset_view(v))
            tb1.addWidget(b)
            
        tb1.addSeparator()
        
        for sname, iid, tip in [
            ("xray", "style_xray", "Raio-X"),
            ("wireframe", "style_wireframe", "Aramado"),
            ("hidden_line", "rect", "Linhas Ocultas"),
            ("shaded", "style_shaded", "Sombreado"),
        ]:
            b = QToolButton(self)
            b.setIcon(make_icon(iid))
            b.setToolTip(tip)
            b.clicked.connect(lambda ch, s=sname: self.viewport.set_display_mode(s))
            tb1.addWidget(b)
            
        tb1.addSeparator()
        
        b_sh = QToolButton(self)
        b_sh.setIcon(make_icon("shadows"))
        b_sh.setCheckable(True)
        b_sh.setChecked(True)
        b_sh.toggled.connect(self.viewport.set_shadows)
        tb1.addWidget(b_sh)
        
        tb1.addSeparator()
        
        b_wh = QToolButton(self)
        b_wh.setIcon(make_icon("warehouse"))
        b_wh.setToolTip("3D Warehouse")
        tb1.addWidget(b_wh)
        
        # Toolbar 2: Large Toolset matching picture-1.png
        self.addToolBarBreak()
        tb2 = QToolBar("Conjunto de Ferramentas", self)
        tb2.setIconSize(QSize(20, 20))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tb2)
        
        self.tool_buttons = {}
        tools_list = [
            ("select", "select", "Selecionar (Espaço)"),
            ("eraser", "eraser", "Borracha (E)"),
            ("line", "line", "Linha (L)"),
            ("freehand", "freehand", "Mão Livre"),
            ("arc", "arc", "Arco 2 Pontos (A)"),
            ("arc3", "arc3", "Arco 3 Pontos"),
            ("pie", "pie", "Pizza"),
            ("rect", "rect", "Retângulo (R)"),
            ("rect_rot", "rect_rot", "Retângulo Girado"),
            ("circle", "circle", "Círculo (C)"),
            ("polygon", "polygon", "Polígono"),
            ("paint", "paint", "Pintura (B)"),
            ("orbit", "orbit", "Órbita (O)"),
            ("pan", "pan", "Panorâmica (H)"),
            ("zoom", "zoom", "Zoom (Z)"),
            ("zoom_extents", "zoom_extents", "Modelo Centralizado (Shift+Z)"),
        ]
        
        for tid, iid, tip in tools_list:
            b = QToolButton(self)
            b.setIcon(make_icon(iid))
            b.setToolTip(tip)
            b.setCheckable(True)
            if tid == "select":
                b.setChecked(True)
            b.clicked.connect(lambda ch, t=tid: self.set_active_tool(t))
            tb2.addWidget(b)
            self.tool_buttons[tid] = b

    def set_active_tool(self, tool_id):
        self.viewport.set_tool(tool_id)
        for tid, btn in self.tool_buttons.items():
            btn.setChecked(tid == tool_id)
            
        tips = {
            "select": "Clique ou arraste para selecionar objetos. Shift = Adicionar/Subtrair. Ctrl = Adicionar. Shift + Ctrl = Subtrair.",
            "eraser": "Clique ou arraste sobre arestas ou superfícies para apagar.",
            "line": "Clique para o primeiro ponto, mova o cursor e clique para o ponto final.",
            "rect": "Clique para o primeiro canto, mova o cursor e clique para o canto oposto.",
            "circle": "Clique para o centro e mova o cursor para definir o raio.",
            "arc": "Clique para o ponto inicial, ponto final e curvatura.",
            "paint": "Clique em uma face para aplicar o material selecionado.",
            "orbit": "Arraste para girar a câmera em torno do modelo.",
            "pan": "Arraste para mover a câmera paralelamente ao plano de visão.",
            "zoom": "Arraste para aumentar ou diminuir o zoom.",
            "zoom_extents": "Centraliza todo o modelo no campo de visão.",
        }
        self.status_label.setText(tips.get(tool_id, "Pronto."))

    def _create_right_tray(self):
        self.tray_widget = QWidget(self)
        self.tray_widget.setStyleSheet("background-color: #F8FAFC;")
        tray_layout = QVBoxLayout(self.tray_widget)
        tray_layout.setContentsMargins(4, 4, 4, 4)
        tray_layout.setSpacing(4)
        
        # Tray Header
        hb = QWidget()
        hbl = QHBoxLayout(hb)
        hbl.setContentsMargins(4, 2, 4, 2)
        tl = QLabel("Bandeja padrão", hb)
        tl.setStyleSheet("font-weight: bold; font-size: 12px; color: #0F172A;")
        hbl.addWidget(tl)
        hbl.addStretch()
        
        pin = QToolButton(hb)
        pin.setText("📌")
        pin.setStyleSheet("border: none; font-size: 11px;")
        hbl.addWidget(pin)
        
        cl = QToolButton(hb)
        cl.setText("✕")
        cl.setStyleSheet("border: none; font-size: 11px; font-weight: bold;")
        cl.clicked.connect(lambda: self.tray_widget.setVisible(False))
        hbl.addWidget(cl)
        tray_layout.addWidget(hb)
        
        # Scroll Area for Accordions
        scroll = QScrollArea(self.tray_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #F8FAFC; border: none;")
        
        content = QWidget(scroll)
        content.setStyleSheet("background-color: #F8FAFC;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(4)
        
        # 1. Informações da entidade
        cl.addWidget(AccordionSection("Informações da entidade", QLabel("Nenhum objeto selecionado."), is_expanded=False))
        
        # 2. Materiais (Expanded by default as in picture-1.png)
        cl.addWidget(AccordionSection("Materiais", self._build_materials_panel(), is_expanded=True))
        
        # 3. Componentes
        cl.addWidget(AccordionSection("Componentes", QLabel("Biblioteca de componentes 3D."), is_expanded=False))
        
        # 4. Estilos
        cl.addWidget(AccordionSection("Estilos", QLabel("Estilo Simples - Métrico."), is_expanded=False))
        
        # 5. Ambientes
        cl.addWidget(AccordionSection("Ambientes", QLabel("Céu ativado, Solo cinza padrão."), is_expanded=False))
        
        # 6. Etiquetas (Tags) (Expanded by default as in picture-1.png)
        cl.addWidget(AccordionSection("Etiquetas", self._build_tags_panel(), is_expanded=True))
        
        # 7. Sombras
        cl.addWidget(AccordionSection("Sombras", self._build_shadows_panel(), is_expanded=False))
        
        # 8. Cenas
        cl.addWidget(AccordionSection("Cenas", QLabel("Cena 1 - Perspectiva"), is_expanded=False))
        
        # 9. Instrutor
        cl.addWidget(AccordionSection("Instrutor", QLabel("Guia e atalhos da ferramenta ativa."), is_expanded=False))
        
        cl.addStretch()
        scroll.setWidget(content)
        tray_layout.addWidget(scroll)

    def _build_materials_panel(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(5)
        
        # Slanted split swatch preview matching picture-1.png
        swatch_frame = QFrame()
        swatch_frame.setFixedHeight(72)
        swatch_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:0.48 #FFFFFF, stop:0.52 #9BA9B8, stop:1 #7D8E9E);
                border: 1px solid #CBD5E1;
                border-radius: 2px;
            }
        """)
        lay.addWidget(swatch_frame)
        
        # Name row: "Nome: [ Predeterminado ]"
        nrow = QHBoxLayout()
        nrow.addWidget(QLabel("Nome"))
        self.mat_input = QLineEdit("Predeterminado")
        self.mat_input.setReadOnly(True)
        nrow.addWidget(self.mat_input)
        lay.addLayout(nrow)
        
        # Tabs row: "Selecionar" / "Editar" + Eyedropper + Paint+
        trow = QHBoxLayout()
        s_btn = QPushButton("Selecionar")
        s_btn.setStyleSheet("font-size: 11px; font-weight: 500; background-color: #E2E8F0; padding: 3px 6px; border: 1px solid #CBD5E1; color: #1E293B;")
        e_btn = QPushButton("Editar")
        e_btn.setStyleSheet("font-size: 11px; padding: 3px 6px; border: 1px solid #CBD5E1; color: #1E293B;")
        trow.addWidget(s_btn)
        trow.addWidget(e_btn)
        trow.addStretch()
        
        drop = QToolButton()
        drop.setText("🖌️")
        trow.addWidget(drop)
        
        b_add = QToolButton()
        b_add.setText("➕")
        trow.addWidget(b_add)
        lay.addLayout(trow)
        
        # Secondary toolbar: Home icon, In model, Dropdown category ("Vidro")
        srow = QHBoxLayout()
        h_btn = QToolButton()
        h_btn.setText("🏠")
        srow.addWidget(h_btn)
        
        cat = QComboBox()
        cat.addItems(["Vidro", "Cores", "Madeira", "Metal", "Pedra", "Tijolo", "Asfalto e concreto"])
        srow.addWidget(cat)
        lay.addLayout(srow)
        
        # Material 3D Cube Thumbnail Grid matching picture-1.png Vidro category
        grid_w = QWidget()
        grid = QGridLayout(grid_w)
        grid.setContentsMargins(0, 2, 0, 2)
        grid.setSpacing(4)
        
        glass_mats = [
            ("Vidro Translúcido Azul", "#38BDF8"),
            ("Vidro Escuro Fumê", "#475569"),
            ("Vidro Cristalino", "#60A5FA"),
            ("Vidro Refletivo", "#94A3B8"),
        ]
        
        for idx, (mname, mcol) in enumerate(glass_mats):
            btn = QPushButton()
            btn.setFixedSize(68, 54)
            btn.setToolTip(mname)
            
            swatch_pix = QPixmap(68, 54)
            swatch_pix.fill(Qt.GlobalColor.transparent)
            sp = QPainter(swatch_pix)
            sp.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            col = QColor(mcol)
            # Top face
            sp.setBrush(QBrush(QColor(col.red(), col.green(), col.blue(), 180)))
            sp.setPen(QPen(QColor(255, 255, 255, 200), 1.0))
            sp.drawPolygon([QPointF(34, 8), QPointF(58, 20), QPointF(34, 30), QPointF(10, 20)])
            # Left face
            sp.setBrush(QBrush(QColor(int(col.red()*0.75), int(col.green()*0.75), int(col.blue()*0.75), 210)))
            sp.drawPolygon([QPointF(10, 20), QPointF(34, 30), QPointF(34, 48), QPointF(10, 38)])
            # Right face
            sp.setBrush(QBrush(QColor(int(col.red()*0.6), int(col.green()*0.6), int(col.blue()*0.6), 230)))
            sp.drawPolygon([QPointF(34, 30), QPointF(58, 20), QPointF(58, 38), QPointF(34, 48)])
            sp.end()
            
            btn.setIcon(QIcon(swatch_pix))
            btn.setIconSize(QSize(68, 54))
            btn.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 3px; background-color: #F8FAFC;")
            btn.clicked.connect(lambda ch, c=mcol, n=mname: self._set_material(c, n))
            grid.addWidget(btn, 0, idx)
            
        lay.addWidget(grid_w)
        return w

    def _set_material(self, color_hex, name):
        self.mat_input.setText(name)
        self.viewport.current_material_color = QColor(color_hex)

    def _build_tags_panel(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(4)
        
        # Toolbar: (+) Add tag, Folder icon, Search box
        tb_lay = QHBoxLayout()
        add_b = QToolButton()
        add_b.setText("➕")
        add_b.setStyleSheet("border: none; font-size: 11px;")
        tb_lay.addWidget(add_b)
        
        folder_b = QToolButton()
        folder_b.setText("📁")
        folder_b.setStyleSheet("border: none; font-size: 11px;")
        tb_lay.addWidget(folder_b)
        
        search = QLineEdit()
        search.setPlaceholderText("Pesquisar")
        tb_lay.addWidget(search)
        lay.addLayout(tb_lay)
        
        # Tags Table matching picture-1.png with visible header
        table = QTableWidget(1, 3)
        table.setHorizontalHeaderLabels(["", "Nome", "Tracejado"])
        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(0, 24)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setFixedHeight(84)
        
        vis_item = QTableWidgetItem("👁")
        vis_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        name_item = QTableWidgetItem("Sem etiquetas")
        dash_item = QTableWidgetItem("Predeterminado")
        
        table.setItem(0, 0, vis_item)
        table.setItem(0, 1, name_item)
        table.setItem(0, 2, dash_item)
        
        lay.addWidget(table)
        return w

    def _build_shadows_panel(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(6)
        
        cb = QCheckBox("Exibir sombras")
        cb.setChecked(True)
        cb.toggled.connect(self.viewport.set_shadows)
        lay.addWidget(cb)
        
        time_lbl = QLabel("Horário: 14:30")
        lay.addWidget(time_lbl)
        time_sl = QSlider(Qt.Orientation.Horizontal)
        time_sl.setRange(60, 180)
        time_sl.setValue(145)
        time_sl.valueChanged.connect(lambda v: (
            time_lbl.setText(f"Horário: {v // 10:02d}:{(v % 10) * 6:02d}"),
            self.viewport.set_shadow_time(v / 10.0)
        ))
        lay.addWidget(time_sl)
        return w

    def _create_status_bar(self):
        sb = self.statusBar()
        
        # Information circle icon + instruction matching picture-1.png
        info_icon = QLabel("ⓘ", sb)
        info_icon.setStyleSheet("font-size: 14px; color: #1E293B; margin-right: 2px;")
        sb.addWidget(info_icon)
        
        self.status_label = QLabel(
            "Clique ou arraste para selecionar objetos. Shift = Adicionar/Subtrair. Ctrl = Adicionar. Shift + Ctrl = Subtrair.",
            sb
        )
        self.status_label.setStyleSheet("color: #1E293B; font-size: 12px;")
        sb.addWidget(self.status_label, 1)
        
        # Measurements (Medidas) container
        mw = QWidget(sb)
        mwl = QHBoxLayout(mw)
        mwl.setContentsMargins(0, 0, 4, 0)
        mwl.setSpacing(6)
        
        mlbl = QLabel("Medidas", mw)
        mlbl.setStyleSheet("color: #1E293B; font-size: 12px;")
        mwl.addWidget(mlbl)
        
        self.meas_input = QLineEdit(mw)
        self.meas_input.setFixedWidth(130)
        self.meas_input.setStyleSheet("background-color: #FFFFFF; border: 1px solid #94A3B8; border-radius: 2px;")
        mwl.addWidget(self.meas_input)
        
        sb.addPermanentWidget(mw)

    def update_measurements(self, text):
        self.meas_input.setText(text)


# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SketchCraft 2026")
    parser.add_argument("--screenshot", type=str, help="Save screenshot to image file and exit", default=None)
    args, _ = parser.parse_known_args()
    
    app = QApplication(sys.argv)
    app.setApplicationName("SketchCraft 2026")
    app.setStyle("Fusion")
    
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = SketchCraftWindow(screenshot_path=args.screenshot)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
