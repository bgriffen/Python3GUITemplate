from traits.api import HasTraits, Instance
from traitsui.api import View, Item, Handler
from traitsui.editor import Editor
from traitsui.basic_editor_factory import BasicEditorFactory

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

from pyface.qt import QtGui

from numpy import sin, cos, linspace, pi
from matplotlib.widgets import RectangleSelector


class _MPLFigureEditor(Editor):
    scrollable = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def set_size_policy(self, direction, resizable, springy, stretch):
        pass
    # Rest of your class code.

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # matplotlib commands to create a canvas
        frame = QtGui.QWidget()
        mpl_canvas = FigureCanvas(self.value)
        mpl_canvas.setParent(frame)
        mpl_toolbar = NavigationToolbar(mpl_canvas, frame)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(mpl_canvas)
        vbox.addWidget(mpl_toolbar)
        frame.setLayout(vbox)

        return frame


class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor


class MPLInitHandler(Handler):
    """Handler calls mpl_setup() to initialize mpl events"""

    def init(self, info):
        """This method gets called after the controls have all been
        created but before they are displayed.
        """
        info.object.mpl_setup()
        return True


class Test(HasTraits):
    figure = Instance(Figure, ())

    view = View(
        Item('figure', editor=MPLFigureEditor(), show_label=False),
        handler=MPLInitHandler,
        resizable=True
    )

    def __init__(self):
        super(Test, self).__init__()
        self.axes = self.figure.add_subplot(111)
        t = linspace(0, 2 * pi, 200)
        self.axes.plot(sin(t) * (1 + 0.5 * cos(11 * t)), cos(t) * (1 + 0.5 * cos(11 * t)))

    def mpl_setup(self):
        def onselect(eclick, erelease):
            print(f"Start position: {eclick}, End position: {erelease}")

        self.rs = RectangleSelector(self.axes, onselect, useblit=True)



if __name__ == "__main__":
    Test().configure_traits()
