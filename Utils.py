#coding: utf-8

import cv2
import math
import time
import sys
import os
import numpy as np
from PIL import Image

now_time = time.gmtime()

face = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
glass_cas = cv2.CascadeClassifier('Haar/haarcascade_eye_tree_eyeglasses.xml')

WHITE = [255, 255, 255]


def LerArquivo():
    Info = open("Nomes.txt", "r")
    NOME = []
    while (True):
        Linha = Info.readline()
        if Linha == '':
            break
        NOME.append (Linha.split(",")[1].rstrip())
       
    return NOME

def DetectarOlhos (Imagem):
    Theta = 0
    rows, cols = Imagem.shape
    
    #Detecto os olhos
    glass = glass_cas.detectMultiScale(Imagem)

    for (sx, sy, sw, sh) in glass:
        
        # Verifico se na imagem possui os 2 olhos
        if glass.shape[0] == 2:

            if glass[1][0] > glass[0][0]:
                DY = ((glass[1][1] + glass[1][3] / 2) - (glass[0][1] + glass[0][3] / 2))
                DX = ((glass[1][0] + glass[1][2] / 2) - glass[0][0] + (glass[0][2] / 2))
            else:
                DY = (-(glass[1][1] + glass[1][3] / 2) + (glass[0][1] + glass[0][3] / 2))
                DX = (-(glass[1][0] + glass[1][2] / 2) + glass[0][0] + (glass[0][2] / 2))

            if (DX != 0.0) and (DY != 0.0):
                Theta = math.degrees(math.atan(round(float(DY) / float(DX), 2)))

                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), Theta, 1)
                # Image = cv2.warpAffine(Imagem, M, (cols, rows))

                #Detecto o rosto na imagem
                Face = face.detectMultiScale(Imagem, 1.3, 5)
                for (fx, fy, fw, fh) in Face:
                    RostoRecortado = Imagem[fy: fy + fh, fx: fx + fh]
                    return RostoRecortado

def AdicionarNome(Nome):
    Info = open("Nomes.txt", "r+")
    ID = ((sum(1 for line in Info))+1)
    Info.write(str(ID) + "," + Nome + "\n")
    print ("Seu codigo de identificação é o " + str(ID))
    Info.close()
    return ID

def BuscarImagemPorID (path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    FaceList = []
    IDs = []
    for imagePath in imagePaths:
        faceImage = Image.open(imagePath).convert('L')  # Open image and convert to gray
        faceImage = faceImage.resize((110,110))         # resize the image so the EIGEN recogniser can be trained
        faceNP = np.array(faceImage, 'uint8')           # convert the image to Numpy array
        ID = int(os.path.split(imagePath)[-1].split('.')[1])    # Retreave the ID of the array
        FaceList.append(faceNP)                         # Append the Numpy Array to the list
        IDs.append(ID)                                  # Append the ID to the IDs list
        cv2.imshow('Treinando Inteligência de Reconhecimento', faceNP)              # Show the images in the list
        cv2.waitKey(1)
    return np.array(IDs), FaceList                      # The IDs are converted in to a Numpy array

def Treinar(): 
    EigenFace = cv2.face.EigenFaceRecognizer_create(15)
    path = 'Capturas'
    IDs, FaceList = BuscarImagemPorID(path)

    print('Treinando inteligência de reconhecimento facial...')
    EigenFace.train(FaceList, IDs)
    print('Treinamento Finalizado.')
    EigenFace.write('Reconhecimento/TreinamentoEigenFaces.xml')

    cv2.destroyAllWindows()

def RetornaNomeIdentificado(ID, Confidence):
    Nomes = LerArquivo()
    Reconhecido = False
    if ID > 0 and Nomes != []:
        Confidence = 100 - (Confidence/100)
        StringNome = Nomes[ID-1]
        StringConfidence = "CONFIABILIDADE : " + (str(round(Confidence))+ "%" )
        Reconhecido = True
    else:
        StringNome = "SEM CADASTRO"
        StringConfidence = ""
        Reconhecido = False
    return StringNome, StringConfidence, Reconhecido

