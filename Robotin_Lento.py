import pygame
import random

class Robo:
    g = -0.2
    def __init__(self,robo):
        self.korkeus = robo[0].get_height()
        self.leveys = robo[0].get_width()
        self.x = 150
        self.y = 480-self.korkeus
        self.nopeus = 0
        
    
    def move(self,ylos):
        if ylos :
            self.nopeus += Robo.g
        else:
            self.nopeus -= Robo.g
        
        if self.y + self.nopeus <0 or self.y + self.nopeus > 480-self.korkeus:
            self.nopeus = 0
        else:
            self.y += self.nopeus
    

class Lentava:
    def __init__(self,kuva):
        self.x = 640
        self.kuva = kuva[0]
        self.korkeus = kuva[0].get_height()
        self.leveys = kuva[0].get_width()
        self.i = kuva[1]
        self.y = random.randint(0,480-self.korkeus)
        self.nopeusy = 0
        self.nopeusx = -1
    
    def move(self):
        self.y += self.nopeusy
        self.x += self.nopeusx
        if self.x < 0 and self.nopeusy!=0:
            return True
        else:
            return False

class Hyppy:
    def __init__(self):
        pygame.init()
    
        self.lataa_kuvat()
        self.korkeus = 480
        self.leveys = 640

        self.taajuus = 120

        pygame.display.set_caption("Robotin lento")
        
        self.uusi_peli()

        

    def lataa_kuvat(self):
        self.kuvat = []
        self.nimet = ["robo","hirvio","kolikko","ovi"]
        i = 0
        for nimi in self.nimet:
            self.kuvat.append((pygame.image.load(nimi + ".png"),i))
            i+=1

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
    
    def uusi_peli(self):

        self.robotti = Robo(self.kuvat[0])

        self.lentavat = []

        self.laskuri = 0

        self.ylos = False

        self.kello = pygame.time.Clock()

        self.havio = False

        self.pisteet = 0

        self.ero = 15
        
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.silmukka()
                
    
    def lisaa(self,laskuri):
        luku = random.randint(1,self.taajuus)
        laskuri += 1
        if luku == 1 and laskuri>self.taajuus:
            murkula = Lentava(self.kuvat[1])
            self.lentavat.append(murkula)
            laskuri = 0
        if luku == 2 and laskuri>self.taajuus:
            murkula = Lentava(self.kuvat[2])
            self.lentavat.append(murkula)
            laskuri = 0
        return laskuri

    def piirra_naytto(self):
        self.naytto.fill((0, 100, 0))  
        
        self.naytto.blit(self.kuvat[0][0], (self.robotti.x,self.robotti.y))
        if self.ylos:
            self.naytto.blit(self.kuvat[3][0], (self.robotti.x,self.robotti.y+self.robotti.korkeus-self.ero))

        for alkio in self.lentavat:
            totuus = alkio.move()
            if self.robotti.x + self.robotti.leveys > alkio.x and self.robotti.x < alkio.x + alkio.leveys:
                if self.robotti.y < alkio.y + alkio.korkeus and self.robotti.y + self.robotti.korkeus > alkio.y:
                    
                    if alkio.i == 1:
                        self.havio = True
                        self.lentavat.remove(alkio)
                    if alkio.i == 2:
                        self.pisteet += 1
                        self.lentavat.remove(alkio)
            

            if alkio in self.lentavat:        
                if self.ylos:
                    if self.robotti.x + self.robotti.leveys > alkio.x and self.robotti.x < alkio.x + alkio.leveys:
                        if self.robotti.y+self.robotti.korkeus-self.ero<alkio.y+alkio.korkeus and self.robotti.y+self.robotti.korkeus-self.ero+self.kuvat[3][0].get_height()>alkio.y:
                            
                            self.lentavat.remove(alkio)
                    
            
            if alkio.x+alkio.leveys<0:
                if alkio.i == 2:
                    self.havio = True
                self.lentavat.remove(alkio)
            
            
            if totuus:
                tulos = True
            self.naytto.blit(alkio.kuva, (alkio.x, alkio.y))
        
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render(f"Pisteet: {self.pisteet}                                                                F2: Uusi peli      Esc: Poistu", True, (255, 0, 0))
        self.naytto.blit(teksti, (0,0))
        pygame.display.flip()
    
    def silmukka(self):
        
        while True:
            self.tutki_tapahtumat()
            self.laskuri = self.lisaa(self.laskuri)
            self.robotti.move(self.ylos)
            self.piirra_naytto()
            self.kello.tick(self.taajuus)
            if self.havio:
                break
            #print(self.lentavat)
        
        
        self.naytto.fill((0, 100, 0))
        fontti = pygame.font.SysFont("Arial", 30)
        teksti1 = fontti.render("Hävisit pelin :(", True, (255, 0, 0))
        teksti1x = self.leveys/2 - teksti1.get_width()/2
        teksti1y = self.korkeus/2 - teksti1.get_height()
        self.naytto.blit(teksti1, (teksti1x, teksti1y))
        teksti2 = fontti.render(f"Loppupisteet: {self.pisteet}",True, (255, 0, 0))
        teksti2x = teksti1x
        teksti2y = self.korkeus/2 
        self.naytto.blit(teksti2, (teksti2x, teksti2y))
        fontti = pygame.font.SysFont("Arial", 24)
        teksti = fontti.render(f"Pisteet: {self.pisteet}                                                                F2: Uusi peli      Esc: Poistu", True, (255, 0, 0))
        self.naytto.blit(teksti, (0,0))
        pygame.display.flip()
        while True:
            self.tutki_tapahtumat()
        
            

if __name__=="__main__":
    Hyppy()
