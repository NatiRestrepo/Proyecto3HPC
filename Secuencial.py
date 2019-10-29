import operator, os, sys, re, time, collections
import numpy as np

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
                 "yours", "yourself", "yourselves", "z", "zero","ii"]

def getOcurrence(rootDir):
    ocurrenceFile = []
    dictFiles={}
    filesOrganized = []
    filesOrganized = list(os.walk(rootDir))[0][2]
    for i in filesOrganized:
        dictFiles[os.stat(rootDir+i).st_size]=i

    sort = sorted(dictFiles.keys())[::-1]
    for cont in range(len(sort)):
        file = open(rootDir + dictFiles[sort[cont]], 'r')
        ocurrenceWords = []
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word not in stopwordsman:
                    ocurrenceWords.append(word)
        file.close()
        sorted_ocurrenceWords = collections.Counter(ocurrenceWords).most_common(10)
        frequentWords =[]
        for i in range(10):
            frequentWords.append(sorted_ocurrenceWords[i][0])
        ocurrenceFile = list(set(ocurrenceFile).union(set(frequentWords)))
    return ocurrenceFile

def ft(ocurrenceFile):
    dictionary = {}
    dictFiles={}
    filesOrganized = []
    filesOrganized = list(os.walk(rootDir))[0][2]
    for i in filesOrganized:
        dictFiles[os.stat(rootDir+i).st_size]=i

    sort = sorted(dictFiles.keys())[::-1]
    for cont in range(len(sort)):
        arrOcurrence = []
        for i in range(len(ocurrenceFile)):
            arrOcurrence.append(0)
        # Lee el documento por orden de tamano.
        file = open(rootDir + dictFiles[sort[cont]], 'r')
        for line in file:
            line = patron.sub(" ",line.strip().lower())
            for word in line.split():
                if word in ocurrenceFile:
                    arrOcurrence[ocurrenceFile.index(word)] += 1
        dictionary[dictFiles[sort[cont]]] = arrOcurrence

    return dictionary

def preJaccard(fdt):
    sizeDict = len(fdt)
    matrixC = np.empty((sizeDict, sizeDict))
    listFiles = list(fdt.keys())
    for i in range(sizeDict):
        for j in range(sizeDict):
            matrixC[i][j] = 1.0 - (jaccard(fdt[listFiles[i]], fdt[listFiles[j]]))

    return matrixC

def jaccard(x, y):
    sumMin=0
    sumMax=0
    for i in range(len(x)):
        sumMin+=min(x[i],y[i])
        sumMax+=max(x[i],y[i])
    resultado=float(sumMin)/float(sumMax)
    return resultado

def kMeans(fdt,X, K, maxIters=6, plot_progress=None):
    group = []
    centroids = X[np.random.choice(np.arange(len(X)), K), :]
    for i in range(maxIters):
        C = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in centroids]) for x_i in X])
        centroids = [X[C == k].mean(axis=0) for k in range(K)]
    for i in range(K):
        group.insert(i,[])
    listFiles=list(fdt.keys())
    cont=0
    for i in C:
        group[i].append(listFiles[cont])
        cont+=1
    return np.array(centroids), C, group

if __name__ == '__main__':
    timeini = time.time()
    k = 10
    rootDir = sys.argv[1]
    ocurrenceFile = getOcurrence(rootDir)
    fdt = ft(ocurrenceFile)
    matrizJaccard = preJaccard(fdt)
    centroides, finalList, group = kMeans(fdt,matrizJaccard, k)
    finalTime= time.time() - timeini
    cont=0
    for i in group:
        print("Cluster numero ",cont,":")
        for j in i:
            print("Documento: ",j)
        print("--"*50)
        cont+=1
    print("Tiempo final: ", finalTime)
