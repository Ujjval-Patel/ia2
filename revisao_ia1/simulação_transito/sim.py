#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 22/07/18 at 13:55
"""
import os
import time
import random


def tem_espaco(trecho):
    return trecho.count(0) > 0


def atualiza_trecho(idt, cid, sinals, slots):
    # TODO: considerar sinals
    pode_alimentar = False  # a partir do semáforo que precede
    pode_liberar = False  # a partir do semáforo que sucede
    pode_atualizar = False  # avaliando total de bits ativos

    # TODO: em vez do valor 4 usar total_semaforos

    # Tem espaço OU semáforo à frente está (verde E vazio)
    if tem_espaco(cid[idt]) or (sinals[(idt+1) % 4] and not slots[(idt+1) % 4][0]):
        pode_atualizar = True

    # Semáforo pode alimentar E (trecho tem espaço OU vai liberar espaço)
    if slots[idt][0] and (tem_espaco(cid[idt]) or not slots[(idt+1) % 4][0]):
        pode_alimentar = True

    # Semáforo vazio e trecho com último bit ativo
    if not slots[(idt+1) % 4][0] and cid[idt][-1]:
        pode_liberar = True

    # TODO: checar se a ordem atualizar-liberar-alimentar está OK

    if pode_liberar:
        # Move um bit do trecho pro semáforo que sucede
        slots[(idt+1) % 4][0] = 1
        slots[(idt+1) % 4][1] = 1  # Ativo, significa que acabou de ser ativado
        cid[idt] = [0] + cid[idt][:-1]  # Remove o último bit

    if pode_atualizar and not pode_liberar:
        # Move bits ativos, se possível
        for i in range(len(cid[idt]) - 1, 0, -1):
            if cid[idt][i] == 0 and cid[idt][i - 1] == 1:
                cid[idt][i], cid[idt][i - 1] = 1, 0

    # Se pode e não foi modificado nesse clock
    if pode_alimentar and not slots[idt][1]:
        slots[idt][0] = 0
        cid[idt][0] = 1


def return_reverse(trecho):
    trecho.reverse()
    return trecho


def mostra_cidade(cidade, slots):
    # TODO: use um loop, torne menos estático e mais escalável
    print(str(slots[0][0]) + " " + str(cidade[0])[1:-1].replace(', ', ' ') + " " + str(slots[1][0]))

    for i in range(5):
        print(str(cidade[3][4-i]) + '\t\t\t' + str(cidade[1][i]))

    print(str(slots[3][0]) + " " + str(return_reverse(cidade[2].copy()))[1:-1].replace(', ', ' ') + " " + str(slots[2][0]))

    print()


def criar_cidade(total_trechos, tamanho_trecho, total_semaforos):

    """
    S 0 0 0 0 0 S
    0           0
    0           0
    0           0
    0           0
    0           0
    S 0 0 0 0 0 S

    Em sentido horário, a partir de cima, temos: S0 T0 S1 T1 S2 T2 S3 T3.

    Cada trecho tem tamanho 5 com semáforos atrás e à frente. São 4 trechos, logo 4 semáforos aqui.
    """

    # TODO: usar modulo bitvector
    #cidade = [[1 if b % 2 == 0 else 0 for b in range(tam_trecho)] for _ in range(total_trechos)]
    cidade = [[1 if random.randint(0, 1) == 0 else 0 for _ in range(tamanho_trecho)] for _ in range(total_trechos)]
    sinal_semaforos = [1 for _ in range(total_semaforos)]  # Todos ativos (verdes)
    slot_semaforos = [[0, 0] for _ in range(total_semaforos)]  # Todos vazios

    return cidade, sinal_semaforos, slot_semaforos


def rodar_simulacao(cidade, sinais, slots, n_trechos):
   while True:
        for id_trecho in range(n_trechos):
            atualiza_trecho(id_trecho, cidade, sinais, slots)
        for s in slots:
            s[1] = 0
        os.system('clear')
        mostra_cidade(cidade, slots)
        time.sleep(5)


def main():
    n_trechos = 4
    cidade, sinais, slots = criar_cidade(4, 5, n_trechos)
    rodar_simulacao(cidade, sinais, slots, n_trechos)

    # Registra congestionamentos


if __name__ == '__main__':
    main()
