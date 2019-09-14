#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Canopy Vibrator
# Author: Peter F Bradshaw
# Description: A simple audio source to vibrate the canopy
# Generated: Sat Sep 14 22:55:59 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sys


class vibrate(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Canopy Vibrator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Canopy Vibrator")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "vibrate")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.source_frequency = source_frequency = 1000
        self.source_amplitude = source_amplitude = 0.5
        self.samp_rate = samp_rate = 44100

        ##################################################
        # Blocks
        ##################################################
        self._source_frequency_range = Range(100, 10000, 10, 1000, 200)
        self._source_frequency_win = RangeWidget(self._source_frequency_range, self.set_source_frequency, 'Source Frequency', "counter_slider", int)
        self.top_layout.addWidget(self._source_frequency_win)
        self._source_amplitude_range = Range(0, 1, 0.01, 0.5, 200)
        self._source_amplitude_win = RangeWidget(self._source_amplitude_range, self.set_source_amplitude, 'Source Amplitude', "counter_slider", float)
        self.top_layout.addWidget(self._source_amplitude_win)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, source_frequency, source_amplitude, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, source_frequency, source_amplitude, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.audio_sink_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vibrate")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_source_frequency(self):
        return self.source_frequency

    def set_source_frequency(self, source_frequency):
        self.source_frequency = source_frequency
        self.analog_sig_source_x_1.set_frequency(self.source_frequency)
        self.analog_sig_source_x_0.set_frequency(self.source_frequency)

    def get_source_amplitude(self):
        return self.source_amplitude

    def set_source_amplitude(self, source_amplitude):
        self.source_amplitude = source_amplitude
        self.analog_sig_source_x_1.set_amplitude(self.source_amplitude)
        self.analog_sig_source_x_0.set_amplitude(self.source_amplitude)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)


def main(top_block_cls=vibrate, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
