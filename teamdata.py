import pandas as pd
import numpy as np


class teamdata:
    def __init__(self,teamNameSearch):
        self.teamNameSearch = teamNameSearch

    def load_data(self):
        self.data = pd.read_csv('iplteam_info.csv',index_col=False)
        self.searchteam_df = self.data[self.data['Team'] == self.teamNameSearch]
        self.searchteam_df['Total Wicket Taken'] = self.searchteam_df['Total Wicket Taken'].astype('int64')
        self.searchteam_df['total_runs'] = self.searchteam_df['total_runs'].astype('int64')
        self.top5_Batsman=self.searchteam_df.sort_values(by=['total_runs'],ascending=False)[:5]
        self.top5_Bowler=self.searchteam_df.sort_values(by=['Total Wicket Taken'],ascending=False)[:5]
        return self.top5_Batsman,self.top5_Bowler
