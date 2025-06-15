# weights_config.py

# Preset weights (example profiles)
weight_profiles = {
    "balanced": {
        "POINT_DIFF_WEIGHT": 0.30,
        "lead_changes_weight": 0.15,
        "comeback_weight": 0.1,
    },
    "drama_lover": {
        "POINT_DIFF_WEIGHT": 0.50,
        "lead_changes_weight": 0.10,
        "comeback_weight": 0.15
    },
    "stat_nerd": {
        "POINT_DIFF_WEIGHT": 0.15,
        "lead_changes_weight": 0.15,
        "comeback_weight": 0.05
    },
    "momentum_swinger": {
        "POINT_DIFF_WEIGHT": 0.10,        
        "lead_changes_weight": 0.45,     
        "comeback_weight": 0.05           
}

}

# Default profile
default_profile = "momentum_swinger"
