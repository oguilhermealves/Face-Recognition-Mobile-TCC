
# def CarregarVideo(self, *args):
#         recognise = cv2.face.EigenFaceRecognizer_create(15, 4000)  # Crio o Reconhecimento usando Eigen Faces
#         recognise.read("Reconhecimento/TreinamentoEigenFaces.xml") # Carrego o Treinamento


#         ret, Frame = self.capture.read()

#         FrameCinza = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
#         RostosDetectados = HaarCascade.detectMultiScale(FrameCinza, 1.3, 5)
#         for (x, y, w, h) in RostosDetectados:
            
#             if(self.TreinamentoConcluido):
#                 FrameRostoCinza = cv2.resize((FrameCinza[y: y+h, x: x+w]), (110, 110))
#                 OlhosDetectados = HaarCascadeEye.detectMultiScale(FrameRostoCinza)
#                 for (ex, ey, ew, eh) in OlhosDetectados:

#                     # Define o ID e a Porcentagem de confiança, pela Foto
#                     ID, Confidence = recognise.predict(FrameRostoCinza)
#                     NAME, CONFIDENCE, RESULT = Utils.RetornaNomeIdentificado(ID, Confidence)

#                     cv2.putText(Frame, CONFIDENCE, (20, 20), cv2.FONT_HERSHEY_DUPLEX, 1, WHITE)
#                     cv2.putText(Frame, NAME, (x, y-30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0))
#                     cv2.rectangle(Frame, (x,y), (x+w, y+h), (0,0,0), 2)

#             if(self.OptionMenu == '1') :
#                 FrameRostoCinza = cv2.resize((FrameCinza[y: y+h, x: x+w]), (110, 110))
#                 OlhosDetectados = HaarCascadeEye.detectMultiScale(FrameRostoCinza)
#                 for (ex, ey, ew, eh) in OlhosDetectados:

#                     # Define o ID e a Porcentagem de confiança, pela Foto
#                     ID, Confidence = recognise.predict(FrameRostoCinza)
#                     NAME, CONFIDENCE, RESULT = Utils.RetornaNomeIdentificado(ID, Confidence)

#                     cv2.putText(Frame, CONFIDENCE, (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, WHITE)
#                     cv2.putText(Frame, NAME, (x, y-30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0))
#                     cv2.rectangle(Frame, (x,y), (x+w, y+h), (255,255,255), 2)

#             elif(self.OptionMenu == '2') :
#                 cv2.rectangle(Frame, (x,y), (x+w, y+h), (255,0,0), 2)
#                 cv2.putText(Frame, "ROSTO DETECTADO", (x, y-5), cv2.FONT_HERSHEY_DUPLEX, 0.5, WHITE)

#                 if (self.QuantidadeCapturas == 51) :
#                     print("Todas as 75 capturas foram realizadas.")
#                     self.QuantidadeCapturas = 0
#                     self.CapturarImagens = False
                    
#                     Utils.Treinar()
#                     self.TreinamentoConcluido = True
#                 elif (self.CapturarImagens) :

#                     FrameRosto = FrameCinza[y - int(h / 2): y + int(h * 1.5), x - int(x / 2): x + int(w * 1.5)]
#                     FrameDetectada = (Utils.DetectarOlhos(FrameRosto))
                    
#                     if FrameDetectada is not None:
#                         Foto = FrameDetectada
#                     else:
#                         Foto = FrameCinza[y: y+h, x: x+w]

#                     print ("User." + str(self.ID) + "." + str(self.QuantidadeCapturas) + ".jpg")
                    
#                     #salvo a foto capturada
#                     cv2.imwrite("Capturas/User." + str(self.ID) + "." + str(self.QuantidadeCapturas) + ".jpg", Foto)
#                     cv2.waitKey(300)

#                     # Exibo a foto capturada
#                     cv2.imshow("Captura Realizada", Foto)
#                     self.QuantidadeCapturas += 1

#         self.image_frame = Frame
#         buffer = cv2.flip(Frame, 0).tostring()
#         texture = Texture.create(size=(Frame.shape[1], Frame.shape[0]), colorfmt='bgr')
#         texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
#         self.image.texture = texture
