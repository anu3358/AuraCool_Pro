import numpy as np

class SovereignEngine:
    def __init__(self):
        # Industrial Constants - The "Math of Winning"
        self.ev_battery_avg_kwh = 60 
        self.carbon_price_per_ton = 28.50 # USD
        self.water_evap_rate = 1.26 # Liters per m2 per degree reduction

    def optimize_intervention(self, current_temp, target_temp, area_sq_km):
        """AI Optimizer: Calculates the most cost-effective cooling strategy."""
        delta_needed = max(0, current_temp - target_temp)
        
        # Coefficients based on Punjab's semi-arid urban climate
        albedo_coverage = delta_needed * 0.42  
        greenery_needed = (delta_needed - (albedo_coverage * 0.55)) / 0.85
        
        # Economic modeling (CAPEX in INR)
        # Albedo coating is cheap/fast; Urban Forestry is expensive/long-term
        cost = (albedo_coverage * area_sq_km * 62000) + (greenery_needed * area_sq_km * 245000)
        return round(albedo_coverage, 2), round(greenery_needed, 2), cost

    def calculate_v2g_impact(self, ev_count):
        """Virtual Power Plant (VPP) Logic."""
        # Assume 20% of the fleet is plugged in and ready to discharge during peak heat
        total_mwh = (ev_count * self.ev_battery_avg_kwh * 0.20) / 1000
        return round(total_mwh, 2)

    def calculate_nexus_savings(self, delta_temp, area_sq_km):
        """The 'Problem Solver': Water and Carbon recovery."""
        # Saving water for agriculture by reducing urban 'heat-thirst'
        water_saved_ml = (delta_temp * self.water_evap_rate * area_sq_km * 1000) / 1000
        co2_tons = delta_temp * area_sq_km * 12.5
        return round(water_saved_ml, 2), round(co2_tons, 1)

def get_sector_data():
    """Strategic Baseline Data for Punjab Districts."""
    return {
        "Ludhiana Central": {"lat": 30.901, "lon": 75.857, "temp": 47.1, "evs": 14500, "area": 159},
        "Amritsar Heritage": {"lat": 31.634, "lon": 74.872, "temp": 44.8, "evs": 9200, "area": 170},
        "Ferozpur Industrial": {"lat": 30.925, "lon": 74.622, "temp": 46.2, "evs": 3400, "area": 45},
        "Gurdaspur Sector": {"lat": 32.041, "lon": 75.405, "temp": 42.5, "evs": 2800, "area": 136}
    }
