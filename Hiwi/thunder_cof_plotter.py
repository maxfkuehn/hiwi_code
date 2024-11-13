
import numpy as np
import glob
import os
from IPython import embed
import pandas as pd
import math
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate

#### thunderloader
#laods .csv 
#
#
# 
def thunderloader(path_way):
    # load all *waveeod files
    laoded_names_waveeod = []
    os.chdir(path_way)
    # go thourgh all waveeodf.csv files and get the file names and sort them 
    for file in glob.glob('*waveeodfs.csv'):
        laoded_names_waveeod.append(file)

    file_names_waveeod = sorted(laoded_names_waveeod)
    
    # loop over every waveeodf.csv and load data of the right fish

    combined_waveforms_mean_all_fish = []
    combined_waveforms_times_all_fish = []

    combined_waveforms_mean_single_fish = []
    combined_waveforms_time_single_fish = []

    normalised_waveform_mean_af = []
    normalised_waveform_mean_sf = []

    p_p_amp_sf = []
    p_p_amp_af = []

    counter = 0
    previous_name = 'first'

    amount_fish_present_list = []
    fish_present = []
    
    
    #list of which window of then second recording it belons to
    t_window_list = []
    t_window = []
    af_frequency_list = []
    

    for name in file_names_waveeod:
        previous_name.split('_')
        counter += 1
        
        if  previous_name == 'first':

            index_raw = name.split('_')
            fish_eodf = int(index_raw[4].split('-')[0])
            #laod fish index
            waveeod_data = pd.read_csv(path_way+'/'+name)

            # look in the files where the EODf of the fish is clsoest to the one in the title, get the index and load EODf waveforms of the fish
            waveod_index = np.where(waveeod_data['EODf'] == min(waveeod_data['EODf'], key=lambda x:abs(x-fish_eodf)))[0][0]
            csv_index = str(waveeod_data['index'][waveod_index])
    
            #cheking how many fish are present in the recording
            amount_fish_present = len(waveeod_data['index'])
           
            

            if csv_index.isnumeric() == False:
                continue
            
            if  name.split('_')[3] == '1':
                if name.split('-')[1] == 't0s':
                    tw = 10
                elif name.split('-')[1] == 't2s':
                    tw = 12                
                elif name.split('-')[1] == 't4s':
                    tw = 14
                elif name.split('-')[1] == 't6s':
                    tw = 16
                else:
                    tw = 18
            elif  name.split('_')[3] == '2':
                if name.split('-')[1] == 't0s':
                    tw = 20
                elif name.split('-')[1] == 't2s':
                    tw = 22                
                elif name.split('-')[1] == 't4s':
                    tw = 24
                elif name.split('-')[1] == 't6s':
                    tw = 26
                else:
                    tw = 28                   
            else:
                if name.split('-')[1] == 't0s':
                    tw = 30
                elif name.split('-')[1] == 't2s':
                    tw = 32                
                elif name.split('-')[1] == 't4s':
                    tw = 34
                elif name.split('-')[1] == 't6s':
                    tw = 36
                else:
                    tw = 38
                  
         
           
        
            # open waveform data
            path_wafeform_csv = path_way+ '/' + name.split('-')[0]+'-'+name.split('-')[1]+'-eodwaveform-'+ csv_index+'.csv'

            eod_waveform_loaded = pd.read_csv(path_wafeform_csv)


             # read data with wavefish specific attributes of selected fish


            wavefish_csv_path = path_way+ '/' + name.split('-')[0]+'-'+name.split('-')[1]+'-wavefish.csv'
            wavefish_attributes = pd.read_csv(wavefish_csv_path)

            p_p_amp = wavefish_attributes['p-p-amplitude'][int(csv_index)]
            rel_peak_amp_sf = wavefish_attributes['relpeakampl'][int(csv_index)]
            ptp_dist = wavefish_attributes['p-p-distance'][int(csv_index)]
            minptp_dist = wavefish_attributes['min-p-p-distance'][int(csv_index)]
            trough_width = wavefish_attributes['troughwidth'][int(csv_index)]  
            thd_sf = wavefish_attributes['thd'][int(csv_index)]
 

            # laod wave time and amplitudeint
            time_wf =   np.array(eod_waveform_loaded['time'])
            mean_wf = np.array(eod_waveform_loaded['mean'])

            p_p_amp_sf.append(p_p_amp)

            combined_waveforms_mean_single_fish.append(mean_wf)
            combined_waveforms_time_single_fish.append(time_wf)
            normalised_waveform_mean_sf.append((np.array(mean_wf)-min(mean_wf))/np.max(mean_wf-min(mean_wf)))
            fish_present.append(amount_fish_present)
            
            t_window.append(tw)
            
            previous_name = name
            if counter == len(file_names_waveeod):
                combined_waveforms_mean_all_fish.append(combined_waveforms_mean_single_fish)
                combined_waveforms_times_all_fish.append(combined_waveforms_time_single_fish)
                af_frequency_list.append(fish_eodf)
                amount_fish_present_list.append(fish_present)
                t_window_list.append(t_window)
                normalised_waveform_mean_af.append(normalised_waveform_mean_sf)
        else:
            pn = previous_name.split('_')
            nn = name.split('_')

            if pn[1] == nn[1] and pn[2] == nn[2]:
                        
                index_raw = name.split('_')
                fish_eodf = int(index_raw[4].split('-')[0])

                waveeod_data = pd.read_csv(path_way+'/'+name)
                # look in the files where the EODf of the fish is clsoest to the one in the title, get the index and load EODf waveforms of the fish
                waveod_index = np.where(waveeod_data['EODf'] == min(waveeod_data['EODf'], key=lambda x:abs(x-fish_eodf)))[0][0]
                csv_index = str(waveeod_data['index'][waveod_index])

                if csv_index.isnumeric() == False:
                    continue
                


                path_wafeform_csv = path_way+ '/' + name.split('-')[0]+'-'+name.split('-')[1]+'-eodwaveform-'+ csv_index+'.csv'
              
                eod_waveform_loaded = pd.read_csv(path_wafeform_csv)



                #cheking how many fish are present in the recording
                amount_fish_present = len(waveeod_data['index'])
                #check which time window
                if  name.split('_')[3] == '1':
                    if name.split('-')[1] == 't0s':
                        tw = 10
                    elif name.split('-')[1] == 't2s':
                        tw = 12                
                    elif name.split('-')[1] == 't4s':
                        tw = 14
                    elif name.split('-')[1] == 't6s':
                        tw = 16
                    else:
                        tw = 18
                elif  name.split('_')[3] == '2':
                    if name.split('-')[1] == 't0s':
                        tw = 20
                    elif name.split('-')[1] == 't2s':
                        tw = 22                
                    elif name.split('-')[1] == 't4s':
                        tw = 24
                    elif name.split('-')[1] == 't6s':
                        tw = 26
                    else:
                        tw = 28                   
                else:
                    if name.split('-')[1] == 't0s':
                        tw = 30
                    elif name.split('-')[1] == 't2s':
                        tw = 32                
                    elif name.split('-')[1] == 't4s':
                        tw = 34
                    elif name.split('-')[1] == 't6s':
                        tw = 36
                    else:
                        tw = 38


                time_wf =   np.array(eod_waveform_loaded['time'])
                mean_wf = np.array(eod_waveform_loaded['mean'])

   

                #get waveform time mean and standardised mean
            
      
                combined_waveforms_mean_single_fish.append(mean_wf)
                combined_waveforms_time_single_fish.append(time_wf)
                normalised_waveform_mean_sf.append((np.array(mean_wf)-min(mean_wf))/np.max(mean_wf-min(mean_wf)))
                fish_present.append(amount_fish_present)
                
                t_window.append(tw)


                previous_name = name
                if counter == len(file_names_waveeod):
                    combined_waveforms_mean_all_fish.append(combined_waveforms_mean_single_fish)
                    combined_waveforms_times_all_fish.append(combined_waveforms_time_single_fish)
                    af_frequency_list.append(fish_eodf)
                    amount_fish_present_list.append(fish_present)
                    t_window_list.append(t_window)
                    normalised_waveform_mean_af.append(normalised_waveform_mean_sf)
                    p_p_amp_af.append(p_p_amp)
            
            else:
               
                combined_waveforms_mean_all_fish.append(combined_waveforms_mean_single_fish)
                combined_waveforms_times_all_fish.append(combined_waveforms_time_single_fish)
                af_frequency_list.append(fish_eodf)
                amount_fish_present_list.append(fish_present)
                t_window_list.append(t_window)
                normalised_waveform_mean_af.append(normalised_waveform_mean_sf)

                combined_waveforms_mean_single_fish = []
                combined_waveforms_time_single_fish = []
                fish_present= []
                t_window = []
                normalised_waveform_mean_sf = []

                p_p_amp_af.append(p_p_amp_sf)

                index_raw = name.split('_')
                fish_eodf = int(index_raw[4].split('-')[0])

                waveeod_data = pd.read_csv(path_way+'/'+name)
                # look in the files where the EODf of the fish is clsoest to the one in the title, get the index and load EODf waveforms of the fish
                waveod_index = np.where(waveeod_data['EODf'] == min(waveeod_data['EODf'], key=lambda x:abs(x-fish_eodf)))[0][0]
                csv_index = str(waveeod_data['index'][waveod_index])

                if csv_index.isnumeric() == False:
                    continue

                path_wafeform_csv = path_way+ '/' + name.split('-')[0]+'-'+name.split('-')[1]+'-eodwaveform-'+ csv_index+'.csv'
                                          
                eod_waveform_loaded = pd.read_csv(path_wafeform_csv)

                # read data with wavefish specific attributes of selected fish


                wavefish_csv_path = path_way+ '/' + name.split('-')[0]+'-'+name.split('-')[1]+'-wavefish.csv'
                wavefish_attributes = pd.read_csv(wavefish_csv_path)
            
     
                p_p_amp = wavefish_attributes['p-p-amplitude'][int(csv_index)]
                rel_peak_amp_sf = wavefish_attributes['relpeakampl'][int(csv_index)]
                ptp_dist = wavefish_attributes['p-p-distance'][int(csv_index)]
                minptp_dist = wavefish_attributes['min-p-p-distance'][int(csv_index)]
                trough_width = wavefish_attributes['troughwidth'][int(csv_index)]  
                thd_sf = wavefish_attributes['thd'][int(csv_index)]

                p_p_amp_sf.append(p_p_amp)

                #cheking how many fish are present in the recording
                amount_fish_present = len(waveeod_data['index'])
                #check which time window
                if  name.split('_')[3] == '1':
                    if name.split('-')[1] == 't0s':
                        tw = 10
                    elif name.split('-')[1] == 't2s':
                        tw = 12                
                    elif name.split('-')[1] == 't4s':
                        tw = 14
                    elif name.split('-')[1] == 't6s':
                        tw = 16
                    else:
                        tw = 18
                elif  name.split('_')[3] == '2':
                    if name.split('-')[1] == 't0s':
                        tw = 20
                    elif name.split('-')[1] == 't2s':
                        tw = 22                
                    elif name.split('-')[1] == 't4s':
                        tw = 24
                    elif name.split('-')[1] == 't6s':
                        tw = 26
                    else:
                        tw = 28                   
                else:
                    if name.split('-')[1] == 't0s':
                        tw = 30
                    elif name.split('-')[1] == 't2s':
                        tw = 32                
                    elif name.split('-')[1] == 't4s':
                        tw = 34
                    elif name.split('-')[1] == 't6s':
                        tw = 36
                    else:
                        tw = 38
                        
                time_wf =   np.array(eod_waveform_loaded['time'])
                mean_wf = np.array(eod_waveform_loaded['mean'])

      
                combined_waveforms_mean_single_fish.append(mean_wf)
                combined_waveforms_time_single_fish.append(time_wf)
                normalised_waveform_mean_sf.append((np.array(mean_wf)-min(mean_wf))/np.max(mean_wf-min(mean_wf)))
                fish_present.append(amount_fish_present)

               
                t_window.append(tw)
                    

                previous_name = name
                if counter == len(file_names_waveeod):
                    combined_waveforms_mean_all_fish.append(combined_waveforms_mean_single_fish)
                    combined_waveforms_times_all_fish.append(combined_waveforms_time_single_fish)
                    af_frequency_list.append(fish_eodf)
                    amount_fish_present_list.append(fish_present)
                    t_window_list.append(t_window)
                    normalised_waveform_mean_af.append(normalised_waveform_mean_sf)
                    p_p_amp_af.append(p_p_amp_sf)
    
    int_waveforms_af = []
    unique_cor_af = []


    for af in range(len(combined_waveforms_mean_all_fish)):
        int_waveforms_sf = []

        sf_nor_waveform = normalised_waveform_mean_af[af]
        sf_time = combined_waveforms_times_all_fish[af]
        
        min_sf_time = []
        max_sf_time = []

        if sf_time == [] or len(sf_time) < 2:
            continue

        for sft in sf_time:
            min_sf_time.append(min(sft))
            max_sf_time.append(max(sft))

        start_time = max(min_sf_time)
        end_time = min(max_sf_time)

        int_time = np.arange(start_time, end_time, 0.03)

        for sf in range(len(sf_nor_waveform)):
            if af ==280:
                continue
            
            intpol = interpolate.interp1d(sf_time[sf],sf_nor_waveform[sf], kind='cubic' )
            
            ynew = intpol(int_time)
            int_waveforms_sf.append(ynew)

        int_waveforms_af.append(int_waveforms_sf)

        """
        Create Correlation Matrix
        """
        
        cor_matrix = np.corrcoef(int_waveforms_sf)
        if af == 280:
            continue
        else:    
            try:
                triu_mat = np.triu(cor_matrix,1)
            except TypeError:
                embed()
            print(af)
            triu_array = triu_mat.ravel()
            unique_cor = triu_array[np.where(triu_array>0)[0]]
            unique_cor_af.append(unique_cor)

            min_cor = np.min(unique_cor)
            max_cor =  np.max(unique_cor)
            average_cor = np.mean(unique_cor)
            std_cor = np.std(unique_cor)
        
        
    
            


  
     
        

##### Main function

if __name__ == "__main__":
    ### setting

    path_wavforms = '/home/kuehn/data/waveforms/thunderfish'
    time_window_thunderfish = ['t0','t2','t4','t6','t8']
    thunderloader(path_wavforms)

