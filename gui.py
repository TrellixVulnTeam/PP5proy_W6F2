import wx
import pygame
import model

class VentanaMain(wx.Frame):
    """Frame de la ventana principal donde se elige jugar, ver las reglas, o cambiar el ptje ganador"""
    def __init__(self):
        super().__init__(None, title="10.000", size=(600, 500), style=wx.DEFAULT_FRAME_STYLE &
                                                                      ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.panel = wx.Panel(self)  # incia panel
        self.juego = model.Juego()  # instancia juego desde el modelo

        sizer = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        # titulo
        STextTitulo = wx.StaticText(self.panel, -1, "", style=wx.ALIGN_CENTER)  # texto titulo
        # quedo reemplazado por el titulo en el fondo, pero necesito el espacio vacio en el BoxSizer
        font = wx.Font(100, wx.ROMAN, wx.ITALIC, wx.NORMAL)  # fuente
        STextTitulo.SetFont(font)  # set fuente titulo
        STextTitulo.SetForegroundColour((200, 200, 200))  # color fondo

        # botones
        buttonIniciar = wx.Button(self.panel, -1, "Nueva partida", pos=(400, 200), size=(200, 50))  # boton empezar
        buttonCargar = wx.Button(self.panel, -1, "Cargar partida", pos=(400, 200), size=(200, 50))  # boton cargar
        buttonReglas = wx.Button(self.panel, -1, "Reglas", pos=(400, 200), size=(200, 50))  # boton ver reglas
        buttonRanking = wx.Button(self.panel, -1, "Ranking", pos=(400, 200), size=(200, 50))  # boton ver reglas

        # eventos de los botones
        self.panel.Bind(wx.EVT_BUTTON, self.onClickIniciar, buttonIniciar)
        self.panel.Bind(wx.EVT_BUTTON, self.onClickCargar, buttonCargar)
        self.panel.Bind(wx.EVT_BUTTON, self.onClickReglas, buttonReglas)
        self.panel.Bind(wx.EVT_BUTTON, self.onClickRanking, buttonRanking)

        # agrega titulo y botones al sizer
        sizer.Add(STextTitulo, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 50)
        sizer.Add(buttonIniciar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)
        sizer.Add(buttonCargar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)
        sizer.Add(buttonReglas, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)
        sizer.Add(buttonRanking, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)

        # fijar el sizer
        self.panel.SetSizer(sizer)
        self.Centre(True)

        # imagen de fondo
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.background)

    def onClickIniciar(self, event):
        """evento al hacer click en boton iniciar el juego
           abre la pantalla para elegir el puntaje ganador"""
        ventanaPuntos = VentanaPuntos(self.juego)  # le pasa el juego instanciado
        ventanaPuntos.Show()
        self.Close()

    def onClickCargar(self, event):
        frame = wx.Frame(None, -1, "Elegir partida")

        openFileDialog = wx.FileDialog(frame, "Abrir", "./assets/savedata", "Elegí una partida",
                                       "Partidas guardadas (*.sav)|*.sav",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:  # cerro la ventana sin elegir nada
            return  # vuelve al menu

        path = openFileDialog.GetPath()  # toma el path de la partida seleccionada
        partida = model.Partida.unpickle(path)  # deserializa el objeto partida
        ventana = VentanaJuego(partida.juego, partida.dados, partida.puntosTirada)  # abre ventana de partida
        ventana.Show()
        openFileDialog.Destroy()
        self.Close()

    def onClickReglas(self, event):
        """evento al hacer click en el boton de ver las reglas
           abre la pantalla que muestra las reglas"""
        ventanaReglas = VentanaReglas()
        ventanaReglas.Show()

    def onClickRanking(self, event):
        """evento al hacer click en el boton de ver el ranking
           abre la pantalla que muestra el ranking"""
        ventanaRanking = VentanaRanking()
        ventanaRanking.Show()

    def background (self, event):
        """Fija la imagen de fondo"""
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRegion(rect)
        dc.Clear()
        fondo = wx.Bitmap('./assets/fondo.bmp')
        dc.DrawBitmap(fondo, 0, 0)


class VentanaRanking(wx.Frame):
    """ventana que muestra las reglas del juego
       se abre al apretar el boton reglas en el menu principal"""
    def __init__(self):
        super().__init__(None, title="10.000 - Ranking", size=(350, 470), style = wx.DEFAULT_FRAME_STYLE &
                                                                                  ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.panel = wx.Panel(self)  # incia panel
        sizer = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        # fuente titulo
        STextTitulo = wx.StaticText(self, -1, "Ranking de puntajes", style=wx.ALIGN_CENTRE_HORIZONTAL)
        fontTitulo = wx.Font(18, wx.SWISS, wx.ITALIC, wx.BOLD)
        STextTitulo.SetFont(fontTitulo)

        # nombre: puntos ranking
        fontRanking = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL) # fuente
        y = 80  #  posicion en y para que salgan los nombres
        file = open("./assets/ranking.txt", "r")  # abrir el archivo

        line = file.readline()  # lee primera linea del archivo

        while line:  # !EOF
            # muestra linea
            wx.StaticText(self, -1, f"{line}", style=wx.ALIGN_LEFT, pos=(30, y), size=(200, -1)).SetFont(fontRanking)
            line = file.readline()  # siguiente linea
            y += 30  # baja posicion

        # agregar titulo al sizer
        sizer.Add(STextTitulo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 15)

        # fijar el sizer y color fondo
        self.SetSizer(sizer)
        self.SetBackgroundColour((184, 213, 222))
        self.Centre(True)


class VentanaReglas(wx.Frame):
    """ventana que muestra las reglas del juego
       se abre al apretar el boton reglas en el menu principal"""
    def __init__(self):
        super().__init__(None, title="10.000 - Reglas", size=(1080, 550), style = wx.DEFAULT_FRAME_STYLE &
                                                                                  ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana

        ##################################################################
        # panel con el texto
        ##################################################################
        panelSub = wx.Panel(self)  # incia panel
        sizerSub = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        # texto titulo y reglas
        STextTituloReglas = wx.StaticText(panelSub, -1, "Bienvenido al juego de los diez mil!", style=wx.ALIGN_CENTRE_HORIZONTAL)
        STextObjetivo = wx.StaticText(panelSub, -1,
                                    "OBJETIVO: \n\tLlegar al puntaje ganador. El puntaje ganador por defecto es 10.000. "
                                    " \nEl turno en el que algún jugador haya llegado al puntaje ganador es el turno final.",
                                    style=wx.ALIGN_LEFT, size=wx.Size(600,-1))

        STextComo = wx.StaticText(panelSub, -1,
                                    "\nCOMO JUGAR:\n\t Los jugadores toman turnos para tirar los 6 dados."
                                    " El jugador decide qué \ndados separar de su tirada para poder acumular puntos que dependerán del valor de los \ndados."
                                    " Los dados que no fueron seleccionados pueden volver a tirarse."
                                    " En ese punto, \nel jugador puede elegir dejar de tirar los dados y guardar los puntos acumulados en el turno,"
                                    " o volver a tirar los dados que no seleccionó para tratar de acumular más puntos \nen el turno."
                                    "\n\tSi en alguna tirada ninguno de los dados suma puntos, se toma el turno como pedido.",
                                    style=wx.ALIGN_LEFT, size=wx.Size(600,-1))

        STextPuntos = wx.StaticText(panelSub, -1,
                                    "\nPUNTAJE:\n\tLos 1 valen 100 puntos.\n\tLos 5 valen 50 puntos."
                                    " \n\tEn el caso de tener 3 dados del mismo valor, esos tres juntos valdrán el valor \n\tdel dado * 100."
                                    " \n\tPor ejemplo, 3 dados con valor 4 valen 400 puntos, y 3 dados con valor 1 \n\tvalen 1000 puntos."
                                    " \n\tCuando los 6 dados forman una escalera (1, 2, 3, 4, 5, 6) valen 2500 puntos.",
                                    style=wx.ALIGN_LEFT, size=wx.Size(600,-1))

        # fuentes del texto
        fontTitulo = wx.Font(18, wx.SWISS, wx.ITALIC, wx.BOLD)
        fontReglas = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        STextTituloReglas.SetFont(fontTitulo)
        STextObjetivo.SetFont(fontReglas)
        STextComo.SetFont(fontReglas)
        STextPuntos.SetFont(fontReglas)

        # agrega al sizer
        sizerSub.Add(STextTituloReglas, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 30)
        sizerSub.Add(STextObjetivo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 50)
        sizerSub.Add(STextComo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 50)
        sizerSub.Add(STextPuntos, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 50)

        # fija el sizer
        panelSub.SetSizer(sizerSub)
        panelSub.SetBackgroundColour((184, 213, 222))

        ##################################################################
        # panel principal
        ##################################################################
        sizerMain = wx.BoxSizer(wx.HORIZONTAL)  # inicia sizer

        # foto que indica puntos por dados
        bmp = wx.Bitmap("./assets/puntos.bmp", wx.BITMAP_TYPE_ANY)
        imgPuntos = wx.StaticBitmap(self, bitmap=bmp)

        # agrega al sizer
        sizerMain.Add(panelSub)
        sizerMain.Add(imgPuntos)

        # fija el sizer
        self.SetSizer(sizerMain)
        self.SetBackgroundColour((184, 213, 222))
        self.Centre(True)


class VentanaPuntos(wx.Frame):
    """ventana para cambiar el ptje ganador
       se abre al apretar el boton cambiar ptje ganador en la ventana principal"""
    def __init__(self, juego):  # toma el juego instanciado en la ventana principal
        super().__init__(None, title="10.000 - Cambiar puntaje ganador", size=(350, 270), style = wx.DEFAULT_FRAME_STYLE &
                                                                                                  ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.juego = juego

        ##################################################################
        # panel con el titulo y boton para volver al menu
        ##################################################################
        panelTitulo = wx.Panel(self)
        sizerTitulo = wx.BoxSizer(wx.HORIZONTAL)

        # boton volver atras (menu principal)
        bmp = wx.Bitmap("./assets/back_light.bmp", wx.BITMAP_TYPE_ANY)
        buttonBack = wx.BitmapButton(panelTitulo, -1, bmp, size=(25, 25))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickBack, buttonBack)

        # titulo y texto explicativo
        STextTituloPuntos = wx.StaticText(panelTitulo, -1, "Cambiar el puntaje ganador",
                                          style=wx.ALIGN_CENTRE_HORIZONTAL)

        # fuentes
        fontTitulo = wx.Font(15, wx.SWISS, wx.ITALIC, wx.BOLD)
        fontDescripcion = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        STextTituloPuntos.SetFont(fontTitulo)


        sizerTitulo.Add(buttonBack, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |wx.LEFT, 5)
        sizerTitulo.Add(STextTituloPuntos, 0, wx.ALIGN_CENTER_VERTICAL | wx. ALIGN_CENTER_HORIZONTAL | wx.LEFT, 15)
        panelTitulo.SetSizer(sizerTitulo)

        ##################################################################
        # panel con texto descriptivo sobre cambiar el puntaje ganador
        ##################################################################
        panelTexto = wx.Panel(self)  # inicia panel
        sizerTexto = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        STextDescripcion = wx.StaticText(panelTexto, -1,
                                         "\n\nA este puntaje debe llegarse para ganar.\nEl juego original usa el puntaje 10.000.",
                                         style=wx.ALIGN_LEFT)
        self.STextEstado = wx.StaticText(panelTexto, -1, "Ingresá el puntaje ganador: \n", style=wx.ALIGN_CENTRE)

        # fuentes
        STextDescripcion.SetFont(fontDescripcion)
        self.STextEstado.SetFont(fontDescripcion)

        # agrega al sizer
        sizerTexto.Add(STextDescripcion, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT | wx.BOTTOM, 20)
        sizerTexto.Add(self.STextEstado, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT, 50)

        # fija el sizer y color fondo
        panelTexto.SetSizer(sizerTexto)
        panelTexto.SetBackgroundColour((184, 213, 222))

        ##################################################################
        # panel con caja para escribir el nuevo puntaje y boton para cambiarlo
        ##################################################################
        panelIngreso = wx.Panel(self)  # incia panel
        sizerIngreso = wx.BoxSizer(wx.HORIZONTAL)  # incia sizer

        self.tCtrlPuntos = wx.TextCtrl(panelIngreso, -1)  # caja ingreso de texto para nuevo ptje
        buttonPuntos = wx.Button(panelIngreso, -1, "Confirmar")  # confirmar ingreso

        # agrega al sizer
        sizerIngreso.Add(self.tCtrlPuntos, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizerIngreso.Add(buttonPuntos, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 80)

        # evento del boton que genere el cambio de los puntos
        self.Bind(wx.EVT_BUTTON, self.onClickPuntos, buttonPuntos)

        # fija el sizer y el color de fondo
        panelIngreso.SetSizer(sizerIngreso)
        panelIngreso.SetBackgroundColour((184, 213, 222))

        ##################################################################
        # sizer principal de la ventana
        ##################################################################
        sizerMain = wx.BoxSizer(wx.VERTICAL)

        # agrega los paneles al sizer principal
        sizerMain.Add(panelTitulo, 0, wx.ALIGN_LEFT | wx.TOP, 20)
        sizerMain.Add(panelTexto, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizerMain.Add(panelIngreso, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

        # fija sizer principal de la ventana y color de fondo
        self.SetSizer(sizerMain)
        self.SetBackgroundColour((184, 213, 222))
        self.Centre(True)

    def onClickBack(self, event):
        """evento al hacer click en el boton atras, vuelve al menu principal"""
        ventana = VentanaMain()
        ventana.Show()
        self.Close()

    def onClickPuntos(self, event):
        """Toma el puntaje ingresado y lo cambia en el modelo
           despues abre la ventana de eleccion de jugadores"""
        try:  # ingreso int correcto
            ptje = int(self.tCtrlPuntos.GetValue())  # toma el valor de la caja de ingreso y castea a int
            self.juego.elegir_puntaje(ptje)  # fija nuevo puntaje en el juego

            ventana = VentanaJugadores(self.juego)  # abre ventana de elegir jugadores, pasa instancia de juego
            ventana.Show()
            self.Close()

        except:  # si no ingresa int pide reingreso
            self.STextEstado.SetForegroundColour((255, 0, 0))  # cambia letra a rojo
            self.STextEstado.SetLabel("Tenés que ingresar un número entero")
            self.tCtrlPuntos.Clear()  # borra numero ingresado en la caja de ingreso


class VentanaJugadores(wx.Frame):
    """ventana para elegir los jugadores antes de inciar el juego"""
    def __init__(self, juego):
        super().__init__(None, title="10.000 - Elegir jugadores", size=(550, 330), style = wx.DEFAULT_FRAME_STYLE &
                                                                                           ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.juego = juego  # instancia de juego recibida de ventana de puntaje ganador
        self.lista = []  # lista temporal en la que se agregan los jugadores para despues pasarsela al juego

        ##################################################################
        # panel con el titulo y boton para volver al menu
        ##################################################################
        panelTitulo = wx.Panel(self)
        sizerTitulo = wx.BoxSizer(wx.HORIZONTAL)

        # boton volver atras (menu principal)
        bmp = wx.Bitmap("./assets/back_light.bmp", wx.BITMAP_TYPE_ANY)
        buttonBack = wx.BitmapButton(panelTitulo, -1, bmp, size=(25, 25))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickBack, buttonBack)

        # titulo
        STextTitulo = wx.StaticText(panelTitulo, -1, "Agregar jugadores", style=wx.ALIGN_CENTRE_HORIZONTAL)
        fontTitulo = wx.Font(18, wx.SWISS, wx.ITALIC, wx.BOLD)
        STextTitulo.SetFont(fontTitulo)

        # agrega al sizer
        sizerTitulo.Add(buttonBack, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 7)
        sizerTitulo.Add(STextTitulo, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 140)
        panelTitulo.SetSizer(sizerTitulo)

        # texto descriptivo
        STextDescripcion = wx.StaticText(self, -1,
                                         "Ingresá el nombre del jugador que querés agregar y su tipo, y elegí\n"
                                         '"confirmar" para agregarlo. Cuando termines, elegí "finalizar".')
        fontDescripcion = wx.Font(13, wx.ROMAN, wx.BOLD, wx.NORMAL)
        STextDescripcion.SetFont(fontDescripcion)

        ##################################################################
        # panel con caja para ingresar nombre, menu con tipos de jugador y boton para agregar
        ##################################################################
        panelIngreso = wx.Panel(self)
        sizerIngreso = wx.BoxSizer(wx.HORIZONTAL)

        self.tCtrlNombre = wx.TextCtrl(panelIngreso, -1)  # caja ingreso de texto para nombre del jugador

        # menu con tipos para elegir
        tipo = ["Humano", "Máquina - Fácil", "Máquina - Normal", "Máquina - Difícil"] # lista para elegir tipo de jugador
        self.menu = wx.ComboBox(panelIngreso, choices=tipo, style=wx.CB_SIMPLE, size=(110, -1))  # menu elegir tipo jugador

        buttonConfirmar = wx.Button(panelIngreso, -1, "Confirmar")  # boton para agregar jugador

        # evento del boton que confirma
        self.Bind(wx.EVT_BUTTON, self.onClickConfirmar, buttonConfirmar)

        # agrega al sizer
        sizerIngreso.Add(self.tCtrlNombre, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizerIngreso.Add(self.menu, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 80)
        sizerIngreso.Add(buttonConfirmar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT, 80)

        # fija el sizer y el color de fondo
        panelIngreso.SetSizer(sizerIngreso)
        panelIngreso.SetBackgroundColour((184, 213, 222))

        # texto de estado (se agrego el jugador, tenes que elegir un tipo, etc)
        self.STextEstado = wx.StaticText(self, -1, " ", style= wx.ALIGN_CENTRE_HORIZONTAL)
        fontEstado = wx.Font(13, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.STextEstado.SetFont(fontEstado)

        # Boton finalizar y empezar a jugar
        buttonFinalizar = wx.Button(self, -1, "Finalizar")

        # evento del boton que confirma
        self.Bind(wx.EVT_BUTTON, self.onClickFinalizar, buttonFinalizar)

        ##################################################################
        # sizer principal de la ventana y agrega al sizer
        ##################################################################
        sizerMain = wx.BoxSizer(wx.VERTICAL)  # incia sizer

        # agrega elementos al sizer
        sizerMain.Add(panelTitulo, 0, wx.TOP, 10)
        sizerMain.Add(STextDescripcion, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM , 20)
        sizerMain.Add(panelIngreso, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        sizerMain.Add(self.STextEstado, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
        sizerMain.Add(buttonFinalizar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

        # fija sizer y color fondo
        self.SetBackgroundColour((184, 213, 222))
        self.SetSizer(sizerMain)
        self.Centre(True)

    def onClickBack(self, event):
        """evento al hacer click en el boton atras, vuelve al menu principal"""
        ventana = VentanaPuntos(self.juego)
        ventana.Show()
        self.Close()

    def onClickConfirmar(self, event):
        """toma el valor de la caja de ingreso de cdad de jugadores y tipo y agrega a lista temporal de jugadores"""
        nombre = self.tCtrlNombre.GetValue() # toma valor del nombre que se escribio en la caja
        tipo = self.menu.GetCurrentSelection()  # devuelve indice de lo que selecciono

        if self.menu.GetStringSelection(): # si la eleccion de tipo en el menu no es vacia (eligio un tipo)
            if nombre:  # ingreso nombre (no vacio)
                # 0 - Humano, 1 - Máquina (Fácil), 2 - Máquina (Normal), 3 - Máquina (Difícil)
                self.lista.append([nombre, tipo]) # agrego a la lista de jugadores
                self.STextEstado.SetForegroundColour((255, 0, 0))  # cambia letra a rojo
                self.STextEstado.SetLabel(f"Se agregó al jugador.")  # aviso
                self.tCtrlNombre.Clear()  # borra numero ingresado en la caja de ingreso

            else:  # nombre vacio
                self.STextEstado.SetForegroundColour((255, 0, 0))  # cambia letra a rojo
                self.STextEstado.SetLabel(f"Tenés que ingresar un nombre")  # aviso

        else:  # no eligio ningun tipo
            self.STextEstado.SetForegroundColour((255, 0, 0))  # cambia letra a rojo
            self.STextEstado.SetLabel("Tenés que elegir un tipo de jugador")  # aviso

    def onClickFinalizar(self, event):
        """envía la lista temporal de jugadores al modelo y abre la ventana del juego"""
        if not self.lista:  # todavia no se agrego ningun judador
            self.STextEstado.SetForegroundColour((255, 0, 0))  # cambia letra a rojo
            self.STextEstado.SetLabel("Tenés que agregar al menos un jugador")

        else:  # agrego al menos un jugador
            # envía la lista de jugadores al modelo
            self.juego.elegir_jugadores(self.lista)  # lista tipo [[nombre, tipo], [nombre2, tipo2]]

            # abre la ventana siguiente (pantalla del juego)

            # primera tirada, instancia 6 objetos dado en una lista
            dados = self.juego.primera_tirada()

            ventana = VentanaJuego(self.juego, dados, 0)  # pasa la instancia de juego, dados, puntos tirada (0)
            ventana.Show()
            self.Close()


class VentanaJuego(wx.Frame):
    """Ventana en la que se juega - indica jugador, ptos acumulados, y los dados"""
    def __init__(self, juego, dados, puntosTirada):
        super().__init__(None, title="10.000 - Jugar", size=(900, 500), style = wx.DEFAULT_FRAME_STYLE &
                                                                                ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana

        # musica de fondo
        pygame.mixer.init()  # inciar el mixer
        pygame.mixer.music.load("./assets/Sediment_Pool.wav")  # cargar archivo
        pygame.mixer.music.play(-1)  # reproducir en loop

        self.juego = juego  # instancia de juego recibida de ventana de jugadores
        self.juego.jugadorActual = self.juego.listaJugadores[0]  # pone como jugador actual al primer jugador de la lista
        self.puntosTirada = puntosTirada  # puntos que acumulan los dados seleccionados en la ronda actual
        self.dados = dados

        ##################################################################
        # panel que muestra nombre de la persona del turno
        ##################################################################
        panelNombre = wx.Panel(self)  # panel
        sizerNombre = wx.BoxSizer(wx.HORIZONTAL)  # sizer

        # texto descriptivo
        STextTurno = wx.StaticText(panelNombre, -1, "Turno de:", style=wx.ALIGN_LEFT)
        fontTurno = wx.Font(22, wx.ROMAN , wx.NORMAL, wx.NORMAL)
        STextTurno.SetFont(fontTurno)
        STextTurno.SetForegroundColour((200, 200, 200))

        # texto que indica el nombre del jugador
        self.STextNombre = wx.StaticText(panelNombre, -1, f"{self.juego.jugadorActual.nombre}",
                                         style=wx.ALIGN_LEFT, size=(200, -1))
        fontBold = wx.Font(22, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.STextNombre.SetFont(fontBold)
        self.STextNombre.SetForegroundColour((255, 255, 255))

        # boton para ir al menu principal
        bmp = wx.Bitmap("./assets/back_dark.bmp", wx.BITMAP_TYPE_ANY)
        buttonBack = wx.BitmapButton(panelNombre, -1, bmp, size=(25, 25), pos=(5, 5))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickBack, buttonBack)

        # agrega y fija al sizer
        sizerNombre.Add(buttonBack, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        sizerNombre.Add(STextTurno, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        sizerNombre.Add(self.STextNombre, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        panelNombre.SetSizer(sizerNombre)
        panelNombre.SetBackgroundColour((50, 80, 163))

        ##################################################################
        # panel que muestra puntos acumulados por el jugador
        ##################################################################
        panelPuntosA = wx.Panel(self)
        sizerPuntosA = wx.BoxSizer(wx.HORIZONTAL)

        # texto descriptivo
        STextPuntosAcum = wx.StaticText(panelPuntosA, -1, "Puntos acumulados: ", style=wx.ALIGN_LEFT)
        STextPuntosAcum.SetFont(fontTurno)
        STextPuntosAcum.SetForegroundColour((200, 200, 200))

        # texto que muestra puntos acumulados por el jugador
        self.STextPuntosA = wx.StaticText(panelPuntosA, -1, f"{str(self.juego.jugadorActual.puntosTotal)}",
                                          style=wx.ALIGN_CENTER_VERTICAL, size=(100, -1))
        self.STextPuntosA.SetFont(fontBold)
        self.STextPuntosA.SetForegroundColour((255, 255, 255))

        # agrega al sizer y fija sizer
        sizerPuntosA.Add(STextPuntosAcum, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 25)
        sizerPuntosA.Add(self.STextPuntosA, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        panelPuntosA.SetSizer(sizerPuntosA)
        panelPuntosA.SetBackgroundColour((50, 80, 163))

        ##################################################################
        # panel con la tirada de dados para elegir/tirar
        ##################################################################
        self.panelTirada = wx.Panel(self)
        sizerTirada = wx.BoxSizer(wx.HORIZONTAL)

        # boton para tirar los dados
        fontButton = wx.Font(15, wx.ROMAN, wx.BOLD, wx.NORMAL)
        self.buttonTirar = wx.Button(self.panelTirada, -1, "Tirar", size=(80, 40))
        self.buttonTirar.SetFont(fontButton)
        self.buttonTirar.SetBackgroundColour((79, 216, 137))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickTirar, self.buttonTirar)

        # imagenes para los dados y el espacio vacio
        self.vacio = wx.Bitmap("./assets/vacio.bmp", wx.BITMAP_TYPE_ANY)
        self.dado1 = wx.Bitmap("./assets/dado_1.bmp", wx.BITMAP_TYPE_ANY)
        self.dado2 = wx.Bitmap("./assets/dado_2.bmp", wx.BITMAP_TYPE_ANY)
        self.dado3 = wx.Bitmap("./assets/dado_3.bmp", wx.BITMAP_TYPE_ANY)
        self.dado4 = wx.Bitmap("./assets/dado_4.bmp", wx.BITMAP_TYPE_ANY)
        self.dado5 = wx.Bitmap("./assets/dado_5.bmp", wx.BITMAP_TYPE_ANY)
        self.dado6 = wx.Bitmap("./assets/dado_6.bmp", wx.BITMAP_TYPE_ANY)

        # para relacionar valor del dado con la imagen que corresponde
        self.dado_imagen = {
            1: self.dado1,
            2: self.dado2,
            3: self.dado3,
            4: self.dado4,
            5: self.dado5,
            6: self.dado6
                            }

        # crea los botones dados de tirada y verifica si estan guardados o no (si viene de juego cargado)
        self.inicializar_dados_tirada()

        # agrega al sizer
        sizerTirada.Add(self.buttonTirar, 0, wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, 20)
        sizerTirada.Add(self.buttonDado1, 0, wx.LEFT, 15)
        sizerTirada.Add(self.buttonDado2, 0, wx.LEFT, 15)
        sizerTirada.Add(self.buttonDado3, 0, wx.LEFT, 15)
        sizerTirada.Add(self.buttonDado4, 0, wx.LEFT, 15)
        sizerTirada.Add(self.buttonDado5, 0, wx.LEFT, 15)
        sizerTirada.Add(self.buttonDado6, 0, wx.LEFT, 15)

        # fija el sizer
        self.panelTirada.SetSizer(sizerTirada)
        self.panelTirada.SetBackgroundColour((50, 80, 163))

        ##################################################################
        # panel con los dados guardados
        ##################################################################
        self.panelGuardados = wx.Panel(self)
        sizerGuardados = wx.BoxSizer(wx.HORIZONTAL)

        # boton para guardar los puntos de la ronda
        self.buttonGuardar = wx.Button(self.panelGuardados, -1, "Guardar", size=(80, 40))
        self.buttonGuardar.SetFont(fontButton)
        self.buttonGuardar.SetBackgroundColour((162, 162, 162))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickGuardar, self.buttonGuardar)

        # crea los botones dados guardados y verifica si estan guardados o no (si viene de juego cargado)
        self.inicializar_dados_guardados()

        # agrega al sizer
        sizerGuardados.Add(self.buttonGuardar, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        sizerGuardados.Add(self.buttonDGuardado1, 0, wx.LEFT, 15)
        sizerGuardados.Add(self.buttonDGuardado2, 0, wx.LEFT, 15)
        sizerGuardados.Add(self.buttonDGuardado3, 0, wx.LEFT, 15)
        sizerGuardados.Add(self.buttonDGuardado4, 0, wx.LEFT, 15)
        sizerGuardados.Add(self.buttonDGuardado5, 0, wx.LEFT, 15)
        sizerGuardados.Add(self.buttonDGuardado6, 0, wx.LEFT, 15)

        # fija el sizer
        self.panelGuardados.SetSizer(sizerGuardados)
        self.panelGuardados.SetBackgroundColour((50, 80, 163))

        ##################################################################
        # textos puntos de dados guardados
        ##################################################################
        # texto descriptivo
        STextTituloPuntos = wx.StaticText(self, -1, "Puntos: ", style=wx.ALIGN_CENTER)
        STextTituloPuntos.SetFont(fontButton)
        STextTituloPuntos.SetForegroundColour((200, 200, 200))

        # texto que muestra puntos que acumulan los dados guardados
        self.STextPuntos = wx.StaticText(self, -1, f"{self.puntosTirada}", style=wx.ALIGN_CENTER)  # valor inicial, cambia al tirar dado
        fontPuntos = wx.Font(17, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.STextPuntos.SetFont(fontPuntos)
        self.STextPuntos.SetForegroundColour((255, 255, 255))

        ##################################################################
        # sizer principal de la ventana
        ##################################################################
        sizerMain = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        # agrega al sizer
        sizerMain.Add(panelNombre, 0, wx.ALIGN_LEFT | wx.BOTTOM, 10)
        sizerMain.Add(panelPuntosA, 0, wx.BOTTOM | wx.LEFT, 25)
        sizerMain.Add(self.panelTirada, 0, wx.BOTTOM, 15)
        sizerMain.Add(self.panelGuardados, 0, wx.BOTTOM, 15)
        sizerMain.Add(STextTituloPuntos, 0, wx.ALIGN_LEFT | wx.LEFT, 20)
        sizerMain.Add(self.STextPuntos, 0, wx.ALIGN_LEFT | wx.LEFT, 20)

        # fija sizer
        self.SetSizer(sizerMain)
        self.SetBackgroundColour((50, 80, 163))
        self.Centre(True)

        # boton para mutear/desmutear la musica de fondo
        # imagenes
        self.mute = wx.Bitmap("./assets/mute.bmp", wx.BITMAP_TYPE_ANY)
        self.unmute = wx.Bitmap("./assets/unmute.bmp", wx.BITMAP_TYPE_ANY)

        #boton
        self.buttonMute = wx.BitmapButton(self, -1, self.mute, size=(50, 50), pos=(800,50))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickMute, self.buttonMute)

        # boton para guardar la partida
        # imagen
        save = wx.Bitmap("./assets/save.bmp", wx.BITMAP_TYPE_ANY)
        buttonSave = wx.BitmapButton(self, -1, save, size=(50, 50), pos=(745, 50))

        # evento del boton
        self.Bind(wx.EVT_BUTTON, self.onClickSave, buttonSave)

        if isinstance(self.juego.jugadorActual, model.MaquinaConservador):
            self.turno_maquina()  # si la lista empieza con una maquina

    def inicializar_dados_tirada(self):
        # botones dado - verifica si estan guardados o no y pone la imagen correspondiente
        if not self.dados[0].guardado:
            self.buttonDado1 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[0].valor])
        else:
            self.buttonDado1 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        if not self.dados[1].guardado:
            self.buttonDado2 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[1].valor])
        else:
            self.buttonDado2 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        if not self.dados[2].guardado:
            self.buttonDado3 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[2].valor])
        else:
            self.buttonDado3 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        if not self.dados[3].guardado:
            self.buttonDado4 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[3].valor])
        else:
            self.buttonDado4 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        if not self.dados[4].guardado:
            self.buttonDado5 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[4].valor])
        else:
            self.buttonDado5 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        if not self.dados[5].guardado:
            self.buttonDado6 = wx.BitmapButton(self.panelTirada, -1, self.dado_imagen[self.dados[5].valor])
        else:
            self.buttonDado6 = wx.BitmapButton(self.panelTirada, -1, self.vacio)

        # eventos de botones dado
        self.Bind(wx.EVT_BUTTON, self.onClickDado1, self.buttonDado1)
        self.Bind(wx.EVT_BUTTON, self.onClickDado2, self.buttonDado2)
        self.Bind(wx.EVT_BUTTON, self.onClickDado3, self.buttonDado3)
        self.Bind(wx.EVT_BUTTON, self.onClickDado4, self.buttonDado4)
        self.Bind(wx.EVT_BUTTON, self.onClickDado5, self.buttonDado5)
        self.Bind(wx.EVT_BUTTON, self.onClickDado6, self.buttonDado6)

    def inicializar_dados_guardados(self):
        # botones dados guardados - verifica si estan guardados o no y le pone imagen correspondiente
        if self.dados[0].guardado:
            self.buttonDGuardado1 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[0].valor])
        else:
            self.buttonDGuardado1 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        if self.dados[1].guardado:
            self.buttonDGuardado2 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[1].valor])
        else:
            self.buttonDGuardado2 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        if self.dados[2].guardado:
            self.buttonDGuardado3 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[2].valor])
        else:
            self.buttonDGuardado3 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        if self.dados[3].guardado:
            self.buttonDGuardado4 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[3].valor])
        else:
            self.buttonDGuardado4 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        if self.dados[4].guardado:
            self.buttonDGuardado5 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[4].valor])
        else:
            self.buttonDGuardado5 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        if self.dados[5].guardado:
            self.buttonDGuardado6 = wx.BitmapButton(self.panelGuardados, -1, self.dado_imagen[self.dados[5].valor])
        else:
            self.buttonDGuardado6 = wx.BitmapButton(self.panelGuardados, -1, self.vacio)

        # eventos de botones dado guardado
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado1, self.buttonDGuardado1)
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado2, self.buttonDGuardado2)
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado3, self.buttonDGuardado3)
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado4, self.buttonDGuardado4)
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado5, self.buttonDGuardado5)
        self.Bind(wx.EVT_BUTTON, self.onClickDGuardado6, self.buttonDGuardado6)

    def turno_maquina(self):
        """Turno de un jugador no humano"""
        if isinstance(self.juego.jugadorActual, model.MaquinaConservador) or \
            isinstance(self.juego.jugadorActual, model.MaquinaNormal) or \
            isinstance(self.juego.jugadorActual, model.MaquinaAgresivo):  # si es un jugador maquina

                    valores = []  # valores de las caras de los dados de la tirada
                    eleccion = []  # indices de dados elegidos por la maquina
                    valoresGuardados = []  # valores de los dados elegidos

                    for dado in self.dados:
                        if not dado.guardado:
                            valores.append(dado.valor)  # guarda valores de la tirada de dados
                        else:
                            # si el dado esta guardado lo marco como 0 para que me coincidan los 6 indices
                            valores.append(0)

                    eleccion = self.juego.jugadorActual.elegir(valores)  # indices de los dados elegidos por la maquina

                    for indice in eleccion:
                        valoresGuardados.append(self.dados[indice].valor)  # toma valores de los dados elegidos

                        # marca dados como guardados
                        if indice == 0:
                            # simula apretar boton dado 1
                            evt1 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado1.GetId())
                            wx.PostEvent(self, evt1)

                        elif indice == 1:
                            # simula apretar boton dado 2
                            evt2 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado2.GetId())
                            wx.PostEvent(self, evt2)

                        elif indice == 2:
                            # simula apretar boton dado 3
                            evt3 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado3.GetId())
                            wx.PostEvent(self, evt3)

                        elif indice == 3:
                            # simula apretar boton dado 4
                            evt4 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado4.GetId())
                            wx.PostEvent(self, evt4)

                        elif indice == 4:
                            # simula apretar boton dado 5
                            evt5 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado5.GetId())
                            wx.PostEvent(self, evt5)

                        elif indice == 5:
                            # simula apretar boton dado 6
                            evt6 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonDado6.GetId())
                            wx.PostEvent(self, evt6)

                    # verifica si la maquina se planta o sigue tirando (sigue = True -> tira de vuelta)
                    sigue = self.juego.jugadorActual.seguir(self.juego.puntosRonda)

                    # instancia ventana que explica que dados eligio la maquina
                    ventana = VentanaMaquina(self.juego, valoresGuardados, sigue)
                    # dialogo que frena la ejecucion hasta que se cierre para que no pase tan rapido
                    ventana.ShowModal()

                    if sigue:
                        # simula el evento de apretar el boton tirar
                        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonTirar.GetId()))

                    else:
                        # simula el evento de apretar el boton guardar
                        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.buttonGuardar.GetId()))

    def refresh_pantalla_turno(self):
        """pasa el turno y refresca el nombre y puntos del jugador en pantalla"""
        # pasar el turno y mostrar el nombre y puntos del siguiente jugador
        self.juego.pasar_turno()  # pasa turno al siguiente jugador
        self.STextNombre.SetLabel(self.juego.jugadorActual.nombre)  # refresh nombre
        self.STextPuntosA.SetLabel(str(self.juego.jugadorActual.puntosTotal))  # refresh puntos acumulados

        # volver a vaciar los dados guardados
        self.buttonDGuardado1.SetBitmap(self.vacio)
        self.buttonDGuardado2.SetBitmap(self.vacio)
        self.buttonDGuardado3.SetBitmap(self.vacio)
        self.buttonDGuardado4.SetBitmap(self.vacio)
        self.buttonDGuardado5.SetBitmap(self.vacio)
        self.buttonDGuardado6.SetBitmap(self.vacio)

        # tirar los 6 dados de nuevo y reiniciar puntaje que acumulan los dados guardados
        self.STextPuntos.SetLabel("0")
        self.dados = self.juego.primera_tirada()

        if pygame.mixer.music.get_busy():  # si no se muteo la musica
            # efecto sonido dados tirados
            pygame.mixer.music.pause()  # pausa musica de fondo
            roll = pygame.mixer.Sound("./assets/dice_roll.wav")  # carga sonido
            pygame.mixer.Sound.play(roll)  # reproduce el sonido
            pygame.mixer.music.unpause()  # seguir musica de fondo

        # verifica si perdio turno con la nueva tirada
        if self.juego.turno_perdido([dado.valor for dado in self.dados]):
            ventana = VentanaTurnoPerdido()
            ventana.Show()
            self.juego.puntosRonda = 0
            self.refresh_pantalla_turno()  # vuelve a refrescar pantalla y pasar turno si perdio la tirada

        # refresca imagenes de los dados al valor correspondiente de la tirada nueva
        self.buttonDado1.SetBitmap(self.dado_imagen[self.dados[0].valor])
        self.buttonDado2.SetBitmap(self.dado_imagen[self.dados[1].valor])
        self.buttonDado3.SetBitmap(self.dado_imagen[self.dados[2].valor])
        self.buttonDado4.SetBitmap(self.dado_imagen[self.dados[3].valor])
        self.buttonDado5.SetBitmap(self.dado_imagen[self.dados[4].valor])
        self.buttonDado6.SetBitmap(self.dado_imagen[self.dados[5].valor])

        self.turno_maquina()  # verificar si sigue siendo el turno de la maquina

    def refresh_puntos_ronda(self):
        """calcula los puntos de la ronda segun los dados que esten guardados
           Se llama cuando se quieren volver a tirar los dados, para que no tome los dados ya guardados de un
           turno anterior como dados elegidos en el turno actual y sume mas puntos de los que deberia"""
        eleccion = []  # lista con valores de los dados elegidos

        for dado in self.dados:
            # el dado tiene que estar guardado y no se tiene que haber elegido una ronda anterior,
            # es decir que su puntaje ya fue "sumado" en una ronda anterior (en la que se eligio)
            if dado.guardado and not dado.sumado:
                eleccion.append(dado.valor)  # lo agrega como dado guardado a la lista
                dado.sumado = True  # marca que se sumo su puntaje en esta ronda

        if eleccion:  # eligio algun dado en la ronda
            # calcula puntos de los dados elegidos en la ronda actual y los suma a los puntos acumulados en el turno
            self.juego.puntosRonda += self.juego.calcular_puntos(eleccion)
            self.STextPuntos.SetLabel(str(self.juego.puntosRonda))  # refresca valor en la gui

    def calculo_puntos_ronda(self):
        """Calcula cuando valdran los dados elegidos en la ronda actual
           LLamada cuando se elige un dado para mostrar los puntos que daria la eleccion actual
           NO los marca como "sumados" hasta que se elija "guardar" y llame a la func refresh_puntos_ronda"""
        eleccion = []  # lista con valores de los dados

        for dado in self.dados:
            # el dado tiene que estar guardado y no se tiene que haber elegido una ronda anterior,
            # es decir que su puntaje ya fue "sumado" en una ronda anterior (en la que se eligio)
            if dado.guardado and not dado.sumado:
                eleccion.append(dado.valor)  # agrega valor a la lista

        self.puntosTirada = self.juego.calcular_puntos(eleccion)  # calcula puntos de dados elegidos en tirada actual
        tot = self.puntosTirada + self.juego.puntosRonda  # calcula cuanto valdria si los guarda
        self.STextPuntos.SetLabel(str(tot))  # refresca valor en la gui

    def onClickTirar(self, event):
        """Tira los dados que no estan guardados"""
        restantes = []  # lista con valores de los dados que se pueden volver a tirar

        if pygame.mixer.music.get_busy():  # si no se mutearon los sonidos
            # efecto sonido dados tirados
            pygame.mixer.music.pause()  # pausa musica de fondo
            roll = pygame.mixer.Sound("./assets/dice_roll.wav")  # carga sonido
            pygame.mixer.Sound.play(roll)  # reproduce el sonido
            pygame.mixer.music.unpause()  # seguir musica de fondo

        for dado in self.dados:
            if not dado.guardado:  # si el dado no esta guardado se puede volver a tirar
                restantes.append(dado.valor)  # agrega a la lista

        # refresca valor de los puntos acumulados por los dados elegidos en la ronda anterior
        # y los marca como "sumados" para que en la siguiente ronda no se vuelvan a sumar
        self.refresh_puntos_ronda()

        if all(dado.guardado for dado in self.dados):  # si todos los dados estan guardados tira de vuelta
            # volver a vaciar los dados guardados
            self.buttonDGuardado1.SetBitmap(self.vacio)
            self.buttonDGuardado2.SetBitmap(self.vacio)
            self.buttonDGuardado3.SetBitmap(self.vacio)
            self.buttonDGuardado4.SetBitmap(self.vacio)
            self.buttonDGuardado5.SetBitmap(self.vacio)
            self.buttonDGuardado6.SetBitmap(self.vacio)

            # tirar los 6 dados de nuevo
            self.dados = self.juego.primera_tirada()  # creo objeto dado nuevo apra que no queden los flags en True

            self.buttonDado1.SetBitmap(self.dado_imagen[self.dados[0].valor])
            self.buttonDado2.SetBitmap(self.dado_imagen[self.dados[1].valor])
            self.buttonDado3.SetBitmap(self.dado_imagen[self.dados[2].valor])
            self.buttonDado4.SetBitmap(self.dado_imagen[self.dados[3].valor])
            self.buttonDado5.SetBitmap(self.dado_imagen[self.dados[4].valor])
            self.buttonDado6.SetBitmap(self.dado_imagen[self.dados[5].valor])

        # tirada nueva (sin instanciar objetos dado de vuelta)
        else:
            self.dados = self.juego.tirar_dados(self.dados)

            # refresca imagen en boton dado
            if not self.dados[0].guardado:
                self.buttonDado1.SetBitmap(self.dado_imagen[self.dados[0].valor])

            if not self.dados[1].guardado:
                self.buttonDado2.SetBitmap(self.dado_imagen[self.dados[1].valor])

            if not self.dados[2].guardado:
                self.buttonDado3.SetBitmap(self.dado_imagen[self.dados[2].valor])

            if not self.dados[3].guardado:
                self.buttonDado4.SetBitmap(self.dado_imagen[self.dados[3].valor])

            if not self.dados[4].guardado:
                self.buttonDado5.SetBitmap(self.dado_imagen[self.dados[4].valor])

            if not self.dados[5].guardado:
                self.buttonDado6.SetBitmap(self.dado_imagen[self.dados[5].valor])

        # checkea si los dados que tiro pueden sumar puntos o se pierde el turno
        dadosTirados = []  # lista con valores de los dados que se acaban de tirar

        for dado in self.dados:
            if not dado.guardado:
                dadosTirados.append(dado.valor)  # guarda valor del dado si no esta guardado (se tiro de vuelta)

        if self.juego.turno_perdido(dadosTirados):  # dados no suman puntos (se pierde el turno)
            ventana = VentanaTurnoPerdido()  # muestra ventana diciendo que se perdio el turno
            ventana.Show()
            self.juego.puntosRonda = 0  # pierde los puntos acumulados
            self.refresh_pantalla_turno()  # pasa turno

        self.turno_maquina()  # verifica si es el turno de la maquina

    def onClickGuardar(self, event):
        """Le agrega los puntos al jugador que fueron acumulados en la ronda por los dados guardados"""
        self.juego.puntosRonda += self.puntosTirada  # agrega los puntos que suman los dados elegidos en la ultima tirada
        self.juego.agregar_puntos()  # agrega los puntos acumulados en el turno al jugador

        # verifica si gano el jugador
        if self.juego.jugadorActual.puntosTotal >= self.juego.puntajeGanador:
            # para la musica
            # no pongo stop pq confirmo en ventanaGanador si se mutearon o no los sonidos
            # evaluando pygame.mixer.music.get_busy() que devuelve True si esta pausada
            # y False si estaba parada (pygame.mixer.music.stop())
            pygame.mixer.music.pause()

            # abre la ventana que indica que es el ganador, le pasa el jugador que gano
            ventana = VentanaGanador(self.juego.jugadorActual)
            ventana.Show()
            self.Destroy()  # cierra la ventana de juego actual

        else: # si no gano el jugador
            self.juego.puntosRonda = 0  # reset puntos de la ronda
            self.STextPuntos.SetLabel("0")  # reset gui
            self.refresh_pantalla_turno()  # pasa turno y refresca gui

    def onClickDado1(self, event):
        """evento al hacer click en el primer dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[0].guardado:  # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[0].guardado = True  # lo marca como guardado
            bmp = self.buttonDado1.GetBitmap()  # toma imagen del dado
            self.buttonDado1.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado1.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDado2(self, event):
        """evento al hacer click en el segundo dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[1].guardado: # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[1].guardado = True  # lo marca como guardado
            bmp = self.buttonDado2.GetBitmap() # toma imagen del dado
            self.buttonDado2.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado2.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDado3(self, event):
        """evento al hacer click en el tercer dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[2].guardado:  # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[2].guardado = True  # lo marca como guardado
            bmp = self.buttonDado3.GetBitmap()  # toma imagen del dado
            self.buttonDado3.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado3.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDado4(self, event):
        """evento al hacer click en el cuarto dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[3].guardado:  # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[3].guardado = True  # lo marca como guardado
            bmp = self.buttonDado4.GetBitmap()  # toma imagen del dado
            self.buttonDado4.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado4.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDado5(self, event):
        """evento al hacer click en el quinto dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[4].guardado:  # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[4].guardado = True  # lo marca como guardado
            bmp = self.buttonDado5.GetBitmap()  # toma imagen del dado
            self.buttonDado5.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado5.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDado6(self, event):
        """evento al hacer click en el sexto dado de la tirada
           lo pasa a los dados guardados y actualiza la imagen a un espacio vacio"""
        if not self.dados[5].guardado:  # no hace nada si el dado esta guardado (osea que es un espacio vacio)
            self.dados[5].guardado = True  # lo marca como guardado
            bmp = self.buttonDado6.GetBitmap()  # toma imagen del dado
            self.buttonDado6.SetBitmap(self.vacio)  # cambia por imagen de espacio vacio
            self.buttonDGuardado6.SetBitmap(bmp)  # pasa imagen a los dados guardados

            self.calculo_puntos_ronda()  # calcula puntos de los dados elegidos en la ronda

    def onClickDGuardado1(self, event):
        """evento al hacer click en el primer dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[0].guardado and not self.dados[0].sumado: 
            bmp = self.buttonDGuardado1.GetBitmap()  # toma imagen del dado que se guardo
            self.buttonDado1.SetBitmap(bmp)  # cambia la imagen
            self.buttonDGuardado1.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[0].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickDGuardado2(self, event):
        """evento al hacer click en el segundo dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[1].guardado and not self.dados[1].sumado:
            self.buttonDado2.SetBitmap(self.buttonDGuardado2.GetBitmap())  # cambia imagen del dado que se guardo
            self.buttonDGuardado2.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[1].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickDGuardado3(self, event):
        """evento al hacer click en el tercer dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[2].guardado and not self.dados[2].sumado:
            self.buttonDado3.SetBitmap(self.buttonDGuardado3.GetBitmap())  # cambia imagen del dado que se guardo
            self.buttonDGuardado3.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[2].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickDGuardado4(self, event):
        """evento al hacer click en el cuarto dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[3].guardado and not self.dados[3].sumado:
            self.buttonDado4.SetBitmap(self.buttonDGuardado4.GetBitmap())  # cambia imagen del dado que se guardo
            self.buttonDGuardado4.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[3].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickDGuardado5(self, event):
        """evento al hacer click en el quinto dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[4].guardado and not self.dados[4].sumado:
            self.buttonDado5.SetBitmap(self.buttonDGuardado5.GetBitmap())  # cambia imagen del dado que se guardo
            self.buttonDGuardado5.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[4].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickDGuardado6(self, event):
        """evento al hacer click en el sexto dado guardado
           lo pasa a los dados de la tirada y actualiza la imagen a un espacio vacio
           si fue guardado en esa misma ronda (funciona como un "undo" de haber elegido cierto dado)"""
        # no hace nada si el dado fue guardado en una ronda anterior (sumado)
        if self.dados[5].guardado and not self.dados[5].sumado:
            self.buttonDado6.SetBitmap(self.buttonDGuardado6.GetBitmap())  # cambia imagen del dado que se guardo
            self.buttonDGuardado6.SetBitmap(self.vacio)  # lo vuelve a poner como vacio
            self.dados[5].guardado = False  # le cambia el valor de guardado

            self.calculo_puntos_ronda()  # calcula de nuevo puntos de los dados guardados

    def onClickMute(self, event):
        """evento al hacer click en el boton mute, frena la reproduccion de la musica y sonidos"""
        if pygame.mixer.music.get_busy(): # si esta la musica reproduciendose
            pygame.mixer.music.fadeout(800)  # frena la musica
            self.buttonMute.SetBitmap(self.unmute)  # cambia el boton a unmute

        else:  # la musica esta parada
            pygame.mixer.music.play()  # reproduce la musica
            self.buttonMute.SetBitmap(self.mute)  # cambia el boton a mute

    def onClickSave(self, event):
        """Evento al hacer click en el boton guardar, guarda partida
           abre ventana para elegir path y nombre de archivo"""
        frame = wx.Frame(None, -1, "Guardar partida")  # incia frame

        # inicia dialog (file explorer) para elegir donde guardar y con que nombre.
        # por defecto aparece en el path ./assets/savedata
        # pregunta si se quiere sobreescribir si ya existe el archivo
        saveFileDialog = wx.FileDialog(frame, "Guardar", "./assets/savedata", "-Elegí un nombre-",
                                       "Partidas guardadas (*.sav)|*.sav",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:  # cerro la ventana sin elegir nada
            return  # vuelve al juego

        path = saveFileDialog.GetPath()  # toma el path de la partida seleccionada
        objeto = model.Partida(self.juego, self.dados, self.puntosTirada)  # crea objeto partida
        model.Partida.pickle(path, objeto)  # serializa el objeto en el archivo

        saveFileDialog.Destroy()

    def onClickBack(self, event):
        """evento al hacer click en el boton atras, vuelve al menu principal"""
        ventana = VentanaMain()
        ventana.Show()
        pygame.mixer.music.stop()
        self.Close()

class VentanaMaquina(wx.Dialog):
    """Ventana que muestra que dados eligio la maquina en su turno
       Es un dialogo que frena la ventana del juego hasta que se cierre, para que no pase tan rapido el turno
       y no se entienda que paso en el turno de la maquina"""
    def __init__(self, juego, eleccion, sigue):
        super().__init__(None, title="10.000 - Turno", size=(400, 200), style = wx.DEFAULT_FRAME_STYLE &
                                                                                ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        posic = wx.Point(800, 150)  # posicion de la ventana para que no tape la tirada
        self.Move(posic)  # mueve a la posicion
        self.Update()  # mueve a la posicion

        self.panel = wx.Panel(self)  # inicia panel
        sizer = wx.BoxSizer(wx.VERTICAL)  # incia sizer

        self.juego = juego  # clase juego que hereda de VentanaJuego

        # texto descriptivo
        STextTitulo = wx.StaticText(self, -1, f"{self.juego.jugadorActual.nombre} elige los dados:",
                                    style=wx.ALIGN_CENTER_HORIZONTAL)
        fontTitulo = wx.Font(16, wx.SWISS, wx.ITALIC, wx.NORMAL)
        STextTitulo.SetFont(fontTitulo)

        # texto que muestra la eleccion de la maquina
        STextEleccion = wx.StaticText(self, -1, " ", style=wx.ALIGN_CENTER_HORIZONTAL)
        fontEleccion = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        STextEleccion.SetFont(fontEleccion)
        STextEleccion.SetForegroundColour((255, 0, 0))

        if eleccion:  # si eligio algun dado (pasada por VentanaJuego)
            STextEleccion.SetLabel(f"{eleccion}")  # muestra lista con valores de dados elegidos
        else:
            STextEleccion.SetLabel("ninguno")  # no eligio ningun dado (para que no muestre "[]")

        # texto que indica si la maquina sigue tirando o se planta
        STextSeguir = wx.StaticText(self, -1, " ", style=wx.ALIGN_LEFT)
        STextSeguir.SetFont(fontTitulo)

        if sigue:  # si sigue tirando (pasado por VentanaJuego)
            STextSeguir.SetLabel("Y sigue tirando los dados.")
        else:  # si deja de tirar
            STextSeguir.SetLabel("y deja de tirar.")

        # agrega al sizer
        sizer.Add(STextTitulo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer.Add(STextEleccion, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(STextSeguir, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        # fija sizer y color fondo
        self.SetSizer(sizer)
        self.SetBackgroundColour((184, 213, 222))

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)  # evento cerrar la ventana

    def onCloseWindow(self, event):
        self.Destroy()  # vuelve ejecucion de la ventana principal


class VentanaTurnoPerdido(wx.Dialog):
    """Ventana que indica que se perdio el turno porque la tirada no suma puntos"""
    def __init__(self):
        super().__init__(None, title="10.000 - Turno perdido", size=(400, 150), style = wx.DEFAULT_FRAME_STYLE &
                                                                                        ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))  # incia frame
        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.panel = wx.Panel(self)  # inicia panel
        posic = wx.Point(700, 150)  # posicion (para que no tape la tirada)
        self.Move(posic)  # mueve a posicion
        self.Update()  # mueve a posicion
        sizer = wx.BoxSizer(wx.VERTICAL)  # inicia sizer

        # texto explicativo
        STextTitulo = wx.StaticText(self, -1, "La tirada no suma puntos;",
                                    style=wx.ALIGN_CENTER_HORIZONTAL)
        fontTitulo = wx.Font(18, wx.SWISS, wx.ITALIC, wx.NORMAL)
        STextTitulo.SetFont(fontTitulo)
        STextTitulo.SetForegroundColour((255, 255, 255))

        STextTPer = wx.StaticText(self, -1, "perdiste el turno.",
                                    style=wx.ALIGN_CENTER_HORIZONTAL)
        fontTPer = wx.Font(18, wx.SWISS, wx.ITALIC, wx.BOLD)
        STextTPer.SetFont(fontTPer)
        STextTPer.SetForegroundColour((255, 0, 0))

        # agrega al sizer
        sizer.Add(STextTitulo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer.Add(STextTPer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # fija el sizer y color fondo
        self.SetSizer(sizer)
        self.SetBackgroundColour((50, 80, 163))

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)  # evento cerrar la ventana

    def onCloseWindow(self, event):
        self.Destroy()  # cierra ventana


class VentanaGanador(wx.Frame):
    """Ventana que aparece cuando gana un jugador"""
    def __init__(self, ganador):
        super().__init__(None, title="10.000 - Ganaste!", size=(400, 200), style = wx.DEFAULT_FRAME_STYLE &
                                                                                   ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        if pygame.mixer.music.get_busy():  # si no se muteo la musica
            # sonido
            jingle = pygame.mixer.Sound("./assets/GK2_jingle.wav")  # carga el sonido
            pygame.mixer.Sound.play(jingle) # reproduce el sonido

        self.SetIcon(wx.Icon("./assets/icon.ico", wx.BITMAP_TYPE_ICO))  # icono de la ventana
        self.ganador = ganador  # recibe jugador ganador de la ventana del juego
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # texto que muestra nombre del jugador que gano
        STextGanador = wx.StaticText(self, -1, "", style=wx.ALIGN_CENTER, size=(350, -1))
        STextGanador.SetLabel(str(self.ganador.nombre))
        font = wx.Font(50, wx.ROMAN, wx.ITALIC, wx.NORMAL)  # fuente
        STextGanador.SetFont(font)

        # texto explicativo
        STextGanaste = wx.StaticText(self, -1, "Ganaste!", style=wx.ALIGN_CENTER)  # texto
        STextGanaste.SetFont(font)  # set fuente titulo
        STextGanaste.SetForegroundColour((75, 75, 75))  # color

        # agrega al sizer
        sizer.Add(STextGanador, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(STextGanaste, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # fija el sizer
        self.SetSizer(sizer)
        self.SetBackgroundColour((184, 213, 222))
        self.Centre(True)

        ventana = VentanaMain()  # abre la pantalla principal de vuelta para volver a jugar
        ventana.Show()

        # grabar en el ranking - nombre: puntos
        cantidad = len(open("./assets/ranking.txt", "r").readlines())  # veo cuantas lineas hay

        if cantidad < 10:  # no hay 10 entradas en el ranking
            file = open("./assets/ranking.txt", "a")  # append
            entry = str(self.ganador.nombre) + ": " + str(self.ganador.puntosTotal)+ "\n"  # formato
            file.writelines(entry) # agrega al final del ranking
            file.close()  # cierra el archivo

        else:  # ya hay 10 entradas, tiene que sobreescribir la ultima si el puntaje es mayor
            file = open("./assets/ranking.txt", "r")  # abre el archivo, modo lectura
            nuevo = self.ganador.puntosTotal  # guarda el puntaje del jugador que gano recien

            ultimo = file.readlines()[-1]  # toma la ultima linea en el archivo
            ultimo = int(ultimo.split(": ")[1].split("\n")[0])  # toma el valor

            file.close()  # cierra el archivo
            if nuevo > ultimo:  # si el que acaba de ganar el juego recien hizo mas puntos que el mas bajo del ranking
                file = open("./assets/ranking.txt", "r")
                entry = str(self.ganador.nombre) + ": " + str(self.ganador.puntosTotal) + "\n"

                lines = file.readlines()  # lee todas las lineas del archivo
                lines[9] = entry  # cambia la ultima linea por la del ganador de recien
                file.close()  # cierra archivo

                file = open("./assets/ranking.txt", "w")  # abre archivo en modo escritura
                file.writelines(lines)  # reescribe ranking con la linea cambiada
                file.close()  # cierra el archivo

        self.ordenar_ranking()  # ordena ranking por puntos

    def ordenar_ranking(self):
        """Ordena el ranking segun mayor puntaje"""
        file = open("./assets/ranking.txt", "r")  # abre modo lectura
        lista = []

        for line in file:  # !EOF
            lista.append(line)  # agrega linea por linea a una lista

        lista.sort(key=lambda x: int(x.split(": ")[1].split("\n")[0]), reverse=True)  # ordena lista por puntajes

        file.close()  # cierra el archivo
        file = open("./assets/ranking.txt", "w")  # abre modo escritura
        file.writelines(lista)  # reescribe lista ordenada


# mainloop
if __name__ == '__main__':
    app = wx.App(False)
    frame = VentanaMain()
    frame.Show()
    app.MainLoop()
