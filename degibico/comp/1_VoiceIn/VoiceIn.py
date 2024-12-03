#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file VoiceIn.py
 @brief ModuleDescription
 @date $Date$
"""

import sys
import time
import threading
import queue
from datetime import datetime

import pyaudio
import RTC
import OpenRTM_aist
sys.path.append(".")


voice2in_spec = ["implementation_id", "VoiceIn", 
                 "type_name",         "VoiceIn", 
                 "description",       "ModuleDescription", 
                 "version",           "1.0.0", 
                 "vendor",            "test", 
                 "category",          "test", 
                 "activity_type",     "STATIC", 
                 "max_instance",      "1", 
                 "language",          "Python", 
                 "lang_type",         "SCRIPT",
                 ""]

class Voice2in(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._d_Now_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        self._Now_voiceOut = OpenRTM_aist.OutPort("Now_voice", self._d_Now_voice)
        self._d_Save_voice = OpenRTM_aist.instantiateDataType(RTC.TimedOctetSeq)
        self._Save_voiceOut = OpenRTM_aist.OutPort("Save_voice", self._d_Save_voice)

        self.monitoring = False
        self.lock = threading.Lock()
        self.input_queue = queue.Queue()
        self.recording_requested = False

        self.stop_event = threading.Event()

    def onInitialize(self):
        self.addOutPort("Now_voice", self._Now_voiceOut)
        self.addOutPort("Save_voice", self._Save_voiceOut)
        return RTC.RTC_OK

    def onActivated(self, ec_id):
        self.monitoring = True
        self.stop_event.clear()  # Reset the stop event
        self.monitor_thread = threading.Thread(target=self.monitor_audio)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        self.record_thread = threading.Thread(target=self.wait_for_enter_and_record)
        self.record_thread.daemon = True
        self.record_thread.start()

        self.input_thread = threading.Thread(target=self.capture_input)
        self.input_thread.daemon = True
        self.input_thread.start()
        return RTC.RTC_OK

    def onDeactivated(self, ec_id):
        self.monitoring = False
        self.stop_event.set()  # Signal to stop input thread
        if self.monitor_thread:
            self.monitor_thread.join()
        if self.record_thread:
            self.record_thread.join()
        if self.input_thread:
            self.input_thread.join()
        return RTC.RTC_OK

    def onExecute(self, ec_id):
        if self.recording_requested:
            self.recording_requested = False
            self.record_audio()
        return RTC.RTC_OK

    def record_audio(self):
        time.sleep(0.08)
        print("Recording...")
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 3

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        voice_data = b''.join(frames)
        timed_voice_data = RTC.TimedOctetSeq(self.get_current_time(), voice_data)
        self._Save_voiceOut.write(timed_voice_data)

        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Recording finished.")

    def monitor_audio(self):
        time.sleep(0.08)
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        while self.monitoring:
            data = stream.read(CHUNK, exception_on_overflow=False)
            NowVoiceOut = RTC.TimedOctetSeq(self.get_current_time(), data)
            self._Now_voiceOut.write(NowVoiceOut)

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def wait_for_enter_and_record(self):
        while self.monitoring:
            try:
                command = self.input_queue.get(timeout=0.1)
                if command is None:
                    break
                if command == "record":
                    with self.lock:
                        self.recording_requested = True
            except queue.Empty:
                continue

    def capture_input(self):
        while not self.stop_event.is_set():
            user_input = input("録音を開始するにはEnterキーを押してください (終了するにはqを押してください)\n")
            if user_input == "q":
                self.stop_event.set()
                self.monitoring = False
                break
            elif user_input == "":
                self.input_queue.put("record")

    def get_current_time(self):
        now = datetime.now()
        return RTC.Time(now.second, now.microsecond * 1000)

def Voice2inInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=voice2in_spec)
    manager.registerFactory(profile,
                            Voice2in,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    Voice2inInit(manager)
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
    comp = manager.createComponent("VoiceIn" + args)

def main():
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    mgr = OpenRTM_aist.Manager.init(argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()
