# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:15:46 2020

@author: mohammed
"""



# FUNCTION START -----------------------------------------------------------------------------------------

def cat_to_num (dataframe,column): #DONE DONE DONE
    import re
    import numpy as np
    import pandas as pd
    vector = list(dataframe[column]) # we will be seperating out the following column from the data frame 
    vector = np.char.upper(vector) # converting the list to upper array
    #this is an  easy way to write for loop in python  
    #please learn
    # please learn
    vector =[ re.sub(r'[^\w\s]','',i)  for i in vector] # removing signs/ speacial Characters
    vector = [re.sub(' ' , '_', i) for i in vector]  # removing white space.
    vector = np.array(vector)
#    Now we will create empty dataframe with row number tagging from 1: nrow of the dataframe
    empty_df = pd.DataFrame(
            {
                    'row_number' : range( 1 , int(dataframe.shape[0]+ 1) )
                    }
            )
    arrange_zone = pd.DataFrame({
        'vector' : vector
        })
    arrange_zone = arrange_zone.groupby('vector')['vector'].count().nlargest(1000)
#    --avoid these lines arrange_zone = dataframe.groupby(column)[column].count().nlargest(1000) 
    arrange_zone = np.array(arrange_zone.index) # through this we are making the array as character array 
    arrange_zone_length = int(len(arrange_zone))
    col_name_below_5 = column + '_' + arrange_zone
    col_name_equal_two = column + '_' + arrange_zone[0]
    arrange_above_5 = arrange_zone
    if(arrange_zone_length > 4) :
        arrange_above_5[4:] = ['other'] *   len(arrange_above_5[4:])
        arrange_above_5  = np.array(arrange_above_5)
        arrange_5_length = len(np.unique(arrange_above_5))
        unique_arrange_5 = np.array(pd.Series(arrange_above_5).drop_duplicates())
        unique_arrange_5 = column + '_' + unique_arrange_5
    if(arrange_zone_length == 4) :
        grouping = np.where(vector == arrange_zone[0],arrange_zone[0],
                            np.where(vector == arrange_zone[1],arrange_zone[1],
                                     np.where(vector == arrange_zone[2],arrange_zone[2],
                                              np.where(vector == arrange_zone[3],arrange_zone[3], 'other'))))      
        for i in range(0,arrange_zone_length) :
            column_record = np.where(grouping == arrange_zone[i],1,0)
            empty_df['col_' + str(i)] = column_record
    elif (arrange_zone_length == 3) :
        grouping = np.where(vector == arrange_zone[0],arrange_zone[0],
                            np.where(vector == arrange_zone[1],arrange_zone[1],
                                     np.where(vector == arrange_zone[2],arrange_zone[2], 'other')))
        for i in range(0,arrange_zone_length) :
            column_record = np.where(grouping == arrange_zone[i],1,0)
            empty_df['col_' + str(i)] = column_record
    elif (arrange_zone_length == 2) :
        grouping = np.where(vector == arrange_zone[0],arrange_zone[0],
                            np.where(vector == arrange_zone[1],arrange_zone[1],'other'))
        for i in [1] :
            column_record = np.where(grouping == arrange_zone[i],1,0)
            empty_df['col_' + str(i)] = column_record
    elif ( arrange_zone_length > 4) : 
        grouping = np.where(vector == arrange_zone[0],arrange_zone[0],
                            np.where(vector == arrange_zone[1],arrange_zone[1],
                                     np.where(vector == arrange_zone[2],arrange_zone[2],
                                              np.where(vector == arrange_zone[3],arrange_zone[3], 'other'))))
        for i in  range(0 , (arrange_5_length)):
            column_record =  np.where(grouping == arrange_above_5[i],1,0)
            empty_df['col_' + str(i)] = column_record
    ## further editing  # function works well till this point
    empty_df = empty_df.drop(empty_df.columns[0], axis = 1)  # dropping the first column.
    if(arrange_zone_length > 4) : 
        empty_df.columns = list(unique_arrange_5)
    elif(arrange_zone_length == 2) :
        empty_df.columns = list(col_name_equal_two)
    else :
        empty_df.columns = list(col_name_below_5)
    dataframe = pd.concat([dataframe.reset_index(drop=True), empty_df], axis=1)
    return(dataframe)