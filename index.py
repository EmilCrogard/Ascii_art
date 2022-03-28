import numpy as np
import math

from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

gscale2 = '@%#*+=-:. '

#Average_light hjälpfunktion till Asciiconvert. Tar in en del av bild-filen med en brickas dimensioner som input. Output är ett genomsnitt av ljushet i en bricka. 
def Average_light(image):

	im = np.array(image)
 
	w,h = im.shape
 
	return np.average(im.reshape(w*h))


#Asciiconvert funktionens Input: Bild-filen som skall konverteras, antal columner till ascii bilden, skalan ascii-bilden skall printas i, en boolean som bestämmer ascii-tecken paketet.
#Asciiconvert funktionen bestämmer ascii-tecken för varje beräknad bricka i bilden och lägger till dem i en sträng för varje rad som läggs in i listan aimg. I loopen skickas en del av bilden med måtten av den beräknade brickan till hjälpfunktionen Average_light och får tillbaka ett värde på dess genomsnittliga ljushet. Värdet används för att välja korrekt tecken. 
#Asciiconvert funktionen output: Listan aimg som består av en sträng ascii-tecken per rad. 
def Asciiconvert(imgFile, columns, scale, moreLevels):
    
	global gscale1, gscale2

	image = Image.open(imgFile).convert('L')

	W, H = image.size[0], image.size[1]
	print("input image dims: %d x %d" % (W, H))

	w = W/columns
 
	h = w/scale
 
	rows = int(H/h)
	
	print("columns: %d, rows: %d" % (columns, rows))
	print("tile dims: %d x %d" % (w, h))

	if columns > W or rows > H:
		print("Image too small for specified columns!")
		exit(0)

	aimg = []

	for j in range(rows):
		y1 = int(j*h)
		y2 = int((j+1)*h)
		if j == rows-1:
			y2 = H

		aimg.append("")
  
		for i in range(columns):

			x1 = int(i*w)
			x2 = int((i+1)*w)

			if i == columns-1:
				x2 = W

			img = image.crop((x1, y1, x2, y2))
   
			avg = int(Average_light(img))
			if moreLevels:
				gsval = gscale1[int((avg*69)/255)]
			else:
				gsval = gscale2[int((avg*9)/255)]

			aimg[j] += gsval
			
	
	return aimg

#main funktionen är den interaktiva delen av programmet. Den tar input från användaren i form av bild-fil, skala, antal columner och en boolean för vilket tecken-packet som används. Main funktionen kallar även på Asciiconvert funktionen, öppnar output-filen och skriver ut aimg-listan rad för rad. 
def main():     
	imgFile = input("Paste IMG file here: \n")
 			
	scale = input("Input scale in decimals or press Enter for standard settings: \n")
	if scale == '':
		scale = 0.43
	else:
		scale = float(scale)
	
	
	
	outFile = input("Input wanted output file or press ENTER for standard settings: \n")
	if outFile == '':
		outFile = 'out.txt'
	
	columns = input("Input number of columns or press ENTER for standard settings: \n")
	if columns == '':
		columns = 100
	else:
		columns = int(columns)
  
	moreLevels = input("Input HIGH for more levels of gray scale or press ENTER for standard grayscale \n")
	if moreLevels == '':
		moreLevels = False
	elif moreLevels == 'HIGH':
		moreLevels = True
	elif moreLevels == 'high':
		moreLevels = True
	else:
		print("Input incorrect. Follow the instructions or the program will not funktion properly \n")
		exit(0)

	print('generating ASCII art...')
	
	aimg = Asciiconvert(imgFile, columns, scale, moreLevels)

	f = open(outFile, 'w')

	for row in aimg:
		f.write(row + '\n')

	f.close()
	print("ASCII art written to %s" % outFile)

#kallar på main funktionen
main()
