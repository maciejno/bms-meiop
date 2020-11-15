import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter as sg
from matplotlib.colors import ListedColormap

#kolorki
colormap1 = ListedColormap(["red","lawngreen"])
colormap2 = ListedColormap(["blue","lawngreen"])
colormap3 = ListedColormap(["magenta","lawngreen"])
colormap4 = ListedColormap(["cyan","lawngreen"])
colormap5 = ListedColormap(["gray","lawngreen"])
colormap6 = ListedColormap(["black","lawngreen"])

#funkcja obliczająca wartości wielomianu i pochodnej
def bat_poly_calc(x, c):
    return c[0] + c[1]*x+c[2]*x**2+c[3]*x**3+c[4]*x**4+c[5]*x**5+c[6]*x**6+c[7]*x**7+c[8]*x**8+c[9]*x**9
def bat_diff_calc(x, c):
    return (c[1]+2*c[2]*x+3*c[3]*x**2+4*c[4]*x**3+5*c[5]*x**4+6*c[6]*x**5+7*c[7]*x**6+8*c[8]*x**7+9*c[9]*x**8)


bat_time = np.linspace(10,7200,720) #BATtery_time - całk. czas ipeh1+ipeh2

bat_data = pd.read_csv('ipeh1.csv') #BATtery data
bat_data1 = pd.read_csv("ipeh2.csv")
bat_data = bat_data.append(bat_data1, ignore_index=True)
print(bat_data) #ipeh1+ipeh2

#wykres zbiorczy napięć
plt.scatter(bat_time, bat_data.U1, s=4, c="red", label='U1')
plt.scatter(bat_time, bat_data.U2, s=4, c="blue", label='U2')
plt.scatter(bat_time, bat_data.U3, s=4, c="magenta", label='U3')
plt.scatter(bat_time, bat_data.U4, s=4, c="cyan", label='U4')
plt.scatter(bat_time, bat_data.U5, s=4, c="gray", label='U5')
plt.scatter(bat_time, bat_data.U6, s=4, c="black", label='U6')
plt.xlabel("t [s]")
plt.ylabel("U [V]")
plt.legend(loc='best')
plt.savefig('Lion_voltages.png', dpi=420)

#krzywe ładowania
bat_ref_1C = pd.read_csv('NMC_1C.csv', sep='; ',decimal=',') #krzywa referencyjna 1C
bat_ref_1C["U"] = bat_ref_1C["U"].values[::-1]
bat_ref_1C["Q"] = bat_ref_1C["Q"].values*0.01
coeffs_1C = np.polynomial.polynomial.polyfit(bat_ref_1C.Q,bat_ref_1C.U,9) #dopasowanie wielomianu


bat_ref_02C = pd.read_csv('NMC_02C.csv', sep='; ',decimal=',') #krzywa referencyjna 0,2C
bat_ref_02C["Q"] = bat_ref_02C["Q"].values[::-1]
bat_ref_02C["Q"] = bat_ref_02C["Q"].values*0.01
coeffs_02C = np.polynomial.polynomial.polyfit(bat_ref_02C.Q,bat_ref_02C.U,9) #dopasowanie wielomianu

bat_data_charge = bat_data[:472] #cięcie na część ładowania i rozładowania
bat_data_discharge = bat_data[472:]
bat_data_discharge = bat_data_discharge.reset_index(drop=True)

bat_data_charge['Q'] = (bat_data_charge.index+1)*10*5000/3600/6560 #przeliczanie kolumny z ładunkiem
bat_data_discharge['Q'] = (6560-(bat_data_discharge.index+1)*10*200/3600)/6560

bat_data_charge['StdevCh'] = bat_data_charge.Stdev/bat_diff_calc(bat_data_charge.Q,coeffs_1C) #obliczanie odchylenia ładunku
bat_data_discharge['StdevCh'] = bat_data_discharge.Stdev/bat_diff_calc(bat_data_discharge.Q,coeffs_02C)

bat_data = bat_data_charge  #końcowe sumowanie danych
bat_data = bat_data.append(bat_data_discharge)
bat_mobil = 42

#wykres
fig, axs = plt.subplots(8,sharex=True, gridspec_kw={'hspace': 0})
axs[0].scatter(bat_time, bat_data.U1, s=5, c=bat_data.B1, cmap=colormap1)
axs[1].scatter(bat_time, bat_data.U2, s=5, c=bat_data.B2, cmap=colormap2)
axs[2].scatter(bat_time, bat_data.U3, s=5, c=bat_data.B3, cmap=colormap3)
axs[3].scatter(bat_time, bat_data.U4, s=5, c=bat_data.B4, cmap=colormap4)
axs[4].scatter(bat_time, bat_data.U5, s=5, c=bat_data.B5, cmap=colormap5)
axs[5].scatter(bat_time, bat_data.U6, s=5, c=bat_data.B6, cmap=colormap6)
axs[6].scatter(bat_time, bat_data.Stdev, s=1)
axs[7].scatter(bat_time, bat_data.StdevCh, s=1)
axs[0].set(xlabel='$t$ / s', ylabel='$U_1$ / V')
axs[1].set(xlabel='$t$ / s', ylabel='$U_2$ / V')
axs[2].set(xlabel='$t$ / s', ylabel='$U_3$ / V')
axs[3].set(xlabel='$t$ / s', ylabel='$U_4$ / V')
axs[4].set(xlabel='$t$ / s', ylabel='$U_5$ / V')
axs[5].set(xlabel='$t$ / s', ylabel='$U_6$ / V')
axs[6].set(xlabel='$t$ / s', ylabel='$\sigma$ / V')
axs[7].set(xlabel='$t$ / s', ylabel='$\sigma_Q$ / C')
plt.xlabel("t /s")
plt.savefig('Lion_multiplot.png', dpi=420)
plt.show()


#ipeh3
################################################################################
# bat_data3 = pd.read_csv('ipeh3.csv')
#
# plt.scatter(bat_data3.t, bat_data3.U1, s=5, c=bat_data3.B1, cmap=colormap1)
# plt.scatter(bat_data3.t, bat_data3.U2, s=5, c=bat_data3.B2, cmap=colormap2)
# plt.scatter(bat_data3.t, bat_data3.U3, s=5, c=bat_data3.B3, cmap=colormap3)
# plt.scatter(bat_data3.t, bat_data3.U4, s=5, c=bat_data3.B4, cmap=colormap4)
# plt.scatter(bat_data3.t, bat_data3.U5, s=5, c=bat_data3.B5, cmap=colormap5)
# plt.scatter(bat_data3.t, bat_data3.U6, s=5, c=bat_data3.B6, cmap=colormap6)
# plt.xlabel("t [s]")
# plt.ylabel("U [V]")
# plt.legend(loc='best')
# plt.show()
