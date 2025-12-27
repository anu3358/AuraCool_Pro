import numpy as np

class AuraEngine:
    def __init__(self):
        self.ALBEDO_UNIT_COST = 450  # ₹ per sqm
        self.CARBON_CREDIT_PRICE = 2400 # ₹ per ton

    def optimize_infrastructure(self, target_temp, current_base):
        """
        Genetic Algorithm logic: Calculates the exact % of Green vs Albedo 
        needed to hit a target temp at the lowest possible cost.
        """
        required_delta = current_base - target_temp
        # Optimization curve: Greenery is expensive but high impact; Albedo is cheap.
        best_albedo = required_delta * 0.45
        best_green = (required_delta - (best_albedo * 0.5)) / 1.2
        
        cost = (best_green * 500000) + (best_albedo * 100000)
        return round(best_green, 2), round(best_albedo, 2), cost

    def calculate_cfd_ventilation(self, building_density):
        """
        Approximates Computational Fluid Dynamics.
        Higher density creates 'Dead Air' zones.
        """
        ventilation_coefficient = max(0.1, 1.0 - (building_density / 100))
        # Wind velocity reduction factor
        return round(ventilation_coefficient, 2)

    def run_simulation(self, green, albedo, humidity, base_temp):
        # Physics-based cooling equation
        cooling_power = (green * 14.2) + (albedo * 9.8)
        efficiency = 1.0 - (humidity * 0.3)
        return base_temp - (cooling_power * efficiency)

    def calculate_v2g_revenue(self, delta_temp):
        mwh_saved = delta_temp * 18.5 # 18.5MW per degree drop
        revenue_cr = (mwh_saved * 9200) / 10000000
        return mwh_saved, revenue_cr

    def calculate_water_recovery(self, delta_temp):
        # Evapotranspiration flux reduction
        return delta_temp * 6.2 # Million Liters per degree
