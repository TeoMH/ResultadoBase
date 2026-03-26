"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║           APLICACIÓN DE DESPLIEGUE - MODELO RANDOM FOREST                    ║
║                    CLASIFICACIÓN DE CLIENTES - ENAHO 2024                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

INSTRUCCIONES DE INSTALACIÓN:
1. Crear ambiente virtual: python -m venv venv
2. Activar: .\venv\Scripts\activate  (Windows)
3. Instalar dependencias: pip install streamlit pandas joblib scikit-learn
4. Ejecutar: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
from joblib import load
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE LA PÁGINA
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Modelo Predictivo ENAHO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CARGAR MODELO
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    """Cargar el modelo una sola vez"""
    try:
        modelo = load('modelo_rfchurn_tunning.joblib')
        return modelo
    except FileNotFoundError:
        st.error("❌ Archivo 'modelo_rfchurn_tunning.joblib' no encontrado")
        return None

clf = load_model()

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
st.title("📊 Sistema Predictivo - Clasificación de Clientes")
st.markdown("---")
st.markdown("""
**Modelo:** Random Forest con Grid Search Optimization  
**Dataset:** ENAHO 2024 - 303,219 registros  
**Rendimiento:** Accuracy 100% | AUC-ROC 1.0
""")

# ═══════════════════════════════════════════════════════════════════════════════
# CREAR TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🔮 Predicción Individual", "📤 Predicción por Lote", "📈 Información del Modelo"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: PREDICCIÓN INDIVIDUAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Realizar Predicción Individual")
    st.markdown("Ingrese los datos del cliente para obtener la predicción")
    
    col1, col2 = st.columns(2)
    
    with col1:
        geography = st.number_input(
            "Dominio/Región (Geography)",
            min_value=1,
            max_value=10,
            value=4,
            help="Numeración del dominio/región"
        )
        
        age = st.number_input(
            "Edad (Age)",
            min_value=18,
            max_value=100,
            value=35,
            help="Edad en años"
        )
        
        balance = st.number_input(
            "Balance/Ingresos",
            min_value=0.0,
            max_value=10000.0,
            value=500.0,
            step=10.0,
            help="Monto en moneda local"
        )
    
    with col2:
        num_of_products = st.number_input(
            "Número de Productos",
            min_value=1,
            max_value=10,
            value=2,
            help="Cantidad de productos que utiliza"
        )
        
        is_active_member = st.number_input(
            "Miembro Activo (IsActiveMember)",
            min_value=0,
            max_value=5,
            value=2,
            help="Indicador de actividad"
        )
    
    # Botón de predicción
    if st.button("🔮 Realizar Predicción", key="predict_btn", use_container_width=True):
        # Preparar datos
        X_input = pd.DataFrame({
            'Geography': [geography],
            'Age': [age],
            'Balance': [balance],
            'NumOfProducts': [num_of_products],
            'IsActiveMember': [is_active_member]
        })
        
        # Realizar predicción
        if clf is not None:
            try:
                prediction = clf.predict(X_input)[0]
                probability = clf.predict_proba(X_input)[0]
                
                st.success("✅ Predicción Realizada")
                
                # Mostrar resultados en columnas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label="Clasificación",
                        value="Clase 1" if prediction == 1 else "Clase 0",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        label="Confianza Clase 0",
                        value=f"{probability[0]:.2%}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        label="Confianza Clase 1",
                        value=f"{probability[1]:.2%}",
                        delta=None
                    )
                
                # Gráfico de probabilidades
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Clase 0', 'Clase 1'],
                        y=[probability[0], probability[1]],
                        marker_color=['#1f77b4', '#ff7f0e']
                    )
                ])
                fig.update_layout(
                    title="Distribución de Probabilidades",
                    yaxis_title="Probabilidad",
                    xaxis_title="Clase",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error en predicción: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: PREDICCIÓN POR LOTE (ARCHIVO CSV)
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("Predicción por Lote")
    st.markdown("Cargue un archivo CSV con múltiples registros")
    
    # Parámetros de carga
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Seleccione archivo CSV",
            type=['csv'],
            help="El archivo debe contener las columnas: Geography, Age, Balance, NumOfProducts, IsActiveMember"
        )
    
    with col2:
        if uploaded_file is not None:
            st.write("")  # Espaciado
    
    if uploaded_file is not None:
        try:
            # Leer archivo
            df_input = pd.read_csv(uploaded_file)
            
            # Validar columnas
            columnas_requeridas = ['Geography', 'Age', 'Balance', 'NumOfProducts', 'IsActiveMember']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df_input.columns]
            
            if columnas_faltantes:
                st.error(f"❌ Columnas faltantes: {', '.join(columnas_faltantes)}")
            else:
                st.success(f"✅ Archivo cargado: {len(df_input)} registros")
                
                # Vista previa
                st.subheader("Vista previa de datos")
                st.dataframe(df_input.head(10), use_container_width=True)
                
                # Botón para predecir
                if st.button("🚀 Procesar Lote", use_container_width=True, key="batch_btn"):
                    if clf is not None:
                        try:
                            # Predicciones
                            predictions = clf.predict(df_input[columnas_requeridas])
                            probabilities = clf.predict_proba(df_input[columnas_requeridas])
                            
                            # Crear dataframe de resultados
                            df_resultados = df_input.copy()
                            df_resultados['Predicción'] = predictions
                            df_resultados['Prob_Clase_0'] = probabilities[:, 0]
                            df_resultados['Prob_Clase_1'] = probabilities[:, 1]
                            df_resultados['Confianza'] = np.max(probabilities, axis=1)
                            
                            st.success("✅ Predicciones completadas")
                            
                            # Mostrar estadísticas
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Total registros", len(df_resultados))
                            
                            with col2:
                                st.metric("Clase 0", (df_resultados['Predicción'] == 0).sum())
                            
                            with col3:
                                st.metric("Clase 1", (df_resultados['Predicción'] == 1).sum())
                            
                            with col4:
                                st.metric("Confianza promedio", f"{df_resultados['Confianza'].mean():.2%}")
                            
                            # Mostrar resultados
                            st.subheader("Resultados de Predicción")
                            st.dataframe(df_resultados, use_container_width=True)
                            
                            # Descargar resultados
                            csv = df_resultados.to_csv(index=False)
                            st.download_button(
                                label="📥 Descargar Resultados (CSV)",
                                data=csv,
                                file_name="predicciones_resultados.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                            
                            # Gráficos
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                fig = px.pie(
                                    values=[
                                        (df_resultados['Predicción'] == 0).sum(),
                                        (df_resultados['Predicción'] == 1).sum()
                                    ],
                                    names=['Clase 0', 'Clase 1'],
                                    title='Distribución de Predicciones',
                                    color_discrete_sequence=['#1f77b4', '#ff7f0e']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                fig = px.histogram(
                                    df_resultados,
                                    x='Confianza',
                                    nbins=20,
                                    title='Distribución de Confianza',
                                    color_discrete_sequence=['#2ca02c']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        except Exception as e:
                            st.error(f"Error al procesar lote: {str(e)}")
        
        except Exception as e:
            st.error(f"Error al leer archivo: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: INFORMACIÓN DEL MODELO
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("Información del Modelo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Características del Modelo")
        st.markdown("""
        **Algoritmo:** Random Forest Classifier
        
        **Split Training/Test:** 80% / 20%
        
        **Validación:** RepeatedStratifiedKFold (5 splits × 2 repeats)
        
        **Hiperparámetros Optimizados:**
        - ccp_alpha: [0.01, 0.03]
        - n_estimators: [50, 100]
        - max_features: [5, 8]
        """)
    
    with col2:
        st.subheader("📈 Rendimiento del Modelo")
        st.markdown("""
        **Conjunto de Entrenamiento:**
        - Accuracy: 100%
        - Precision: 100%
        - Recall: 100%
        - F1-Score: 100%
        - AUC-ROC: 1.0
        
        **Conjunto de Prueba:**
        - Accuracy: 100%
        - Precision: 100%
        - Recall: 100%
        - F1-Score: 100%
        - AUC-ROC: 1.0
        """)
    
    st.markdown("---")
    
    st.subheader("🔧 Variables de Entrada")
    st.markdown("""
    | Variable | Descripción | Rango |
    |----------|-------------|-------|
    | Geography | Dominio/Región | 1-10 |
    | Age | Edad | 18-100 años |
    | Balance | Ingresos/Balance | 0-10,000 |
    | NumOfProducts | Número de Productos | 1-10 |
    | IsActiveMember | Indicador de Actividad | 0-5 |
    """)
    
    st.markdown("---")
    
    st.subheader("📝 Dataset Original")
    st.markdown("""
    - **Fuente:** ENAHO 2024
    - **Total de Registros:** 303,219
    - **Registros después de limpieza:** 33,680
    - **Período:** Enero - Diciembre 2024
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p style='color: #888;'>
        Aplicación de Despliegue - Random Forest Model | ML Producción 2026
    </p>
</div>
""", unsafe_allow_html=True)

# Nota: El bloque debajo era código duplicado/legacy y puede provocar errores (variables no definidas, flujo confuso).
# Se elimina para mantener una sola interfaz de app con tabs y evitar sintaxis/ejecución inválida.


