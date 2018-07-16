#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python

cshtml = open('cell_series.html', 'w')

cshtml.write('<HTML><HEAD><TITLE>Volts</TITLE></HEAD><BODY>\n')
for i in range(31):
	cshtml.write(f'<IMG src="i{100+i}_cell_{i+1}_volts.png" alt="Cell {i+1} Volts">\n')
	cshtml.write('<BR>\n')

cshtml.write('</BODY></HTML>\n')

cshtml.close()
