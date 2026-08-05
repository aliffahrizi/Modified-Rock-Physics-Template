import numpy as np
import matplotlib.pyplot as plt

def CPEI(AI, VpVs, CPEIparameter):    
    return ((AI ** CPEIparameter[0]) * ((VpVs) ** CPEIparameter[1]) * np.cos(np.radians(CPEIparameter[2])) + (AI ** CPEIparameter[0]) * ((1/VpVs) ** CPEIparameter[1]) * np.sin(np.radians(CPEIparameter[2])))

def PEIL(AI, VpVs, CPEIparameter):
    return ((-1*(AI ** CPEIparameter[0]) * ((VpVs) ** CPEIparameter[1]) * np.sin(np.radians(CPEIparameter[2]))) + (AI ** CPEIparameter[0]) * ((1/VpVs) ** CPEIparameter[1]) * np.cos(np.radians(CPEIparameter[2])))

def scaled(Data, Target):
    a0 = np.min(Target)
    at = np.max(Target)
    b0 = np.min(Data)
    bt = np.max(Data)
    
    return a0 + ((Data - b0) / (bt - b0)) * (at - a0)

def porosityDensity(rho_matrix, rho_bulk, rho_fluid):
    return (rho_matrix - rho_bulk) / (rho_matrix - rho_fluid)


def FluidSaturation(rho_matrix, rho_fluid, rho_water, Vp_matrix, Vp_fluid, Vp_water, porosity, AI):
    a = rho_matrix 
    b = porosity * (rho_water - rho_matrix)
    c = AI * ((1 / Vp_matrix) + porosity * ((1 / Vp_water) - (1 / Vp_matrix)))
    d = porosity * (AI * ((1 / Vp_fluid) - (1 / Vp_water)) - (rho_fluid - rho_water))
    
    return (a + b - c) / d


def VolumeofShale(AI, Vp_matrix, Vs_matrix, Vp_water, Vp_shale, rho_matrix, rho_shale, rho_water, porosity):
    a = rho_matrix - (AI/Vp_matrix) - (1 - porosity)
    b = AI * (1/Vp_water - 1/Vp_matrix) - (rho_water - rho_matrix)
    c = (rho_shale - rho_matrix) - AI * (1 / Vp_shale - 1 / Vp_matrix)
    
    return a * b / c
    
    
def porosityFawad(Vp, Vs, alpha, G, N):
    return 1 - ((Vs / (Vp * G * alpha)) ** (1/N))


def porosityKrishna(Vp_matrix, Vs_saturated, rho_saturated, rho_matrix, alpha, G, N):
    a = (Vs_saturated ** 2) * rho_saturated
    b = (alpha ** 2) * (G ** 2) * (Vp_matrix ** 2) * rho_matrix
    c = 1 / (2 * N + 1)
    
    porosity = 1 - ((a / b) ** c)
    
    return porosity


def MatrixModulus(method, fraction_of_shale, K_shale, mu_shale, K_sand, mu_sand):
    fraction_of_sand = 1 - fraction_of_shale
    if method == 'Voigt':
        K_matrix = fraction_of_shale * K_shale + fraction_of_sand * K_sand
        mu_matrix = fraction_of_shale * mu_shale + fraction_of_sand * mu_sand
    elif method == 'Reuss':
        K_matrix = 1 / (fraction_of_shale / K_shale + fraction_of_sand / K_sand)
        mu_matrix = 1 / (fraction_of_shale / mu_shale + fraction_of_sand / mu_sand)
    elif method == 'Hill':
        K_matrix_voigt = fraction_of_shale * K_shale + fraction_of_sand * K_sand
        mu_matrix_voigt = fraction_of_shale * mu_shale + fraction_of_sand * mu_sand
        
        K_matrix_reuss = 1 / (fraction_of_shale / K_shale + fraction_of_sand / K_sand)
        mu_matrix_reuss = 1 / (fraction_of_shale / mu_shale + fraction_of_sand / mu_sand)
        
        K_matrix = (K_matrix_voigt + K_matrix_reuss) / 2
        mu_matrix = (mu_matrix_voigt + mu_matrix_reuss) / 2
    return K_matrix, mu_matrix


def MatrixDensity(fraction_of_shale, rho_shale, rho_sand):
    return fraction_of_shale * rho_shale + (1 - fraction_of_shale) * rho_sand


def velocities(K, mu, rho):
    Vp = np.sqrt((K + 4/3 * mu) / rho)
    Vs = np.sqrt(mu / rho)
    return Vp, Vs


def rescaled(predicted_data, actual_data):
        # Early
        # predicted_hist, bins_predicted = np.histogram(predicted_data, bins='auto', density = True)
        # actual_hist, bins_actual = np.histogram(actual_data, bins='auto', density = True)

        det_bin = 'doane'
        if (det_bin == 'doane'):
            def doanes_rule(data):
                # Panjang data
                n = len(data)
    
                # Menghitung skewness (g1)
                mean = np.mean(data)
                std_dev = np.std(data)
                g1 = np.sum(((data - mean) / std_dev) ** 3) / n
    
                # Menghitung standar error skewness (sigma_g1)
                sigma_g1 = np.sqrt(6 * (n - 2) / ((n + 1) * (n + 3)))
    
                # Menghitung jumlah bin
                k = 1 + np.log2(n) + np.log2(1 + abs(g1) / sigma_g1)
    
                return int(np.round(k))
            
            num_bins_predicted = doanes_rule(predicted_data)
            num_bins_actual = doanes_rule(actual_data)        
        # debug
        print("predicted_data shape:", predicted_data.shape)
        print("actual_data shape:", actual_data.shape)
        print("data type:", predicted_data.dtype)
        print("sample predicted_data:", predicted_data[:5])
        print("sample actual_data:", actual_data[:5])

        predicted_hist, bins_predicted = np.histogram(predicted_data, bins='auto', density = True)
        actual_hist, bins_actual = np.histogram(actual_data, bins=num_bins_actual, density = True)

        # Calculate cumulative distribution functions (CDFs)
        cdf_predicted = np.cumsum(predicted_hist) * np.diff(bins_predicted)
        cdf_actual = np.cumsum(actual_hist) * np.diff(bins_actual)

        # Normalisasi CDF untuk memastikan berada di rentang [0, 1]
        cdf_predicted = cdf_predicted / cdf_predicted[-1]
        cdf_actual = cdf_actual / cdf_actual[-1]        
        
        # Map predicted data to actual data CDF
        predicted_rescaled = np.interp(predicted_data, bins_predicted[:-1], np.interp(cdf_predicted, cdf_actual, bins_actual[:-1]))
        
        return predicted_rescaled


    
import numpy as np
from scipy.interpolate import interp1d

def quantile_match(source_data, target_data, n_quantiles=100):
    """
    Adjust the distribution of source_data to match that of target_data using quantile matching.

    Parameters:
        source_data (array-like): The data to be transformed.
        target_data (array-like): The reference data whose distribution is the target.
        n_quantiles (int): Number of quantiles to use (default: 100).

    Returns:
        np.ndarray: Transformed source_data with matched quantiles.
    """
    source_data = np.asarray(source_data)
    target_data = np.asarray(target_data)
    
    # Compute quantiles
    quantiles = np.linspace(0, 1, n_quantiles)
    source_q = np.quantile(source_data, quantiles)
    target_q = np.quantile(target_data, quantiles)

    # Build interpolation function
    match_func = interp1d(source_q, target_q, bounds_error=False, fill_value="extrapolate")

    # Apply quantile transformation
    matched_data = match_func(source_data)
    return matched_data


def rhob_to_rho_shales(rho_bulk, porosity, water_saturation, rho_hc, rho_water, rho_quartz, volume_of_shale):
    a = rho_bulk 
    b = porosity * (1 - water_saturation) * rho_hc
    c = porosity * water_saturation * rho_water
    d = rho_quartz * (1 - porosity) * (1 - volume_of_shale)
    e = volume_of_shale * (1 - porosity)
    shale_density = (a - b - c - d) / e
    return shale_density

def rho_matrix_to_rho_shales(rho_matrix, rho_quartz, volume_of_shale):
    shale_density = (rho_matrix - (rho_quartz * (1 - volume_of_shale))) / volume_of_shale
    return shale_density

def wyllie_with_vsh(porosity, Vsh, SW, Vp_qtz, Vp_shale, Vp_water, Vp_hc):
    
    
    matrix_component = (1 - porosity) * (((1 - Vsh) / Vp_qtz) + (Vsh / Vp_shale))
    fluid_component = porosity * ((SW / Vp_water) + ((1 - SW) / Vp_hc))
    
    Vp = 1 / (matrix_component + fluid_component)
    return Vp

def Vs_Pranatikta(porosity, Vp_matrix, rho_matrix, rho_bulk, G, alpha, n):
    
    sqrt_part = np.sqrt(((1 - porosity) * rho_matrix )/ rho_bulk)
    Vs_part = G * alpha * Vp_matrix
    porosity_part = (1 - porosity) ** n
    
    Vs = sqrt_part * Vs_part * porosity_part
    return Vs

def rhob(rho_qtz, rho_shale, Vsh):
    rhob = rho_qtz * (1 - Vsh) + rho_shale * Vsh
    return rhob

def Vsh_alip(AI, Vp_quartz, Vp_shale, Vp_water, rho_quartz, rho_shale, rho_water, porosity):

    AI_top = AI * (((1 - porosity) / Vp_quartz) + (porosity / Vp_water))
    rho_top = rho_quartz * (1 - porosity) + rho_water * porosity
    AI_bottom = AI * ((1 / Vp_quartz) - (1 / Vp_shale) - porosity * ((1 / Vp_quartz) - (1 / Vp_shale)))
    rho_bottom = rho_shale - rho_quartz - porosity * (rho_quartz - rho_shale)
    
    Vsh = (AI_top - rho_top) / (AI_bottom + rho_bottom)
    return Vsh

def Vsh_baru(AI, Vp_quartz, Vp_shale, Vp_water, rho_quartz, rho_shale, rho_water, porosity):
    AI_top = AI * ((1 / Vp_quartz) + porosity * ((1 / Vp_quartz) - (1 / Vp_water)))
    rho_top = rho_quartz * (1 - porosity) + rho_water * porosity
    AI_bottom = AI * ((1 / Vp_shale) - (1 / Vp_quartz) + porosity * ((1 / Vp_quartz) - (1 / Vp_shale)))
    rho_bottom = rho_quartz * (1 - porosity) - rho_shale * (1 - porosity)
    Vsh = (AI_top + rho_top) / (AI_bottom + rho_bottom)
    return Vsh