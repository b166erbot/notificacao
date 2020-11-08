from psutil import virtual_memory
from time import sleep
import gi
from threading import Thread
from datetime import datetime, timedelta, date, time  # noqa
from json import load
gi.require_version('Notify', '0.7')
from gi.repository import Notify  # noqa


class Notificacao:
    def __init__(self, urgencia, *args, **kwargs):
        Notify.init(args[0])
        self.notificacao = Notify.Notification.new(*args, **kwargs)
        self.notificacao.set_urgency(urgencia)

    def rodar(self, vezes=1):
        for a in range(vezes):
            self.notificacao.show()
            sleep(20)


class AlertMemory(Notificacao):
    def rodar(self):
        while True:
            if virtual_memory()[2] >= 90:
                self.notificacao.show()
                sleep(10)
            sleep(5)


class AgendarTarefas:
    def __init__(self, tarefas: dict):
        self.tarefas = tarefas

    def rodar(self):
        hoje = datetime.combine(date.today(), time())
        for nome, hora in self.tarefas.items():
            temp = dict(zip(('hours', 'minutes'), hora))
            self.tarefas[nome] =  timedelta(**temp)
        self.tarefas = dict(sorted(
            self.tarefas.items(), key=(lambda item: item[1]), reverse=True
        ))
        while self.tarefas:
            nome, delta = self.tarefas.popitem()
            tempo = (hoje + delta) - datetime.now()
            if tempo.total_seconds() >= 0:
                print(f'{nome} em: {tempo}')
                sleep(tempo.total_seconds())
                Notificacao(2, nome).rodar()


class ProcessosParalelos:
    def __init__(self, funcoes: tuple):
        self.processos = []
        for a in funcoes:
            temp = Thread(target=a.rodar, name=a.rodar.__name__, daemon=True)
            self.processos.append(temp)

    def __getitem__(self, index):
        return self.processos[index]

    def __iter__(self):
        return iter(self.processos)

    def rodar(self):
        for processo in self.processos:
            processo.start()
        self.processos[0].join()


def main():
    print('para encerrar o programa, precione ctrl + c\n')
    with open('src/agenda.json') as arquivo:
        afazeres = load(arquivo)
    alerta = AlertMemory(
        2, 'aviso de memória cheia', 'sua memória está lotada!'
    )
    afazeres = dict(sorted(afazeres.items(), key=lambda x: x[1]))
    agenda = AgendarTarefas(afazeres)
    ProcessosParalelos((alerta, agenda)).rodar()
