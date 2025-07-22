"""
Modèles de propagation radio pour la 5G

Ce module implémente les modèles de propagation spécifiques à la 5G,
y compris le modèle 3GPP TR 38.901 pour les bandes FR1 et FR2.
"""
import math
import numpy as np
from typing import Literal

class PropagationModel5G:
    """Classe de base pour les modèles de propagation 5G"""
    
    @staticmethod
    def free_space_path_loss(frequency: float, distance: float) -> float:
        """
        Calcule l'affaiblissement en espace libre (FSPL) en dB
        
        Args:
            frequency: Fréquence en Hz
            distance: Distance en mètres
            
        Returns:
            Perte en espace libre en dB
        """
        if frequency <= 0 or distance <= 0:
            raise ValueError("La fréquence et la distance doivent être positives")
            
        # Constante de vitesse de la lumière
        c = 3e8  # m/s
        
        # Longueur d'onde
        wavelength = c / frequency
        
        # Calcul de la perte en espace libre (formule de Friis)
        fspl = 20 * math.log10((4 * math.pi * distance) / wavelength)
        return fspl


class ThreeGPP_TR_38901(PropagationModel5G):
    """
    Implémentation du modèle 3GPP TR 38.901 pour les bandes FR1 et FR2
    
    Référence: 3GPP TR 38.901 V16.1.0 (2019-12)
    """
    
    @classmethod
    def path_loss(
        cls,
        frequency: float,
        distance: float,
        scenario: Literal["UMa", "UMi", "RMa", "InH-Office", "InH-ShoppingMall"],
        los_condition: Literal["LOS", "NLOS"],
        h_bs: float = 10.0,
        h_ut: float = 1.5,
        h: float = 5.0,
        w: float = 20.0,
        h_roof: float = 20.0,
        street_width: float = 20.0,
    ) -> float:
        """
        Calcule la perte de propagation selon le modèle 3GPP TR 38.901
        
        Args:
            frequency: Fréquence en Hz (0.5-100 GHz)
            distance: Distance 2D entre l'émetteur et le récepteur en mètres (10-10000 m)
            scenario: Scénario de déploiement (UMa, UMi, RMa, InH-Office, InH-ShoppingMall)
            los_condition: Condition de visibilité (LOS ou NLOS)
            h_bs: Hauteur de la station de base en mètres (10-150 m)
            h_ut: Hauteur de l'utilisateur en mètres (1-22.5 m)
            h: Hauteur moyenne des bâtiments en mètres (5-50 m)
            w: Largeur moyenne des routes en mètres (5-50 m)
            h_roof: Hauteur moyenne des toits en mètres (5-50 m)
            street_width: Largeur des rues en mètres (5-50 m)
            
        Returns:
            Perte de propagation en dB
        """
        # Vérification des paramètres d'entrée
        if not (0.5e9 <= frequency <= 100e9):
            raise ValueError("La fréquence doit être comprise entre 0.5 et 100 GHz")
            
        if not (10 <= distance <= 10000):
            raise ValueError("La distance doit être comprise entre 10 et 10000 mètres")
            
        # Conversion en GHz pour les formules
        f_ghz = frequency / 1e9
        
        # Calcul de la distance 3D
        d_3d = math.sqrt(distance**2 + (h_bs - h_ut)**2)
        
        # Sélection du modèle en fonction du scénario
        if scenario == "UMa":  # Urban Macro
            if los_condition == "LOS":
                # Calcul de la distance de rupture
                dbp = 4 * h_bs * h_ut * (frequency / 3e8)
                
                if distance < dbp:
                    # Formule pour la région proche (d2D < dbp)
                    pl = 28.0 + 22 * math.log10(d_3d) + 20 * math.log10(f_ghz)
                else:
                    # Formule pour la région éloignée (d2D >= dbp)
                    pl = 28.0 + 40 * math.log10(d_3d) + 20 * math.log10(f_ghz) - 9 * math.log10(dbp**2 + (h_bs - h_ut)**2)
            else:  # NLOS
                # Calcul de la perte en LOS d'abord
                pl_los = cls.path_loss(frequency, distance, "UMa", "LOS", h_bs, h_ut)
                
                # Calcul de la perte en NLOS
                pl_nlos = 13.54 + 39.08 * math.log10(d_3d) + 20 * math.log10(f_ghz) - 0.6 * (h_ut - 1.5)
                
                # Prendre le maximum entre LOS et NLOS
                pl = max(pl_los, pl_nlos)
                
        elif scenario == "UMi":  # Urban Micro
            if los_condition == "LOS":
                pl = 32.4 + 21 * math.log10(d_3d) + 20 * math.log10(f_ghz)
            else:  # NLOS
                pl_los = 32.4 + 21 * math.log10(d_3d) + 20 * math.log10(f_ghz)
                pl_nlos = 35.3 * math.log10(d_3d) + 22.4 + 21.3 * math.log10(f_ghz) - 0.3 * (h_ut - 1.5)
                pl = max(pl_los, pl_nlos)
                
        elif scenario == "RMa":  # Rural Macro
            if los_condition == "LOS":
                # Calcul de la distance de rupture
                dbp = 2 * math.pi * h_bs * h_ut * (frequency / 3e8)
                
                if distance < 10:
                    pl = cls.free_space_path_loss(frequency, 10) + 10 * 2.1 * math.log10(distance/10)
                elif 10 <= distance <= dbp:
                    pl = cls.free_space_path_loss(frequency, distance) + 10 * 2.1 * math.log10(distance/10)
                else:  # distance > dbp
                    pl = cls.free_space_path_loss(frequency, dbp) + 10 * 2.1 * math.log10(dbp/10) + 40 * math.log10(distance/dbp)
            else:  # NLOS
                pl_los = cls.path_loss(frequency, distance, "RMa", "LOS", h_bs, h_ut)
                pl_nlos = 161.04 - 7.1 * math.log10(w) + 7.5 * math.log10(h) - (24.37 - 3.7 * (h/h_bs)**2) * math.log10(h_bs) + \
                         (43.42 - 3.1 * math.log10(h_bs)) * (math.log10(d_3d) - 3) + 20 * math.log10(f_ghz) - \
                         (3.2 * (math.log10(11.75 * h_ut))**2 - 4.97)
                pl = max(pl_los, pl_nlos)
                
        elif scenario == "InH-Office":  # Indoor Hotspot - Office
            if los_condition == "LOS":
                pl = 32.4 + 17.3 * math.log10(d_3d) + 20 * math.log10(f_ghz)
            else:  # NLOS
                pl_los = 32.4 + 17.3 * math.log10(d_3d) + 20 * math.log10(f_ghz)
                pl_nlos = 38.3 * math.log10(d_3d) + 17.3 + 24.9 * math.log10(f_ghz)
                pl = max(pl_los, pl_nlos)
                
        elif scenario == "InH-ShoppingMall":  # Indoor Hotspot - Shopping Mall
            if los_condition == "LOS":
                pl = 32.4 + 17.3 * math.log10(d_3d) + 20 * math.log10(f_ghz)
            else:  # NLOS
                pl_los = 32.4 + 17.3 * math.log10(d_3d) + 20 * math.log10(f_ghz)
                pl_nlos = 42.7 * math.log10(d_3d) + 11.3 + 20 * math.log10(f_ghz)
                pl = max(pl_los, pl_nlos)
                
        else:
            raise ValueError(f"Scénario {scenario} non pris en charge. Choisissez parmi: UMa, UMi, RMa, InH-Office, InH-ShoppingMall")
        
        return pl


class MillimeterWavePropagation(PropagationModel5G):
    """
    Modèle de propagation pour les ondes millimétriques (mmWave)
    
    Ce modèle est adapté pour les fréquences au-dessus de 24 GHz (FR2)
    """
    
    @classmethod
    def path_loss(
        cls,
        frequency: float,
        distance: float,
        los_condition: Literal["LOS", "NLOS"],
        material_attenuation: float = 0.0,
    ) -> float:
        """
        Calcule la perte de propagation pour les ondes millimétriques
        
        Args:
            frequency: Fréquence en Hz (24-100 GHz)
            distance: Distance en mètres
            los_condition: Condition de visibilité (LOS ou NLOS)
            material_attenuation: Atténuation supplémentaire due aux matériaux (dB/m)
            
        Returns:
            Perte de propagation en dB
        """
        if not (24e9 <= frequency <= 100e9):
            raise ValueError("La fréquence doit être comprise entre 24 et 100 GHz pour les ondes mmWave")
            
        # Perte en espace libre
        fspl = cls.free_space_path_loss(frequency, distance)
        
        # Facteur d'atténuation supplémentaire pour NLOS
        nlos_penalty = 0 if los_condition == "LOS" else 20
        
        # Atténuation due aux matériaux
        material_loss = material_attenuation * distance
        
        # Perte totale
        total_loss = fspl + nlos_penalty + material_loss
        
        return total_loss


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple d'utilisation du modèle 3GPP TR 38.901
    frequency = 3.5e9  # 3.5 GHz (bande moyenne 5G)
    distance = 200  # mètres
    
    # Calcul de la perte de propagation pour différents scénarios
    model = ThreeGPP_TR_38901()
    
    # Scénario UMa (Urban Macro) en condition LOS
    pl_uma_los = model.path_loss(frequency, distance, "UMa", "LOS")
    print(f"Perte de propagation (UMa, LOS): {pl_uma_los:.2f} dB")
    
    # Scénario UMa en condition NLOS
    pl_uma_nlos = model.path_loss(frequency, distance, "UMa", "NLOS")
    print(f"Perte de propagation (UMa, NLOS): {pl_uma_nlos:.2f} dB")
    
    # Exemple pour les ondes millimétriques
    mmwave_model = MillimeterWavePropagation()
    pl_mmwave = mmwave_model.path_loss(28e9, 100, "LOS")
    print(f"Perte de propagation (mmWave, 28 GHz, LOS): {pl_mmwave:.2f} dB")
