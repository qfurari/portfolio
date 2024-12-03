#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file ObjectData.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
import cv2
import numpy as np

sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
objectdata_spec = ["implementation_id", "ObjectData", 
         "type_name",         "ObjectData", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class ObjectData
# @brief ModuleDescription
# 
# 
# </rtc-template>
class ObjectData(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_voice_amp = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        """
        """
        self._voice_ampIn = OpenRTM_aist.InPort("voice_amp", self._d_voice_amp)
        self._d_image = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._imageOut = OpenRTM_aist.OutPort("image", self._d_image)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("voice_amp",self._voice_ampIn)
		
        # Set OutPort buffers
        self.addOutPort("image",self._imageOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def generate_image(self, amplitude):
        shape_index = (amplitude - 1) // 500
        
        num_sides = min(shape_index + 3, 100)

        blue = min(255, int((amplitude / 50000) * 255)) 
        green = 0
        red = min(255, int(((10000 - amplitude) / 50000) * 255))
        
        color = (blue, green, red)
        
        size = 500
        image = np.full((size, size, 3), 255,dtype=np.uint8)
        
        center = (size // 2, size // 2)
        radius = size // 3
        angle_step = 2 * np.pi / num_sides
        
        points = []
        for i in range(num_sides):
            angle = i * angle_step
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            points.append((x, y))
        
        cv2.fillPoly(image, [np.array(points)], color)
        return image
    
    
    def onExecute(self, ec_id):
         if self._voice_ampIn.isNew():
            data = self._voice_ampIn.read()
            
            amplitude = data.data
            print(f"Received amplitude: {amplitude}")
            
            image = self.generate_image(amplitude)
            
            _,buffer = cv2.imencode('.png', image)
            image_data = RTC.TimedOctetSeq(RTC.Time(0, 0), buffer.tobytes())
            

            #self._d_image.data = buffer.tobytes()
            self._imageOut.write(image_data)
            print("Image sent successfully")
    
         return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
    

def ObjectDataInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=objectdata_spec)
    manager.registerFactory(profile,
                            ObjectData,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ObjectDataInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("ObjectData" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

