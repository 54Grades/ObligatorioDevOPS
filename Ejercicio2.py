#-*- coding: utf-8 -*-

#Grupo N4A Analista en Infraestructura Informatica.
#Profesores Leonardo Genta && Eduardo Gomez.
#Alumnos Etzequiel Urtman (168879) && Manuel Lanza (194866) && Ulyses Garcia (244277).
#Universidad ORT - Campus Centro.
#Obligatorio Programacion para DevOPS - 4to Semestre

#Ejercicio 2 Python Obligatorio DevOPS [-r] [-t] [-d dominio] Directorio [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir

from subprocess import Popen, PIPE

import sys 

import os 

import re 

import argparse 

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--rec", help="Busca los archivos en forma recursiva a partir del directorio pasado como parametro.", action="store_true")

parser.add_argument("-t","--texto", help="Busca solo los archivos regulares no ocultos con extension .txt.",action="store_true")

parser.add_argument("-d","--dominio", type=str, help="Busca solo los correos de ese dominio.")

parser.add_argument("-e","--encontrados", type=str, choices=["d","t","c"], help="Desplegara la cantidad de correos electronicos encontrados por dominio (opcion d) \
por cantidad de dominios diferentes encontrados opcion (t) y con la opcion (c) despliega la cantidad de correos como la cantidad de dominios diferentes encontrados.")

parser.add_argument("-f", "--regexp", type=str, help="Despliega y cuenta solo correos electronicos que cumplan con la expresion regular precedida del parametro (-f).")

parser.add_argument("-o","--ordenar", type=str, choices=["a","d","l"], help="Ordena la salida de correos, con la opcion (o) ordena los correos aflabeticamente, con la opcion (d) \
ordena los correos por alfabeticamente creciente por dominio y con la opcion (l) ordena los correos por su largo de caracteres en forma creciente.")

parser.add_argument("directorio", type=str, help="Directorio donde se va a hacer la busqueda.")

try:
        args=parser.parse_args()
except SystemExit as e:
    print("Estimado Humano/a, la sintaxis de este script es: Ejercicio2.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir")
    exit(20)

parametrobash = ['/home/grades/Desktop/devopsobligatorio/Ejercicio1.sh']

if args.rec:
        parametrobash.append("-r")

if args.texto:
        parametrobash.append("-t")

if args.dominio:
        parametrobash.append("-d")
        parametrobash.append(args.dominio)
     
parametrobash.append(args.directorio)

process = Popen(parametrobash, stdout = PIPE, stderr = PIPE)

output = process.communicate()

if process.returncode > 0:

 print(output[1].decode(), file = sys.stderr, end="")
 exit(process.returncode)

if output[1].decode() != "":
 print(output[1].decode(), file = sys.stderr, end="")
 exit(0)

mails_list = output[0].decode().split("\n")

mails_list.pop(-1)
mails_list.pop(-1)

if args.regexp != None:
    try:
        patron = re.compile(args.regexp)
    except Exception as e:
        print("Estimado Humano/a, la expresion regular que acaba de ingresar no es la correcta, debe ingresar una expresion que sea regular que sea valida", file=sys.stderr)
        exit(10)

    filtred_mails = []

    for mail in mails_list:
        if patron.match(mail):
            filtred_mails.append(mail)
    mails_list = filtred_mails

for i in mails_list:
    print(i)
print("Sr Humano/a, la cantidad de mails encontrados es de:", args.directorio, len(mails_list))

if args.ordenar == "a":
    mails_list.sort(key=lambda element:(element.split("@")[0]))
    for i in mails_list:
            print(i)
    print("")

elif args.ordenar == "d":
    mails_list.sort(key=lambda element:(element.split("@")[1]))
    for i in mails_list:
        print(i)
    print("")
    
elif args.ordenar == "l":
    mails_list.sort(key=len) 
    for i in mails_list:
        print(i)

if args.encontrados == "d":
    dominios_qty = {}
    print("Estimado Humano/a, se reporta la cantidad de mails encontrados por dominio:")

    for mail in mails_list:
        dominio = mail.split("@")[1]
        if dominio not in dominios_qty:
            dominios_qty[dominio] = 1
        else:
            dominios_qty[dominio] += 1

    for dominio in dominios_qty:
        print (dominio, "-", dominios_qty[dominio])

elif args.encontrados == "t":
    dominios_list = []
    for mail in mails_list:
        dominio=mail.split("@")[1]
        if dominio not in dominios_list:
            dominios_list.append(dominio)
    for i in mails_list:
        print(i)
    print("Estimado Humano/a, la cantidad de dominios diferentes encontrados es: ",len(dominios_list))

elif args.encontrados == "c":
    dominios_qty = {}
    print("Estimado Humano/a, la cantidad de mails encontrados por dominio:")
    for mail in mails_list:
        dominio = mail.split("@")[1]
        if dominio not in dominios_qty:
            dominios_qty[dominio] = 1
        else:
            dominios_qty[dominio] += 1
    for dominio in dominios_qty:
        print(dominio,"-" ,dominios_qty[dominio])

    dominios_list = []
    for mail in mails_list:
        dominio=mail.split("@")[1]
        if dominio not in dominios_list:
            dominios_list.append(dominio)
    print("Estimado Humano/a, la cantidad de dominios diferentes encontrados es: " + str(len(dominios_list)))
