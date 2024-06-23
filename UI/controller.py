import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        anni = self._model.listaAnni
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

    def fillTeam(self,e):
        anno = self._view.ddyear.value
        self._model.loadSquadre(anno)
        squadre = self._model.listaSquadre

        self._view.txtOut.clean()
        self._view.txtOut.controls.append(ft.Text(f"Squadre presente nell'anno {anno} = {len(squadre)}"))
        for s in squadre:
            self._view.ddteam.options.append(ft.dropdown.Option(key=s.ID, text=s))
            self._view.txtOut.controls.append(ft.Text(f"{s.teamCode} ({s.name})"))

        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        self._model.getSalari(anno)
        self._model.buildGraph()
        nN, nE = self._model.getGraphSize()
        self._view.txtOut2.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))
        self._view.update_page()

    def details(self, e):
        iniziale = int(self._view.ddteam.value)
        dettagli = self._model.getDettagli(iniziale)
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Adiacenti per la squadra {self._model.idMap[iniziale]}"))
        for d in dettagli:
            self._view.txtOut2.controls.append(ft.Text(f"{d[0]}       {d[1]}"))

        self._view.update_page()

    def handle_search(self, e):
        self._view.txtOut2.clean()
        bestPath, bestWeight = self._model.getBestPath(int(self._view.ddteam.value))
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Peso percorso ottimo {bestWeight}"))
        for i in range(len(bestPath)-1):
            self._view.txtOut2.controls.append(ft.Text(f"Team: {bestPath[i].ID} --> {bestPath[i+1].ID}- peso= {self._model.salariTeam[bestPath[i].ID] + self._model.salariTeam[bestPath[i+1].ID]}"))

        self._view.update_page()