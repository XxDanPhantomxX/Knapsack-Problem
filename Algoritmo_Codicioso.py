import pandas as pd
import altair as alt
import streamlit as st

default_csv_data = {
    'Indice': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Peso': [62, 40, 77, 56, 22, 79, 71, 63, 39, 23],
    'Valor': [34, 79, 66, 32, 33, 43, 20, 42, 40, 80]
}

def knapsack_greedy(weights, values, capacity):
    index = list(range(len(values)))
    ratio = [v/w for v, w in zip(values, weights)]
    index.sort(key=lambda i: ratio[i], reverse=True)

    max_value = 0
    selected_items = []
    total_weight = 0

    for i in index:
        if total_weight + weights[i] <= capacity:
            selected_items.append(i)
            total_weight += weights[i]
            max_value += values[i]

    return selected_items, max_value, total_weight

def calcular(data, capacidad_maxima):
    weights = data['Peso'].tolist()
    values = data['Valor'].tolist()
    selected_items, max_value, total_weight = knapsack_greedy(weights, values, capacidad_maxima)
    st.subheader("Resultados de la Optimización")
    st.write(f"Valor máximo obtenido: {max_value}")
    st.write(f"Peso total utilizado: {total_weight}")
    st.write("Ítems seleccionados:")
    for i in selected_items:
        st.write(f"Ítem {i+1}: Peso = {weights[i]}, Valor = {values[i]}")
        
    # Visualización interactiva con Altair
    df_plot = pd.DataFrame({
        "Indice": data['Indice'] if 'Indice' in data.columns else pd.Series(range(1, len(values)+1)),
        "Peso": weights,
        "Valor": values,
        "Seleccionado": [i in selected_items for i in range(len(values))]
    })
    return df_plot, max_value, total_weight

def visualizar (df_plot, total_weight=None, capacidad_maxima_value=None):
    highlight = alt.selection_point(on='mouseover', fields=['Indice'], empty=True)
    chart = (
        alt.Chart(df_plot, title='Visualización de Ítems Seleccionados')
        .mark_bar()
        .encode(
            x=alt.X('Indice:O', title='Ítems'),
            y=alt.Y('Valor:Q', title='Valor'),
            color=alt.condition("datum.Seleccionado == true", alt.value('#f58518'), alt.value('#4c78a8')),
            tooltip=[
                alt.Tooltip('Indice:O', title='Ítem'),
                alt.Tooltip('Valor:Q', title='Valor'),
                alt.Tooltip('Peso:Q', title='Peso'),
                alt.Tooltip('Seleccionado:N', title='Seleccionado')
            ],
            opacity=alt.condition(highlight, alt.value(1), alt.value(0.9))
        )
        .add_selection(highlight)
        .interactive()
    )
    st.subheader("Visualización")
    st.altair_chart(chart, use_container_width=True)
    # Barra de progreso que muestra espacio disponible (capacidad - peso utilizado)
    if total_weight is not None and capacidad_maxima_value is not None and capacidad_maxima_value > 0:
        espacio_disponible = max(capacidad_maxima_value - total_weight, 0)
        pct_disponible = espacio_disponible / capacidad_maxima_value
        # Mostrar barra de progreso (0..1) y texto con detalles
        st.write(f"Espacio disponible: {espacio_disponible} / {capacidad_maxima_value} (kg)")
        st.progress(pct_disponible)

def load_data(file):
    if file is not None:
        data = pd.read_csv(file)
    else:
        data = pd.DataFrame(default_csv_data)
    return data

def main():
    """ Streamlit App """
    st.set_page_config(layout="wide")
    st.title("Optimizador de la Mochila (Knapsack Problem)")
    st.text("Este es un optimizador basado en un algoritmo codicioso para el problema de la mochila. Los algoritmos codiciosos tratan de llegar a una solución optima dividiendo un problema completo en \"etapas\" (en iteraciones). En cada iteración buscan la solución optima para esa iteración. Aunque no garantizan una solución optima global, son eficientes y fáciles de implementar.")
    st.markdown("---")
    st.subheader("Datos de Entrada")
    with st.sidebar:
        st.header("1. Carga tus datos")
        uploaded_file = st.file_uploader("Sube un .csv (Opcional)", type="csv")
        st.header("2. Define la Capacidad")
        capacidad_maxima = st.number_input("Capacidad máxima de peso:", min_value=1, value=150, step=10)
        st.header("3. Ejecuta el Algoritmo")
        optimizacion = st.button("Optimizar")
    data = load_data(uploaded_file)
    st.dataframe(data)
    if 'optimizacion' in locals() and optimizacion:
        df_plot, max_value, total_weight = calcular(data, capacidad_maxima)
        visualizar(df_plot, total_weight=total_weight, capacidad_maxima_value=capacidad_maxima)

if __name__ == "__main__":
    main()