#!/bin/bash

#Grupo N4A Analista en Infraestructura Informatica.
#Profesores Leonardo Genta && Eduardo Gomez.
#Alumnos Etzequiel Urtman (168879) && Manuel Lanza (194866) && Ulyses Garcia (244277).
#Universidad ORT - Campus Centro.
#Obligatorio Programacion para DevOPS - 4to Semestre

#Ejercicio 1 Bash Obligatorio DevOPS [-r] [-t] [-d dominio] Directorio.
#BUSCA CORREOS.

rec="-maxdepth 1"

ar="*"

dom="[[:alnum:][[:alnum:]_.]*"

if [ $# -lt 1 ] || [ $# -gt 5 ]
then
  echo "Estimado Humano/a, la cantidad de parametros que acaba de ingresar incorrecta, solo recibiremos los modificadores -t, -d, -r dominio y un directorio accesible en el sistema de archivos" >&2
  exit 4
fi

while getopts "rtd:" parametro
do
   case $parametro in 

	 r)

	  rec=""
          
	 ;;

 	 t)
	  
	  ar="[!.]*.txt"
	 
	 ;;	

	 d)

	   dom="$OPTARG"
              if echo "$dom" | grep -q "^[._]"
              then
              echo "Estimado Humano/a, debe ingresar un dominio que no comience con un guion o un punto" >&2
              exit 2
              fi
	 ;;

 	 *)

          echo "Estimado Humano/a -$OPTARG es incorrecto, solo se aceptamos visa, oca, mastercard, -d, -t y -r" >&2
          exit 5

	 ;;

   esac
done

shift $((OPTIND-1))

if [ $# -gt 1 ]
then
  echo "Estimado Humano/a, la cantidad de parametros que acaba de ingresar es incorrecta, solo se reciben los modificadores -r, -t, -d dominio y un solo directorio accesible en el sistema de archivos." >&2
  exit 4

elif [ $# -eq 1 ]
then

dir=$1

fi

if echo "$dir" | grep -q "^./"

then

  dirtemp=$(echo "$dir" | sed 's/\.//')
 
  dir=$(pwd)"$dirtemp"

fi

if ! echo "$dir"| grep -q "^/"

then

    dir=$(pwd)"/$dir"

fi

if ! test -a "$dir"

then

echo Estimado Humano/a el directorio $dir no existe >&2

exit 1

fi

if ! test -d "$dir"

then

echo Estimado Humano/a el parámetro $dir no es un directorio >&2

exit 2

fi

if ! ([ -r "$dir" ] && [ -x "$dir" ])

then

echo Estimado Humano/a, no se tienen los permisos necesarios para acceder al directorio y buscar correos >&2

exit 3

fi

grep -oh "[[:alnum:]_.]*[[:alnum:]]@$dom" $(find "$dir" $rec -name "$ar" -type f) 1>temp 2>/dev/null

if [ $(wc -l < temp) -eq 0 ]

then

  echo "Estimado Humano/a, no se han encontrado correos en el directorio $dir"
  
  rm temp 

  exit 0

fi

cat temp

echo "La cantidad de correos en "$dir" es: "$(cat temp | wc -l)

rm temp

exit 0

