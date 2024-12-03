#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file Discrimination.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
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
discrimination_spec = ["implementation_id", "Discrimination", 
         "type_name",         "Discrimination", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.h", "5",

         "conf.__widget__.h", "text",
         "conf.__constraints__.h", "h>0",

         "conf.__type__.h", "int",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class Discrimination
# @brief ModuleDescription
# 
# 
# </rtc-template>
class Discrimination(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_char_coord = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        """
        self._char_coordIn = OpenRTM_aist.InPort("char_coord", self._d_char_coord)
        self._d_person_coord = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        """
        self._person_coordIn = OpenRTM_aist.InPort("person_coord", self._d_person_coord)
        self._d_id = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        """
        """
        self._idOut = OpenRTM_aist.OutPort("id", self._d_id)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        
         - Name:  h
         - DefaultValue: 5
        """
        self._h = [5]
		
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
        self.bindParameter("h", self._h, "5")
		
        # Set InPort buffers
        self.addInPort("char_coord",self._char_coordIn)
        self.addInPort("person_coord",self._person_coordIn)
		
        # Set OutPort buffers
        self.addOutPort("id",self._idOut)
		
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
    def onExecute(self, ec_id):
        
        char_data = []
        person_data = []
        
        # �L�����N�^�[���W�̓ǂݍ���
        if self._char_coordIn.isNew():
            while self._char_coordIn.isNew():
                time.sleep(0.005)
                xy_data = self._char_coordIn.read().data
                for i in range(0, len(xy_data), 2):
                 char_data.append((xy_data[i], xy_data[i + 1])) 
            print(f"Received char_coords: {char_data}")
            

            # �l�����W�̓ǂݍ���
            if self._person_coordIn.isNew():
                while self._person_coordIn.isNew():
                     time.sleep(0.005)
                     xy_data = self._person_coordIn.read().data
                     for i in range(0, len(xy_data), 2):
                      person_data.append((xy_data[i], xy_data[i + 1]))
                print(f"Received person_coords: {person_data}")
                print("----------------------------------------")
            
            if char_data and person_data:
                for char_id, (x, y) in enumerate(char_data):    
                    print(char_id)
                
                    for person_id, (a, b) in enumerate(person_data):
                   
                        if (abs(x - a) <= self._h[0] / 2) and (abs(y - b) <= self._h[0] / 2):
                            self._d_id.data = char_id
                            print("true")
                            print(f"Matching id: {self._d_id.data}")
                            self._idOut.write(self._d_id)
                            time.sleep(1.0)
                            return RTC.RTC_OK
                        
                            
                        else:
                            print("false")
                print("----------------------------------------")
        return RTC.RTC_OK
	
        ###
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
	



def DiscriminationInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=discrimination_spec)
    manager.registerFactory(profile,
                            Discrimination,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    DiscriminationInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("Discrimination" + args)

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


