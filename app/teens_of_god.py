from asyncio.windows_events import NULL
import pandas as pd
import pygame as pg
import pygame.camera
import pygame.image
import png
import pyqrcode
from cv2 import flip,rotate,ROTATE_90_COUNTERCLOCKWISE,imread,imwrite,QRCodeDetector
import day
from datetime import date

global display,base_font,users,passs,volu,UID,att
clock=pg.time.Clock()
FPS=5
white=(255,255,255)
black=(0,0,0)
grey=(50,50,50)
blue=(0,0,255)
yellow=(255,255,0)
red=(255,0,0)
green=(0,255,0)
over=0
start=pg.init()
stta=True
FPS=30
display=pg.display.set_mode((700,700),pg.RESIZABLE)
pg.display.set_caption("Teens of God")
base_font = pg.font.Font(None, 32)
alpha=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

admins=pd.read_csv("admin.csv")
users=list(admins["username"])
passs=list(admins["password"])

volu=pd.read_csv("volunterr.csv")
UID=list(volu["email"])
dat=date.today().strftime(r"-%m-%Y")
d=date.today().strftime(r"%d")
dayy=date.today().strftime(r"%a")
if (dayy=="Mon" and day.x==0):
    days=["name","email"]+alpha
    att=pd.DataFrame(columns=days)
    att.to_csv(dat+".csv")
    day.x=1
elif(dayy=="Sun"):
    day.x=0
dat=str(int(d)-alpha.index(dayy))+dat
att=pd.read_csv(dat+".csv")
email=att["email"]


def scan():
    global display
    pg.camera.init()

    cameras = pg.camera.list_cameras()

    webcam = pg.camera.Camera(cameras[0])
    webcam.start()
    img = webcam.get_image()

    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    display=pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption("Qrcode scanner") 
    click=base_font.render("Click",True,red,blue)
    click=pg.transform.rotozoom(click,0,2)
    clickr=click.get_rect()
    clickr.center=(WIDTH/2,HEIGHT-200)
    backk=base_font.render("<<",True,white,None)
    backk=pg.transform.rotozoom(backk,0,2)
    backkr=backk.get_rect()
    backkr.center=(30,30)
    sstt=True
    while(sstt):
        for event in pg.event.get() :
            if event.type == pg.QUIT :
                sstt=False
                pg.quit()
                exit
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1:
                    if(backkr.collidepoint(event.pos)):
                        sstt=False
                        return 0
                    if(clickr.collidepoint(event.pos)):
                        sstt=False
                        return img
        display.blit(img, (0,0))
        display.blit(click,clickr)
        display.blit(backk,backkr)
        pg.display.flip()  
        img = webcam.get_image()
        clock.tick(80)
def add_vol():
    global display
    activec=pg.Color('white')
    passivec=pg.Color('yellow')
    name=base_font.render("Name : ",True,white,None)
    contactt=base_font.render("Contact no : ",True,white,None)
    email=base_font.render("Email-ID : ",True,white,None)
    addhar=base_font.render("Addhar num : ",True,white,None)
    namer=name.get_rect()
    contacttr=contactt.get_rect()
    emailr=email.get_rect()
    addharr=addhar.get_rect()
    namer.center=(200,100)
    contacttr.center=(225,180)
    emailr.center=(213,140)
    addharr.center=(230,220)
    creat=pg.image.load("create.png")
    creat=pg.transform.rotozoom(creat,0,0.3)
    creatr=creat.get_rect()
    creatr.center=(350,350)

    backk=base_font.render("<<",True,red,None)
    backk=pg.transform.rotozoom(backk,0,2)
    backkr=backk.get_rect()
    backkr.center=(30,30)
    warn=0
    global warnn
    warnn=base_font.render("Please enter the details correctly",True,red,None)
    warnnr=warnn.get_rect()
    warnnr.center=(350,350)
    global qrcod
    qrcod=NULL
    qrcodr=NULL
        


    tbox=[NULL,NULL,NULL,NULL]
    class textbox():
        def __init__(self,x,y):
            self.text=""
            self.color=passivec
            self.surf=base_font.render(self.text,True,blue,None)
            self.rect=pg.Rect(x,y,140,32)
            self.rect.w=max(100,self.surf.get_width()+10)

    for i in range(0,4):
        tbox[i]=textbox(250+i*20,85+i*40)

    vstt=True
    while(vstt):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                vstt=False
                exit
                pg.quit()
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1:
                    if(backkr.collidepoint(event.pos)):
                        vstt=False
                    for i in range(0,len(tbox)):
                        if tbox[i].rect.collidepoint(event.pos):
                            tbox[i].color=activec
                        else: tbox[i].color=passivec
                    if creatr.collidepoint(event.pos):
                        for i in range(len(tbox)):
                            if len(tbox[i].text)==0:
                                warn=120
                                for i in range(len(tbox)):
                                    tbox[i].text=""
                        if(warn==120): continue
                        qrcod=pyqrcode.create(tbox[1].text)
                        qrcod.png("qrcodee.png",scale=6)
                        volu.loc[len(volu.index)]=[tbox[0].text,tbox[1].text,tbox[2].text,tbox[3].text]
                        att.loc[len(att.index)]=[tbox[0].text,tbox[1].text,0,0,0,0,0,0,0]
                        print(tbox[0].text,tbox[1].text,tbox[2].text,tbox[3].text)
                        volu.to_csv("volunterr.csv",index=False)
                        att.to_csv(dat+".csv",index=False)
                        warnn=base_font.render("New volunteer created succesfully. Click the qrcode to continue",True,green,None)
                        warn=-1
                        warnnr.center=(190,400)
                        qrcod=pg.image.load("qrcodee.png")
                        qrcodr=qrcod.get_rect()
                        qrcodr.center=(350,100)
                        print("done successfully")
                    try:
                        if qrcodr.collidepoint(event.pos):
                            warn=0
                            vstt=False
                    except:
                        continue
                
            if(event.type == pg.KEYDOWN):
                if event.key == pg.K_BACKSPACE:
                    for i in range(0,len(tbox)):
                        if tbox[i].color==activec:
                            tbox[i].text = tbox[i].text[:-1]
                else:
                    for i in range(0,len(tbox)):
                        if tbox[i].color==activec:
                            tbox[i].text += event.unicode

        display.fill((20,0,60))
        if(warn>0):
            display.blit(warnn,warnnr)
            pg.display.flip()
            warn-=1
            clock.tick(60)
            continue
        if(warn==-1):
            display.blit(warnn,warnnr)
            display.blit(qrcod,qrcodr)
            pg.display.flip()
            clock.tick(60)
            continue
        for i in range(len(tbox)):
            tbox[i].surf=base_font.render(tbox[i].text,True,blue,None)
            tbox[i].rect.w=max(100,tbox[i].surf.get_width()+10)
            pg.draw.rect(display,tbox[i].color,tbox[i].rect)
            display.blit(tbox[i].surf,tbox[i].rect)
        display.blit(backk,backkr)
        display.blit(creat,creatr)
        display.blit(name,namer)
        display.blit(contactt,contacttr)
        display.blit(email,emailr)
        display.blit(addhar,addharr)
        pg.display.flip()
        clock.tick(60)
    

def view_attendance():
    global display
    datax,datay=100,100
    next=base_font.render(">>",True,red)
    prev=base_font.render("<<",True,red)
    nextr=next.get_rect()
    prevr=prev.get_rect()
    prevr.center=(300,600)
    nextr.center=(390,600)
    backk=base_font.render("<<",True,red,None)
    backkr=backk.get_rect()
    backkr.center=(30,30)
    download=base_font.render("Download data.",True,yellow,None)
    downloadr=download.get_rect()
    downloadr.center=(360,650)

    class shower():
        def __init__(self,x,datax,datay):
            self.surf=base_font.render(x,True,white,None)
            self.surf=pg.transform.rotozoom(self.surf,0,0.6)
            self.rect=self.surf.get_rect()
            self.rect.center=(datax,datay)
        def blitt(self):
            display.blit(self.surf,self.rect)
            pg.display.flip()
    
    astt=True
    i,j=0,0
    colum=0
    display.fill((20,0,60))
    while(astt):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                astt=False
                pg.quit()
                exit
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1:
                    if backkr.collidepoint(event.pos):
                        astt=False
                    elif prevr.collidepoint(event.pos):
                        if i>=10:
                            i-=10
                            j=0
                            colum=0
                            display.fill((20,0,60))
                    elif nextr.collidepoint(event.pos):
                        if i<len(att.index):
                            i+=10
                            j=0
                            colum=0
                            display.fill((20,0,60))
        if colum==0:
            colum=100
            for t in range(len(att.columns)):
                text=str(att.columns[t])
                userr=shower(text,colum,50)
                userr.blitt()
                if(t==0 or t==1):
                    colum+=100
                else: colum+=50
            colum=0
        if colum==0:
            colum=i
            while((datay<600) and (j<len(att.columns))):
                while(datax<650 and (i<colum+10) and (i<len(att.index))):
                    text=str(att.iloc[i,j])
                    userr=shower(text,datax,datay)
                    userr.blitt()
                    i+=1
                    datay+=50
                j+=1
                i=colum
                datay=100
                if(j==1 or j==2):
                    datax+=100
                else: datax+=50
            datax,datay=100,100
            i=colum
            colum=1
        display.blit(backk,backkr)
        display.blit(prev,prevr)
        display.blit(next,nextr)
        display.blit(download,downloadr)
        pg.display.flip()
        clock.tick(60)
        


def dashboard():
    global display
    scanner=pg.image.load("scanner.png")
    scannerr=scanner.get_rect()
    scannerr.center=(200,200)
    newvol=pg.image.load("newvolu.png")
    newvolr=newvol.get_rect()
    newvolr.center=(300,300)
    atndnc=pg.image.load("attendance.png")
    atndncr=atndnc.get_rect()
    atndncr.center=(400,200)
    found=base_font.render("Not found",True,red,blue)
    foundr=found.get_rect()
    foundr.center=(150,350)
    backk=base_font.render("<<",True,red,None)
    backk=pg.transform.rotozoom(backk,0,2)
    backkr=backk.get_rect()
    backkr.center=(30,30)

    cover=pg.image.load("back.jpg")
    cover=pg.transform.rotozoom(cover,0,0.5)
    coverr=cover.get_rect()
    coverr.center=(350,350)    
    got=0

    dstt=True
    while(dstt):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                dstt=False
                pg.quit()
                exit
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1:
                    if(backkr.collidepoint(event.pos)):

                        dstt=False
                    if newvolr.collidepoint(event.pos):
                        add_vol()
                    elif scannerr.collidepoint(event.pos):
                        image=scan()
                        if image==0:
                            display=pg.display.set_mode((700,700))
                            pg.display.set_caption("Teens of God")
                            continue
                        image=pg.surfarray.array3d(image)
                        image=flip(image,1)
                        image=rotate(image, ROTATE_90_COUNTERCLOCKWISE)
                        display.fill(white)
                        imwrite("qrcodee1.png",image)
                        display=pg.display.set_mode((700,700))
                        pg.display.set_caption("Teens of God")
                        try:
                            image=imread("qrcodee1.png")
                            detect=QRCodeDetector()
                            image, points, straight_qrcode = detect.detectAndDecode(image)
                            email_ind=list(att["email"]).index(image)
                            print(email_ind,alpha.index(dayy))
                            att.iloc[email_ind,alpha.index(dayy)+2]=1
                            att.to_csv(dat+".csv",index=False)
                            print(1)
                            UID=list(volu["email"])
                            if(image in UID):
                                email_ind=UID.index(image)
                                found=base_font.render("Found the record and marked present",True,green,blue)
                            got=120
                        except:
                            got=120
                    elif atndncr.collidepoint(event.pos):
                        view_attendance()
        display.fill((20,0,60))
        if(got>0):
            display.blit(found,foundr)
            pg.display.flip()
            got-=1
            clock.tick(60)
            continue
        display.blit(cover,coverr)
        display.blit(backk,backkr)
        display.blit(scanner,scannerr)
        display.blit(atndnc,atndncr)
        display.blit(newvol,newvolr)
        pg.display.flip()
        clock.tick(60)


def login():
    lstt=True
    global display
    user_rect = pg.Rect(300, 285, 140, 32)
    pass_rect = pg.Rect(300, 330, 140, 32)
    username = ''
    password=''
    hashh=''
    show=0
    x=0
    active=False
    passive=False

    op1=base_font.render("Username:",True,white,None)
    op1r=op1.get_rect()
    op1r.center=(200,300)
    op2=base_font.render("Password:",True,white,None)
    op2r=op2.get_rect()
    op2r.center=(200,350)
    logg=pg.image.load("logg.png")
    logg=pg.transform.rotozoom(logg,0,0.5)
    loggr=logg.get_rect()
    loggr.center=(350,500)
    eye=pg.image.load("eye.png")
    eye=pg.transform.rotozoom(eye,0,0.1)
    eyer=eye.get_rect()
    eyer.center=(440,345)
    logo=pg.image.load("logo.png")
    logo=pg.transform.rotozoom(logo,0,0.7)
    logor=logo.get_rect()
    logor.center=(350,130)

    color_active = pg.Color('white')
    color_passive = pg.Color('yellow')
    color = color_passive
    color2=color_passive

    while(lstt):
        dt=clock.tick(FPS)/1000
        for event in pg.event.get():
            if event.type==pg.QUIT:
                lstt=False
                pg.quit()
                exit
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1:
                    if user_rect.collidepoint(event.pos):
                        active=True
                        passive=False
                    elif pass_rect.collidepoint(event.pos):
                        active=False
                        passive=True
                    elif eyer.collidepoint(event.pos):
                        show=1
                    elif loggr.collidepoint(event.pos):
                        try:
                            if(users.index(username)==passs.index(password)):
                                print(f"{username} logged in!")
                                username=""
                                password=""
                                hashh=""
                                dashboard()
                        except:
                            pass
                
            if(event.type == pg.KEYDOWN) and (active==True):
                if event.key == pg.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif(event.type == pg.KEYDOWN) and (passive==True):
                if event.key == pg.K_BACKSPACE:
                    password = password[:-1]
                    hashh=hashh[:-1]
                    x-=1
                    if(x>6):
                        eyer.x-=10
                else:
                    password += event.unicode
                    hashh+="1"
                    x+=1
                    if(x>6):
                        eyer.x+=10
        display.fill((20,0,60))
        if active:
            color = color_active
            color2=color_passive
        elif passive:
            color = color_passive
            color2=color_active
    
        display.blit(op1,op1r)
        display.blit(op2,op2r)

        display.blit(logo,logor)
        user_text = base_font.render(username, True, (0,0, 255))
        pass_text = base_font.render(password, True, (0,0, 255))
        hash_text = base_font.render(hashh,True,(0,0,60))

        user_rect.w=max(100,user_text.get_width()+10)
        pass_rect.w=max(100,pass_text.get_width()+10)

        pg.draw.rect(display,color,user_rect)
        pg.draw.rect(display,color2,pass_rect)

        display.blit(eye,eyer)
        display.blit(logg,loggr)
        display.blit(user_text,(user_rect.x+5, user_rect.y+5))
        if(show):
            display.blit(pass_text,(pass_rect.x+5, pass_rect.y+5))
            show+=1
        else:
            display.blit(hash_text,(pass_rect.x+5, pass_rect.y+5))
        if(show>25):
            show=0
        pg.display.flip()
        clock.tick(60)

            

while(stta):
    dt=clock.tick(FPS)/1000
    go=pg.image.load("started.png").convert_alpha()
    go=pg.transform.rotozoom(go,0,0.3)
    gor=go.get_rect()
    gor.center=(350,350)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            stta=False
            exit
        elif event.type==pg.MOUSEBUTTONDOWN:
            if event.button==1:
                if(gor.collidepoint(event.pos)):
                    login()
        display.fill((20,0,60))
        display.blit(go,gor)
        pg.display.flip()   
    clock.tick(60)
pg.quit()
exit()