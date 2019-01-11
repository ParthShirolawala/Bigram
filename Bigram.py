import csv
import json, pickle
import sys
import math
def readData(fileName):
    data = []
    file = open(fileName, "r")

    for word in file.read().split(" "):
        data.append(word)

    file.close()
    return data

def createBigram(data):
    Bigramslist = []
    bigramCount = {}
    unigramCount = {}


    for i in range(len(data)):
        if i < len(data) - 1:

            Bigramslist.append((data[i], data[i + 1]))

            if (data[i], data[i + 1]) in bigramCount:
                bigramCount[(data[i], data[i + 1])] += 1
            else:
                bigramCount[(data[i], data[i + 1])] = 1

        if data[i] in unigramCount:
            unigramCount[data[i]] += 1
        else:
            unigramCount[data[i]] = 1

    return Bigramslist, unigramCount, bigramCount

def BigramProbability(Bigramslist, unigramCount, bigramCount):
    allProbabilities = {}
    for bigram in Bigramslist:
        word1 = bigram[0]
        word2 = bigram[1]

        allProbabilities[bigram] = float(bigramCount.get(bigram)) / float(unigramCount.get(word1))

    file = open('NoSmoothingBigram.txt', 'w')

    file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

    for bigrams in Bigramslist:
        file.write(str(bigrams) + ' : ' + str(bigramCount[bigrams])
                   + ' : ' + str(allProbabilities[bigrams]) + '\n')

    file.close()

    return allProbabilities

def addOneSmoothingProbability(Bigramslist, unigramCount, bigramCount):
    allProbabilities = {}
    cStar = {}

    for bigram in Bigramslist:
        word1 = bigram[0]
        word2 = bigram[1]
        allProbabilities[bigram] = (float)(bigramCount.get(bigram) + 1) / (unigramCount.get(word1) + len(unigramCount))
        cStar[bigram] = (bigramCount[bigram] + 1) * unigramCount[word1] / (unigramCount[word1] + len(unigramCount))

    file = open('addOneSmoothingBigram.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

    for bigrams in Bigramslist:
        file.write(str(bigrams) + ' : ' + str(bigramCount[bigrams])
                   + ' : ' + str(allProbabilities[bigrams]) + '\n')

    file.close()

    return allProbabilities, cStar

def goodTuringDiscountingProbability(Bigramslist, bigramCount, totalBigram):
    allProbabilities = {}
    bucket = {}
    buckets = []
    cStar = {}
    pStar = {}
    countList = {}
    i = 1

    for bigram in bigramCount.items():
        key = bigram[0]
        value = bigram[1]

        if not value in bucket:
            bucket[value] = 1
        else:
            bucket[value] += 1

    # Sorted Bucket
    buckets = sorted(bucket.items(), key=lambda t: t[0])
    zeroOccurenceProb = (float) (buckets[0][1] / totalBigram)
    lastItem = buckets[len(buckets) - 1][0]

    for x in range(1, lastItem):
        if x not in bucket:
            bucket[x] = 0

    bucketList = sorted(bucket.items(), key=lambda t: t[0])
    lenBucketList = len(buckets)

    for k, v in buckets:

        if i < lenBucketList - 1:
            if v == 0:
                cStar[k] = 0
                pStar[k] = 0

            else:
                cStar[k] = (float)(i + 1) * buckets[i][1] / v
                pStar[k] = (float)(cStar[k] / totalBigram)

        else:
            cStar[k] = 0
            pStar[k] = 0

        i += 1

    for bigram in Bigramslist:
        allProbabilities[bigram] = (float)(pStar.get(bigramCount[bigram]))
        countList[bigram] = cStar.get(bigramCount[bigram])

    file = open('goodTuringDiscountingBigram.txt', 'w')
    file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

    for bigrams in Bigramslist:
        file.write(str(bigrams) + ' : ' + str(bigramCount[bigrams])
                   + ' : ' + str(allProbabilities[bigrams]) + '\n')

    file.close()

    return allProbabilities, zeroOccurenceProb, countList

if __name__ == '__main__':
    fileName = 'HW2_S18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt'
    data = readData(fileName)
    Bigramslist, unigramCount, bigramCount = createBigram(data)
    bigramProb = BigramProbability(Bigramslist, unigramCount, bigramCount)
    bigramAddOne, addOneCstar = addOneSmoothingProbability(Bigramslist, unigramCount, bigramCount)
    bigramGoodTuring, zeroOccurenceProb, goodTuringCstar = goodTuringDiscountingProbability(Bigramslist, bigramCount, len(Bigramslist))