import math
import time

class Rettangolo:
    numeroRettangolo=str
    altezza=int
    larghezza=int
    costo=int
    posizione=(int,int)
    profitto=int
    def __init__(self, attributi, j):
        self.altezza = int(attributi[0])
        self.larghezza = int(attributi[1])
        self.costo = int(attributi[2])
        self.numeroRettangolo = "Rettangolo_"+str(j+1)
    def chiavePerOrdinare(self):
        return self.costo/(self.altezza*self.larghezza)
    def posiziona(self, x, y):
        self.posizione = (x,y)
    def __str__(self):
        return self.numeroRettangolo+": Altezza-" + str(self.altezza)+"; Larghezza-"+str(self.larghezza)+"; Costo-"+str(self.costo)
#definiamo una classe che registri l'iterazione dell'algoritmo
class Iterazione:
    rettangolo = Rettangolo
    fObiettivo=int
    tempoDiCalcolo=float
    TFine=float
    def __init__(self, rettangolo, valoreFObiettivo, tempoDiCalcolo, TFine):
        self.rettangolo=rettangolo
        self.fObiettivo=valoreFObiettivo
        self.tempoDiCalcolo=tempoDiCalcolo
        self.TFine=TFine
    def __str__(self):
        txtReturn = "{spazioRettangolo:^16s} {valoreDellaFunzioneObiettivo:^10} {tempoDiCalcolo:^33.4f} {tempoDiFine:^16.3f} \n"
        return txtReturn.format(spazioRettangolo = self.rettangolo.numeroRettangolo, valoreDellaFunzioneObiettivo=str(self.fObiettivo), tempoDiCalcolo=self.tempoDiCalcolo, tempoDiFine=self.TFine)


#apriamo il file di tutte le istanze
fileRead=open("nomiFile.txt", 'r')
nomeIstanza='1'
while(nomeIstanza!=''):
    #registriamo l'istante in cui inizia l'algoritmo
    tic=time.time()
    #leggiamo l'istanza che andremo a risolvere
    nomeIstanza=fileRead.readline()
    file = open(nomeIstanza[:-1])
    nameFile=file.name.split("/")
    nameFile=nameFile[len(nameFile)-1]
    print(nameFile)
    #registriamo il numero di righe
    riga=file.readline()
    righe = int(riga)
    #registriamo il numero di colonne
    colonna=file.readline()
    colonne=int(colonna)
    #costruiamo l'entità griglia, in cui ogni entrata rappresenterà un profitto
    grid = [file.readline().split(',') for j in range(righe)]

    #registriamo il numero di rettangoli
    rettangoli=int(file.readline())
    #definiamo ogni rettangolo
    R=[Rettangolo(file.readline().split(','), j) for j in range(rettangoli)]

    #definiamo alcune strutture dati utili per l'algoritmo
    rettPosizionati = []
    R2=R.copy()
    cardR =len(R)

    #definiamo le variabili soluzione migliore e soluzione corrente
    soluzioneMigliore=-math.inf
    soluzioneCorrente=0

    #definiamo il contatore che indicherà l'iterazione dell'algoritmo
    c=0

    #creiamo un file in cui scriviamo i nostri progressi
    fileWrite = open("Solution_con_valutazione/"+nameFile, "a")
    fileWrite.write("Istanza: "+ nameFile)

    #definiamo una funzione che posiziona il rettangolo
    def posizionaRettangolo(ret, gridT, righe, colonne):
        profittoMigliore=-math.inf
        profittoCorrente=0
        posizioneMigliore=(0, 0)
        for i in range(righe):
            for j in range(colonne):
                for profitto in [gridT[k][m] for k in range(i, i+ret.altezza) for m in range(j, j+ret.larghezza) if (i+ret.altezza)<righe and (j+ret.larghezza)<colonne]:
                    profittoCorrente=profittoCorrente+int(profitto)
                if profittoCorrente>profittoMigliore:
                    profittoMigliore=profittoCorrente
                    posizioneMigliore=(i,j)
                profittoCorrente=0
        return (posizioneMigliore, profittoMigliore);

    #Costruiamo una funzione che pone a 0 le entrate già considerate
    def riduciEntrate(posizione, griglia, ret):
        for i in range(posizione[0], posizione[0]+ret.altezza):
            for j in range(posizione[1], posizione[1]+ret.larghezza):
                grid[i][j]=0

    #definiamo una funzione per formattare il file di uscita
    def scrivi():
        fileWrite.write("Posizionamento del rettangolo: " + str(rettangoloMigliore)+"\n"+"Rettangolo posizionato in posizione: "+ str(posizionamento[0])+"\n" + "Tempo di calcolo: "+str(fine-inizio)+"\n Valore della funzione obiettivo: "+ str(soluzioneCorrente)+"\n")

    #definiamo una struttura dati in cui registreremo le iterazioni
    iterazioni=[]

    #iniziamo l'algoritmo
    while(len(R)>0):
        inizio=time.time()
        soluzioneMigliore=soluzioneCorrente
        R.sort(key=Rettangolo.chiavePerOrdinare)
        if len(R)==0:
            break
        rettangoloMigliore=R.pop(0)
        posizionamento = posizionaRettangolo(rettangoloMigliore, grid, righe, colonne)
        soluzioneCorrente=soluzioneCorrente+posizionamento[1]-rettangoloMigliore.costo
        if soluzioneCorrente>soluzioneMigliore:
            rettPosizionati.append(rettangoloMigliore)
            rettangoloMigliore.posiziona(posizionamento[0][0], posizionamento[0][1])
            riduciEntrate(posizionamento[0], grid, rettangoloMigliore)
            fine=time.time()
            scrivi()
            it=Iterazione(rettangoloMigliore, soluzioneCorrente, ((fine-inizio)*1000), (fine-tic))
            iterazioni.append(it)
        else:
            soluzioneCorrente=soluzioneMigliore

    toc=time.time()
    fileWrite.write("Tempo di elaborazione totale: "+ str(toc-tic)+"\n Valore della soluzione ottima trovata: "+ str(soluzioneMigliore) +"\n Nome rettangolo | Valore FO | Tempo di calcolo(millisecondi) | Tempo finale \n")
    for i in iterazioni:
        fileWrite.write(str(i))


#provare a togliere i primi rettangoli ed inserire quelli successivi + verifica che le soluzioni diano quel valore della funzione obiettivo
#verificare che le soluzioni trovate diano come valore della funzione obiettivo quello trovato
