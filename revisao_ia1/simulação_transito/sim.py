#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 22/07/18 at 13:55
"""

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
        # Move bits ativos, se poslotsível
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


total_trechos = 4
total_sem = 4
tam_trecho = 5

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
cidade = [[1 for _ in range(tam_trecho)] for _ in range(total_trechos)]
sinal_semaforos = [1 for _ in range(total_sem)]  # Todos ativos (verdes)
slot_semaforos = [[0, 0] for _ in range(total_sem)]  # Todos vazios

mostra_cidade(cidade, slot_semaforos)

for i in range(11):
    for id_trecho in range(total_trechos):
        atualiza_trecho(id_trecho, cidade, sinal_semaforos, slot_semaforos)
    print('Iteração ', i+1)
    for s in slot_semaforos:
        s[1] = 0
    mostra_cidade(cidade, slot_semaforos)

    # Registra congestionamentos
