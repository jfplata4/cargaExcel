import pandas as pd
from django.http import HttpResponse
import matplotlib
matplotlib.use('Agg')  # Usa un backend no interactivo para evitar la GUI
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render

# Función para exportar una plantilla de Excel con tres categorías
def export_template_excel(request):
    # Datos de ejemplo para la plantilla de Excel
    data = {
        'Categoría': ['Categoría 1', 'Categoría 2', 'Categoría 3'],
        'Demanda': [0, 0, 0],
        'Inventario': [0, 0, 0],
        'Producción': [0, 0, 0]
    }
    df = pd.DataFrame(data)
    
    # Configuración de respuesta para la descarga
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="plantilla_datos.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    
    return response

def upload_excel(request):
    if request.method == 'POST':
        # Verificar si se cargó un archivo Excel o se ingresaron datos manuales
        if 'file' in request.FILES:
            # Procesar archivo de Excel
            file = request.FILES['file']
            df = pd.read_excel(file)
            
            # Verifica las columnas del archivo
            expected_columns = {'Categoría', 'Demanda', 'Inventario', 'Producción'}
            if not expected_columns.issubset(df.columns):
                return HttpResponse("El archivo Excel no tiene las columnas correctas.")
            
            # Verifica que los datos no estén vacíos
            if df.empty or df.isnull().values.any():
                return HttpResponse("El archivo Excel no contiene datos válidos.")
            
        else:
            # Procesar datos del formulario manual
            categorias = [
                request.POST['categoria_1'], request.POST['categoria_2'], request.POST['categoria_3']
            ]
            demandas = [
                int(request.POST['demanda_1']), int(request.POST['demanda_2']), int(request.POST['demanda_3'])
            ]
            inventarios = [
                int(request.POST['inventario_1']), int(request.POST['inventario_2']), int(request.POST['inventario_3'])
            ]
            producciones = [
                int(request.POST['produccion_1']), int(request.POST['produccion_2']), int(request.POST['produccion_3'])
            ]
            
            # Crear un DataFrame con los datos ingresados manualmente
            df = pd.DataFrame({
                'Categoría': categorias,
                'Demanda': demandas,
                'Inventario': inventarios,
                'Producción': producciones
            })

        # Genera el gráfico y lo pasa como contexto a la plantilla
        graphic_data = generar_grafico(df)
        return render(request, 'grouped_bar_chart.html', {'graphic': graphic_data})
    
    return render(request, 'grouped_bar_chart.html')

# Función para generar el gráfico en base64
def generar_grafico(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Verifica que haya datos antes de graficar
    if not df.empty:
        df.plot(x='Categoría', y=['Demanda', 'Inventario', 'Producción'], kind='bar', ax=ax)
    
    # Guarda la figura en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close(fig)
    return graphic_data
