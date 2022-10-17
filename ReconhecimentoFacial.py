from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
import cv2
import numpy as np
import Utils

Window.clearcolor = (1,1,1,1)

HaarCascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
HaarCascadeEye = cv2.CascadeClassifier('Haar/haarcascade_eye.xml')

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [240/255,20/255,40/255]
BLUE = [48/255,84/255,150/255,1]
FONT_SIZE = 16

class ReconhecimentoFacial(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.capture = cv2.VideoCapture(0)
        self.limiteCapturas = 50
        self.QuantidadeCapturas = 1
        self.TreinamentoConcluido = False
        self.OptionMenu = '0'
        
        self.btnReconhecimento = Button(
            text="Reconhecimento em Tempo real",
            font_size=FONT_SIZE,
            background_color=BLUE,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.1)
)
        self.btnReconhecimento.bind(on_press=self.ReconhecerRosto)
        self.layout.add_widget(self.btnReconhecimento)

        self.btnCadastrar = Button(
            text="Cadastrar Rosto",
            font_size=FONT_SIZE,
            background_color=BLUE,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.1),
        )
        self.btnCadastrar.bind(on_press=self.CadastrarRosto)
        self.layout.add_widget(self.btnCadastrar)

        self.btnAutenticar = Button(
            text="Autenticar",
            font_size=FONT_SIZE,
            background_color=BLUE,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.1),
        )
        self.btnAutenticar.bind(on_press=self.Autenticar)
        self.layout.add_widget(self.btnAutenticar)


        self.btnSair = Button(
            text="Sair",
            font_size=FONT_SIZE,
            background_color=RED,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.1)
        )
        self.btnSair.bind(on_press=self.Sair)
        self.layout.add_widget(self.btnSair)

        return self.layout

    def ReconhecerRosto(self, *args):
        self.CapturarRosto('1')

    def CadastrarRosto(self, *args):
        self.ModalCadastro = ModalView(auto_dismiss=False, background_color=WHITE,size_hint=(None, None), size=(400, 200))
        Container = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label_NomeUsuario = Label(
            text='Informe seu nome abaixo para se cadastrar: ', 
            color=(0,0,0,1),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            size_hint=(0.8, 0.35),
            font_size=FONT_SIZE,
        )
        Container.add_widget(label_NomeUsuario)

        self.Input_NomeUsuario = TextInput(
            multiline=False, 
            readonly=False,
            halign="left", 
            font_size=14,
            pos_hint={"center_x": 0.5, "center_y": 0.5}, 
            size_hint=(0.8, 0.4)
        )
        Container.add_widget(self.Input_NomeUsuario)

        ContainerButtons = BoxLayout(orientation='horizontal', spacing=15, padding= [40, 0])

        Button_FecharModal = Button(
            text="Fechar",
            font_size=FONT_SIZE,
            background_color=RED,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.35)
            # size_hint=(None, None),
            # size=(100, 30)
        )
        Button_FecharModal.bind(on_press=self.ModalCadastro.dismiss)
        ContainerButtons.add_widget(Button_FecharModal)

        Button_SalvarModal = Button(
            text="Salvar",
            font_size=FONT_SIZE,
            background_color=(50/255,205/255,50/255,1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.35)
            # size_hint=(None, None),
            # size=(100, 30)
        )
        Button_SalvarModal.bind(on_press=self.Salvar)
        ContainerButtons.add_widget(Button_SalvarModal)
        
        Container.add_widget(ContainerButtons)

        self.ModalCadastro.add_widget(Container)
        self.ModalCadastro.open()

    def Salvar(self, *args) : 
        if (self.Input_NomeUsuario.text != ''):
            self.ID = Utils.AdicionarNome(self.Input_NomeUsuario.text)
            self.Input_NomeUsuario.text = ''
            self.ModalCadastro.dismiss()
            self.CapturarRosto('2')

    def Autenticar(self, *args):
        print('ok')

    def CapturarRosto(self, Option) : 
        self.ModalCaptura = ModalView(auto_dismiss=False, background_color=WHITE,size_hint=(None, None), size=(675, 515), padding=10)
        Container = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.image = Image()
        Container.add_widget(self.image)

        btnSair = Button(
            text="Sair",
            font_size=FONT_SIZE,
            background_color=RED,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.4, 0.1)
        )
        btnSair.bind(on_press=self.FecharCamera)
        Container.add_widget(btnSair)

        self.ModalCaptura.add_widget(Container)
        self.ModalCaptura.open()

        self.OptionMenu = Option
        Clock.schedule_interval(self.CarregarVideo, 1.0/60.0)

    def FecharCamera(self, *args):
        self.ModalCaptura.dismiss()

    def Sair(self, *args):
        self.stop()

    def CarregarVideo(self, *args):

        recognise = cv2.face.EigenFaceRecognizer_create(15, 4000)  # Crio o Reconhecimento usando Eigen Faces
        recognise.read("Reconhecimento/TreinamentoEigenFaces.xml") # Carrego o Treinamento

        ret, Frame = self.capture.read() #Pego a imagem da camera
        FrameCinza = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY) # Converto a imagem da camera para tons de cinza

        RostosDetectados = HaarCascade.detectMultiScale(FrameCinza, 1.3, 5 )#Detecto o rosto
        for (x, y, w, h) in RostosDetectados:
            
            cv2.rectangle(Frame, (x,y), (x+w, y+h), (255,255,255), 2) # Exibo o retangulo no rosto

            FrameRostoCinza = cv2.resize((FrameCinza[y: y+h, x: x+w]), (110, 110))
           
            # Opção Cadastrar Rosto
            if(self.OptionMenu == '2') :

                # Se atingiu o limite de caputuras definidas, então treino a I.A
                if (self.QuantidadeCapturas == self.limiteCapturas + 1) :
                    cv2.destroyAllWindows()

                    print("Todas as 50 capturas foram realizadas.")
                    self.QuantidadeCapturas = 0                        
                    
                    Utils.Treinar()
                    self.OptionMenu = '1'
                    self.ModalCaptura.dismiss()
                # Senão capturo as fotos
                else :

                    FrameRosto = FrameCinza[y - int(h / 2): y + int(h * 1.5), x - int(x / 2): x + int(w * 1.5)]
                    FrameDetectada = (Utils.DetectarOlhos(FrameRosto))
                    
                    if FrameDetectada is not None:
                        Foto = FrameDetectada
                    else:
                        Foto = FrameCinza[y: y+h, x: x+w]

                    print ("User." + str(self.ID) + "." + str(self.QuantidadeCapturas) + ".jpg")
                    
                    #salvo a foto capturada
                    cv2.imwrite("Capturas/User." + str(self.ID) + "." + str(self.QuantidadeCapturas) + ".jpg", Foto)
                    cv2.waitKey(100)
                    # Exibo a foto capturada
                    cv2.imshow("Captura Realizada", Foto)
                    self.QuantidadeCapturas += 1
            else :
                # Define o ID do usuário e a Porcentagem de confiança, pela Foto
                ID, Confidence = recognise.predict(FrameRostoCinza)
                NAME, CONFIDENCE, RESULT = Utils.RetornaNomeIdentificado(ID, Confidence)
                
                # Exibo a precisão no reconhecimento
                cv2.putText(Frame, CONFIDENCE, (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, WHITE, 2)
                # Exibo o nome
                cv2.putText(Frame, NAME, (x, y-30), cv2.FONT_HERSHEY_DUPLEX, 1, WHITE, 2)
                
        self.image_frame = Frame
        buffer = cv2.flip(Frame, 0).tostring()
        texture = Texture.create(size=(Frame.shape[1], Frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

ReconhecimentoFacial().run()

