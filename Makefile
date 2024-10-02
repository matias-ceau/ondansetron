pdf:
	pandoc -s -C -o memoire.pdf memoire.md
docx:
	pandoc -s -C -o memoire.tex memoire.md
	pandoc -o memoire.docx memoire.tex
