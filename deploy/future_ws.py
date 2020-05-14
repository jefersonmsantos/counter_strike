from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json
import argparse
from adjust_data import adjust_data
import warnings

warnings.filterwarnings('ignore')

ap=argparse.ArgumentParser()
ap.add_argument('-s','--site',required=True,help='url from match to predict')
args=ap.parse_args()


driver=webdriver.Chrome()

date=[]
team1=[]
team2=[]

team1Players=[]
team2Players=[]

tournament=[]

datePlayers=[]
playersPlayers=[]
playerteamPlayers=[]
overallKillsPlayers = []
overallDeathsPlayers = []
overallKill_DeathPlayers = []
overallKill_RoundPlayers = []
overallRoundsWithKillsPlayers = []
overallKillDeathDiffPlayers = []
openingTotalKillsPlayers = []
openingTotalDeathsPlayers = []
openingKillRatioPlayers = []
openingKillRatingPlayers = []
openingTeamWinPercentAfterFirstKillPlayers = []
openingFirstKillInWonRoundsPlayers = []

months = {
    'January':'01',
    'February':'02',
    'March':'03',
    'April':'04',
    'May':'05',
    'June':'06',
    'July':'07',
    'August':'08',
    'September':'09',
    'October':'10',
    'November':'11',
    'December':'12'
}

##columnsModel = ['Player','Player Team','Overall Kills','Overall Deaths','Overal Kill / Death','Overall Kill / Round','Overall Rounds with Kills',
               #'Overall Kill - Death Diff','Opening Total Kills','Opening Total Deaths','Opening Kill Ratio', 'Opening Kill rating',
               #'Opening Team win percent after 1st kill','Opening 1st kill in won rounds','Opposing Team']


url = args.site       
driver.get(url)

content=driver.page_source
soup=BeautifulSoup(content)
matchesLinks=[]

for div in soup.findAll('div',attrs={'class':'upcoming-matches'}):
    for a in div.findAll('a',attrs={'class':'a-reset'}):
        link = a['href']
        matchesLinks.append(link)
m=0

for link in matchesLinks:




    url='https://www.hltv.org'+link
    driver.get(url)

    content=driver.page_source
    soup=BeautifulSoup(content,features='lxml')


    for div in soup.findAll('div', attrs={'class':'match-page'}):
        pageDate=div.find('div',attrs={'class':'date'}) 
        pageTournament=div.find('div',attrs={'class':'event text-ellipsis'})
        date.append(pageDate.text)
        tournament.append(pageTournament.text)


    for div in soup.findAll('div', attrs={'class':'team1-gradient'}):
        pageTeam1=div.find('div',attrs={'class':'teamName'})
        #pageResult1=div.find('div',attrs={'class':['won','lost','tie']})
        team1.append(pageTeam1.text)
        #finalResult1.append(pageResult1.text)

    for div in soup.findAll('div', attrs={'class':'team2-gradient'}):
        pageTeam2=div.find('div',attrs={'class':'teamName'})
        #pageResult2=div.find('div',attrs={'class':['won','lost','tie']})
        team2.append(pageTeam2.text)
        #finalResult2.append(pageResult2.text)
        
    for div in soup.findAll('div', attrs={'class':'lineups-compare-container'}):
        
        data_team = ['data-team1-players-data','data-team2-players-data']
        
        for team in data_team:
            dictionary = json.loads(div[team])
            for key in dictionary.keys():
                link_aux=dictionary[key]['statsLinkUrl']
                link = link_aux.split('?')

                stats_auxiliary = {}

                dateStats = pageDate.text
                dateSplit = dateStats.split(' ')
                year = dateSplit[-1]
                month = months[dateSplit[-2]]
                if len(dateSplit[0])==3:
                    toInt = int(dateSplit[0][0])
                    day_aux = toInt-1
                    day = '0'+str(day_aux)

                else:

                    toInt = int(dateSplit[0][0:2])
                    day_aux = toInt-1
                    day = str(day_aux)

                url='https://www.hltv.org'+link[0][:15]+'/'+link[0][15:]+'?startDate=2013-01-01&endDate='+year+'-'+month+'-'+day
                driver.get(url)

                content=driver.page_source
                soup=BeautifulSoup(content,features='lxml')


                ##for div in soup.find('div', attrs={'class':'stats-section stats-player stats-player-overview'}):
                img=""
                datePlayers.append(pageDate.text)
                for img in soup.findAll(class_='summaryBodyshot'):
                    playersPlayers.append(img['title'])
                if img=="":
                    for img in soup.findAll(class_='summarySquare'):
                        playersPlayers.append(img['title'])

                for img in soup.findAll(class_='team-logo'):
                    playerteamPlayers.append(img['title'])
                    team1Players.append(pageTeam1.text)
                    team2Players.append(pageTeam2.text)
                    break




                url='https://www.hltv.org'+link[0][:15]+'individual/'+link[0][15:]+'?startDate=2013-01-01&endDate='+year+'-'+month+'-'+day
                driver.get(url)

                content=driver.page_source
                soup=BeautifulSoup(content,features='lxml')


                for divpl in soup.findAll('div',attrs={'class','standard-box'}):
                    for divst in divpl.findAll('div',attrs={'class','stats-row'}):
                        stat = []
                        for span in divst.findAll('span'):
                            if (span.text != 'K - D diff.'):
                                stat.append(span.text)

                        stats_auxiliary[stat[0]]=stat[1]
                overallKillsPlayers.append(stats_auxiliary['Kills'])
                overallDeathsPlayers.append(stats_auxiliary['Deaths'])
                overallKill_DeathPlayers.append(stats_auxiliary['Kill / Death'])
                overallKill_RoundPlayers.append(stats_auxiliary['Kill / Round'])
                overallRoundsWithKillsPlayers.append(stats_auxiliary['Rounds with kills'])
                overallKillDeathDiffPlayers.append(stats_auxiliary['Kill - Death difference'])
                openingTotalKillsPlayers.append(stats_auxiliary['Total opening kills'])
                openingTotalDeathsPlayers.append(stats_auxiliary['Total opening deaths'])
                openingKillRatioPlayers.append(stats_auxiliary['Opening kill ratio'])
                openingKillRatingPlayers.append(stats_auxiliary['Opening kill rating'])
                openingTeamWinPercentAfterFirstKillPlayers.append(stats_auxiliary['Team win percent after first kill'])
                openingFirstKillInWonRoundsPlayers.append(stats_auxiliary['First kill in won rounds'])
    m+=1
    if m>=4:
        break


df=pd.DataFrame({'Date':date,'Team1':team1,'Team2':team2,'Tournament':tournament})
df.to_csv('futurecsMatches4.csv',index=False)

df=pd.DataFrame({'Date':datePlayers,'Team1':team1Players,'Team2':team2Players,'Player Team':playerteamPlayers,
                'Player':playersPlayers,
                'Overall Kills':overallKillsPlayers,'Overall Deaths':overallDeathsPlayers,'Overal Kill / Death':overallKill_DeathPlayers,
                'Overall Kill / Round':overallKill_RoundPlayers,'Overall Rounds with Kills':overallRoundsWithKillsPlayers,
                'Overall Kill - Death Diff':overallKillDeathDiffPlayers,'Opening Total Kills':openingTotalKillsPlayers,
                'Opening Total Deaths':openingTotalDeathsPlayers,'Opening Kill Ratio':openingKillRatioPlayers,
                'Opening Kill rating':openingKillRatingPlayers,'Opening Team win percent after 1st kill':openingTeamWinPercentAfterFirstKillPlayers,
                'Opening 1st kill in won rounds':openingFirstKillInWonRoundsPlayers})

df.to_csv('futurecsplayers4.csv',index=False)

predictions = adjust_data('futurecsplayers4.csv')
 
#importar matches
matches=pd.read_csv('futurecsMatches4.csv')
#criar coluna ID
matchcolumn = []

i = 0
while i <= (matches.shape[0]-1):
    date = matches.iloc[i]['Date']
    team1 = matches.iloc[i]['Team1']
    team2 = matches.iloc[i]['Team2']
    
    
    matchcolumn.append(str(date)+str(team1)+str(team2))
    i+=1
    
matches['Match column']=matchcolumn

#criar coluna ID em Predictions
matchcolumn = []

i = 0
while i <= (predictions.shape[0]-1):
    date = predictions.iloc[i]['Date']
    team1 = predictions.iloc[i]['Team1']
    team2 = predictions.iloc[i]['Team2']
    
    
    matchcolumn.append(str(date)+str(team1)+str(team2))
    i+=1
    
predictions['Match column']=matchcolumn



#somar predictions 1 e 2 no matches
team1_prediction=[]
team2_prediction=[]

for i in range(0,len(matches)):
    team1_score=predictions[(predictions['Match column']==matches.iloc[i]['Match column']) & 
                                (predictions['Player Team']==matches.iloc[i]['Team1'])].sum()['Predictions']
    team2_score=predictions[(predictions['Match column']==matches.iloc[i]['Match column']) & 
                                (predictions['Player Team']==matches.iloc[i]['Team2'])].sum()['Predictions']
    
    team1_prediction.append(team1_score)
    team2_prediction.append(team2_score)



matches['Team1 Prediction']=team1_prediction
matches['Team2 Prediction']=team2_prediction
matches['Team1 Prediction']=matches['Team1 Prediction'].astype(int)
matches['Team2 Prediction']=matches['Team2 Prediction'].astype(int)


# fazer diferença
prediction_difference=[]

for i in range(0,len(matches)):
    difference = matches.iloc[i]['Team1 Prediction'] - matches.iloc[i]['Team2 Prediction']
    if difference <0:
        difference = difference*(-1)
    prediction_difference.append(difference)
matches['Prediction difference score']=prediction_difference


#salvar dataframe
matches.to_csv('predictions.csv')


#printar resultados
for i in range(0,len(matches)):
    print(matches.iloc[i]['Team1'] + ': ' + str(matches.iloc[i]['Team1 Prediction']))
    print(matches.iloc[i]['Team2'] + ': ' + str(matches.iloc[i]['Team2 Prediction']))
    print('Difference: '+str(matches.iloc[i]['Prediction difference score']))
    print('\n')
