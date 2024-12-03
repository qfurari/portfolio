#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file VoiceAnalize.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import numpy as np
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
analysis2_spec = ["implementation_id", "VoiceAnalize", 
         "type_name",         "VoiceAnalize", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "test", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class VoiceAnalize
# @brief ModuleDescription
# 
# 
# </rtc-template>
class analysis2(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_Now_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._Now_voiceIn = OpenRTM_aist.InPort("Now_voice", self._d_Now_voice)
        self._d_save_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        """
        self._save_voiceIn = OpenRTM_aist.InPort("save_voice", self._d_save_voice)
        self._d_Now_analysis = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        """
        """
        self._Now_analysisOut = OpenRTM_aist.OutPort("Now_analysis", self._d_Now_analysis)
        self._d_sava_analysis = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        """
        """
        self._sava_analysisOut = OpenRTM_aist.OutPort("sava_analysis", self._d_sava_analysis)


		


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
        self.addInPort("Now_voice",self._Now_voiceIn)
        self.addInPort("save_voice",self._save_voiceIn)
		
        # Set OutPort buffers
        self.addOutPort("Now_analysis",self._Now_analysisOut)
        self.addOutPort("sava_analysis",self._sava_analysisOut)
		
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
        if self._save_voiceIn.isNew():
            print("----------------------resived save voice----------------------------")
            data = self._save_voiceIn.read().data

            # バイト列からnumpy配列に変換
            audio_data = np.frombuffer(data, dtype=np.int16)

            # 振幅データの取得
            amplitude = np.abs(audio_data)

            # 最大振幅を計算
            max_amplitude = int(np.max(amplitude))
            print("最大振幅値:", max_amplitude)
            MAX = RTC.TimedShort(RTC.Time(0,0),max_amplitude)
            # 最大振幅をアウトポートに出力
            print(type(MAX))
            #self._d_VoiceMax.data = MAX
            self._sava_analysisOut.write(MAX)
        if self._Now_voiceIn.isNew():
            print("######### resived voice ###########")
            now_data=self._Now_voiceIn.read().data
            numpy_data = np.frombuffer(now_data, dtype=np.int16)
            peak = int(np.abs(numpy_data).max())
            print(f"ピーク振幅: {peak}", end='\r')
            am_data = RTC.TimedShort(RTC.Time(0, 0), peak)
            self._Now_analysisOut.write(am_data)

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
	



def analysis2Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=analysis2_spec)
    manager.registerFactory(profile,
                            analysis2,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    analysis2Init(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("VoiceAnalize" + args)

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

