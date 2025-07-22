from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import folium
import selenium
from selenium import webdriver
from PIL import Image
from folium.plugins import HeatMap
import tempfile
import os
import time
from django.conf import settings
import matplotlib.pyplot as plt
import numpy as np
import json

def generate_pdf_report(simulation):
    """
    Generate a PDF report for a simulation.
    
    Parameters:
    - simulation: Simulation object
    
    Returns:
    - PDF file as BytesIO object
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title_style = styles['Heading1']
    title = Paragraph(f"Rapport de Simulation: {simulation.name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Description
    if simulation.description:
        desc_style = styles['Normal']
        desc = Paragraph(f"Description: {simulation.description}", desc_style)
        elements.append(desc)
        elements.append(Spacer(1, 12))
    
    # Simulation Parameters
    elements.append(Paragraph("Paramètres de Simulation", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    params = simulation.parameters.first()
    if params:
        param_data = [
            ["Paramètre", "Valeur"],
            ["Technologie", params.get_technology_display()],
            ["Modèle de propagation", params.get_propagation_model_display()],
            ["Fréquence", f"{params.frequency} MHz"],
            ["Hauteur d'antenne", f"{params.antenna_height} m"],
            ["Puissance d'antenne", f"{params.antenna_power} dBm"],
            ["Type de terrain", params.get_terrain_type_display()],
            ["Coordonnées", f"Lon: {params.location.x}, Lat: {params.location.y}"],
            ["Rayon", f"{params.radius} km"],
        ]
        
        if params.population_density:
            param_data.append(["Densité de population", f"{params.population_density} hab/km²"])
        
        param_table = Table(param_data, colWidths=[200, 300])
        param_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(param_table)
        elements.append(Spacer(1, 12))
    
    # Simulation Results
    elements.append(Paragraph("Résultats de Simulation", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    result = simulation.results.first()
    if result:
        result_data = [
            ["Métrique", "Valeur"],
            ["Pourcentage de couverture", f"{result.coverage_percentage:.2f}%"],
        ]
        
        if result.population_covered:
            result_data.append(["Population couverte", f"{result.population_covered} habitants"])
        
        result_table = Table(result_data, colWidths=[200, 300])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(result_table)
        elements.append(Spacer(1, 12))
        
        # Generate coverage map
        if result.signal_strength_data:
            elements.append(Paragraph("Carte de Couverture", styles['Heading2']))
            elements.append(Spacer(1, 6))
            
            # Create a coverage map using matplotlib
            try:
                map_image = create_coverage_map(params, result)
                elements.append(map_image)
                elements.append(Spacer(1, 12))
            except Exception as e:
                elements.append(Paragraph(f"Erreur lors de la génération de la carte: {str(e)}", styles['Normal']))
                elements.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_coverage_map(params, result):
    """
    Create a coverage map image for the PDF report.
    
    Parameters:
    - params: SimulationParameter object
    - result: SimulationResult object
    
    Returns:
    - Image object for the PDF
    """
    # Create a temporary file for the map image
    temp_html=tempfile.NamedTemporaryFile(suffix='.html', delete=False).name
    #temp_html = os.path.join(os.getcwd(), "test_map.html")
    temp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    
    # Create a map centered at the antenna location
    m = folium.Map(
        location=[params.location.y, params.location.x],
        zoom_start=12,
        tiles='CartoDB positron'
    )
    
    # Add antenna marker
    folium.Marker(
        [params.location.y, params.location.x],
        popup=f"Antenne {params.get_technology_display()}",
        icon=folium.Icon(color='red', icon='antenna', prefix='fa')
    ).add_to(m)
    
    # Add coverage circles
    signal_data = result.signal_strength_data
    
    # Group signal strengths into categories
    excellent = []
    good = []
    fair = []
    poor = []
    
    for coord, signal in signal_data.items():
        if isinstance(coord, str):
            lon, lat = map(float, coord.split(','))
        else:
            lon, lat = coord
        #lon, lat = map(float, coord.split(','))
        if signal >= -70:
            excellent.append([lat, lon])
        elif signal >= -85:
            good.append([lat, lon])
        elif signal >= -100:
            fair.append([lat, lon])
        else:
            poor.append([lat, lon])
    
    # Add heatmap layers
    if excellent:
        HeatMap(
            excellent,
            radius=15,
            gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'},
            min_opacity=0.5,
            max_val=1.0,
            blur=10
        ).add_to(m)
    
    if good:
        HeatMap(
            good,
            radius=12,
            gradient={0.4: 'green', 0.65: 'yellow', 1: 'red'},
            min_opacity=0.3,
            max_val=0.8,
            blur=15
        ).add_to(m)
    
    if fair:
        HeatMap(
            fair,
            radius=10,
            gradient={0.4: 'blue', 0.65: 'purple', 1: 'red'},
            min_opacity=0.2,
            max_val=0.6,
            blur=20
        ).add_to(m)
        
    from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import folium
import selenium
from selenium import webdriver
from PIL import Image
from folium.plugins import HeatMap
import tempfile
import os
import time
from django.conf import settings
import matplotlib.pyplot as plt
import numpy as np
import json

def generate_pdf_report(simulation):
    """
    Generate a PDF report for a simulation.
    
    Parameters:
    - simulation: Simulation object
    
    Returns:
    - PDF file as BytesIO object
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title_style = styles['Heading1']
    title = Paragraph(f"Rapport de Simulation: {simulation.name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Description
    if simulation.description:
        desc_style = styles['Normal']
        desc = Paragraph(f"Description: {simulation.description}", desc_style)
        elements.append(desc)
        elements.append(Spacer(1, 12))
    
    # Simulation Parameters
    elements.append(Paragraph("Paramètres de Simulation", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    params = simulation.parameters.first()
    if params:
        param_data = [
            ["Paramètre", "Valeur"],
            ["Technologie", params.get_technology_display()],
            ["Modèle de propagation", params.get_propagation_model_display()],
            ["Fréquence", f"{params.frequency} MHz"],
            ["Hauteur d'antenne", f"{params.antenna_height} m"],
            ["Puissance d'antenne", f"{params.antenna_power} dBm"],
            ["Type de terrain", params.get_terrain_type_display()],
            ["Coordonnées", f"Lon: {params.location.x}, Lat: {params.location.y}"],
            ["Rayon", f"{params.radius} km"],
        ]
        
        if params.population_density:
            param_data.append(["Densité de population", f"{params.population_density} hab/km²"])
        
        param_table = Table(param_data, colWidths=[200, 300])
        param_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(param_table)
        elements.append(Spacer(1, 12))
    
    # Simulation Results
    elements.append(Paragraph("Résultats de Simulation", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    result = simulation.results.first()
    if result:
        result_data = [
            ["Métrique", "Valeur"],
            ["Pourcentage de couverture", f"{result.coverage_percentage:.2f}%"],
        ]
        
        if result.population_covered:
            result_data.append(["Population couverte", f"{result.population_covered} habitants"])
        
        result_table = Table(result_data, colWidths=[200, 300])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(result_table)
        elements.append(Spacer(1, 12))
        
        # Generate coverage map
        if result.signal_strength_data:
            elements.append(Paragraph("Carte de Couverture", styles['Heading2']))
            elements.append(Spacer(1, 6))
            
            # Create a coverage map using matplotlib
            try:
                map_image = create_coverage_map(params, result)
                elements.append(map_image)
                elements.append(Spacer(1, 12))
            except Exception as e:
                elements.append(Paragraph(f"Erreur lors de la génération de la carte: {str(e)}", styles['Normal']))
                elements.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_coverage_map(params, result):
    """
    Create a coverage map image for the PDF report.
    
    Parameters:
    - params: SimulationParameter object
    - result: SimulationResult object
    
    Returns:
    - Image object for the PDF
    """
    # Create a temporary file for the map image
    temp_html=tempfile.NamedTemporaryFile(suffix='.html', delete=False).name
    #temp_html = os.path.join(os.getcwd(), "test_map.html")
    temp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    
    # Create a map centered at the antenna location
    m = folium.Map(
        location=[params.location.y, params.location.x],
        zoom_start=12,
        tiles='CartoDB positron'
    )
    
    # Add antenna marker
    folium.Marker(
        [params.location.y, params.location.x],
        popup=f"Antenne {params.get_technology_display()}",
        icon=folium.Icon(color='red', icon='antenna', prefix='fa')
    ).add_to(m)
    
    # Add coverage circles
    signal_data = result.signal_strength_data
    
    # Group signal strengths into categories
    excellent = []
    good = []
    fair = []
    poor = []
    
    for coord, signal in signal_data.items():
        if isinstance(coord, str):
            lon, lat = map(float, coord.split(','))
        else:
            lon, lat = coord
        #lon, lat = map(float, coord.split(','))
        if signal >= -70:
            excellent.append([lat, lon])
        elif signal >= -85:
            good.append([lat, lon])
        elif signal >= -100:
            fair.append([lat, lon])
        else:
            poor.append([lat, lon])
    
    # Add heatmap layers
    if excellent:
        HeatMap(
            excellent,
            radius=15,
            gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'},
            min_opacity=0.5,
            max_val=1.0,
            blur=10
        ).add_to(m)
    
    if good:
        HeatMap(
            good,
            radius=12,
            gradient={0.4: 'green', 0.65: 'yellow', 1: 'red'},
            min_opacity=0.3,
            max_val=0.8,
            blur=15
        ).add_to(m)
    
    if fair:
        HeatMap(
            fair,
            radius=10,
            gradient={0.4: 'blue', 0.65: 'purple', 1: 'red'},
            min_opacity=0.2,
            max_val=0.6,
            blur=20
        ).add_to(m)
        
    m.save(temp_html)
    # Vérification que le fichier HTML existe bien
    if not os.path.exists(temp_html) or os.path.getsize(temp_html) == 0:
        raise RuntimeError(f"Le fichier HTML {temp_html} est vide ou inexistant !")
    else:
        print(f"Fichier HTML généré : {temp_html}, Taille : {os.path.getsize(temp_html)} octets")
    
    # Capturer l'image avec Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200x800")

    driver = webdriver.Chrome(options=options)
    driver.get("file://" + temp_html)

    # Attendre le rendu de la carte
    time.sleep(99)

    driver.save_screenshot(temp_png)
    driver.quit()

    # Vérifier que l'image est bien enregistrée
    img = Image.open(temp_png)
    img.save(temp_png, format="PNG")

    # Retourner l'image pour ReportLab
    return ReportLabImage(temp_png, width=500, height=300)
    
    # Capturer l'image avec Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200x800")

    driver = webdriver.Chrome(options=options)
    driver.get("file://" + temp_html)

    # Attendre le rendu de la carte
    time.sleep(99)

    driver.save_screenshot(temp_png)
    driver.quit()

    # Vérifier que l'image est bien enregistrée
    img = Image.open(temp_png)
    img.save(temp_png, format="PNG")

    # Retourner l'image pour ReportLab
    return ReportLabImage(temp_png, width=500, height=300)