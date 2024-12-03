#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file VoiceOut.py
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
voiceout_spec = ["implementation_id", "VoiceOut", 
         "type_name",         "VoiceOut", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "TaigaKadoguchi", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class VoiceOut
# @brief ModuleDescription
# 
# 
# </rtc-template>
class VoiceOut(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_InVoice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        """
        音声のバイナリファイル(wavファイル)の配列を受け取る
        """
        self._InVoiceIn = OpenRTM_aist.InPort("InVoice", self._d_InVoice)
        self._d_ID = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        """
        配列のID(何番目の音声を再生するか)を受け取る
        """
        self._IDIn = OpenRTM_aist.InPort("ID", self._d_ID)


		


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
        self.addInPort("InVoice",self._InVoiceIn)
        self.addInPort("ID",self._IDIn)
		
        # Set OutPort buffers
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
        self.voice_data_list = []  # 音声データリストをクラス変数として定義
		
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
        import pyaudio
        import wave
        
        
        if self._InVoiceIn.isNew():
            self.voice_data_list.clear()

            while self._InVoiceIn.isNew():
                time.sleep(0.005)
                voice_data = self._InVoiceIn.read().data
                self.voice_data_list.append(voice_data)
                
            print(f"Received {len(self.voice_data_list)} audio files.")  # 音声ファイルのリストの長さを表示



        # IDポートからIDを取得
        if self._IDIn.isNew():
            id_data = self._IDIn.read()
            id_number = id_data.data

            # InVoiceポートから音声ファイルデータを一つずつ受け取り、リストに追加
            #voice_data_list = []
            #while self._InVoiceIn.isNew():
                #voice_data = self._InVoiceIn.read().data
                #voice_data_list.append(voice_data)

            # IDに対応する音声ファイルのインデックスを取得
            file_index = id_number  # ×IDは1から始まるが、インデックスは0から始まるため

            # 取得したインデックスの音声データを再生
            if 0 <= file_index < len(self.voice_data_list):
                # バイナリデータをpyaudioで再生
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(2),  # フォーマットを指定
                                channels=1,                         # モノラル
                                rate=44100,                         # サンプリングレート
                                output=True)                        # 出力用ストリームとして開く

                # 音声データを再生
                stream.write(self.voice_data_list[file_index])  # 指定したインデックスの音声データを再生

                stream.stop_stream()
                stream.close()
                p.terminate()

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
	



def VoiceOutInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=voiceout_spec)
    manager.registerFactory(profile,
                            VoiceOut,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    VoiceOutInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("VoiceOut" + args)

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

