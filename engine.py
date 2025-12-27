import numpy as np

class SovereignEngine:
    def __init__(self):
        self.ev_battery_avg_kwh = 60 
        self.water_evap_rate = 1.28  
        self.carbon_credit_value = 2850 

    def optimize_intervention(self, current_temp, target_temp, area_sq_km):
        delta_needed = max(0, current_temp - target_temp)
        albedo_coverage = delta_needed * 0.40  
        greenery_needed = (delta_needed - (albedo_coverage * 0.50)) / 0.82
        cost = (albedo_coverage * area_sq_km * 65000) + (greenery_needed * area_sq_km * 260000)
        return round(albedo_coverage, 2), round(greenery_needed, 2), cost

    def calculate_v2g_impact(self, ev_count):
        total_mwh = (ev_count * self.ev_battery_avg_kwh * 0.20) / 1000
        return round(total_mwh, 2)

    def calculate_nexus_savings(self, delta_temp, area_sq_km):
        water_saved_ml = (delta_temp * self.water_evap_rate * area_sq_km * 1000) / 1000
        co2_tons = delta_temp * area_sq_km * 14.2
        return round(water_saved_ml, 2), round(co2_tons, 1)

    def calculate_labor_protection(self, temp, humidity=0.48):
        wbgt = (0.7 * (temp * humidity)) + (0.3 * temp)
        if wbgt > 32.5:
            return "🔴 CRITICAL", "0 min/hr", "Fatal heat exposure risk."
        elif wbgt > 30.5:
            return "🟠 EXTREME", "15 min/hr", "Mandatory shade breaks."
        return "🟢 STABLE", "60 min/hr", "Safe operational capacity."

def get_sector_data():
    return {
        "Gurdaspur (Border Zone)": {"lat": 32.041, "lon": 75.405, "temp": 42.8, "evs": 4200, "area": 136},
        "Ludhiana (Industrial Hub)": {"lat": 30.901, "lon": 75.857, "temp": 47.1, "evs": 15800, "area": 159},
        "Amritsar (Heritage Core)": {"lat": 31.634, "lon": 74.872, "temp": 44.2, "evs": 9800, "area": 170},
        "Ferozpur (Agri-Sector)": {"lat": 30.925, "lon": 74.622, "temp": 46.5, "evs": 3100, "area": 45}
    }
