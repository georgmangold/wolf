from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QMutex, QObject, QThread, Signal
from PySide6.QtWidgets import QProgressDialog
from ui import UI

import osmnx as ox
import contextily as cx

from time import sleep

import matplotlib
from svgpathtools import svg2paths
from svgpath2mpl import parse_path

import dijkstra
from greedy import greedy
from astar import astar

class Controller:
    def __init__(self):
        self.ui = UI()
        
        ##### Settings #####
        self.background = "Kein Hintergrund" #
        self.eges_beschriftung = "Keine Kantenbeschriftung" #
        self.nodes_beschriftung = "Keine Knotenbeschriftung" #
        self.weight="length"
        self.algo = 'Dijkstra'
        self.heuristik = '0'
        #### Noch nicht in GUI ####
        ox.settings.use_cache=True
        ox.settings.log_console=True
        ox.settings.default_crs='epsg:4326' #default ist epsg:4326, leider nicht epsg:3857...
        self.network_type='drive'
        #self.network_type='walk'
        self.marker = self.getCustomMarker()
        self.node_id = False
        self.edge_id = False
        self.route_color="orange"
        self.route_linewidth=6
        self.orig_dest_size=0
        self.route_alpha = 1
        # Eins von beiden muss > 0
        self.edge_linewidth=0.5 #0.01
        self.node_size=0
        
        self.start_color = 'red'
        self.ende_color = 'blue'
        self.routenmarkierung_color = 'green'
        
        self.velocity = 1
        
        self.color_new_steps = "red"
        self.color_steps = "blue"
        self.steps_linewidth = 2
        self.steps_alpha = 0.5
        ##### Variablen #####
        self.start = None
        self.start_point = None
        self.end = None
        self.end_point = None
        self.routen_punkte = []
        
        self.plot_steps = {}
                
        self.graph = None
        #self.besuchte_routen = []
        self.besuchte_routen = [
            [[295704006, 295704008],[295704006, 379493008],[295704006, 341097090]],
            [[295704008, 295704040],[295704008, 295704010],[379493008, 295704010],[341097090, 379493100],[341097090, 341097088]],
            [[295704040, 295704024],[295704040, 379493005],[295704040, 379493119],[295704010, 379493005],[379493100, 379493227],[379493100, 379493102],[341097088, 324775669]],
            [[295704024, 298157835],[295704024, 299395054],[379493119, 299395098],[379493119, 379493227],[379493227, 299395098],[324775669, 324775529],[324775669, 343477485]],
            [[298157835, 298196377],[299395054, 298196528],[299395054, 295704034],[299395054, 299395098],[299395098, 324775529],[324775529, 295704036],[343477485, 341442403],[343477485, 324772600]],
            [[298196377, 298196528],[298196528, 298196326],[298196528, 299395054],[295704034, 298196326],[295704036, 295704034],[295704036, 295704075],[341442403, 324776715],[341442403, 324775672],[324772600, 324775672]],
            [[298196326, 295704075],[295704075, 343479324],[295704075, 9182217733],[324776715, 324776188],[324776715, 295704255],[324775672, 492150429]],
            [[9182217733, 343477595],[9182217733, 379570454]],
            [[379570454, 343477573]],
        ]
        self.found_path = [295704006, 341097090, 379493100, 379493227, 299395098, 324775529, 295704036, 295704075, 9182217733, 379570454, 343477573]

        self.current_step = 0
        self.mutex_button_press = QMutex()
        self.mutex_slider = QMutex()
        self.thread = QThread()
        self.worker = None
        #####
        
        # connectSlotsByName functionen zu btns
        QtCore.QMetaObject.connectSlotsByName(self.ui)

        self.ui.canvas.mpl_connect('button_press_event', self.on_canvas_click)

        self.ui.btn_get_by_name.clicked.connect(self.btn_get_by_name_clicked)
        self.ui.btn_bbox.clicked.connect(self.btn_bbox_clicked)
        self.ui.btn_auswahl.clicked.connect(self.btn_auswahl_clicked)

        self.ui.btn_save_settings.clicked.connect(self.btn_save_settings_clicked)

        self.ui.btn_begin.clicked.connect(self.btn_begin_clicked)
        self.ui.btn_stepBwd.clicked.connect(self.btn_stepBwd_clicked)
        self.ui.btn_playBwd.clicked.connect(self.btn_playBwd_clicked)
        self.ui.btn_pause.clicked.connect(self.btn_pause_clicked)
        self.ui.btn_playFwd.clicked.connect(self.btn_playFwd_clicked)
        self.ui.btn_stepFwd.clicked.connect(self.btn_stepFwd_clicked)
        self.ui.btn_end.clicked.connect(self.btn_end_clicked)

        self.ui.radio_dijkstra.clicked.connect(self.update_dijkstra)
        self.ui.radio_greedy.clicked.connect(self.update_greedy)
        self.ui.radio_astar.clicked.connect(self.update_astar)

        self.ui.slider_velocity.valueChanged.connect(self.slider_velocity_value_changed)
        
        self.ui.slider_Steps.valueChanged.connect(self.slider_Steps_value_changed)
        # Slider Tracking is disabled so value_changed triggers on release but gives value
        #self.ui.slider_Steps.sliderReleased.connect(self.slider_Steps_sliderReleased)
        self.ui.slider_Steps.sliderMoved.connect(self.slider_Steps_moved)
        
        ## Bbox vom Start
        north, south, east, west = 50.32942276889266, 50.32049083973944, 11.944606304168701, 11.929510831832886
        ## north, south, east, west = 50.3277, 50.32049083973944, 11.9474, 11.929510831832886
        
        ## create network from that bounding box
        #self.graph = ox.graph_from_bbox(north, south, east, west, network_type=self.network_type)

        #self.plotStreetGraph()
        self.graph_thread_bbbox(north, south, east, west, self.network_type)

    def show_main_window(self):
        self.ui.show()
        
    
    def update_dijkstra(self):
        self.ui.image_widget.setPixmap(QtGui.QPixmap("gfx/dijkstra.png"))
        self.ui.groupbox_add.show()
        self.ui.groupbox_heuristic.hide()
        # Start und Ziel wurden gesetzt! Routen erstellen!
        if self.start is not None and self.end is not None:
            self.generateRoutes()

    def update_greedy(self):
        self.ui.image_widget.setPixmap(QtGui.QPixmap("gfx/greedy.png"))
        self.ui.groupbox_add.hide()
        self.ui.groupbox_heuristic.show()
        # Start und Ziel wurden gesetzt! Routen erstellen!
        if self.start is not None and self.end is not None:
            self.generateRoutes()
        
    def update_astar(self):
        self.ui.image_widget.setPixmap(QtGui.QPixmap("gfx/astern.png"))
        self.ui.groupbox_add.hide()
        self.ui.groupbox_heuristic.show()
        # Start und Ziel wurden gesetzt! Routen erstellen!
        if self.start is not None and self.end is not None:
            self.generateRoutes()

    def slider_velocity_value_changed(self, value):
        value /= 100
        self.ui.label_velocity.setText(f"Aktuelle Geschwindigkeit: {value: .2f}x")
        self.velocity = value
    
    def slider_Steps_moved(self, value):
        self.ui.label_steps.setText(f"Schritte: {value} von {len(self.besuchte_routen)+1}")

    def slider_Steps_value_changed(self, value):
        '''
        Slot welcher aufgerufen wird wenn sich Slider ändert,
        egal ob händisch / Button oder StepsTimer
        '''
        #print(f'Slider changed: {value}')
        mutex = self.mutex_slider.tryLock(0)
        if mutex:
            #print("Slider locked")
            self.ui.label_steps.setText(f"Schritte: {value} von {len(self.besuchte_routen)+1}")
            if value > self.current_step:
                self.plotRoutesSteps(self.besuchte_routen, self.current_step, value)
            elif value < self.current_step:              
                self.delete_last_lines(value)
            else:
                #print(value)
                pass
            self.current_step = value
            self.mutex_slider.unlock()
        
    def getCustomMarker(self):
        # Eigener Mappin Marker von SVG
        #_, attributes = svg2paths('icons/map-pin.svg')
        _, attributes = svg2paths('icons/wolf3.svg')
        mappin_marker = parse_path(attributes[0]['d'])
        
        # Center Position
        mappin_marker.vertices -= mappin_marker.vertices.mean(axis=0)
        # Calculate the height of the marker
        height = mappin_marker.vertices[:, 1].max()

        # Move the marker upwards
        mappin_marker.vertices[:, 1] -= height

        # Image is upside down and flipped
        mappin_marker = mappin_marker.transformed(matplotlib.transforms.Affine2D().rotate_deg(180))
        mappin_marker = mappin_marker.transformed(matplotlib.transforms.Affine2D().scale(-1,1))
        
        return mappin_marker
    
    def plotStreetGraph(self):
        '''
        Funktion zum Zeichnen des aktuellen Graphen
        '''
        
        self.start = None
        self.start_point = None
        self.end = None
        self.end_point = None
        self.routen_punkte = []
        
        self.ui.canvas.axes.cla()
        #self.ui.canvas.axes.figure.clf()

        self.graph = ox.add_edge_speeds(self.graph)
        self.graph = ox.add_edge_travel_times(self.graph)
        
        # Projeziere Graph von epsg:4326 zu epsg:3857
        if(self.graph.graph['crs'] != "epsg:3857"):
            self.graph = ox.project_graph(self.graph, to_crs='epsg:3857')
            
        self.fig, self.ax = ox.plot_graph(self.graph, ax=self.ui.canvas.axes, edge_linewidth=self.edge_linewidth, node_size=self.node_size, show=False, close=False)
        
        # Beschriftungen
        if self.eges_beschriftung != "Keine Kantenbeschriftung":
            for _, edge in ox.graph_to_gdfs(self.graph, nodes=False).fillna("").iterrows():
                if self.eges_beschriftung == "Straßenname":
                    text = edge["name"]
                elif self.eges_beschriftung == "Länge":
                    text = str(round(edge["length"]))+"m"
                elif self.eges_beschriftung == "Dauer":
                    text = str(edge["travel_time"])+"s"
                else:
                    text = ""
                c = edge["geometry"].centroid
                self.ax.annotate(text, (c.x, c.y), c="black")
        
        if self.nodes_beschriftung != "Keine Knotenbeschriftung":
            for node_id, node in ox.graph_to_gdfs(self.graph, edges=False).fillna("").iterrows():
                if self.nodes_beschriftung == "ID":
                    text = str(node_id)
                else:
                    text = ""
                c = node["geometry"].centroid
                self.ax.annotate(text, (c.x, c.y), c="black")
                
        if self.background != "Kein Hintergrund":
            print("Hintergrund hinzufügen..")
            cx.add_basemap(self.ax, crs='epsg:3857', source=eval(f'cx.providers.{self.background}'))
            #cx.add_basemap(self.ax, crs='epsg:3857', source=globals()[f'cx.providers.{self.background}'])
            print("... done.")
            
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def on_canvas_click(self, event):
        '''
        Methode, die beim Klicken auf dem Canvas aufgerufen wird,
        zum setzen von Start, Ziel und Wegepunkte
        '''
        #print(event)
        if (event.xdata != None and event.ydata != None):
            
            # scikit-learn must be installed to search an unprojected graph
            node = ox.distance.nearest_nodes(self.graph, event.xdata, event.ydata)
            print(f'Nearest node: {node}')
            
            x = self.graph.nodes[node]["x"]
            y = self.graph.nodes[node]["y"]
            
            if (event.button == 1):
                #linksklick Start
                self.start = node
                  
                if self.start_point is not None:
                    self.start_point.remove()
                
                points = self.ax.plot(x, y, color=self.start_color, marker=self.marker, markersize=50, zorder=2.5, label="start")
                self.start_point = points[0]
         
            elif (event.button == 3):
                #Rechtsklick Ende
                self.end = node
                
                if self.end_point is not None:
                    self.end_point.remove()
                
                points = self.ax.plot(x, y, color=self.ende_color, marker=self.marker, markersize=50, zorder=2.5, label="ende")
                self.end_point = points[0]
            
            elif (event.button == 2):
                #Mittelklick Routen
                points = self.ax.plot(x, y, color=self.routenmarkierung_color, marker=self.marker, markersize=100, zorder=2.5, label="route_punkte")
                self.routen_punkte.append(node)
                print(self.routen_punkte)
            
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
            # Start und Ziel wurden gesetzt! Routen erstellen!
            if self.start is not None and self.end is not None:
                self.generateRoutes()


    # Karten Buttons:
    
    def btn_get_by_name_clicked(self):
        place = 'Hof, Bayern, DE'
        if (self.ui.lineedit_place_name.text() != ""):
            place = self.ui.lineedit_place_name.text()
        #self.graph = ox.graph_from_place(place, network_type=self.network_type)

        #self.plotStreetGraph()
        self.graph_thread_place(place, self.network_type)
    
    def btn_bbox_clicked(self):
        north, south, east, west = 50.32942276889266, 50.32049083973944, 11.944606304168701, 11.929510831832886

        if(self.ui.lineedit_north.text() != "" and self.ui.lineedit_south.text() != "" and self.ui.lineedit_east.text() != "" and self.ui.lineedit_west.text() != ""):
            north = self.ui.lineedit_north.text()
            south = self.ui.lineedit_south.text()
            east = self.ui.lineedit_east.text()
            west = self.ui.lineedit_west.text()
        
        #self.graph = ox.graph_from_bbox(north, south, east, west, network_type=self.network_type)

        #self.plotStreetGraph()
        
        self.graph_thread_bbbox(north, south, east, west, self.network_type)



    def btn_auswahl_clicked(self):

        west, east = self.ui.canvas.axes.get_xlim()
        south, north = self.ui.canvas.axes.get_ylim()
        
        #self.graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')
        # Muss wegen Projizierung auf epsg:3857 wieder in epsg:4326 umgewandelt werden
        polygon = ox.utils_geo.bbox_to_poly(north, south, east, west)
        if(self.graph.graph['crs'] == "epsg:3857"):
            polygon, _ = ox.projection.project_geometry(polygon, crs='epsg:3857', to_crs='epsg:4326')
        #self.graph = ox.graph_from_polygon(polygon, self.network_type)
        
        #self.plotStreetGraph()
        self.graph_thread_polygon(polygon, self.network_type)

    #### Control Buttons:

    def btn_pause_clicked(self):
        print("Pause-Button pressed.")
        self.stop_thread()
        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)
        self.update_slider_Steps(self.current_step)

    def btn_begin_clicked(self):
        print("Begin Button pressed.")

        self.stop_thread()
        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)

        self.update_slider_Steps(0)


    def btn_stepBwd_clicked(self):
        print("Step backwards!")

        self.stop_thread()
            
        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)

        if self.current_step > 0:
            self.update_slider_Steps(self.current_step-1)

    

    def btn_playBwd_clicked(self):
        print("Play backwards!")
        if self.thread.isRunning():
            return

        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)
        # Step 1: Create a worker class
        # StepsWorker
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = self.StepsWorker(self.current_step,0, self.velocity)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.worker.progress.connect(self.update_slider_Steps)
        # Step 6: Start the thread
        self.thread.start()
        
    def btn_playFwd_clicked(self):
         
        if self.thread.isRunning():
            return

        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)
        # Step 1: Create a worker class
        # StepsWorker
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = self.StepsWorker(self.current_step,len(self.besuchte_routen)+1, self.velocity)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.worker.progress.connect(self.update_slider_Steps)
        # Step 6: Start the thread
        self.thread.start()
            
            
    def btn_stepFwd_clicked(self):
        print("Step forward!")

        self.stop_thread()

        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)

        if(self.current_step < len(self.besuchte_routen)+1):
            self.update_slider_Steps(self.current_step+1)
        else:
            print("Ende erreicht")

            
    def btn_end_clicked(self):
        print("Go to the end.")

        self.stop_thread()
        
        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)

        if(self.current_step < len(self.besuchte_routen)+1):
            self.update_slider_Steps(len(self.besuchte_routen)+1)
        else:
            print("Ende erreicht")
        
    ### Settings

    def btn_save_settings_clicked(self):
        print("Save settings.")
        self.background = str(self.ui.combo_background.currentText())
        self.eges_beschriftung = self.get_checked_radio_button(self.ui.groupbox_settings_edges).text()
        self.nodes_beschriftung = self.get_checked_radio_button(self.ui.groupbox_settings_nodes).text()

        # Karte neuladen
        self.plotStreetGraph()
        
    ## Funktionen:
        
    def get_checked_radio_button(self, groupBox):
        for widget in groupBox.findChildren(QtWidgets.QRadioButton):
            if widget.isChecked():
                return widget
        return None
    
    
    def plotRoutesSteps(self, routen, von, bis):

        if von < 0:
            return
        
        while von < bis:

            # Routen davor anders färben
            self.route_before_recolor(von, self.color_steps)
            
            # Flatten Routes  
            routes = [item for sublist in routen[von:(von+1)] for item in sublist]
            #print(routes)
            anzahl = len(routes) 
            if anzahl > 1:
                self.fig, self.ax, plots = self.plot_graph_routes(self.graph, routes, ax=self.ui.canvas.axes, route_colors=self.color_new_steps, route_linewidths=self.steps_linewidth, orig_dest_size=0,route_label=f'{von+1}', route_alpha=self.steps_alpha, draw_and_flush=False)
                self.plot_steps[von+1] = plots
            elif anzahl == 1:
                routes = routes[0]
                self.fig, self.ax, plot = self.plot_graph_route(self.graph, routes, ax=self.ui.canvas.axes, route_color=self.color_new_steps, route_linewidth=self.steps_linewidth, orig_dest_size=0,route_label=f'{von+1}', route_alpha=self.steps_alpha, draw_and_flush=False)
                self.plot_steps[von+1] = plot

            von = von+1
            #print(self.plot_steps)
        
        # Draw and Flush erst wenn alle Routen gezeichnet wurden
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        # Am Ende Route malen
        if von > len(self.besuchte_routen):
            self.route_before_recolor(von, self.color_steps)
            
            if self.found_path is not None and len(self.found_path)>0:
                self.fig, self.ax, plot = self.plot_graph_route(self.graph, self.found_path, ax=self.ui.canvas.axes, route_color=self.route_color, route_linewidth=self.route_linewidth, orig_dest_size=0,route_label='route', route_alpha=self.route_alpha)    
                self.plot_steps[von+1] = plot

    def plotRouteDemo(self):
        if self.ui.radio_weight_length.isChecked():
           self.weight = "length"  
        elif self.ui.radio_weight_duration.isChecked():
            self.weight = "travel_time"  
        else:
            self.weight = "length"
          
        # Demo Routenplannung wenn Start und Ziel gesetzt wurden
        if self.start is not None and self.end is not None:
            lines = reversed(self.ax.get_lines())
            for line in lines:
                label = line.get_label()
                if  label != "ende" and label != "start" and label != "route_punkte":
                    line.remove()
            route = ox.shortest_path(self.graph, self.start, self.end, weight=self.weight)
            self.fig, self.ax = ox.plot_graph_route(self.graph, route, ax=self.ui.canvas.axes, route_color=self.route_color, route_linewidth=self.route_linewidth, orig_dest_size=self.orig_dest_size,show=False,route_alpha=1)
        
    def delete_last_lines(self,step):
        '''
        Löschen direkt aus den gespeicherten Lines
        '''
        keys = []
        for key in self.plot_steps.keys():
            if key > step:
                keys.append(key)
        
        for key in keys:
            lines = self.plot_steps.pop(key)
            for line in lines:
                line.remove()
        
        self.route_before_recolor(step, self.color_new_steps)
     
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
                
    def stop_thread(self):
        if self.thread.isRunning():
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()
    
    def thread_finished(self):
        self.thread = QThread()
    
    def update_slider_Steps(self, current_step):
        if self.mutex_button_press.tryLock():
            self.ui.slider_Steps.setValue(current_step)
            if self.worker != None:
                self.worker.setSpeed(self.velocity)
            self.mutex_button_press.unlock()
        
    class StepsWorker(QObject):
        
        def __init__(self, start, ende, velocity):
            super().__init__()
            self.start = start
            self.ende = ende
            self.velocity = velocity
            self.running = True
            
        finished = Signal()
        progress = Signal(int)
        
        def run(self):
            if self.start < self.ende:
                while(self.start < self.ende and self.running ):
                    #print(self.start)
                    self.start += 1
                    self.progress.emit(self.start)
                    sleeptime = 1 / self.velocity
                    sleep(sleeptime)
            elif self.start > self.ende:
                while(self.start > 0 and self.running ):
                    #print(self.start)
                    self.start -= 1
                    self.progress.emit(self.start)
                    sleeptime = 1 / self.velocity
                    sleep(sleeptime)
                    
            self.finished.emit()
        
        def setSpeed(self, velocity):
            self.velocity = velocity
             
        def stop(self):
            self.running = False
            
    def set_graph(self,graph):
        self.graph = graph
        self.plotStreetGraph()
        
    def graph_thread_bbbox(self, north, south, east, west, network_type):
        
        if self.thread.isRunning():
            return
        
        self.thread = QThread()
        self.worker = self.GraphWorkerBbox(north, south, east, west, network_type)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.worker.graphed.connect(self.set_graph)
        
        self.progressDialog = QProgressDialog("Bitte warten...\nGraph wird geladen.", None, 0, 0)
        self.thread.started.connect(self.progressDialog.show)
        self.thread.finished.connect(self.progressDialog.hide)

        self.thread.start()
        
    class GraphWorkerBbox(QObject):
        
        def __init__(self, north, south, east, west, network_type):
            super().__init__()
            self.north = north
            self.south = south
            self.east = east
            self.west = west
            self.network_type = network_type
        
        graphed = Signal(object)
        finished = Signal()
        
        def run(self):
            graph = ox.graph_from_bbox(self.north, self.south, self.east, self.west, network_type=self.network_type)
            self.graphed.emit(graph)
            self.finished.emit()
            
        def setSpeed(self, velocity):
            pass
            
    def graph_thread_place(self, place, network_type):
        
        if self.thread.isRunning():
            return
        
        self.thread = QThread()
        self.worker = self.GraphWorkerPlace(place, network_type)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.worker.graphed.connect(self.set_graph)
       
        self.progressDialog = QProgressDialog("Bitte warten...\nGraph wird geladen.", None, 0, 0)
        self.progressDialog.setMinimumDuration(0)
        self.progressDialog.setValue(0)
        self.thread.started.connect(self.progressDialog.show)
        self.thread.finished.connect(self.progressDialog.hide)

        self.thread.start()
        
    class GraphWorkerPlace(QObject):
        
        def __init__(self, place, network_type):
            super().__init__()
            self.place = place
            self.network_type = network_type
        
        graphed = Signal(object)
        finished = Signal()
        
        def run(self):
            graph = ox.graph_from_place(self.place, network_type=self.network_type)
            self.graphed.emit(graph)
            self.finished.emit()
            
        def setSpeed(self, velocity):
            pass
    
    def graph_thread_polygon(self, polygon, network_type):

        if self.thread.isRunning():
            return
        
        self.thread = QThread()
        self.worker = self.GraphWorkerPolygon(polygon, network_type)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.worker.graphed.connect(self.set_graph)

        self.progressDialog = QProgressDialog("Bitte warten...\nGraph wird geladen.", None, 0, 0)
        self.thread.started.connect(self.progressDialog.show)
        self.thread.finished.connect(self.progressDialog.hide)
        
        self.thread.start()
        
    class GraphWorkerPolygon(QObject):
        
        def __init__(self, polygon, network_type):
            super().__init__()
            self.polygon = polygon
            self.network_type = network_type
        
        graphed = Signal(object)
        finished = Signal()
        
        def run(self):
            graph = ox.graph_from_polygon(self.polygon, self.network_type)
            self.graphed.emit(graph)
            self.finished.emit()
        
        def setSpeed(self, velocity):
            pass
    
    
    # Eigene Route Plot Funktionen aus OSMNX angepasst mit Plot Label und draw_and_flash option!
    def plot_graph_route(
        self,
        G,
        route,
        ax,
        route_color="r",
        route_linewidth=4,
        route_alpha=0.5,
        orig_dest_size=100,
        route_label="route",
        draw_and_flush=True,
    ):
        """
        Visualize a route along a graph.

        Parameters
        ----------
        G : networkx.MultiDiGraph
            input graph
        route : list
            route as a list of node IDs
        route_color : string
            color of the route
        route_linewidth : int
            width of the route line
        route_alpha : float
            opacity of the route line
        orig_dest_size : int
            size of the origin and destination nodes
        ax : matplotlib axis
            if not None, plot route on this preexisting axis instead of creating a
            new fig, ax and drawing the underlying graph
 
        Returns
        -------
        fig, ax, plot : tuple
            matplotlib figure, axis, line2D list
        """

        fig = ax.figure

        if orig_dest_size > 0:
            # scatterplot origin and destination points (first/last nodes in route)
            x = (G.nodes[route[0]]["x"], G.nodes[route[-1]]["x"])
            y = (G.nodes[route[0]]["y"], G.nodes[route[-1]]["y"])
            ax.scatter(x, y, s=orig_dest_size, c=route_color, alpha=route_alpha, edgecolor="none")

        # assemble the route edge geometries' x and y coords then plot the line
        x = []
        y = []
        for u, v in zip(route[:-1], route[1:]):
            # if there are parallel edges, select the shortest in length
            data = min(G.get_edge_data(u, v).values(), key=lambda d: d["length"])
            if "geometry" in data:
                # if geometry attribute exists, add all its coords to list
                xs, ys = data["geometry"].xy
                x.extend(xs)
                y.extend(ys)
            else:
                # otherwise, the edge is a straight line from node to node
                x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
                y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))
        
        #plot = None
        plot = ax.plot(x, y, c=route_color, lw=route_linewidth, alpha=route_alpha, label=route_label)

        if draw_and_flush:
            fig.canvas.draw()
            fig.canvas.flush_events()
        
        return fig, ax, plot
    
    def plot_graph_routes(
        self,
        G,
        routes,
        ax,
        route_colors="r",
        route_linewidths=4,
        route_label="route",
        route_alpha=0.5,
        draw_and_flush=True,
        orig_dest_size=0
        ):
        """
        Visualize several routes along a graph.

        Parameters
        ----------
        G : networkx.MultiDiGraph
            input graph
        routes : list
            routes as a list of lists of node IDs
        route_colors : string or list
            if string, 1 color for all routes. if list, the colors for each route.
        route_linewidths : int or list
            if int, 1 linewidth for all routes. if list, the linewidth for each route.

        Returns
        -------
        fig, ax, plots : tuple
            matplotlib figure, axis, lines2d list
        """
        
        # check for valid arguments
        if not all(isinstance(r, list) for r in routes):  # pragma: no cover
            msg = "routes must be a list of route lists"
            raise ValueError(msg)
        if len(routes) <= 1:  # pragma: no cover
            msg = "You must pass more than 1 route"
            raise ValueError(msg)
        if isinstance(route_colors, str):
            route_colors = [route_colors] * len(routes)
        if len(routes) != len(route_colors):  # pragma: no cover
            msg = "route_colors list must have same length as routes"
            raise ValueError(msg)
        if isinstance(route_linewidths, int):
            route_linewidths = [route_linewidths] * len(routes)
        if isinstance(route_linewidths, float):
            route_linewidths = [route_linewidths] * len(routes)
        if len(routes) != len(route_linewidths):  # pragma: no cover
            msg = "route_linewidths list must have same length as routes"
            raise ValueError(msg)

        fig = ax.figure
        
        plots = []
        r_rc_rlw = zip(routes[0:], route_colors[0:], route_linewidths[0:])
        for route, route_color, route_linewidth in r_rc_rlw:
            fig, ax, plot = self.plot_graph_route(
                G,
                route=route,
                route_color=route_color,
                route_linewidth=route_linewidth,
                ax=ax,
                route_alpha=route_alpha,
                route_label=route_label,
                draw_and_flush=False,
                orig_dest_size=orig_dest_size,
            )
            plots.append(plot[0])    
        
        if draw_and_flush:
            fig.canvas.draw()
            fig.canvas.flush_events()
            
        return fig, ax, plots
    
    def generateRoutes(self):
        
        self.update_slider_Steps(0)
        
        self.algo = self.get_checked_radio_button(self.ui.groupbox_algo).text()
        
        weight = self.get_checked_radio_button(self.ui.groupbox_weight).text()
        match weight:
            case 'Länge': self.weight = 'length'
            case 'Dauer': self.weight = 'travel_time'
            
        heuristik = self.get_checked_radio_button(self.ui.groupbox_heuristic).text()
        match heuristik:
            case '0': self.heuristik = '0'
            case 'Euclidean': self.heuristik = 'euklid'
            case 'Euclidean²': self.heuristik = 'eklid_quadrat'
            case 'Manhattan': self.heuristik = 'manhattan'
        
        if self.algo == "Dijkstra":
            print("Dijkstra")
            parent, self.besuchte_routen = dijkstra.dijkstra(self.graph, self.start, self.end, self.ui.checkbox_target.isChecked())
            self.found_path = dijkstra.make_path(parent, self.end)

        elif self.algo == "Greedy":
            print("Greedy")
            #self.besuchte_routen, self.found_path = greedy(self.graph, self.start, self.end)
            self.besuchte_routen, self.found_path = greedy(self.graph, self.start, self.end, metric=self.heuristik, weight=self.weight)

        elif self.algo == "A*":
            print("A*")
            self.besuchte_routen, self.found_path = astar(self.graph, self.start, self.end, metric=self.heuristik, weight=self.weight)
        
        print("Pfade erstellt")
        self.ui.slider_Steps.setMaximum(len(self.besuchte_routen)+1)
        self.ui.label_steps.setText(f"Schritte: {0} von {len(self.besuchte_routen)+1}")
        #print(self.besuchte_routen)
        print(self.found_path)
    
    def route_before_recolor(self,step,color):
        if (step) in self.plot_steps:
            for line in self.plot_steps[step]:
                line.set_color(color)