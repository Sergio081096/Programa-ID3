import numpy as np


count_atri=0
i=1
nombre_columna = np.array(["Numero de ejemplares","Nivel de ventas","Precio"])


datos = np.array([["<=4","buenas","<=150"],
				  [">4","buenas",">150"],
				  [">4","buenas","<=150"],
				  ["<=4","buenas",">150"],
				  [">4","buenas",">150"],
				  [">4","bajas",">150"],
				  ["<=4","bajas",">150"],
				  ["<=4","bajas",">150"],
				  [">4","bajas","<=150"],
				  ["<=4","bajas","<=150"],
				  ["<=4","promedio","<=150"],
				  [">4","promedio","<=150"],
				  ["<=4","promedio",">150"],
				  [">4","promedio",">150"],
				  [">4","promedio","<=150"]])

atributo_descuento = np.array(["si",
							   "si",
							   "si",
							   "si",
							   "si",
							   "si",
							   "no",
							   "si",
							   "si",
							   "no",
							   "no",
							   "no",
							   "si",
							   "si",
							   "no"])

def entropia(p,n,d):
	entropia = -(p/d)*(np.log2(p/d)) - (n/d)*(np.log2(n/d))
	return entropia

def buscar_atributos(columna,lugar,aux):
	j =0
	i= 0
	l = 0
	pos = 0
	neg = 0
	tam = np.size(columna)
	pos_atri = np.zeros((1,0))
	guar_pos = np.zeros((1,0))
	for i in range(0,tam):
		l = lugar[i]
		if(columna[0]==columna[i]):
			pos_atri = np.concatenate((pos_atri,[[l]]),1)
		else:
			guar_pos = np.concatenate((guar_pos,[[l]]),1)
	for j in range(0,np.size(pos_atri)):
		for i in range(0,np.size(aux)):
			if(pos_atri[0,j]==aux[0,i]):
				pos += 1
	neg = np.size(pos_atri) - pos
	val_atri = np.delete(columna,pos_atri)
	return [val_atri,guar_pos,pos,neg]



tam_atri = atributo_descuento.shape[0] 

atri_pos = np.zeros((1,0))
for i in range(0,tam_atri):
	if(atributo_descuento[0]==atributo_descuento[i]):		
		count_atri += 1
		atri_pos = np.concatenate((atri_pos,[[i]]),1)


posi = count_atri
nega = tam_atri - count_atri
entropia_inicial = entropia(posi,nega,tam_atri)
print(entropia_inicial)
cantidad_columna = datos.shape[0] 
cantidad_fila = datos.shape[1]

aux_columna = np.copy(datos[:,0])
lu = np.arange(0,np.size(aux_columna))
[aux_buscar,lug,p,n] = buscar_atributos(aux_columna,lu,atri_pos)

ganancia = entropia_inicial - entropia(p,n,p+n) 
lug = np.copy(lug[0,:])
[aux_buscar,lug,p,n] = buscar_atributos(aux_buscar,lug,atri_pos)

print(p)

