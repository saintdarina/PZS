import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

DATA_DIR = "data/drivedb"
record_name = "drive01"

record = wfdb.rdrecord(
    f"{DATA_DIR}/{record_name}",
    physical=True
)


ecg_index = record.sig_name.index("ECG")
ecg_signal = record.p_signal[:, ecg_index]
fs = record.fs

t = np.arange(len(ecg_signal)) / fs




def remove_dc(signal):
    """
    Odstranění DC složky signálu
    """
    return signal - np.mean(signal)

def normalize_signal(signal):
    """
    Normalizace signálu na interval <-1, 1>
    """
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal
    return signal / max_val

def preprocess_ecg(ecg_signal):
    """
    Předzpracování EKG signálu:
    1) odstranění DC složky
    2) normalizace amplitudy
    """
    ecg_dc = remove_dc(ecg_signal)
    ecg_norm = normalize_signal(ecg_dc)
    return ecg_norm




def bandpass_filter(signal, fs, lowcut=5, highcut=15, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, signal)
    return filtered

def moving_window_integration(signal, fs, window_ms=150):
    window_len = int(fs * window_ms / 1000)
    window = np.ones(window_len) / window_len
    integrated = np.convolve(signal, window, mode='same')
    return integrated

# def highlight_r_peaks(signal, window_size=5):
#     # 1. Derivace
#     deriv = np.zeros_like(signal)
#     deriv[1:-1] = (signal[2:] - signal[:-2]) / 2
#     deriv[0] = deriv[1]
#     deriv[-1] = deriv[-2]
    
#     # 2. Absolutní hodnota
#     abs_deriv = np.abs(deriv)
    
#     # 3. Klouzavý průměr
#     kernel = np.ones(window_size) / window_size
#     smooth_deriv = np.convolve(abs_deriv, kernel, mode='same')


    
#     return smooth_deriv

def adaptive_thresholding(signal, percent=0.3):
    max_val = np.max(signal)
    threshold = percent * max_val
    
    # Prahování
    thresholded_signal = np.where(signal >= threshold, signal, 0)
    
    return thresholded_signal

def detect_r_peaks(thresholded_signal):
    peaks = []
    for i in range(1, len(thresholded_signal) - 1):
        if (thresholded_signal[i] > thresholded_signal[i - 1] and
            thresholded_signal[i] > thresholded_signal[i + 1] and
            thresholded_signal[i] > 0):  # Už je nad prahem díky prahování
            peaks.append(i)
    return peaks


def detect_r_peaks_pantompkins(ecg_signal, fs):
    # 1. Bandpass filtr
    filtered = bandpass_filter(ecg_signal, fs)
    
    # 2. Derivace (centrální diference)
    deriv = np.zeros_like(ecg_signal)
    deriv[1:-1] = (ecg_signal[2:] - ecg_signal[:-2]) / 2
    deriv[0] = deriv[1]
    deriv[-1] = deriv[-2]
    
    # 3. Umocnění (squaring)
    squared = deriv ** 2
    
    # 4. Klouzavá integrace
    integrated = moving_window_integration(squared, fs)
    
    # 5. Adaptivní práh - jednoduchý dynamický prah (můžeš ladit)
    threshold = 0.3 * np.max(integrated)
    
    # Prahování
    # thresholded_signal = np.where(integrated >= threshold, integrated, 0)
    thresholded = (integrated > threshold).astype(int)
    
    # 6. Detekce lokálních maxim nad prahem
    peaks = []
    for i in range(1, len(thresholded)-1):
        if thresholded[i] == 1 and integrated[i] > integrated[i-1] and integrated[i] > integrated[i+1]:
            peaks.append(i)
    
    # 7. Refrakterní perioda (min 250 ms)
    min_distance = int(fs * 0.25)
    filtered_peaks = []
    for peak in peaks:
        if not filtered_peaks:
            filtered_peaks.append(peak)
        elif peak - filtered_peaks[-1] > min_distance:
            filtered_peaks.append(peak)
        else:
            # Vyber silnější z dvojice blízkých vrcholů
            if integrated[peak] > integrated[filtered_peaks[-1]]:
                filtered_peaks[-1] = peak
    
    return filtered_peaks, filtered, integrated




ecg_raw = ecg_signal
ecg_processed = preprocess_ecg(ecg_raw)

time = np.arange(len(ecg_processed)) / 250

# highlighted = highlight_r_peaks(ecg_processed)
# thresholded = adaptive_thresholding(highlighted, percent=0.3)
# r_peaks_indices = detect_r_peaks(thresholded)
# r_peaks_refined = refine_r_peaks(r_peaks_indices, ecg_raw, fs, refractory_period_s=0.3, search_window_ms=50)

r_peaks, filtered_ecg, integrated_signal = detect_r_peaks_pantompkins(ecg_processed, fs=250)

# plt.figure(figsize=(10, 4))
# plt.plot(t, ecg_processed, label="Processed EKG", alpha=0.6)
# plt.plot(t, thresholded, label="Thresholded EKG")
# plt.title("Derivace signálu")
# plt.tight_layout()
# plt.show()


# def plot_ecg_with_r_peaks(ecg_signal, r_peaks_indices, fs):
#     time = np.arange(len(ecg_signal)) / fs  # časová osa v sekundách
    
#     plt.figure(figsize=(12, 4))
#     plt.plot(time, ecg_signal, label='EKG signál')
#     plt.scatter(time[r_peaks_indices], ecg_signal[r_peaks_indices], color='red', label='R-vrcholy')
    
#     plt.xlabel('Čas [s]')
#     plt.ylabel('Amplituda')
#     plt.title('Detekce R-vrcholu v EKG signálu')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# Příklad použití:
plt.figure(figsize=(15,5))
plt.plot(time, ecg_raw, label='Originální EKG')
plt.plot(time, filtered_ecg, label='Filtrovaný signál')
plt.plot(time, integrated_signal, label='Integrovaný signál')
plt.scatter(time[r_peaks], ecg_raw[r_peaks], color='red', label='R-vrcholy')
plt.legend()
plt.title('Detekce R-vrcholů Pan-Tompkins algoritmem')
plt.show()

print(len(r_peaks))