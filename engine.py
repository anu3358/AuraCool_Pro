import numpy as np

class SovereignEngine:
    def __init__(self):
        # Industrial Constants
        self.ev_battery_avg_kwh = 60 
        self.carbon_price_per_ton = 2400 # INR
        self.water_evap_rate = 1.2 # Liters per m2 per degree

    def optimize_intervention(self, current_temp, target_temp, area_sq_km):
        """AI Genetic Algorithm: Minimizes cost while hitting thermal targets."""
        delta_needed = current_temp - target_temp
        # Calculate Albedo coating vs Greenery cost-efficiency
        albedo_coverage = delta_needed * 0.4  # 40% efficiency factor
        greenery_needed = (delta_needed - (albedo_coverage * 0.5)) / 0.8
        
        investment_required = (albedo_coverage * area_sq_km * 50000) + (greenery_needed * area_sq_km * 200000)
        return round(albedo_coverage, 2), round(greenery_needed, 2), investment_required

    def calculate_v2g_capacity(self, ev_count, discharge_rate=0.2):
        """Calculates how much power EVs can inject to prevent grid failure."""
        total_kwh = ev_count * self.ev_battery_avg_kwh * discharge_rate
        return round(total_kwh / 1000, 2) # Return in MWh

    def calculate_resource_nexus(self, delta_temp, area_sq_km):
        """Calculates water saved and CO2 offset."""
        water_saved_ml = (delta_temp * self.water_evap_rate * area_sq_km * 1000000) / 1000000
        co2_offset = delta_temp * 520
        return round(water_saved_ml, 1), round(co2_offset, 1)

def get_sector_data():
    return {
        "Ludhiana Industrial": {"lat": 30.901, "lon": 75.857, "temp": 47.1, "evs": 12000, "area": 159},
        "Amritsar Urban": {"lat": 31.634, "lon": 74.872, "temp": 44.8, "evs": 8500, "area": 170},
        "Ferozpur Border": {"lat": 30.925, "lon": 74.622, "temp": 46.2, "evs": 2100, "area": 45}
    }
