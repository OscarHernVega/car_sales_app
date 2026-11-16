import pandas as pd
import plotly.graph_objects as go  # Importación de plotly.graph_objects como go
import streamlit as st

# Leer los datos del archivo CSV
car_data = pd.read_csv('new_vehicles.csv')

vehicle_counts = car_data.groupby(
    ['manufacturer', 'type']).size().reset_index(name='count')
manufacturer_order = (
    car_data['manufacturer']
    .value_counts()
    .index.tolist()
)


st.header('Información de vehiculos nuevos del concesionario')

# Visualizador de datos
less_than_1000 = st.checkbox('Incluye fabricantes con menos de 1000 entradas')

if less_than_1000:
    manufacturer_counts = car_data['manufacturer'].value_counts()

    selected_manufacturers = manufacturer_counts[manufacturer_counts < 1000].index

    filtered_data = car_data[car_data['manufacturer'].isin(
        selected_manufacturers)]
else:
    filtered_data = car_data

st.dataframe(filtered_data, use_container_width=True)

# diagrama de barras
fig = go.Figure()

for vehicle_type in vehicle_counts['type'].unique():

    data = vehicle_counts[vehicle_counts['type'] == vehicle_type]

    fig.add_trace(go.Bar(
        x=data['manufacturer'],
        y=data['count'],
        name=vehicle_type
    ))

fig.update_layout(
    title='Vehicle types by manufacturer',
    xaxis_title='Manufacturer',
    yaxis_title='Count',
    barmode='stack',
    xaxis_tickangle=-90
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Vehicle types by manufacturer")

st.plotly_chart(fig, use_container_width=True)
# Crear un botón en la aplicación Streamlit
hist_button = st.button('Construir histograma')
scatter_button = st.button('Construir gráfico de dispersión')

# Lógica a ejecutar cuando se hace clic en el botón
if hist_button:
    # Escribir un mensaje en la aplicación
    st.write(
        'Creación de un histograma para el conjunto de datos de anuncios de venta de coches')

    # Crear un histograma utilizando plotly.graph_objects
    # Se crea una figura vacía y luego se añade un rastro de histograma
    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])

    # Opcional: Puedes añadir un título al gráfico si lo deseas
    fig.update_layout(title_text='Distribución del Odómetro')

    # Mostrar el gráfico Plotly interactivo en la aplicación Streamlit
    # 'use_container_width=True' ajusta el ancho del gráfico al contenedor
    st.plotly_chart(fig, use_container_width=True)


if scatter_button:

    st.write(
        'Creación de un gráfico de dispersión que muestra año del modelo y precio')

    fig = go.Figure(data=[go.Scatter(
        x=car_data['model_year'], y=car_data['price'], mode='markers')])

    fig.update_layout(title_text='Año del modelo vs precio')

    st.plotly_chart(fig, use_container_width=True)
