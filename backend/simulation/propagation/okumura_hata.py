import math

def calculate_path_loss(frequency, antenna_height, mobile_height, distance, area_type):
    """
    Calculate path loss using the Okumura-Hata model.
    
    Parameters:
    - frequency: Frequency in MHz (150-1500 MHz)
    - antenna_height: Base station antenna height in meters (30-200m)
    - mobile_height: Mobile antenna height in meters (1-10m)
    - distance: Distance in kilometers (1-20km)
    - area_type: 'URBAN', 'SUBURBAN', 'RURAL', or 'OPEN'
    
    Returns:
    - Path loss in dB
    """
    # Validate input parameters
    if not (150 <= frequency <= 1500):
        raise ValueError("Frequency must be between 150 and 1500 MHz")
    if not (30 <= antenna_height <= 200):
        raise ValueError("Antenna height must be between 30 and 200 meters")
    if not (1 <= mobile_height <= 10):
        raise ValueError("Mobile height must be between 1 and 10 meters")
    if not (1 <= distance <= 20):
        raise ValueError("Distance must be between 1 and 20 kilometers")
    
    # Calculate mobile antenna height correction factor
    if frequency < 300:
        # For small/medium-sized city
        mobile_correction = 8.29 * (math.log10(1.54 * mobile_height))**2 - 1.1
    else:
        # For large city
        mobile_correction = 3.2 * (math.log10(11.75 * mobile_height))**2 - 4.97
    
    # Calculate basic path loss for urban areas
    L_urban = 69.55 + 26.16 * math.log10(frequency) - 13.82 * math.log10(antenna_height) - mobile_correction + (44.9 - 6.55 * math.log10(antenna_height)) * math.log10(distance)
    
    # Adjust for different area types
    if area_type == 'URBAN':
        return L_urban
    elif area_type == 'SUBURBAN':
        return L_urban - 2 * (math.log10(frequency/28))**2 - 5.4
    elif area_type == 'RURAL':
        return L_urban - 4.78 * (math.log10(frequency))**2 + 18.33 * math.log10(frequency) - 40.94
    elif area_type == 'OPEN':
        return L_urban - 4.78 * (math.log10(frequency))**2 + 18.33 * math.log10(frequency) - 40.94 - 10
    else:
        raise ValueError("Invalid area type. Must be 'URBAN', 'SUBURBAN', 'RURAL', or 'OPEN'")

def calculate_coverage_radius(frequency, antenna_height, antenna_power, receiver_sensitivity, area_type, mobile_height=1.5):
    """
    Calculate the maximum coverage radius for a given antenna configuration.
    
    Parameters:
    - frequency: Frequency in MHz
    - antenna_height: Base station antenna height in meters
    - antenna_power: Transmitter power in dBm
    - receiver_sensitivity: Minimum receiver sensitivity in dBm (negative value)
    - area_type: 'URBAN', 'SUBURBAN', 'RURAL', or 'OPEN'
    - mobile_height: Mobile antenna height in meters (default 1.5m)
    
    Returns:
    - Maximum coverage radius in kilometers
    """
    # Maximum allowed path loss
    max_path_loss = antenna_power - receiver_sensitivity
    
    # Binary search to find the maximum distance
    min_distance = 1  # km
    max_distance = 20  # km
    
    while max_distance - min_distance > 0.01:
        mid_distance = (min_distance + max_distance) / 2
        path_loss = calculate_path_loss(frequency, antenna_height, mobile_height, mid_distance, area_type)
        
        if path_loss <= max_path_loss:
            min_distance = mid_distance
        else:
            max_distance = mid_distance
    
    return min_distance