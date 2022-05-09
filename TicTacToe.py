import mysql.connector as mycon #library for connecting to MySQL database.
import random
import time
import os

#global variable to identify if player is having move X or O-----
XorO=''
#----------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------------------------#

#checks for the winner by running all possible testcases and returns true/false accordingly
def wincheck(roomid):

    box=boXValueFetcher(roomid)

    if (box[0]=='X' and box[1]=='X' and box[2]=='X') or (box[0]=='O' and box[1]=='O' and box[2]=='O'):
        return True
    elif (box[3]=='X' and box[4]=='X' and box[5]=='X') or (box[3]=='O' and box[4]=='O' and box[5]=='O'):
        return True
    elif (box[6]=='X' and box[7]=='X' and box[8]=='X') or (box[6]=='O' and box[7]=='O' and box[8]=='O'):
        return True
    elif (box[0]=='X' and box[3]=='X' and box[6]=='X') or (box[0]=='O' and box[3]=='O' and box[6]=='O'):
        return True
    elif (box[1]=='X' and box[4]=='X' and box[7]=='X') or (box[1]=='O' and box[4]=='O' and box[7]=='O'): 
        return True
    elif (box[2]=='X' and box[5]=='X' and box[8]=='X') or (box[2]=='O' and box[5]=='O' and box[8]=='O'):
        return True
    elif (box[0]=='X' and box[4]=='X' and box[8]=='X') or (box[0]=='O' and box[4]=='O' and box[8]=='O'): 
        return True
    elif (box[2]=='X' and box[4]=='X' and box[6]=='X') or (box[2]=='O' and box[4]=='O' and box[6]=='O'): 
        return True
    else:
        return False


#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#creates the user interface of tic-tac-toe
def ui(boxValue):
    
    os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
    print("TIC-TAC-TOE")
    
    print("YOUR MOVE:'",XorO,"'",sep="")
    print()
    
    print("      |     |")
    print("  ",boxValue[0]," | ",boxValue[1]," | ",boxValue[2],)
    print(" _____|_____|_____")
    print("      |     |")
    print("  ",boxValue[3]," | ",boxValue[4]," | ",boxValue[5],)
    print(" _____|_____|_____")
    print("      |     |")
    print("  ",boxValue[6]," | ",boxValue[7]," | ",boxValue[8],)
    print("      |     |")
    print()


#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#fetches freshly updated boxvalues from database by reconnecting to it
def boXValueFetcher(roomid):

    time.sleep(0.2)#to avoid fast database refreshes.

    #reconnecting to database as mysql creates a session for you so if a person
    #playing  with you  play any move than it will  not reflect on your system,
    #to avoid that thing we need to reconnect it to again and again.
    #****dbcon-1****
    database=mycon.connect(host='shubhamistic.com',user='TicTacToe',password='tictactoe@123',database='TicTacToe')
    cursor=database.cursor()
    
    cmd="""SELECT boxvalue1,
                  boxvalue2,
                  boxvalue3,
                  boxvalue4,
                  boxvalue5,
                  boxvalue6,
                  boxvalue7,
                  boxvalue8,
                  boxvalue9
                  FROM rooms
                  WHERE roomid='%s'
                  """%(roomid)
    cursor.execute(cmd)
    boxValue=cursor.fetchone()

    return boxValue


#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#print the result after completion of match.
def afterMatchScreen(msg,roomid):#msg-message to be printed
    
    os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
    print("TIC-TAC-TOE")
    print()
    print(msg)
    print()

    #changing the room status back to 'unused' as user choosed to go back to the home screen.
    cmd="UPDATE roomlist SET status='unused' WHERE roomid='%s'"%(roomid)
    cursor.execute(cmd)
    database.commit()
    
    input("[ENTER] HOME")
    return


#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#step-4
#play-----------------
#main playing algorithm
def play(roomid):

    global XorO

    for i in range(10):

        if (i==9):
            afterMatchScreen("MATCH DRAW",roomid)
            return

        #reconnecting to database to see whose move is there.
        #****dbcon-2****
        database=mycon.connect(host='shubhamistic.com',user='TicTacToe',password='tictactoe@123',database='TicTacToe')
        cursor=database.cursor()
        
        cmd="SELECT turn FROM rooms WHERE roomid='%s'"%(roomid)
        cursor.execute(cmd)
        turn=cursor.fetchone()[0]

        if (turn==XorO):

            if wincheck(roomid):
                afterMatchScreen("OPPONENT WON",roomid)
                return   
                        
            while True:

                #fetching box values from database
                boxValue=boXValueFetcher(roomid)

                ui(boxValue)

                move=input("YOUR TURN>>> ")
                if (move not in ['1','2','3','4','5','6','7','8','9']):
                    continue

                cmd="SELECT boxvalue%s FROM rooms WHERE roomid='%s'"%(move,roomid)
                cursor.execute(cmd)
                res=cursor.fetchone()

                if (res[0]=='X' or res[0]=='O'):
                    continue
                else:
                    break

            if (XorO=='X'):
                nextturn='O'
            else:
                nextturn='X'
            
            cmd="UPDATE rooms SET boxvalue%s='%s' , turn='%s' WHERE roomid='%s'"%(move,XorO,nextturn,roomid)
            cursor.execute(cmd)
            database.commit()
                
            if wincheck(roomid):
                afterMatchScreen("YOU WON",roomid)
                return

        else:

            #fetching box values from database
            boxValueA=boXValueFetcher(roomid)

            ui(boxValueA)
            print("OPPONENT's TURN...")
                                    
            while True:

                #fetching box values from database
                boxValue=boXValueFetcher(roomid)

                if (boxValueA==boxValue):
                    continue
                else:
                    ui(boxValue)
                    break

            if (i==8):
                afterMatchScreen("MATCH DRAW",roomid)
                return
            
                
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#step-3
#loading Screen-------
def loadScreen(roomid):

    global XorO

    os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
    print("TIC-TAC-TOE")
    print()

    print("ROOM CODE: '",roomid,"'.",sep='')
    print()

    print("WAITING FOR PLAYER")
    print("TO JOIN...")

    #checking if player joined or not
    while True:

        time.sleep(1)#to avoid fast database refreshes.

        #reconnecting to database to check if second player joined or not.
        #****dbcon-3****
        database=mycon.connect(host='shubhamistic.com',user='TicTacToe',password='tictactoe@123',database='TicTacToe')
        cursor=database.cursor()
        
        cmd="SELECT joined FROM rooms WHERE roomid='%s'"%(roomid)
        cursor.execute(cmd)
        joined=cursor.fetchone()[0]
   
        if (joined=='0'):
            continue
        else:
            break
        
    play(roomid)
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#step-2
#frontPageFunctions----------------------------------------------
class frontPageFuncs:

    #func-1---------------
    def createRoom():

        global XorO
        
        #getting an unused room from the database
        cmd="SELECT roomid FROM roomlist WHERE status='unused'"
        cursor.execute(cmd)
        roomid=cursor.fetchall()[0][0]

        #getting date & time from the server
        cmd="SELECT NOW()"
        cursor.execute(cmd)
        datetime=cursor.fetchall()[0][0]

        #changing the room status to 'used' as it is being used by us
        cmd="UPDATE roomlist SET status='used' , time='%s' WHERE roomid='%s'"%(datetime,roomid)
        cursor.execute(cmd)
        database.commit()
        
        #X or O selection---------
        XorO=random.randint(0,1)
        if (XorO=='0'):
            XorO='O'
            joiner='X'
        else:
            XorO='X'
            joiner='O'

        #----------------------------------------------------------

        #ui-create room-----------------------------------------------------------------------------------
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
            
            print("TIC-TAC-TOE")
            print()

            print("[1] PLAY")
            print("[2] BACK")
            print()
            ch=input(">>> ")
            if (ch=='1'):

                #clearing up the room's garbage values to default values---
                cmd="""UPDATE rooms SET owner='%s',
                                        joiner='%s',
                                        joined='0',
                                        boxvalue1='1',
                                        boxvalue2='2',
                                        boxvalue3='3',
                                        boxvalue4='4',
                                        boxvalue5='5',
                                        boxvalue6='6',
                                        boxvalue7='7',
                                        boxvalue8='8',
                                        boxvalue9='9'
                                        WHERE roomid='%s'
                                        """%(XorO,joiner,roomid)
                cursor.execute(cmd)
                database.commit()
                
                loadScreen(roomid)

                return
                  
            elif (ch=='2' or ch.upper()=='BACK' ):
                
                #changing the room status back to 'unused' as user choosed to go back to the home screen.
                cmd="UPDATE roomlist SET status='unused' WHERE roomid='%s'"%(roomid)
                cursor.execute(cmd)
                database.commit()
                return

        #--------------------------------------------------------------------------------------------------


            
    #func-2---------------- 
    def joinRoom():

        global XorO
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
            
            print("TIC-TAC-TOE")
            print()
            print("[1] BACK")
            print()
            roomid=input("ENTER ROOM CODE: ")

            if (roomid=='1' or roomid.upper()=='BACK'):
                return

            #checking room code if valid or not
            cmd="SELECT joined FROM rooms WHERE roomid='%s'"%(roomid)
            cursor.execute(cmd)
            joined=cursor.fetchone()
            
            if joined==None:
                continue
            elif joined[0]=='1':
                continue

            print()
            print("[1] PLAY")
            print("[2] BACK")
            print()
            ch=input(">>> ")
            if (ch=='1'):
                
                #changing the joined status to '1' so that no one can be added anymore.
                cmd="UPDATE rooms SET joined='1' WHERE roomid='%s'"%(roomid)
                cursor.execute(cmd)
                database.commit()

                cmd="SELECT joiner FROM rooms WHERE roomid='%s'"%(roomid)
                cursor.execute(cmd)
                XorO=cursor.fetchone()[0]
                
                play(roomid)

                return
                      
            elif (ch=='2' or ch.upper()=='BACK' ):
                
                #changing the joined status back to '0' so that any other user can join.
                cmd="UPDATE rooms SET joined='0' WHERE roomid='%s'"%(roomid)
                cursor.execute(cmd)
                database.commit()
                return


#------------------------------------------------------------------------------------------------------------------------------------------------------------#
            

#step-1 
def frontPage():#void function
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')#clear-screen
        
        print("TIC-TAC-TOE")
        print()

        print("[1] CREATE ROOM")
        print("[2] JOIN ROOM")
        print("[3] EXIT")
        print()
        
        ch=input(">>> ")

        if (ch=='1'):
            frontPageFuncs.createRoom()

        elif (ch=='2'):
            frontPageFuncs.joinRoom()

        elif (ch=='3' or ch.upper()=='EXIT'):
            return

#------------------------------------------------------------------------------------------------------------------------------------------------------------#


#__main__
#try:
for i in range(1):
    #****dbcon-4****
    database=mycon.connect(host='shubhamistic.com',user='TicTacToe',password='tictactoe@123',database='TicTacToe')
    cursor=database.cursor()
  
    #front-page-----------------------------------------------------------
    frontPage()

else:        
#except:#if any other exception occurs this print.
    print("error connecting to database.")
       




        
        
