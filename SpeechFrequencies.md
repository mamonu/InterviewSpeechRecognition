https://dsp.stackexchange.com/questions/2993/human-speech-noise-filter

 -  Does anyone know of a filter to attenuate non-speech? 
        
        
        I am writing speech recognition software and would like to filter out everything but human speech. 
        This would include background noise, noise produced by a crappy microphone, or even background music. 
        I have already implemented a first order filter that compensates for the 6 dB roll-off of the power spectrum, 
        but I'm still hearing noise (though the speech sounds a lot clearer). 
        I have thought to use a low-pass filter,but I am iffy about doing that for two reasons:

        I don't know whether or not a low-pass pre-filter will interfere with the rest of the speech processing. 
        Even though the human ear can only detect sounds lower than 20 kHz, I don't want to risk eliminating any 
        higher order harmonics that might be necessary to process the speech 
        (though I don't know if this is the case or not. But I don't want to take any chances).

        I understand that the excitation of certain consonants (such as f, h, and s) are almost entirely white noise. 
        I don't want to implement a noise filter that will eliminate good noise, so to speak.
        Ideally, I would like to be left with only the speech of the person speaking into the microphone. 
        If you have any ideas, or there is something that I'm missing, please let me know. Much appreciated!
        
        
A speech communication channel as used in telephony typically has a frequency response of 300 Hz to 3 kHz.
Although this rejects a lot of the energy in normal speech, intelligibility is still quite good - 
the main problem seems to be that certain plosive consonants, e.g. "p" and "t", can be a little hard to 
discriminate without the higher frequency components.

So you're probably looking for a "sweet spot" somewhere between using the full 20 Hz - 20 kHz bandwidth
typically found in consumer audio and the most aggressive filtering used for voice comms (see above).
I would suggest starting with a bandpass filter from say 50 Hz to 8 kHz. 
It will probably only improve SNR by a few dB at best, but it may help, 
particularly if you have a lot of high frequency background noise.
