from django.core.exceptions import ValidationError
import re

def validate_frequency(value):
    """
    Validate that the frequency is within a valid range for mobile networks.
    """
    if not (700 <= value <= 2600):
        raise ValidationError(
            f'La fréquence {value} MHz est en dehors de la plage valide pour les réseaux mobiles (700-2600 MHz)'
        )

def validate_antenna_height(value):
    """
    Validate that the antenna height is within a reasonable range.
    """
    if not (3 <= value <= 200):
        raise ValidationError(
            f'La hauteur d\'antenne {value} m est en dehors de la plage valide (3-200 m)'
        )

def validate_antenna_power(value):
    """
    Validate that the antenna power is within a reasonable range.
    """
    if not (10 <= value <= 60):
        raise ValidationError(
            f'La puissance d\'antenne {value} dBm est en dehors de la plage valide (10-60 dBm)'
        )

def validate_coordinates(longitude, latitude):
    """
    Validate that the coordinates are valid.
    """
    if not (-180 <= longitude <= 180):
        raise ValidationError(
            f'La longitude {longitude} est en dehors de la plage valide (-180 à 180)'
        )
    
    if not (-90 <= latitude <= 90):
        raise ValidationError(
            f'La latitude {latitude} est en dehors de la plage valide (-90 à 90)'
        )

def validate_simulation_name(value):
    """
    Validate that the simulation name contains only valid characters.
    """
    if not re.match(r'^[a-zA-Z0-9_\- ]+$', value):
        raise ValidationError(
            'Le nom de la simulation ne peut contenir que des lettres, chiffres, espaces, tirets et underscores'
        )