#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file Character_Management.py
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
character_management_spec = ["implementation_id", "Character_Management", 
         "type_name",         "Character_Management", 
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
# @class Character_Management
# @brief ModuleDescription
# 
# 
# </rtc-template>
class Character_Management(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_coordinate = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        """
        self._coordinateIn = OpenRTM_aist.InPort("coordinate", self._d_coordinate)
        self._d_image = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._imageIn = OpenRTM_aist.InPort("image", self._d_image)
        self._d_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._voiceIn = OpenRTM_aist.InPort("voice", self._d_voice)
        self._d_processed_coordinate = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        """
        self._processed_coordinateOut = OpenRTM_aist.OutPort("processed_coordinate", self._d_processed_coordinate)
        self._d_processed_image = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._processed_imageOut = OpenRTM_aist.OutPort("processed_image", self._d_processed_image)
        self._d_processed_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._processed_voiceOut = OpenRTM_aist.OutPort("processed_voice", self._d_processed_voice)


		


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
        self.addInPort("coordinate",self._coordinateIn)
        self.addInPort("image",self._imageIn)
        self.addInPort("voice",self._voiceIn)
		
        # Set OutPort buffers
        self.addOutPort("processed_coordinate",self._processed_coordinateOut)
        self.addOutPort("processed_image",self._processed_imageOut)
        self.addOutPort("processed_voice",self._processed_voiceOut)
		
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
        #追加座標
        if self._voiceIn.isNew():
            print("#####オブジェクト管理######")
            #追加音声の読み込み
            print("音声読み込み開始")
            voiceIn_data_list = []
            while self._voiceIn.isNew():
                voiceIn_data = self._voiceIn.read().data
                #voiceIn_data_list += voiceIn_data
                voiceIn_data_list.append(voiceIn_data)
            print("現在の音声配列の長さ："+ str(len(voiceIn_data_list)))
            #Voice出力
            for data in voiceIn_data_list:
                Outvoice = RTC.TimedOctetSeq(RTC.Time(0,0),data)
                self._processed_voiceOut.write(Outvoice)

        if self._imageIn.isNew():
            #追加画像の読み込み
            print("画像読み込み開始")
            imageIn_data_list = []
            while self._imageIn.isNew():
                imageIn_data = self._imageIn.read().data
                #imageIn_data_list += imageIn_data
                imageIn_data_list.append(imageIn_data)
            print("現在の画像配列の長さ："+ str(len(imageIn_data_list)))
            #imageの出力
            for data in imageIn_data_list:
                Outimage = RTC.TimedOctetSeq(RTC.Time(0,0),data)
                self._processed_imageOut.write(Outimage)

        if self._coordinateIn.isNew():
            #追加座標の読み込み
            print("座標読み込み開始")
            coordinateIn_data_list = []
            while self._coordinateIn.isNew():
                coordinateIn_data = self._coordinateIn.read().data
                coordinateIn_data_list.append(coordinateIn_data)
            print("現在の座標配列の長さ："+ str(len(coordinateIn_data_list)))
            #追加座標の出力
            for data in coordinateIn_data_list:
                OutCoordinate = RTC.TimedShortSeq(RTC.Time(0,0),data)
                self._processed_coordinateOut.write(OutCoordinate)

            
    
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
	



def Character_ManagementInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=character_management_spec)
    manager.registerFactory(profile,
                            Character_Management,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    Character_ManagementInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("Character_Management" + args)

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

