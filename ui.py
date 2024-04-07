import matplotlib

matplotlib.use("svg")  # svg export
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QDesktopServices,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QToolBox,
    QVBoxLayout,
    QWidget,
)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("W.O.L.F. - Ways with OpenStreetMap Location Finder")
        self.setWindowIcon(QIcon("gfx/wolf_logo_old.png"))

        version = "1.01 vom 07.07.2024"

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # splitter
        splitter = QSplitter()

        # linke Spalte
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # Create the matplotlib FigureCanvas object
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        left_layout.addWidget(toolbar)
        left_layout.addWidget(self.canvas)

        # Hier die ganzen Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Button begin
        self.btn_begin = QPushButton()
        self.btn_begin.setIcon(QIcon("icons/backward-fast.svg"))
        self.btn_begin.setIconSize(QSize(35, 35))
        self.btn_begin.setObjectName("btn_begin")
        self.btn_begin.setFixedSize(QSize(50, 50))
        self.btn_begin.setToolTip("Zum Anfang springen")
        buttons_layout.addWidget(self.btn_begin)

        # Button Step Backwards
        self.btn_stepBwd = QPushButton()
        self.btn_stepBwd.setIcon(QIcon("icons/backward-step.svg"))
        self.btn_stepBwd.setIconSize(QSize(35, 35))
        self.btn_stepBwd.setObjectName("btn_stepBwd")
        self.btn_stepBwd.setFixedSize(QSize(50, 50))
        self.btn_stepBwd.setToolTip("Gehe einen Schritt zurück")
        buttons_layout.addWidget(self.btn_stepBwd)

        # Button Play Backwards
        self.btn_playBwd = QPushButton()
        self.btn_playBwd.setIcon(QIcon("icons/back_play.svg"))
        self.btn_playBwd.setIconSize(QSize(35, 35))
        self.btn_playBwd.setObjectName("btn_playBwd")
        self.btn_playBwd.setFixedSize(QSize(50, 50))
        self.btn_playBwd.setToolTip("Rückwärts abspielen")
        buttons_layout.addWidget(self.btn_playBwd)

        # Button Pause
        self.btn_pause = QPushButton()
        self.btn_pause.setIcon(QIcon("icons/pause.svg"))
        self.btn_pause.setIconSize(QSize(35, 35))
        self.btn_pause.setObjectName("btn_pause")
        self.btn_pause.setFixedSize(QSize(50, 50))
        self.btn_pause.setToolTip("Animation anhalten")
        buttons_layout.addWidget(self.btn_pause)

        # Button Play Forward
        self.btn_playFwd = QPushButton()
        self.btn_playFwd.setIcon(QIcon("icons/play.svg"))
        self.btn_playFwd.setIconSize(QSize(35, 35))
        self.btn_playFwd.setObjectName("btn_playFwd")
        self.btn_playFwd.setFixedSize(QSize(50, 50))
        self.btn_playFwd.setToolTip("Vorwärts abspielen")
        buttons_layout.addWidget(self.btn_playFwd)

        # Button Step Forward
        self.btn_stepFwd = QPushButton()
        self.btn_stepFwd.setIcon(QIcon("icons/forward-step.svg"))
        self.btn_stepFwd.setIconSize(QSize(35, 35))
        self.btn_stepFwd.setObjectName("btn_stepFwd")
        self.btn_stepFwd.setFixedSize(QSize(50, 50))
        self.btn_stepFwd.setToolTip("Gehe einen Schritt vorwärts")
        buttons_layout.addWidget(self.btn_stepFwd)

        # Button End
        self.btn_end = QPushButton()
        self.btn_end.setIcon(QIcon("icons/forward-fast.svg"))
        self.btn_end.setIconSize(QSize(35, 35))
        self.btn_end.setObjectName("btn_end")
        self.btn_end.setFixedSize(QSize(50, 50))
        self.btn_end.setToolTip("Zum Ende springen")

        buttons_layout.addWidget(self.btn_end)
        buttons_layout.addStretch()

        left_layout.addLayout(buttons_layout)

        # Labels
        label_layout = QHBoxLayout()
        self.label_velocity = QLabel("Aktuelle Geschwindigkeit: 1.00x")
        self.label_velocity.setMaximumHeight(20)
        self.label_steps = QLabel("Schritte")
        self.label_steps.setMaximumHeight(20)
        label_layout.addWidget(self.label_velocity)
        label_layout.addStretch()
        label_layout.addWidget(self.label_steps)

        left_layout.addLayout(label_layout)

        # Sliders
        slider_layout = QHBoxLayout()
        # slider_layout.addStretch()

        # Slider für Geschwindigkeit
        self.slider_velocity = QSlider()
        self.slider_velocity.setObjectName("slider_velocity")
        self.slider_velocity.setOrientation(Qt.Horizontal)
        self.slider_velocity.setMinimum(25)
        self.slider_velocity.setMaximum(500)
        self.slider_velocity.setMaximumWidth(150)
        self.slider_velocity.setMinimumWidth(50)
        self.slider_velocity.setValue(100)
        self.slider_velocity.setTracking(False)
        slider_layout.addWidget(self.slider_velocity)

        slider_layout.addStretch()

        # Slider für einzelne Schritte

        self.slider_Steps = QSlider()
        self.slider_Steps.setObjectName("slider_Steps")
        self.slider_Steps.setOrientation(Qt.Horizontal)
        self.slider_Steps.setMaximum(0)
        self.slider_Steps.setTracking(False)
        slider_layout.addWidget(self.slider_Steps)

        # Checkbox um Slider optional am Ende stehen zu lassen
        self.checkbox_slider_steps_lock = QCheckBox("Ende fixieren")
        self.checkbox_slider_steps_lock.setObjectName("checkbox_slider_steps_lock")
        slider_layout.addWidget(self.checkbox_slider_steps_lock)

        # slider_layout.addStretch()

        left_layout.addLayout(slider_layout)

        self.btn_pause.raise_()
        self.btn_end.raise_()
        self.btn_playFwd.raise_()
        self.btn_stepFwd.raise_()
        self.slider_Steps.raise_()
        self.btn_begin.raise_()
        self.btn_stepBwd.raise_()
        self.btn_playBwd.raise_()
        self.slider_velocity.raise_()

        splitter.addWidget(left_widget)

        # Right side
        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        # QTabWidget mit Tabs
        tab_widget = QTabWidget()

        tab_map = QWidget()
        tab_algo = QWidget()
        tab_settings = QWidget()
        tab_about = QWidget()

        tab_widget.addTab(tab_map, "Karte")
        tab_widget.addTab(tab_algo, "Algorithmen")
        tab_widget.addTab(tab_settings, "Einstellungen")
        tab_widget.addTab(tab_about, "About")

        right_layout.addWidget(tab_widget)

        # Create the menus
        # Create a QVBoxLayout to stack the QToolBoxes vertically
        layout_map = QVBoxLayout()
        tab_map.setLayout(layout_map)

        ## Karte nach Ort
        label_map_city = QLabel("Suche Stadt/Ort")
        label_map_city.setMaximumHeight(20)
        self.lineedit_place_name = QLineEdit()
        self.btn_get_by_name = QPushButton("Setze Ort")
        self.btn_get_by_name.setObjectName("btn_get_by_name")

        layout_map.addWidget(label_map_city)
        layout_map.addWidget(self.lineedit_place_name)
        layout_map.addWidget(self.btn_get_by_name)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout_map.addWidget(line)

        # Karte von Bbox
        # north, south, east, west = 50.32942276889266, 50.32049083973944, 11.944606304168701, 11.929510831832886
        label_north = QLabel("Nord 50.32942276889266")
        label_north.setMaximumHeight(20)
        self.lineedit_north = QLineEdit()
        label_south = QLabel("Süd 50.32049083973944")
        label_south.setMaximumHeight(20)
        self.lineedit_south = QLineEdit()
        label_east = QLabel("Ost 11.944606304168701")
        label_east.setMaximumHeight(20)
        self.lineedit_east = QLineEdit()
        label_west = QLabel("West 11.929510831832886")
        label_west.setMaximumHeight(20)
        self.lineedit_west = QLineEdit()

        self.btn_bbox = QPushButton("Setze Bbox")
        self.btn_bbox.setObjectName("btn_bbox")

        layout_map.addWidget(label_north)
        layout_map.addWidget(self.lineedit_north)
        layout_map.addWidget(label_south)
        layout_map.addWidget(self.lineedit_south)
        layout_map.addWidget(label_east)
        layout_map.addWidget(self.lineedit_east)
        layout_map.addWidget(label_west)
        layout_map.addWidget(self.lineedit_west)
        layout_map.addWidget(self.btn_bbox)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout_map.addWidget(line)

        ## Karte nach aktueller Plot Auswahl

        label_auswahl = QLabel(
            "Benutze die Luppe aus der Toolbar um einen Bereich auszuwählen und zu zoomen. Reset der Zoomstufe mit Home oder Zurück Button"
        )
        label_auswahl.setWordWrap(True)

        self.btn_auswahl = QPushButton("Setze aktuelle Auswahl")
        self.btn_auswahl.setObjectName("btn_auswahl")

        layout_map.addWidget(label_auswahl)
        layout_map.addWidget(self.btn_auswahl)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout_map.addWidget(line)

        ## Graph von und zu GraphML File
        label_map_graphml = QLabel("Graph aus GraphML File")
        label_map_graphml.setMaximumHeight(20)
        self.lineedit_graphml_path = QLineEdit()
        self.lineedit_graphml_path.setPlaceholderText("Pfad zur GraphML File .graphml")

        self.checkbox_gephi = QCheckBox("NUR für Gephi speichern (Workaround)")
        self.checkbox_gephi.setObjectName("checkbox_gephi")

        self.btn_save_graphml = QPushButton("Speichere GraphML")
        self.btn_save_graphml.setObjectName("btn_save_graphml")

        self.btn_load_graphml = QPushButton("Lade GraphML")
        self.btn_load_graphml.setObjectName("btn_load_graphml")

        layout_map.addWidget(label_map_graphml)
        layout_map.addWidget(self.lineedit_graphml_path)
        layout_map.addWidget(self.checkbox_gephi)
        layout_map.addWidget(self.btn_save_graphml)
        layout_map.addWidget(self.btn_load_graphml)

        layout_map.addStretch()

        # Algo-Tab

        layout_algo = QVBoxLayout()
        tab_algo.setLayout(layout_algo)

        # Radio Buttons
        self.groupbox_algo = QGroupBox("Algorithmus:")
        radio_layout = QHBoxLayout()
        self.groupbox_algo.setLayout(radio_layout)
        self.radio_dijkstra = QRadioButton("Dijkstra")
        self.radio_dijkstra.setObjectName("radio_dijkstra")
        self.radio_greedy = QRadioButton("Greedy")
        self.radio_greedy.setObjectName("radio_greedy")
        self.radio_astar = QRadioButton("A*")
        self.radio_astar.setObjectName("radio_astar")
        self.radio_dijkstra.setChecked(True)
        radio_layout.addWidget(self.radio_dijkstra)
        radio_layout.addWidget(self.radio_greedy)
        radio_layout.addWidget(self.radio_astar)
        radio_layout.addStretch()

        layout_algo.addWidget(self.groupbox_algo)

        # Kantengewichtung
        self.groupbox_weight = QGroupBox("Kantengewichtung:")
        radio_layout_weight = QHBoxLayout()
        self.groupbox_weight.setLayout(radio_layout_weight)

        self.radio_weight_length = QRadioButton("Länge")
        self.radio_weight_length.setObjectName("radio_weight_length")
        self.radio_weight_duration = QRadioButton("Dauer")
        self.radio_weight_duration.setObjectName("radio_weight_duration")
        self.radio_weight_length.setChecked(True)
        radio_layout_weight.addWidget(self.radio_weight_length)
        radio_layout_weight.addWidget(self.radio_weight_duration)
        radio_layout_weight.addStretch()

        layout_algo.addWidget(self.groupbox_weight)

        # Zusatzeinstellungen
        self.groupbox_add = QGroupBox("Zusatzeinstellungen:")

        self.layout_add_1 = QVBoxLayout()
        self.layout_add_1.setObjectName("layout_add_1")
        self.checkbox_target = QCheckBox("mit Ziel")
        self.checkbox_target.setObjectName("checkbox_target")
        self.checkbox_target.setChecked(True)
        self.layout_add_1.addWidget(self.checkbox_target)

        self.groupbox_add.setLayout(self.layout_add_1)

        self.groupbox_heuristic = QGroupBox("Heuristik:")
        layout_add_boxes = QHBoxLayout()
        self.groupbox_heuristic.setLayout(layout_add_boxes)
        self.radio_null = QRadioButton("0")
        self.radio_null.setObjectName("radio_null")
        self.radio_euclid = QRadioButton("Euclidean")
        self.radio_euclid.setObjectName("radio_euclid")
        self.radio_euclidsquare = QRadioButton("Euclidean²")
        self.radio_euclidsquare.setObjectName("radio_euclidsquare")
        self.radio_manhattan = QRadioButton("Manhattan")
        self.radio_manhattan.setObjectName("radio_manhattan")
        self.radio_euclid.setChecked(True)
        layout_add_boxes.addWidget(self.radio_null)
        layout_add_boxes.addWidget(self.radio_euclid)
        layout_add_boxes.addWidget(self.radio_euclidsquare)
        layout_add_boxes.addWidget(self.radio_manhattan)
        layout_add_boxes.addStretch()

        layout_algo.addWidget(self.groupbox_add)
        layout_algo.addWidget(self.groupbox_heuristic)
        self.groupbox_heuristic.hide()

        # Widget für die Bilder
        self.image_widget = QLabel()
        self.image_widget.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("gfx/dijkstra.png")
        self.image_widget.setPixmap(pixmap)

        layout_algo.addWidget(self.image_widget)

        # Start, Ziel, Gewicht, Länge, Dauer, Routen
        self.label_start_target = QLabel("Start: None, Ziel: None")
        self.label_start_target.setMaximumHeight(20)
        self.label_start_target.setTextFormat(Qt.RichText)
        self.label_start_target.setOpenExternalLinks(True)
        self.label_cost_weight = QLabel("Gewicht: x, Länge: x m, Dauer: x s")
        self.label_cost_weight.setMaximumHeight(20)
        self.label_routen_punkte = QLabel("Über: []")
        # self.label_routen_punkte.setMaximumHeight(20)
        self.label_routen_punkte.setWordWrap(True)
        self.label_routen = QLabel("Route: []")
        # self.label_routen.setMaximumHeight(20)
        self.label_routen.setWordWrap(True)

        layout_algo.addWidget(self.label_start_target)
        layout_algo.addWidget(self.label_cost_weight)
        layout_algo.addWidget(self.label_routen_punkte)
        layout_algo.addWidget(self.label_routen)

        layout_algo.addStretch()

        # Settings Tab

        layout_settings = QVBoxLayout()
        tab_settings.setLayout(layout_settings)

        # Einstellung für Edges
        self.groupbox_settings_edges = QGroupBox("Kantenbeschriftung:")
        radio_layout_edges = QVBoxLayout()
        self.groupbox_settings_edges.setLayout(radio_layout_edges)
        self.radio_settings_name = QRadioButton("Straßenname")
        self.radio_settings_name.setObjectName("radio_settings_name")
        self.radio_settings_length = QRadioButton("Länge")
        self.radio_settings_length.setObjectName("radio_settings_length")
        self.radio_settings_duration = QRadioButton("Dauer")
        self.radio_settings_duration.setObjectName("radio_settings_duration")
        self.radio_settings_none_edges = QRadioButton("Keine Kantenbeschriftung")
        self.radio_settings_none_edges.setObjectName("radio_settings_none")
        self.radio_settings_none_edges.setChecked(True)
        radio_layout_edges.addWidget(self.radio_settings_name)
        radio_layout_edges.addWidget(self.radio_settings_length)
        radio_layout_edges.addWidget(self.radio_settings_duration)
        radio_layout_edges.addWidget(self.radio_settings_none_edges)

        layout_settings.addWidget(self.groupbox_settings_edges)

        # Einstellung für Nodes
        self.groupbox_settings_nodes = QGroupBox("Knotenbeschriftung:")
        radio_layout_nodes = QVBoxLayout()
        self.groupbox_settings_nodes.setLayout(radio_layout_nodes)
        self.radio_settings_id = QRadioButton("ID")
        self.radio_settings_id.setObjectName("radio_settings_id")
        self.radio_settings_none_nodes = QRadioButton("Keine Knotenbeschriftung")
        self.radio_settings_none_nodes.setObjectName("radio_settings_none")
        self.radio_settings_none_nodes.setChecked(True)
        radio_layout_nodes.addWidget(self.radio_settings_id)
        radio_layout_nodes.addWidget(self.radio_settings_none_nodes)

        layout_settings.addWidget(self.groupbox_settings_nodes)

        # Hintergrundtyp

        label_settings_background = QLabel("Hintergrund")
        label_settings_background.setMaximumHeight(20)
        layout_settings.addWidget(label_settings_background)

        self.combo_background = QComboBox()
        self.combo_background.addItem("Kein Hintergrund")
        self.combo_background.addItem("OpenStreetMap.Mapnik")
        self.combo_background.addItem("CartoDB.Voyager")
        self.combo_background.addItem("CartoDB.Positron")
        self.combo_background.addItem("CartoDB.PositronOnlyLabels")
        self.combo_background.addItem("CartoDB.DarkMatter")
        self.combo_background.addItem("OpenTopoMap")
        layout_settings.addWidget(self.combo_background)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout_settings.addWidget(line)

        # Save Settings
        self.btn_save_settings = QPushButton("Speichern und Anwenden")
        self.btn_auswahl.setObjectName("btn_save_settings")

        layout_settings.addWidget(self.btn_save_settings)

        layout_settings.addStretch()

        # About
        layout_about = QVBoxLayout()
        tab_about.setLayout(layout_about)

        label_about = QLabel(
            "Erstellt von:\nGeorg Mangold, Christoph Schmidhuber, Marco Rinn\n\nAuftraggeber:\nProf. Dr. Johannes Michael\nFakultät Informatik\nHochschule für angewandte Wissenschaften Hof\nAlfons-Goppel-Platz 1\n95028 Hof"
        )
        label_about.setWordWrap(True)

        layout_about.addWidget(label_about)

        version_text = f"Version:\n{version}"
        label_version = QLabel(version_text, self)
        layout_about.addWidget(label_version)

        layout_logos = QHBoxLayout()

        label_logo = QLabel()
        label_logo.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("gfx/wolf_logo.png")
        scaled_pixmap = pixmap.scaled(
            150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        label_logo.setPixmap(scaled_pixmap)

        layout_logos.addWidget(label_logo)

        label_logo_haw = QLabel()
        label_logo_haw.setAlignment(Qt.AlignCenter)
        pixmap_haw = QPixmap("gfx/HAW_logo.png")
        scaled_pixmap_haw = pixmap_haw.scaled(
            150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        label_logo_haw.setPixmap(scaled_pixmap_haw)

        layout_logos.addWidget(label_logo_haw)

        layout_about.addLayout(layout_logos)

        label_license = QLabel()
        html_text = 'Lizenzen:<br>\
                    <a href="https://www.openstreetmap.org/copyright">OpenStreetMap®</a> sind offene Daten (open data), lizenziert unter der \
                        <a href="https://opendatacommons.org/licenses/odbl/1">Open Data Commons Open Database-Lizenz </a>(ODbL) \
                        von der <a href="https://osmfoundation.org/">OpenStreetMap Stiftung</a> (OSMF).<br><br>\
                    <a href="https://osmnx.readthedocs.io/en/stable/">OSMnx</a> ist Open Source und lizenziert unter der MIT Lizenz.<br><br>\
                    <a href="https://github.com/georgmangold/wolf">W.O.L.F.</a> ist lizenziert unter der <a href="https://choosealicense.com/licenses/mit/">MIT Lizenz</a>.'
        label_license.setTextFormat(Qt.RichText)
        label_license.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_license.setOpenExternalLinks(True)
        label_license.setWordWrap(True)
        label_license.setText(html_text)

        layout_about.addWidget(label_license)

        layout_about.addStretch()

        # Splitter settings
        splitter.addWidget(right_frame)

        splitter.setSizes([1000, 200])
        splitter.setHandleWidth(10)

        main_layout.addWidget(splitter)
