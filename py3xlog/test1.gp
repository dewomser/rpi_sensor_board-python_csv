#
# $Id: simple.dem,v 1.7 2012/11/18 23:12:22 sfeam Exp $
#
# Requires data files "[123].dat" from this directory,

set terminal png size 800,600 enhanced font "Helvetica,20"
set output 'output.png'

set grid
set title 'xtrinsic mpl3115a2 '
set xlabel 'Zeit 0,5 s'
set ylabel 'Temperatur,Höhenmeter'


set auto x
set datafile separator ','
plot "newfile1.csv" using 1:2 with lines title 'Höhenmeter',"newfile1.csv" using 1:3 with lines title 'Temp im Gehäuse'

