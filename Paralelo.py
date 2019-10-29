import operator, os, sys, re, collections
import time
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
sendbuf = []
root = 0
patron = re.compile("[^a-zA-Z']")


stopwordsman = ["a", "able", "about", "above", "according", "accordingly", "across", "actually", "after",
                "afterwards", "again", "against", "all", "allow", "allows", "almost", "alone", "along",
                "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another",
                "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart",
                "appear", "appreciate", "appropriate", "are", "around", "as", "aside", "ask", "asking",
                "associated", "at", "available", "away", "awfully", "b", "be", "became", "because", "become",
                "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below",
                "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "c",
                "came", "can", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes",
                "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider",
                "considering", "contain", "containing", "contains", "corresponding", "could", "course",
                "currently", "d", "definitely", "described", "despite", "did", "different", "do", "does",
                "doing", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "either",
                "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever", "every",
                "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f",
                "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former",
                "formerly", "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting",
                "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had",
                "happens", "hardly", "has", "have", "having", "he", "hello", "help", "hence", "her", "here",
                "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his",
                "hither", "hopefully", "how", "howbeit", "however", "i", "ie", "if", "ignored", "immediate",
                "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar",
                "instead", "into", "inward", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps",
                "kept", "know", "knows", "known", "l", "last", "lately", "later", "latter", "latterly",
                "least", "less", "lest", "let", "like", "liked", "likely", "little", "ll", "look", "looking",
                "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
                "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name",
                "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never",
                "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor",
                "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", "off",
                "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other",
                "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
                "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please",
                "plus", "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r",
                "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards",
                "relatively", "respectively", "right", "s", "said", "same", "saw", "say", "saying", "says",
                "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self",
                "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she",
                "should", "since", "six", "so", "some", "somebody", "somehow", "someone", "something",
                "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
                "specifying", "still", "sub", "such", "sup", "sure", "t", "take", "taken", "tell", "tends",
                "th", "than", "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them",
                "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein",
                "theres", "thereupon", "these", "they", "think", "third", "this", "thorough", "thoroughly",
                "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too",
                "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "u",
                "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us",
                "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "ve",
                "very", "via", "viz", "vs", "w", "want", "wants", "was", "way", "we", "welcome", "well",
                "went", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
                "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
                "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish",
                "with", "within", "without", "wonder", "would", "would", "x", "y", "yes", "yet", "you", "your",
                "yours", "yourself", "yourselves", "z", "zero"]


def jaccard(x, y):
    sumMin=0
    sumMax=0
    for i in range(len(x)):
        sumMin+=min(x[i],y[i])
        sumMax+=max(x[i],y[i])
    return float(sumMin)/float(sumMax)

def getOcurrence(v):
    toSend = []
    for i in range(comm.rank, len(v), comm.size):
        file = open(rootDir + v[i], 'r')
        ocurrenceWords = []
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word not in stopwordsman:
                    ocurrenceWords.append(word)
        file.close()
        sorted_ocurrenceWords = collections.Counter(ocurrenceWords).most_common(10)
        for i in range(10):
            toSend.append(sorted_ocurrenceWords[i][0])

    return toSend

def ft(ocurrenceFile,v):
    dictionary = {}
    for i in range(comm.rank, len(v), comm.size):
        arrOcurrence = []
        for j in range(len(ocurrenceFile)):
            arrOcurrence.append(0)

        file = open(rootDir + v[i], 'r')
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word in ocurrenceFile:
                    arrOcurrence[ocurrenceFile.index(word)] += 1
        dictionary[v[i]] = arrOcurrence

    return dictionary

def preJaccard(x):
    sizeDict = len(x)
    matrixC = np.zeros((sizeDict, sizeDict))
    listFiles = list(x.keys())
    for i in range(comm.rank, len(x), comm.size):
        for j in range(sizeDict):
            matrixC[i][j] = 1.0 - (jaccard(x[listFiles[i]], x[listFiles[j]]))

    return matrixC

def Kmeans(matrizFinal,k,maxIters = 10,):
    C = []
    centroids = []
    if comm.rank == 0:
        centroids = matrizFinal[np.random.choice(np.arange(len(matrizFinal)), k), :]

    for i in range(maxIters):

        cent = comm.bcast(centroids, root)
        tam2 = len(matrizFinal)
        argminList = np.zeros(tam2)

        for i in range(comm.rank, len(matrizFinal), comm.size):
            dotList = []
            for y_k in cent:
                dotList.append(np.dot(matrizFinal[i] - y_k, matrizFinal[i] - y_k))
            argminList[i] = np.argmin(dotList)
        recibC = comm.gather(argminList, root)
        cFinal = []
        if comm.rank == 0:
            cFinal = np.zeros(len(recibC[0]))
            for li in range(len(recibC)):
                cFinal += recibC[li]

        z = comm.bcast(cFinal,root)

        centroidesTemp = []
        for i in range(k):
            centroidesTemp.insert(i, [])

        for i in range(comm.rank, k, comm.size):
            truefalseArr = z == i
            propiosKArr = matrizFinal[truefalseArr]
            promedioArr = propiosKArr.mean(axis=0)
            centroidesTemp[i]=list(promedioArr)
        recibZ = comm.gather(centroidesTemp,root)
        centroidesFinales = []
        for j in range(k):
            centroidesFinales.append([])
        if comm.rank == 0:
            for i in range(len(recibZ)):
                for j in range(len(recibZ[i])):
                    centroidesFinales[j] += recibZ[i][j]
            centroids = centroidesFinales
    return centroids,z


    if __name__ == '__main__':
    timeini = time.time()
    k = 2
    rootDir = sys.argv[1]
    T = []
    Ttemp=[]
    fileListTemp = []
    fileList=[]
    mapFiles={}
    if comm.rank==0:
        fileListTemp = list(os.walk(rootDir))[0][2]
        for i in fileListTemp:
            mapFiles[os.stat(rootDir+i).st_size]=i
        sort = sorted(mapFiles.keys())[::-1]
        del fileListTemp [:]
        for i in sort:
            fileListTemp.append(mapFiles[i])

    fileList = comm.bcast(fileListTemp, root)

    Ttemp = comm.gather(getOcurrence(fileList),root)
    tFinal = []
    if comm.rank == 0:
        for i in range(len(Ttemp)):
            tFinal.extend([element for element in Ttemp[i] if element not in tFinal])
    T=comm.bcast(tFinal, root)

    fdtTemp=comm.gather(ft(T,fileList),root)
    mapaFinal={}
    if comm.rank == 0:
        for i in range(len(fdtTemp)):
            mapaFinal.update(fdtTemp[i])
    fdt=comm.bcast(mapaFinal, root)

    matriz=comm.gather(preJaccard(fdt), root)
    matrizFinalTemp=0
    if comm.rank==0:
        for matrix in matriz:
            matrizFinalTemp += matrix
    matrizFinal=comm.bcast(matrizFinalTemp, root)

    centroides,C= Kmeans(matrizFinal,k)
    group=[]
    if comm.rank==0:
        for i in range(k):
            group.insert(i,[])
        listaFiles=list(fdt.keys())
        cont=0;
        for i in C:
            group[int(i)].append(listaFiles[cont])
            cont+=1
        finalTime=time.time()-timeini
        cont=0
        for i in group:
            print("Cluster numero ",cont,":")
            for j in i:
                print("Documento: ",j)
            print("--"*50)
            cont+=1
        print("Tiempo final: ", finalTime)
