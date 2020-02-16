from tqdm import tqdm
import requests
import os
from bs4 import BeautifulSoup
drive=str(input('select the drive-C /D /E /F >')).upper()
try:
    os.mkdir(f'{drive}:/remix_songs')
except:
    pass    
os.chdir(f'{drive}:/remix_songs')

def songparser():
    songname=str(input('Enter song name: ')).lower()
    url='https://djking.co.in/search.php/'
    # songname='senorita'
    # value=songname.replace(' ','+')
    print('SEARCHING FOR BEST RESULT WAIT..............')
    
    
    payload={'key':f'{songname}'}
    r=requests.get(url,params=payload)

    clist=[]

    searchsoup=BeautifulSoup(r.content, 'html.parser')
    c=list(searchsoup.find("div",{'class':'catList'}))

    if c is None:
        print('Query not found')
    else:
        for i in range(len(c)):
            print(f'song.{i+1}: {c[i].text}')
            clist.append(c[i])
    return clist


while True:
    while True:
        try:
            clist=songparser()
        
        except:
            print('song not found') 
            clist=songparser()   

        print('.....CONTINUE TO DOWNLOAD[Y/N]?......')
        res=str(input()).upper()
        if res=='Y':
            break
    option=int(input('SELECT THE SONG YOU WANNA DOWNLOAD'))
    option=option-1
    url1=clist[option].find('a',{'class':'fileName'})['href']
    name=str(clist[option].text)

    namewithextension=name.split('.',1)[0]
    print(f'{namewithextension}...... downloading started')
    url=str(url1)
    id=url.split('/')[-2]
    downloading_url=f'https://djking.co.in/files/download/{id}.html'
    r=requests.get(downloading_url,stream=True)
    filelength=int(r.headers['Content-Length'])
    with open(f'{namewithextension}.mp3', 'wb') as f:
        pbar=tqdm(total=(filelength/1024))
        for chunk in tqdm(r.iter_content(chunk_size=1024)):
            if chunk:
                pbar.update()
                f.write(chunk)
    f.close()                
    print('.......................donwnloading finished.......................')
    print('.......................download more songs[Y/N]?.....................')
    res=str(input().upper())
    if res=='N':
        break    