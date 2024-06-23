import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listaAnni = []
        self.listaSquadre = []
        self.salariTeam = {}

        self.grafo = nx.Graph()
        self.nodi = []
        self.edge = []
        self.idMap = {}

        self._bestPath = []
        self._bestWeight = 0

        self.loadAnni()

    def getBestPath(self, inizio):
        self._bestPath = []
        self._bestWeight = 0

        parziale = [self.idMap[inizio]]
        peso = 0
        listaPesi = []
        self._ricorsione(parziale, peso, listaPesi)

        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale, peso, listaPesi):
        if peso > self._bestWeight:
            self._bestWeight = peso
            self._bestPath = copy.deepcopy(parziale)

        vicini = sorted(self.grafo[parziale[-1]], key=lambda x: self.grafo[parziale[-1]][x]['weight'], reverse=True)

        for v in vicini:
            p = self.grafo[parziale[-1]][v]['weight']
            if v not in parziale and (not listaPesi or self.grafo[parziale[-1]][v]['weight'] <= min(listaPesi)):
                listaPesi.append(self.grafo[parziale[-1]][v]['weight'])
                peso += self.grafo[parziale[-1]][v]['weight']
                parziale.append(v)
                self._ricorsione(parziale, peso, listaPesi)
                peso -= self.grafo[parziale[-2]][parziale[-1]]['weight']
                listaPesi.pop()
                parziale.pop()

    def loadAnni(self):
        self.listaAnni = DAO.getAnni()

    def loadSquadre(self, anno):
        self.listaSquadre = DAO.getSquadre(anno)

    def getSalari(self, anno):
        salari = DAO.getSalari(anno)
        for s in salari:
            self.salariTeam[s[0]] = s[1]

    def getDettagli(self, nodo_iniziale):
        listaDettagli = []
        v0 = self.idMap[nodo_iniziale]
        for n in self.grafo[v0]:
            listaDettagli.append((n, self.grafo[v0][n]['weight']))

        listaDettagli = sorted(listaDettagli, key=lambda x: x[1], reverse=True)

        return listaDettagli

    def buildGraph(self):
        self.grafo.clear()
        self.grafo.add_nodes_from(self.listaSquadre)
        for s in self.listaSquadre:
            self.nodi.append(s)
            self.idMap[s.ID] = s

        for i in range(len(self.nodi) - 1):
            for j in range(i + 1, len(self.nodi)):
                salario = self.salariTeam[self.nodi[i].ID] + self.salariTeam[self.nodi[j].ID]
                self.grafo.add_edge(self.nodi[i], self.nodi[j], weight=salario)
                self.edge.append((self.nodi[i], self.nodi[j]))

    def getGraphSize(self):
        return len(self.nodi), len(self.edge)
