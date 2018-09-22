import numpy as np


ganan_ini = np.zeros((1,0))##matriz para guardar entropias

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
	a = 0
	pos = 0
	neg = 0
	tam = np.size(columna)
	pos_atri = np.zeros((1,0))
	guar_pos = np.zeros((1,0))
	val_atri = np.zeros((1,0))
	for i in range(0,tam):
		l = lugar[i]
		a = columna[i]
		if(columna[0]==a):
			pos_atri = np.concatenate((pos_atri,[[l]]),1)#posicion de los primeros atributos encontrados
		else:
			guar_pos = np.concatenate((guar_pos,[[l]]),1)#posicion y valor de los residuos
			val_atri = np.concatenate((val_atri,[[a]]),1)
	for j in range(0,np.size(pos_atri)):
		for i in range(0,np.size(aux)):
			if(pos_atri[0,j]==aux[0,i]):
				pos += 1##cantidad de positivos
	neg = np.size(pos_atri) - pos	
	val_atri = np.copy(val_atri[0,:])
	nota = columna[0]
	return [val_atri,guar_pos,pos,neg,pos_atri,nota]

#-----------------------------------------------------


def ganancia_inicial(atribut):
	i = 0
	atri_pos = np.zeros((1,0))
	tam_atri = atribut.shape[0]
	for i in range(0,tam_atri):
		a = atribut[i]
		if(atribut[0]==atribut[i]):
			atri_pos = np.concatenate((atri_pos,[[i]]),1)
	return [atri_pos,tam_atri]

##---------------------------

def entropia_columnas(aux_buscar,lug,atri_ini,ganan,compara):
	[aux_buscar,lug,p,n,atributo,nota] = buscar_atributos(aux_buscar,lug,atri_ini)
	print("inicio: ",nota)
	#print("po: ",p,"ne: ",n)
	if(p == 0 or n == 0):
		ent = 0
	elif(p == n):
		ent = 1
	else:
		ent = entropia(p,n,p+n)
	ganan = ent
	lug = np.copy(lug[0,:])
	return [ aux_buscar,lug,p,n,atributo,ganan,nota ]

#-----------------para el resto del arbol
def entropia_columnas_ocupadas(aux_buscar,lug,atri_ini,ganan,compara):
	[aux_buscar,lug,p,n,atributo,nota] = buscar_atributos(aux_buscar,lug,atri_ini)
	#print("po: ",p,"ne: ",n)
	print("Rama",nota)
	if(p == 0 or n == 0):
		ent = 0
	elif(p == n):
		ent = 1
	else:
		ent = entropia(p,n,p+n)
	ganan = ganan -((p+n)/compara)*ent
	lug = np.copy(lug[0,:])
	#print("final :",ganan)
	return [ aux_buscar,lug,p,n,atributo,ganan,nota ]


###------------------------
def ramas(atributo,ganancia_total,aux_buscar,cal_entro,datos,atri_ini,compara,p,inicio,nueva_mat,nota):
	atributo = np.copy(atributo[0,:])
	mayo_ga = 0	
	#nueva_matri = nueva_mat
	ganan_ini = np.zeros((1,0))##matriz para guardar entropias
	nueva_matri = np.zeros((1,0)).T##matriz para guardar residuos
	if(ganancia_total == 0):
		if(p>0):
			ganancia_total = 1
		else:
			ganancia_total = 0
		a = nota
		cal_entro = np.concatenate((cal_entro,[[a]]))
		cal_entro = np.concatenate((cal_entro,[[ganancia_total]]))
		#print("Primera: \n",cal_entro)
		#print("g:",ganancia_total)
	else:
		print("atr",atributo)
		for i in range(0,datos.shape[1]):
			cal_entro_ramas = np.zeros((1,0))
			ganancia = ganancia_total
			for p in range(0,atributo.shape[0]):
				d = atributo[p]
				d = int(float(d))
				a = datos[d,i]
				cal_entro_ramas = np.concatenate((cal_entro_ramas,[[a]]),1)
			cal_entro_ramas = np.copy(cal_entro_ramas[0,:])
			print(cal_entro_ramas)
			if(cal_entro_ramas.shape[0] > 0):
				luga = atributo
				compara = atributo.shape[0]### tamaño del vector de comparacion 
				print("gan1",ganancia)
				while cal_entro_ramas.shape[0] > 0:
					[cal_entro_ramas,luga,p,n,atributoq,ganancia,nota] = entropia_columnas_ocupadas(cal_entro_ramas,luga,atri_ini,ganancia,compara)
					print("gan2",ganancia)
				ganan_ini = np.concatenate((ganan_ini,[[ganancia]]),1)
				#print("final :",ganancia)
		a = nota
		cal_entro = np.concatenate((cal_entro,[[a]]))
		#print("Primera: \n",cal_entro)
		for i in range(0,ganan_ini.shape[1]):
			if(ganan_ini.max()==ganan_ini[0,i]):		
				mayo_ga = i
	#print(ganancia_total)
	if (ganancia_total != 0 and ganancia_total != 1):
		for j in range(0,atributo.shape[0]):
			mat = atributo[j]
			nueva_matri = np.concatenate((nueva_matri,[[mat]]))
		#print(nueva_matri)
		inicio += 1
		if(inicio == 1):
			nueva_mat = nueva_matri
		else:
			nueva_mat = np.concatenate((nueva_mat,nueva_matri),1)
	#print(nueva_matri, inicio)
	return [mayo_ga,inicio,nueva_mat,cal_entro]
###--------------------reescribir la matriz de datos

def reescribir(nuevo,borrar):	
	inicio = 0
	for i in range(0,nuevo.shape[1]):
		nueva_mat = np.zeros((1,0)).T
		if(i != borrar):
			for j in range(0,nuevo.shape[0]):
				mat = nuevo[j,i]
				nueva_mat = np.concatenate((nueva_mat,[[mat]]))
			inicio += 1
			if(inicio == 1):
				nueva_matriz = nueva_mat
			else:
				nueva_matriz = np.concatenate((nueva_matriz,nueva_mat),1)	
	return [ nueva_matriz, nuevo ]

####---------------------Calculo de la mejor entropia
def inicio_fin(ganancia,aux_buscar,lug,atri_ini,cal_entro,datos,compara,inicio,nueva_mat):
	ganancia = 0###empezamos de nuevo ahora con la nueva ganancia
	n = nombre_columna[mayo_gan]## buscamos el nombre del nodo raiz
	cal_entro = np.zeros((1,0)).T### creamos la matriz donde se guarda la rama resultante
	cal_entro = np.concatenate((cal_entro,[[n]]))## le damos el nombre del nodo raiz
	compara = aux_buscar.shape[0]### tamaño del vector de comparacion
	nueva_mat = np.zeros((1,0)).T##guardar atributos
	inicio = 0
	while aux_buscar.shape[0] > 0:

		[aux_buscar,lug,p,n,atributo,ganancia,nota] = entropia_columnas(aux_buscar,lug,atri_ini,ganancia,compara)	
		if(ganancia == 0):
			if(p>0):
				gananciaq = 1
			else:
				gananciaq = 0
		#print("Primera: \n",cal_entro)
		print("g:",gananciaq)
		#ganancia = 0
		
		[mayo_ga,inicio,nueva_mat,cal_entr] = ramas(atributo,ganancia,aux_buscar,cal_entro,datos,atri_ini,compara,p,inicio,nueva_mat,nota)
		#print(nueva_mat)
		if(aux_buscar.shape[0] > 0):
			a = aux_buscar[0]
			#cal_entro = np.concatenate((cal_entro,[[a]]))
	#return[]
###---------------------
#--------Obtenemos la gancia inicial con el vector de entrada
[atri_ini,tam_ini] = ganancia_inicial(atributo_descuento)
posi = atri_ini.shape[1]
nega = tam_ini - atri_ini.shape[1]
elementos = datos.shape[0]## cantidad de filas
cantidad_fila = datos.shape[1]## cantidad de columnas
nom_atr = np.zeros((1,0))## nombre de la matriz para mostrar
entropia_inicial = entropia(posi,nega,tam_ini)###entropia inicial
### ganancia de cada fila
for i in range(0,cantidad_fila):
	n = nombre_columna[i]	
	ganancia = entropia_inicial
	aux_buscar = np.copy(datos[:,i])## seleccionamos la columna a evaluar
	nom_atr = np.concatenate((nom_atr,[[n]]),1)
	lug = np.arange(0,np.size(aux_buscar))### le damos valor a sus posiciones
	compara = aux_buscar.shape[0]### tamaño del vector de comparacion
	while  aux_buscar.shape[0] > 0:
		[aux_buscar,lug,p,n,atributo,ganancia,nota] = entropia_columnas_ocupadas(aux_buscar,lug,atri_ini,ganancia,compara)
#	print(ganancia)
	ganan_ini = np.concatenate((ganan_ini,[[ganancia]]),1)
primeras_ganacias = np.concatenate((nom_atr,ganan_ini))
#print(primeras_ganacias)
mayo_gan = 0###lugar de la mayor ganancia
for i in range(0,ganan_ini.shape[1]):
#	print("pos: ",ganan_ini[0,i])
	if(ganan_ini.max()==ganan_ini[0,i]):		
		mayo_gan = i

#print(ganan_ini.max()) ## aqui esta la mayor ganancia inicial
aux_buscar = np.copy(datos[:,mayo_gan])##asignamos el vector que tubo la mayor entropia
[datos,original] = reescribir(datos,mayo_gan)
lug = np.arange(0,np.size(aux_buscar))##valor de las posiones
#print(aux_buscar)


ganancia = 0###empezamos de nuevo ahora con la nueva ganancia
n = nombre_columna[mayo_gan]## buscamos el nombre del nodo raiz
cal_entro = np.zeros((1,0)).T### creamos la matriz donde se guarda la rama resultante
cal_entro = np.concatenate((cal_entro,[[n]]))## le damos el nombre del nodo raiz
compara = aux_buscar.shape[0]### tamaño del vector de comparacion
nueva_mat = np.zeros((1,0)).T##guardar atributos
inicio = 0

#inicio_fin(ganancia,aux_buscar,lug,atri_ini,cal_entro,datos,compara,inicio,nueva_mat)

while aux_buscar.shape[0] > 0:
	#print("ramas",lug)
	[aux_buscar,lug,p,n,atributo,ganancia,nota] = entropia_columnas(aux_buscar,lug,atri_ini,ganancia,compara)	
	if(ganancia == 0):
		if(p>0):
			gananciaq = 1
		else:
			gananciaq = 0

	#print("g:",gananciaq)
	[mayo_ga,inicio,nueva_mat,cal_entr] = ramas(atributo,ganancia,aux_buscar,cal_entro,datos,atri_ini,compara,p,inicio,nueva_mat,nota)
	#print(aux_buscar)
	#print(nueva_mat)
	ganancia_ramas = 0
	aux_buscar_ramas = np.copy(datos[:,mayo_ga])##asignamos el vector que tubo la mayor
	[datos_ramas,original] = reescribir(datos,mayo_ga)
	lug_ramas = np.copy(nueva_mat[:,mayo_ga])
	nuevo_vec = np.zeros((1,0))
	cal_entro_n = np.zeros((1,0)).T### creamos la matriz donde se guarda la rama resultante
	compara_ramas = lug_ramas.shape[0]### tamaño del vector de comparacion
	inicio_ramas = 0
	#print(aux_buscar_ramas)
	if(compara_ramas > 0):
		for p in range(0,lug_ramas.shape[0]):
			d = lug_ramas[p]
			d = int(float(d))
			a = aux_buscar_ramas[d]
			nuevo_vec = np.concatenate((nuevo_vec,[[a]]),1)
		aux_buscar_ramas = np.copy(nuevo_vec[0,:])
		#print(aux_buscar_ramas)
		inicio_fin(ganancia_ramas,aux_buscar_ramas,lug_ramas,atri_ini,cal_entro_n,datos_ramas,compara_ramas,inicio_ramas,nueva_mat)

###nota en 150 buscar la equivalnecia de las igualdades para busca el dato final