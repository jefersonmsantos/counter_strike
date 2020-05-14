import pandas as pd
import argparse
import pickle


#ap=argparse.ArgumentParser()
#ap.add_argument('-f','--file',required=True,help='future match file')
#args=ap.parse_args()
#print(args)


#test_X=pd.read_csv(args.file)

def adjust_data(csvFile):
    
    test_X=pd.read_csv(csvFile)

    opposing_team = []
    i = 0
    while i<=(test_X.shape[0]-1):
        if test_X.iloc[i]['Player Team'] == test_X.iloc[i]['Team1']:
            opposing_team.append(test_X.iloc[i]['Team2'])
        else:
            opposing_team.append(test_X.iloc[i]['Team2'])
        i+=1
        
    test_X['Opposing Team']=opposing_team


    columnsModel = ['Player','Player Team','Overall Kills','Overall Deaths','Overal Kill / Death','Overall Kill / Round','Overall Rounds with Kills',
                'Overall Kill - Death Diff','Opening Total Kills','Opening Total Deaths','Opening Kill Ratio', 'Opening Kill rating',
                'Opening Team win percent after 1st kill','Opening 1st kill in won rounds','Opposing Team']

    test_columns_X = test_X[columnsModel]

    first_kill = []
    win_percent=[]

    i = 0
    while i<=(test_columns_X.shape[0]-1):
        first_kill.append(float(test_columns_X.iloc[i]['Opening 1st kill in won rounds'][0:-1])/100)
        win_percent.append(float(test_columns_X.iloc[i]['Opening Team win percent after 1st kill'][0:-1])/100)
        
        i+=1
        
    test_columns_X['Opening 1st kill in won rounds float']=first_kill
    test_columns_X['Opening Team win percent after 1st kill float']=win_percent

    test_columns_X.drop(['Opening 1st kill in won rounds','Opening Team win percent after 1st kill'],axis=1,inplace=True)

    filename='model2_encoder.sav'
    target_enc = pickle.load(open(filename,'rb'))
    cat_features_encoding=['Player','Player Team','Opposing Team']

    test_encoded_X = test_columns_X.join(target_enc.transform(test_columns_X[cat_features_encoding]).add_suffix('_target'))

    test_encoded_X.drop(['Player','Player Team','Opposing Team'],axis=1,inplace=True)

    selected_columns=['Overall Kills', 'Overall Deaths', 'Overal Kill / Death',
        'Overall Kill / Round', 'Overall Rounds with Kills',
        'Overall Kill - Death Diff', 'Opening Total Kills',
        'Opening Total Deaths', 'Opening Kill Ratio', 'Opening Kill rating',
        'Opening 1st kill in won rounds float',
        'Opening Team win percent after 1st kill float', 'Player_target',
        'Player Team_target', 'Opposing Team_target']

    test_encoded_X=test_encoded_X[selected_columns]

    filenameModel='finalized_model.sav'
    model=pickle.load(open(filenameModel,'rb'))

    final_preds = model.predict(test_encoded_X)

    test_X['Predictions']=final_preds
    return test_X
