import numpy as np
import math
import os 
import time

def readimu(*args):
    
    class IMU:
        def __init__(self, name, externalFcn=None, BitsPerEpoch=None, 
                     TimeType=None,DataType=None, HeaderSize=None, 
                     ScaleGyro=None, ScaleAcc=None, format=None, no_of_datavalues=None):
            self.name = name
            self.externalFcn = externalFcn
            self.BitsPerEpoch = BitsPerEpoch
            self.TimeType = TimeType
            self.DataType = DataType
            self.HeaderSize = HeaderSize
            self.ScaleGyro = ScaleGyro
            self.ScaleAcc = ScaleAcc
            self.format = format
            self.no_of_datavalues = no_of_datavalues
        
    imu = []
    # IMAR FSAS
    imu.append(IMU('IMAR', None, None, 'double', 'long', 0, 0.10000000*math.pi/180/3600, 0.00152588/1000))

    # LN200
    imu.append(IMU('LN200', None, None, 'double', 'long', 0, 1/2097152.0, 1/16384.0))

    # LN200IG
    imu.append(IMU('LN200IG', None, None, 'double', 'long', 0, 1/524288.0, 1/16384.0))

    # IXSEA
    imu.append(IMU('IXSEA', None, None, 'double', 'double', 0, math.pi/180/3600, 1/1000))

    # NAVCHIP_FLOAT
    imu.append(IMU('NAVCHIP_FLT', None, None, 'double', 'double', 0, 1/3600/360*2*math.pi, 1/1000))

    # NAVCHIP_INT
    imu.append(IMU('NAVCHIP_INT', None, None, 'double', 'long', 0, 0.00000625, 39.0625e-6))

    # GENERIC_LONG
    imu.append(IMU('GENERIC_LONG', None, None, 'double', 'long', 0, 1, 1))

    # GENERIC_DOUBLE
    imu.append(IMU('GENERIC_DOUBLE', None, None, 'double', 'double', 0, 1, 1))

    # TEXT FILE
    imu.append(IMU('TXT', None, None, None, None, None, None, None, '%f,%f,%f,%f,%f,%f,%f', 7))

    # MAT FILE
    imu.append(IMU('MAT', None, None, None, None, None, None, None, None, None))

    # check for integer imu rate of the following kind: 100Hz, 200Hz, 250Hz, 333HZ, 400Hz, 500Hz, 1000Hz OR the current one
    acceptable_frequencies = [100, 200, 250, 333, 400, 500, 1000] # [Hz]
    
    # list of IMUs (list of dictionaries)
    nImu = len(imu)
    imuList = []
    for i in imu:
        imuList.append(i.name)
        
    imuListstr = imuList

    # dictionary for size of type use
    SizeOf = {
        'double': 8,
        'long': 4
    }

    
     ## IMU FILE
    if len(args) == 0:
        import tkinter as tk
        from tkinter import filedialog as fd
        root = tk.Tk()
        root.withdraw()
        imufile = fd.askopenfilename(title='Please select data file')
        
    else:
        imufile = args[0]
        
    if not os.path.isfile(imufile):
        raise ValueError(f"File {imufile} does not exist.")
    
    ## TYPE OF IMU
    k = 0
    if len(args) > 1:
        for i in range(nImu):
            if imu[i].name.lower() == args[1].lower():
                k = i
                break
        if k == 0:
            raise ValueError(f"The IMU '{args[1]}' could not be found in the list of IMUs ({imuListstr})")
    else:
        print(f"Select an IMU from the following list (indexed starting from 0): {imuListstr}")
        k = int(input())
        
        
     ## READ DATA FILE
    
    if imu[k].name == 'MAT':
        # load data file
        import scipy.io as sio
        mat = sio.loadmat(imufile)
        data = mat['data']
        if data is None:
            raise ValueError(f"There is no 'data' field in the mat-file open {imufile}")
        
        fIMU = 1/np.mean(np.diff(data[:,0]))
        
        print(f"(data @ {fIMU:.2f} Hz, format {imu[k].name}) ... done.")
        
    elif imu[k].name == 'TXT':
        # Open data file
        try:
            fid = open(imufile,'r')
        except:
            raise ValueError(f"Cannot open {imufile}")
            
        # init time counter
        start_time = time.time()
        
        # read the data
        data = np.loadtxt(fid, delimiter=imu[k].delimiter)
        data = data[:,:7]
        
        # Calculate sampling frequency
        fIMU = 1/np.mean(np.diff(data[:,0]))
        
        print(f"(data @ {fIMU:.2f} Hz, format {imu[k].name}) ... done.")
        
        # Close opened file
        fid.close()
        
    else:
        # Open data file
        try:
            fid = open(imufile,'rb')
        except:
            raise ValueError(f"Cannot open {imufile}")
        
        # init time counter
        start_time = time.time()
        
        # BitsPerEpoch
        BitsPerEpoch = SizeOf.get(imu[k].TimeType) + 6*SizeOf.get(imu[k].DataType)

        # Set cursor at end of file
        fid.seek(0, os.SEEK_END)

        # Count epochs and control it
        nEpochs = (fid.tell() - imu[k].HeaderSize) // BitsPerEpoch

        if nEpochs != int(nEpochs):
            raise ValueError(f"The file {imufile} does not have an expected size. Control the type of IMU or if the file is corrupted.")

        # display info to command window
        print(imufile)
        print(f" contains {nEpochs} epochs")
        print('Reading ...')
        
        # Init. data matrix
        data = np.zeros((7, nEpochs))
        
        # Set cursor at begining of data (skip header if it exists)
        fid.seek(imu[k].HeaderSize, 0)
       

        # Read time (1*) acc + gyro (6*)
        data[0:7,:] = np.fromfile(fid, dtype=np.dtype(imu[k].DataType), count=7*nEpochs).reshape((7,nEpochs), order='F')
        
        # Data Rate
        fIMU = int(round(1./np.mean(np.diff(data[0,:]))))

        # if the calculated frequency is not part of the accepted frequencies
        if fIMU not in acceptable_frequencies:
            acceptable_frequencies.append(fIMU)
            freqList = str(acceptable_frequencies)
            print(f"The current frequency of {fIMU:.2f} Hz does not correspond to the usual frequencies used in the Lab.")
            print(f"Select a FREQ from the following list: ({freqList})")
            z = int(input())
            fIMU = z
   
            
        
        #fIMU = round(fIMU) 
        print(' (data @ %.2f Hz, sGr %f sAc %d) ...' % (fIMU,imu[k].ScaleGyro, imu[k].ScaleAcc))

        # Scale data for accelerometer and gyroscope
        data[1:4,:] = data[1:4,:] * imu[k].ScaleGyro  
        data[4:7,:] = data[4:7,:] * imu[k].ScaleAcc

        # Scale data for frequency of the IMU, only if it is not the generic one
        if k < 7:
            data[1:4,:] = data[1:4,:] * fIMU  
            data[4:7,:] = data[4:7,:] * fIMU

        # Transpose to fit in vectors
        data = data.T

        # Close opened file
        fid.close()

        print(' done in %.1f sec.' % (time.time() - start_time))
        return data

