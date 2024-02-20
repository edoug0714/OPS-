import pandas as pd
import numpy as np

#BASIC OPS GUIDELINE:
#calculate slug = (single + double(2) + triple(3) + home run(4)) / at bats
#calculate obp = (hit by pitch + walk + single + double + triple + home run) / plate appearances
#calculate ballpark factor
#calculate players ops using ballpark factor on each event   

class Team:
    def __init__(self):
        self.ops = 0
        self.park_factor = 0

    def calcOps(self):



teams = [ARI, ATL, BAL, BOS, CHC, CWS, CIN, CLE, COL, DET, FLA, HOU, KAN, LAA, LAD, MIL, MIN, NYM, NYY, OAK, PHI, PIT, 
        SD, SF, SEA, STL, TB, TEX, TOR, WAS]
data = pd.read_csv('Statcast_2021.csv')

def calc_ballpack_obp():
    


def main():
    
