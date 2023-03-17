from transformers import pipeline
import pandas as pd
import os, sys
sentiment_pipeline = pipeline("sentiment-analysis")



def analyze_comments(all_comments):
    try:
        pve = {}
        pvelist = []
        nve = {}
        nvelist = []
        neu = {}
        neulist = []

        sentiment_results = sentiment_pipeline(all_comments, truncation=True)
        for result in sentiment_results:
            
            if result.get('label') == 'POSITIVE':
                pve["sentiment"] = result.get('label')
                pve["score"] = result.get('score')
                pvelist.append(result)
                
            
            if result.get('label') == 'NEGATIVE':
                nve["sentiment"] = result.get('label')
                nve["score"] = result.get('score')
                nvelist.append(result)
                

            if result.get('label') == 'NEUTRAL':
                neu["sentiment"] = result.get('label')
                neu["score"] = result.get('score')
                neulist.append(result)
                
            
        positive = 100*len(pvelist)/len(sentiment_results)
        positive_percentage = str(positive)+ '%'

        negative = 100*len(nvelist)/len(sentiment_results)
        negative_percentage = str(negative)+ '%'

        neutral = 100*len(neulist)/len(sentiment_results)
        neutral_percentage = str(neutral)+ '%'


        return (sentiment_results, positive_percentage, negative_percentage, neutral_percentage)
    
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)

