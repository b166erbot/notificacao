#!/usr/bin/python3
from src.ferramentas import main
from contextlib import suppress
from os.path import exists
from os import chdir, remove
from pathlib import Path


if __name__ == '__main__':
    local_deste_arquivo = Path(__file__).parent
    chdir(local_deste_arquivo)
    if exists('/tmp/mensagens.lock'):
        print('o programa já esta rodando. saindo.')
        exit()
    else:
        with open('/tmp/mensagens.lock', 'w') as arquivo:
            arquivo.write('lock')
    with suppress(KeyboardInterrupt, EOFError):
        main()
    print('\nprograma finalizado')
    remove('/tmp/mensagens.lock')
