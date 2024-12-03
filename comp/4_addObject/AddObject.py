

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file AddObject.py
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

# This module's specification
addobject_spec = ["implementation_id", "AddObject", 
                  "type_name",         "AddObject", 
                  "description",       "ModuleDescription", 
                  "version",           "1.0.0", 
                  "vendor",            "arai", 
                  "category",          "test", 
                  "activity_type",     "STATIC", 
                  "max_instance",      "1", 
                  "language",          "Python", 
                  "lang_type",         "SCRIPT",
                  ""]

class AddObject(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_In_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        self._In_voiceIn = OpenRTM_aist.InPort("In_voice", self._d_In_voice)
        
        self._d_In_analysis = OpenRTM_aist.instantiateDataType(RTC.TimedShort)
        self._In_analysis = OpenRTM_aist.InPort("In_analysis", self._d_In_analysis)
        
        self._d_In_VoiceSeq = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        self._In_VoiceSeqIn = OpenRTM_aist.InPort("In_VoiceSeq", self._d_In_VoiceSeq)
        
        self._d_In_analysisSeq = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        self._In_imageSeqIn = OpenRTM_aist.InPort("In_imageSeq", self._d_In_analysisSeq)
        
        self._d_In_PositionSeq = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        self._In_PositionSeqIn = OpenRTM_aist.InPort("In_PositionSeq", self._d_In_PositionSeq)
        
        self._d_Out_VoiceSeq = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        self._Out_VoiceSeqOut = OpenRTM_aist.OutPort("Out_VoiceSeq", self._d_Out_VoiceSeq)
        
        self._d_Out_analysisSeq = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        self._Out_analysisSeqOut = OpenRTM_aist.OutPort("Out_analysisSeq", self._d_Out_analysisSeq)
        
        self._d_Out_PositionSeq = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        self._Out_PositionSeqOut = OpenRTM_aist.OutPort("Out_PositionSeq", self._d_Out_PositionSeq)
        
        self.analysisSeq_data = []
        self.voiceSeq_data = []
        self.positionSeq_data =[]

    def onInitialize(self):
        self.addInPort("In_voice", self._In_voiceIn)
        self.addInPort("In_analysis", self._In_analysis)
        self.addInPort("In_VoiceSeq", self._In_VoiceSeqIn)
        self.addInPort("In_imageSeq", self._In_imageSeqIn)
        self.addInPort("In_PositionSeq", self._In_PositionSeqIn)
        
        self.addOutPort("Out_VoiceSeq", self._Out_VoiceSeqOut)
        self.addOutPort("Out_analysisSeq", self._Out_analysisSeqOut)
        self.addOutPort("Out_PositionSeq", self._Out_PositionSeqOut)
        
        return RTC.RTC_OK

    def onActivated(self, ec_id):
        return RTC.RTC_OK

    def onDeactivated(self, ec_id):
        return RTC.RTC_OK

    def onExecute(self, ec_id):
        import random

        # �����v�f��ǉ�����ꍇ
        if self._In_voiceIn.isNew():

            if len(self.voiceSeq_data)>=8:
                print("Length of read voice sequence data is full")
                #一度追加データを読み込む
                analysis_data = self._In_analysis.read().data
                voice_data = self._In_voiceIn.read().data
                
                
                return RTC.RTC_OK 
            ##データを読み込んで処理する必要あり
            #このままだとずっとここをループする

            # Read additional voice and analysis data
            analysis_data = self._In_analysis.read().data
            voice_data = self._In_voiceIn.read().data
            print("Additional information read complete")
            ppositionSeq_data=[]
            time.sleep(0.8)
            if self._In_PositionSeqIn.isNew():
                print("add inserted!!")
                 # Read position sequence data
                while self._In_PositionSeqIn.isNew():
                    time.sleep(0.005)
                    positionIn_data = self._In_PositionSeqIn.read().data
                    ppositionSeq_data.append(positionIn_data)


               # For verification
            ################################################
            print("before Length of voice sequence: "+str(len(self.voiceSeq_data)))
            print("before Length of analysis sequence: "+str(len(self.analysisSeq_data)))
            print("before Length of position sequence: "+str(len(ppositionSeq_data)))
            ################################################

            # Add the received voice data, analysis data, and position data (50, 50) to each sequence
            self.voiceSeq_data.append(voice_data)
            self.analysisSeq_data.append(analysis_data)
            random_x = random.randint(1, 640)
            random_y = random.randint(1, 480)
            ppositionSeq_data.append([random_x, random_y])
         
            print("Adding elements...")

            # For verification
            ################################################
            print("Addition complete..")
            print("after Length of voice sequence: "+str(len(self.voiceSeq_data)))
            print("after Length of analysis sequence: "+str(len(self.analysisSeq_data)))
            print("after Length of position sequence: "+str(len(ppositionSeq_data)))
            ################################################
            print("positiondata:",ppositionSeq_data)

            # Send data one by one
            # Send voice data
            for data in self.voiceSeq_data:
                Outvoice = RTC.TimedOctetSeq(RTC.Time(0, 0), data)
                self._Out_VoiceSeqOut.write(Outvoice)
            
            # Send analysis data
            Outanalysis = RTC.TimedShortSeq(RTC.Time(0, 0), self.analysisSeq_data)
            self._Out_analysisSeqOut.write(Outanalysis)

            # Send position data
            # Simply send positions one by one (consider pairs of two as coordinates) - under development
            for data in ppositionSeq_data:
                Outimage = RTC.TimedShortSeq(RTC.Time(0, 0), data)
                self._Out_PositionSeqOut.write(Outimage) 
                 
                
        #�z��v�f���������������ꍇ
        elif self._In_VoiceSeqIn.isNew():
            
            if self._In_VoiceSeqIn.isNew():
                # Read voice sequence data
                self.voiceSeq_data.clear()
                while self._In_VoiceSeqIn.isNew():
                    time.sleep(0.005)
                    voiceIn_data = self._In_VoiceSeqIn.read().data
                    self.voiceSeq_data.append(voiceIn_data)
                print("Length of read voice sequence data: "+str(len(self.voiceSeq_data)))
            if self._In_imageSeqIn.isNew():
                # Read analysis sequence data
                self.analysisSeq_data = self._In_imageSeqIn.read().data
                #analysisSeq_data.append(analysisIn_data)
                print(f"Received analysis data: {self.analysisSeq_data}")
            print("before Length of voice sequence: "+str(len(self.voiceSeq_data)))
            print("before Length of analysis sequence: "+str(len(self.analysisSeq_data)))
            for data in self.voiceSeq_data:
                Outvoice = RTC.TimedOctetSeq(RTC.Time(0, 0), data)
                self._Out_VoiceSeqOut.write(Outvoice)
            
            # Send analysis data
            Outanalysis = RTC.TimedShortSeq(RTC.Time(0, 0), self.analysisSeq_data)
            self._Out_analysisSeqOut.write(Outanalysis)
            
        else:
            ppositionSeq_data=[]
            if self._In_PositionSeqIn.isNew():
                 # Read position sequence data
                while self._In_PositionSeqIn.isNew():
                    time.sleep(0.005)
                    positionIn_data = self._In_PositionSeqIn.read().data
                    ppositionSeq_data.append(positionIn_data)
                print(F"Resived position_Data{ppositionSeq_data}")
             
                 # Send position data
                 # Simply send positions one by one (consider pairs of two as coordinates) - under development
            for data in ppositionSeq_data:
                 Outimage = RTC.TimedShortSeq(RTC.Time(0, 0), data)
                 self._Out_PositionSeqOut.write(Outimage)
                 
             
            
        return RTC.RTC_OK

def AddObjectInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=addobject_spec)
    manager.registerFactory(profile, AddObject, OpenRTM_aist.Delete)

def MyModuleInit(manager):
    AddObjectInit(manager)
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
    comp = manager.createComponent("AddObject" + args)

def main():
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

