
import numpy as np


def FluidSaturation(rho_matrix, rho_fluid, rho_water, Vp_matrix, Vp_fluid, Vp_water, porosity, AI):
    a = rho_matrix
    b = porosity * (rho_water - rho_matrix)
    c = AI * ((1 / Vp_matrix) + porosity * ((1 / Vp_water) - (1 / Vp_matrix)))
    d = porosity * (AI * ((1 / Vp_fluid) - (1 / Vp_water)) - (rho_fluid - rho_water))

    return (a + b - c) / d


def porosityKrishna(Vp_matrix, Vs_saturated, rho_saturated, rho_matrix, alpha, G, N):
    a = (Vs_saturated ** 2) * rho_saturated
    b = (alpha ** 2) * (G ** 2) * (Vp_matrix ** 2) * rho_matrix
    c = 1 / (2 * N + 1)

    porosity = 1 - ((a / b) ** c)

    return porosity


def wyllie_with_vsh(porosity, Vsh, SW, Vp_qtz, Vp_shale, Vp_water, Vp_hc):
    matrix_component = (1 - porosity) * (((1 - Vsh) / Vp_qtz) + (Vsh / Vp_shale))
    fluid_component = porosity * ((SW / Vp_water) + ((1 - SW) / Vp_hc))

    Vp = 1 / (matrix_component + fluid_component)
    return Vp
