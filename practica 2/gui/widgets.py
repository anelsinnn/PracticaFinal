# gui/widgets.py
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # Ocultar los ejes para que parezca un lienzo limpio
        self.axes.axis('off')
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

class TreeCanvasWidget(QWidget):
    """
    Un widget contenedor para nuestro lienzo de Matplotlib.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        self.layout.addWidget(self.canvas)

    def clear(self):
        self.canvas.axes.clear()
        self.canvas.axes.axis('off')
        self.canvas.draw()