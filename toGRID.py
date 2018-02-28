from pylab import *
from netCDF4 import Dataset
import pygrib
import sys
from ncepgrib2 import *
from pathlib import Path
from datetime import datetime

def convertToGrid(rootFile='wrfout_d02_2018-02-12_13-00-00.amf'):
    print('Converting file:%r' %rootFile)
    rootgrp = Dataset(rootFile)
    resultfile = Path(rootFile).stem +".grb2"
    Re = 6371229.0 
    No = shape(rootgrp['AM_U'])[2]
    Ne = shape(rootgrp['AM_U'])[3]
    CLat = rootgrp.AM_CEN_LAT
    Dx = rootgrp.AM_DX
    Dy = rootgrp.AM_DY
    Dxc = rootgrp.AM_DX/Re*10**6
    Dyc = rootgrp.AM_DY/Re*10**6

    rangeU = array(rootgrp['AM_U_RANGE']).reshape(1,-1,2,1,1)
    rangeV = array(rootgrp['AM_V_RANGE']).reshape(1,-1,2,1,1)
    rangeW = array(rootgrp['AM_W_RANGE']).reshape(1,-1,2,1,1)

    rangeH = array(rootgrp['AM_H_RANGE']).reshape(1,-1,2,1,1)
    rangeTKE = array(rootgrp['AM_TKE_RANGE']).reshape(1,-1,2,1,1)
    rangeP = array(rootgrp['AM_P_RANGE']).reshape(1,-1,2,1,1)
    rangeT = array(rootgrp['AM_T_RANGE']).reshape(1,-1,2,1,1)
    
    CLon = rootgrp.AM_CEN_LON
    firstLat = (CLat+(Dx/Re)*No/2)*10**6
    lastLat = (CLat-(Dx/Re)*No/2)*10**6

    lastLon = (CLon+(Dy/Re)*Ne/2)*10**6
    firstLon = (CLon-(Dy/Re)*Ne/2)*10**6

    eta = rootgrp['AM_ETA']
    f = open(resultfile,'wb')
    year_creppy=rootgrp.AM_SIMULATION_TIME_TEXT.split()
    fecha=array(year_creppy[0].split('-'))
    hora=array(year_creppy[1].split('-'))
    lul=datetime(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(hora[0]), int(hora[1]),int(hora[2]))
    secondDay=lul.timestamp()
    forecast_time = (rootgrp.AM_FORECAST_TIME-secondDay)
    
    grbo = Grib2Encode(0,int32([7,0,19,0,1,fecha[0],fecha[1],fecha[2],hora[0],hora[1],hora[2],0,1]))
    lul_grid_definition_info = [0,No*Ne,0,0,0]
    print(Ne)
    print(No)

    lul_grid_definition_template = ([int8(6),int8(0),int32(0),int8(0),int32(0),int8(0),int32(0),int32(No),int32(Ne),int32(0),int32(0),int32(firstLat),int32(mod(firstLon,360000000)),int8(48), int32(lastLat),int32(mod(lastLon,360000000)),int32(Dxc),int32(Dyc),int8(0)])
    grbo.addgrid(lul_grid_definition_info,lul_grid_definition_template)
    Ufi = rootgrp['AM_U']
    Vfi = rootgrp['AM_V']
    Wfi = rootgrp['AM_W']

    Tfi = rootgrp['AM_T']
    Pfi = rootgrp['AM_P']
    TKEfi = rootgrp['AM_TKE']
    Hfi = rootgrp['AM_H']
    
    data=rangeU[:,:,0,:,:]+(array(Ufi))/255*(rangeU[:,:,1,:,:]-rangeU[:,:,0,:,:])
    data2=rangeV[:,:,0,:,:]+(array(Vfi))/255*(rangeV[:,:,1,:,:]-rangeV[:,:,0,:,:])
    data3=rangeW[:,:,0,:,:]+(array(Wfi))/255*(rangeW[:,:,1,:,:]-rangeW[:,:,0,:,:])

    dataP = rangeP[:,:,0,:,:]+(array(Pfi))/255*(rangeP[:,:,1,:,:]-rangeP[:,:,0,:,:])
    dataT = rangeT[:,:,0,:,:]+(array(Tfi))/255*(rangeT[:,:,1,:,:]-rangeT[:,:,0,:,:])
    dataH = rangeH[:,:,0,:,:]+(array(Hfi))/255/257*(rangeH[:,:,1,:,:]-rangeH[:,:,0,:,:])
    dataTKE = rangeTKE[:,:,0,:,:]+(array(TKEfi))/255*(rangeTKE[:,:,1,:,:]-rangeTKE[:,:,0,:,:])



    forecast_time=forecast_time/60
    for i in arange(len(eta)):
        LVL = float64(eta[i])
        new_product_definition_template_number = int8(0)
        new_product_definition_template_u = [int32(2),int8(2),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_v = [int32(2),int8(3),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_w = [int32(2),int8(9),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_P = [int32(3),int8(0),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_T = [int32(0),int8(0),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_TKE = [int32(19),int8(11),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]
        new_product_definition_template_H = [int32(3),int8(6),int8(2),int8(2),int8(2),0,0,0,float32(forecast_time),int8(111),int8(3),int32(LVL*1000),int8(111),int8(3),LVL*1000]

        
        new_data_representation_template_number = int8(0)
        new_data_representation_template = [float32(10000),0,3,         11,          0,
                                          1,          0,          0,          0,        213,
                                          0,          4,          1,          1,         64,
                                          6,          1,          2]

        # add product definition template, data representation template
        # and data (including bitmap which is read from data mask).
        # In this case, U, V, W velocities
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_u,new_data_representation_template_number,new_data_representation_template,array(data[0,i,:,:]))
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_v,new_data_representation_template_number,new_data_representation_template,array(data2[0,i,:,:]))
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_w,new_data_representation_template_number,new_data_representation_template,array(data3[0,i,:,:]))

        grbo.addfield(new_product_definition_template_number,new_product_definition_template_P,new_data_representation_template_number,new_data_representation_template,array(dataP[0,i,:,:]))
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_TKE,new_data_representation_template_number,new_data_representation_template,array(dataTKE[0,i,:,:]))
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_H,new_data_representation_template_number,new_data_representation_template,array(dataH[0,i,:,:]))
        grbo.addfield(new_product_definition_template_number,new_product_definition_template_T,new_data_representation_template_number,new_data_representation_template,array(dataT[0,i,:,:]))

        
        # finalize the grib message.
    grbo.end()
    # write it to the file.
    f.write(grbo.msg)

    Ny=len(eta)
    #Range
    #    grbo = Grib2Encode(0,int32([7,0,2,1,1,1997,1,0,0,0,0,0,1]))


    # lul_grid_definition_info = [0,Ny*2,0,0,0]
    # lul_grid_definition_template = [int8(6),int8(0),int32(0),int8(0),int32(0),int8(0),int32(0),int32(Ny),int32(2),int32(0),int32(0),int32(firstLat),int32(firstLon), int8(56), int32(lastLat),int32(lastLon),int32(Dxc),int32(Dyc),int8(0)]
    # grbo.addgrid(lul_grid_definition_info,lul_grid_definition_template)


    # data = rootgrp['AM_U_RANGE']
    # data2 = rootgrp['AM_V_RANGE']
    # data3 = rootgrp['AM_W_RANGE']
        
    
    # new_product_definition_template_number = int8(0)
    # new_product_definition_template_u = [int32(2),int8(2),int8(2),int8(2),int8(2),0,0,13,float32(forecast_time),int8(111),int8(3),0,int8(111),int8(3),0]
    # new_product_definition_template_v = [int32(2),int8(3),int8(2),int8(2),int8(2),0,0,13,float32(forecast_time),int8(111),int8(3),int32(0),int8(111),int8(3),0]
    # new_product_definition_template_w = [int32(2),int8(9),int8(2),int8(2),int8(2),0,0,13,float32(forecast_time),int8(111),int8(3),0,int8(111),int8(3),0]

        
    # new_data_representation_template_number = int8(0)
    # new_data_representation_template = [float32(10000),0,3,         11,          0,
    #                                     1,          0,          0,          0,        213,
    #                                     0,          4,          1,          1,         64,
    #                                     6,          1,          2]
    
    # # add product definition template, data representation template
    # # and data (including bitmap which is read from data mask).
    # # In this case, U, V, W velocities
    # grbo.addfield(new_product_definition_template_number,new_product_definition_template_u,new_data_representation_template_number,new_data_representation_template,array(data[:]))
    # grbo.addfield(new_product_definition_template_number,new_product_definition_template_v,new_data_representation_template_number,new_data_representation_template,array(data2[:]))
    # grbo.addfield(new_product_definition_template_number,new_product_definition_template_w,new_data_representation_template_number,new_data_representation_template,array(data3[:]))

    #     # finalize the grib message.
    # grbo.end()
    # # write it to the file.
    # f.write(grbo.msg)

    
    # close the output file
    f.close()
    rootgrp.close()




if __name__ == "__main__":    

    if(len(sys.argv)>1):
        for filename in sys.argv[1:]:
            convertToGrid(filename)
    else:
        print("The function takes as argument the name of the files you want to convert")
