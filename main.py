"""Ce code utilise le module Kivy pour créer une application de jeu de deviner un nombre. 
Il importe plusieurs classes et fonctions de Kivy pour créer des écrans, des boutons, des 
entrées de texte, des grilles de disposition, des widgets, des propriétés, des fichiers de 
construction de langage, des fenêtres, des images, des horloges et des sons. Il utilise également 
la fonction randint de la bibliothèque random pour générer des nombres aléatoires."""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from random import*
import time

#
kivy.require("1.11.1")
# Construite l'application avec la structure définie dans le fichier main.kv
Builder.load_file('main.kv')
n=100 # Initialisation du niveau du jeu
# Chargement des sons
Sound = SoundLoader.load('gameson.mp3')
Applaud = SoundLoader.load('applaudissement.mp3')
Check = SoundLoader.load('check.mp3')

"""La classe HomePage s'identifie à la page d'accueil de l'application. Ell définit une 
méthode "level" qui permet de définir la plage de nombres dans laquelle le nombre à deviner 
sera généré en fonction de la difficulté choisie par l'utilisateur (niveau 1, niveau 2, niveau 2)"""
class HomePage(Screen):
    def level(self,i):
        global n
        if i==1:
            n=100
        if i==2:
            n=250
        if i==3:
            n=1000

"""La classe GuessNumber est la classe principale de l'application qui gère la logique de jeu. 
Elle hérite de la classe Screen de Kivy et définit plusieurs méthodes pour gérer les actions du joueur,
telles que démarrer, arrêter, réinitialiser et vérifier le jeu , ainsi que mettre à jour l'affichage du temps restant. 
Elle utilise également des variables globales pour stocker des informations telles que le nombre à deviner, les limites de la plage de nombres, 
le moment où le jeu a commencé, etc. """

class GuessNumber(Screen):
    def __init__(self, **kwargs):
        super(GuessNumber, self).__init__(**kwargs)
        self.ids.debut = 0 # Initialisation de l'heure de début du jeut
        self.ids.temps_restant = 0 # Temps restant
        self.ids.temps_label.text ='00:00' # Widget Label affichant le temps restant
        self.ids.timer = None # Le chronométrage
        self.ids.a=1 # La borne inférieure de la plage de nombres sur laquelle est choisie le nombre à deviner
        self.ids.b=n # La borne supérieure
        self.ids.c = (self.ids.a + self.ids.b)//2 # Le centre près de la plage
        self.ids.resultat_label.text = 'Click on Start Game to start' # Widget label affichant le statut du choix du joueur (plus grand/ plus petit/...) 
        self.ids.input.text = '' # Widget TextInput qui affiche reçoit les chiffres entrés par l'utilisateur.
        self.ids.start=0 # définit si le jeu est encours (start=1) ou pas (start=0)
        self.ids.nombre_mystere=0 # définit le nombre à déviner

    #Mise à jour du temps restant
    def update_time(self, dt):
        if self.ids.start==1: # Le jeu est encours
            self.ids.temps_restant = 90-(time.time() - self.ids.debut)
            if self.ids.temps_restant>0:# Il reste encore du temps au joueur
                minutes, seconds = divmod(self.ids.temps_restant, 60) # convertir en minutes et secondes
                self.ids.temps_label.text = "{:02.0f}:{:02.0f}".format(minutes, seconds)
            else: # Le temps accordé au joueur est épuisé sans qu'il ne trouve le nombre à défiver 
                self.ids.timer.cancel() # Arreter le chrono
                self.ids.start=0       
                self.ids.temps_label.text = "Game over !!!"
                self.ids.resultat_label.text = "Ouff... I just imagined : {}".format(self.ids.nombre_mystere)
                Sound.stop() # Arreter le son du jeu
    # Méthode de demarrage du jeu
    def startGame(self):
        Sound.play() # Jouer le son du jeu
        self.ids.start=1
        self.ids.input.text='' 
        self.ids.a=1
        self.ids.b=n
        self.ids.nombre_mystere = randint(self.ids.a,self.ids.b) # choisir le nombre à deviner
        self.ids.debut = time.time() # fixer l'heure du début du jeu
        self.ids.timer = Clock.schedule_interval(self.update_time, 1) # débuter le chronomètrage
        self.ids.resultat_label.text = 'What number did I immagine ?'
        self.ids.c = (self.ids.a + self.ids.b)//2
    # Méthode d'arrêt du jeu
    def EndGame(self):
        if self.ids.start==1 :# si Le jeu est en cours
            self.ids.resultat_label.text = "Ouff... I just imagined : {}".format(self.ids.nombre_mystere) # Afficher le nombre que l'utilisateur devrait deviner
            self.ids.timer.cancel() # Arreter le chronomètrage
            self.ids.start=0
            Sound.stop() # Arreter le son du jeu
    # Méthode restaurer le jeu 
    def resetGame(self):
        if self.ids.start==1: # faire si le jeu est encours
            Sound.stop()
        self.__init__() # initialiser
    # La méthode : vérifier si le nombre entré correspond au nombre à deviner
    def check_number(self):
        if self.ids.start==1: # faire si le jeu est encours
            Check.play() # son de la touche
            if self.ids.input.text=='': # Si il' a pas de nombre de le TextImput à vérifié, demander au joueur de deviner un nombre d'abord
                self.ids.resultat_label.text = 'Guess the number first'
            else:
                rep = int(self.ids.input.text)-self.ids.nombre_mystere
                if rep <0: # le nombre à déviner est plus grand
                    self.ids.a = int(self.ids.input.text)+1 # mettre à jour la borne inférieure
                    self.ids.resultat_label.text = 'Larger, check in : [{} - {}]'.format(self.ids.a,self.ids.b) 
                    self.ids.input.text=''
                elif rep>0: # le nombre à déviner est plus grand
                    self.ids.b=int(self.ids.input.text)-1 # mettre à jour la borne supérieure
                    self.ids.resultat_label.text = 'Smaller, check : [{} - {}]'.format(self.ids.a,self.ids.b)
                    self.ids.input.text=''
                else:   # Le joueur a trouver le nombre à deviner
                    self.ids.resultat_label.text ='Congratulations, you won the game !'
                    self.ids.timer.cancel() # Arrêter le chronométrage
                    Sound.stop() # Arrêter le son du jeu
                    Applaud.play() # Jouer le son d'applaudissement
                    self.ids.start=0
                self.ids.c = (self.ids.a + self.ids.b)//2 
    # La méthode entrer la borne inférieure de la plage sur laquelle le joueur va deviner le nombre (liée à la touche a)
    def a(self):
        self.ids.input.text += str(self.ids.a)
    # La méthode entrer la borne supérieure (liée la touche b du clavier numérique)
    def b(self):
        self.ids.input.text += str(self.ids.b)
    # La méthode entrer le centre près de la page (liée à la touche de recherche dichotomique)
    def c(self):
        self.ids.input.text += str(self.ids.c) 
    # La méthode supprimer tous les caractère du TextInput
    def clear(self):
        if self.ids.start==1:
            self.ids.input.text=''
    # La méthode supprimer le dernier caractère entré
    def remove(self):
        if self.ids.start==1:
            self.ids.input.text = self.ids.input.text[:-1]   
    # La méthode n'autoriser pas l'entrée des caractère non numériques et l'entrée de n'importe quel caratère dans le cas où le jeu n'est n'est pas encours
    def on_text(self, TextInput, value):
        if not value.isdigit() or self.ids.start==0 :
            self.ids.input.text = self.ids.input.text[:-1]

# Créer une instance de la classe gestionnaire d'écran 
ScreenManagement = ScreenManager(transition=FadeTransition())
# Ajouter la page d'acceuil
ScreenManagement.add_widget(HomePage(name ="Home"))
# Ajouter la page du jeu
ScreenManagement.add_widget(GuessNumber(name ="GuessNumber"))

"""La classe "GameNumberApp" hérité de la classe "App" de Kivy définit une méthode build() 
utilisée pour construire l'interface  utilisateur de l'application, qui définit le titre de l'application 
comme "Riddling game" et retourne un objet "ScreenManagement". 
Enfin, l'instanciation de la classe "GameNumberApp" et l'appel de la méthode run() démarrent l'application."""
class GameNumberApp(App):
    def build(self):
        self.title = "Riddling game"
        return ScreenManagement

GameNumberApp().run()
    
