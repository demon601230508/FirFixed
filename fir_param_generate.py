import numpy as np
import scipy.signal as signal
import pylab as pl
import matplotlib.pyplot as plt

fs = 48000.0  # Hz
scaling_factor = 2**14
fir_order = 63 #必现为基数
fig, axs = plt.subplots(2)
ps = 1.3
desired = (0, 0, ps, ps,ps, ps)
for bi, bands in enumerate(((0, 5400, 5600, 6600,7600 , 24000), (0, 20, 150, 355, 390, 24000))):

#desired = (0, 0, 1, 1, 0, 0)
#for bi, bands in enumerate(((0, 1250, 1500, 2500, 2750, 24000), (0,2500, 3000, 4000, 4500, 24000))):
    fir_firls = signal.firls(fir_order, bands, desired, fs=fs)
    #print(fir_firls)
    print(np.round(fir_firls*scaling_factor))
    #print(fir_firls*scaling_factor)
    fir_remez = signal.remez(fir_order, bands, desired[::2], fs=fs)
    fir_firwin2 = signal.firwin2(fir_order, bands, desired, fs=fs)
    hs = list()
    ax = axs[bi]
    for fir in (fir_firls, fir_remez, fir_firwin2):
        #print(fir)
        freq, response = signal.freqz(fir)
        hs.append(ax.semilogy(0.5*fs*freq/np.pi, np.abs(response))[0])
        #print(np.abs(response)[::2])
    for band, gains in zip(zip(bands[::2], bands[1::2]),
                           zip(desired[::2], desired[1::2])):
        ax.semilogy(band, np.maximum(gains, 1e-7), 'k--', linewidth=2)
    if bi == 0:
        ax.legend(hs, ('firls', 'remez', 'firwin2'),
                  loc='lower center', frameon=False)
    else:
        ax.set_xlabel('Frequency (Hz)')
    ax.grid(True)
    ax.set(title='Band-pass %d-%d Hz' % bands[2:4], ylabel='Magnitude')
fig.tight_layout()
plt.xlim(0,5000)
plt.ylim(0.01,3)
plt.show()

np.set_printoptions(suppress=True)

desired = (ps, ps, ps, ps, 0, 0)
lc = 355
tb =35
fir_firls = signal.firls(fir_order, (0, 20, 150, lc, lc+tb, 24000), desired, fs=fs)
print("//lowPss:","(tb",tb,")",lc)
print ("int16_t coeffs_lp"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))

lc = 355
hc = 645
tb = 35
desired = (0, 0, ps, ps, 0, 0)
fir_firls = signal.firls(fir_order, (0, lc-tb, lc, hc, hc+tb, 24000), desired, fs=fs)
print("//bandPass: ","(tb",tb,")",lc,"- -",hc)
print ("int16_t coeffs_bp_1"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))

lc = 645
hc = 1355
tb = 70
desired = (0, 0, ps, ps, 0, 0)
fir_firls = signal.firls(fir_order, (0, lc-tb, lc, hc, hc+tb, 24000), desired, fs=fs)
print("//bandPass: ","(tb",tb,")",lc,"- -",hc)
print ("int16_t coeffs_bp_2"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))

lc = 1355
hc = 2645
tb = 100
desired = (0, 0, ps, ps, 0, 0)
fir_firls = signal.firls(fir_order, (0, lc-tb, lc, hc, hc+tb, 24000), desired, fs=fs)

print("//bandPass: ","(tb",tb,")",lc,"- -",hc)
print ("int16_t coeffs_bp_3"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))

lc = 2645
hc = 5600
tb = 200
desired = (0, 0, ps, ps, 0, 0)
fir_firls = signal.firls(fir_order, (0, lc-tb, lc, hc, hc+tb, 24000), desired, fs=fs)
print("//bandPass: ","(tb",tb,")",lc,"- -",hc)
print ("int16_t coeffs_bp_4"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))


hc = 5600
tb = 200
desired = (0, 0, ps, ps,ps, ps)
fir_firls = signal.firls(fir_order, (0, hc-tb, hc, hc+1000, hc+2000, 24000), desired, fs=fs)
print("//highPass: ","(tb",tb,")",hc)
print ("int16_t coeffs_hp"+"[ FIRFIXED_ORDER ] =")
print(np.round(fir_firls*scaling_factor))
