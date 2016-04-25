NAME=Milcom


default:
	pdflatex ${NAME}
	bibtex ${NAME}
	pdflatex ${NAME}

full:clean
	pdflatex ${NAME}
	pdflatex ${NAME}	
	pdflatex ${NAME}
	bibtex ${NAME}
	pdflatex ${NAME}
	pdflatex ${NAME}
	pdflatex ${NAME}


clean:
	-rm ${NAME}.pdf
	-rm ${NAME}.bbl
	-rm ${NAME}.log
	-rm ${NAME}.aux
	-rm ${NAME}x.blg
