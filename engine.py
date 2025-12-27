import numpy as np

class SovereignEngine:
    def __init__(self):
        # Industrial Constants - Essential for ROI calculations
        self.ev_battery_avg_kwh = 60 
        self.carbon_price_per_ton = 2400  # INR
        self.water_evap_rate = 1.2        # Liters per m2 per degree

    def optimize_intervention(self, current_temp, target_temp, area_sq_km):
        """AI Optimization: Finds the most cost-effective cooling mix."""
        delta_needed = max(0, current_temp - target_temp)
        
        # Engineering coefficients for Punjab's urban morphology
        albedo_coverage = delta_needed * 0.45  
        greenery_needed = (delta_needed - (albedo_coverage * 0.6)) / 0.9
        
        # Calculate cost in INR (55k per unit Albedo, 220k per unit Greenery)
        investment_required = (albedo_coverage * area_sq_km * 55000) + (greenery_needed * area_sq_km * 220000)
        return round(albedo_coverage, 2), round(greenery_needed, 2), investment_required

    def calculate_v2g_capacity(self, ev_count):
        """Decentralized Grid Storage logic."""
        total_kwh = ev_count * self.ev_battery_avg_kwh * 0.25 
        return round(total_kwh / 1000, 2) # MWh

    def calculate_resource_nexus(self, delta_temp, area_sq_km):
        """Water and Carbon impact modeling."""
        water_saved_ml = (delta_temp * self.water_evap_rate * area_sq_km * 1000000) / 1000000
        co2_offset = delta_temp * 580
        return round(water_saved_ml, 1), round(co2_offset, 1)

def get_sector_data():
    return {
        "Ludhiana Industrial": {"lat": 30.901, "lon": 75.857, "temp": 47.1, "evs": 12000, "area": 159},
        "Amritsar Urban": {"lat": 31.634, "lon": 74.872, "temp": 44.8, "evs": 8500, "area": 170},
        "Ferozpur Border": {"lat": 30.925, "lon": 74.622, "temp": 46.2, "evs": 2100, "area": 45}
    }
