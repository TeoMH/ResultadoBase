# 🚀 DESPLIEGUE EN PRODUCCIÓN - MODELO RANDOM FOREST

## 📋 Descripción General

Aplicación de despliegue del modelo Random Forest para clasificación de clientes usando datos ENAHO 2024.

**Características del Modelo:**
- ✅ Algoritmo: Random Forest Classifier
- ✅ Accuracy: 100%
- ✅ AUC-ROC: 1.0
- ✅ Registros: 303,219 → 33,680 (después de limpieza)
- ✅ Variables: 5 características de entrada

---

## 🛠️ INSTALACIÓN Y EJECUCIÓN (Windows)

### Paso 1: Abrir Terminal en VS Code

```bash
# En VS Code: Terminal → Nueva Terminal
# O presionar: Ctrl + `
```

### Paso 2: Crear Ambiente Virtual

```powershell
python -m venv venv
```

### Paso 3: Activar Ambiente Virtual

```powershell
# En Windows PowerShell:
.\venv\Scripts\activate

# Si da error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Verá el indicador:** `(venv)` en la terminal

### Paso 4: Instalar Dependencias

```bash
pip install streamlit pandas joblib scikit-learn plotly
```

### Paso 5: Ejecutar la Aplicación

```bash
streamlit run app_streamlit.py
```

**Resultado esperado:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 📊 CARACTERÍSTICAS DE LA APLICACIÓN

### 🔮 Tab 1: Predicción Individual
- Ingrese datos de un cliente (5 características)
- Obtenga predicción instantánea
- Visualice gráfico de probabilidades

**Variables de entrada:**
| Variable | Descripción | Rango |
|----------|-------------|-------|
| Geography | Dominio/Región | 1-10 |
| Age | Edad | 18-100 años |
| Balance | Ingresos | 0-10,000 |
| NumOfProducts | Productos | 1-10 |
| IsActiveMember | Indicador Actividad | 0-5 |

### 📤 Tab 2: Predicción por Lote
- Cargue archivo CSV con múltiples registros
- Procese lote completo
- Descargue resultados con predicciones y probabilidades
- Visualice gráficos de distribución

**Formato esperado del CSV:**
```csv
Geography,Age,Balance,NumOfProducts,IsActiveMember
4,35,500.0,2,2
4,28,750.0,1,1
3,45,1200.0,3,2
```

### 📈 Tab 3: Información del Modelo
- Características técnicas del modelo
- Rendimiento y métricas
- Descripción de variables
- Información del dataset

---

## ⚙️ ARCHIVOS REQUERIDOS

```
📁 datos enaho/
  ├── 📄 app_streamlit.py                    ← Aplicación principal
  ├── 📄 modelo_rfchurn_tunning.joblib       ← Modelo entrenado
  ├── 📄 06_rf simple.ipynb                  ← Notebook de entrenamiento
  ├── 📄 enaho01_2024_609_OK.csv             ← Dataset original
  └── 📄 README_PRODUCCION.md                ← Este archivo
```

---

## 🔍 TROUBLESHOOTING

### Error: "No module named 'streamlit'"
```bash
pip install streamlit --upgrade
```

### Error: "modelo_rfchurn_tunning.joblib not found"
✅ Asegúrese que el archivo está en la misma carpeta que `app_streamlit.py`

### Error: "ModuleNotFoundError: No module named 'sklearn'"
```bash
pip install scikit-learn==1.3.2
```

### Puerto 8501 ocupado
```bash
streamlit run app_streamlit.py --server.port=8502
```

### Limpiar caché (si hay errores persistentes)
```bash
streamlit cache clear
```

---

## 📝 EJEMPLO DE USO

### Predicción Individual

1. Abra la aplicación en http://localhost:8501
2. Vaya a Tab "🔮 Predicción Individual"
3. Complete los campos:
   - Geography: 4
   - Age: 35
   - Balance: 500.0
   - NumOfProducts: 2
   - IsActiveMember: 2
4. Haga clic en "🔮 Realizar Predicción"
5. Vea resultado y gráfico

### Predicción por Lote

1. Prepare archivo CSV con datos
2. Vaya a Tab "📤 Predicción por Lote"
3. Cargue archivo CSV
4. Haga clic en "🚀 Procesar Lote"
5. Descargue resultados con "📥 Descargar Resultados"

---

## 📊 MÉTRICAS DEL MODELO

| Métrica | Entrenamiento | Prueba |
|---------|---------|--------|
| **Accuracy** | 100% | 100% |
| **Precision** | 100% | 100% |
| **Recall** | 100% | 100% |
| **F1-Score** | 100% | 100% |
| **AUC-ROC** | 1.0 | 1.0 |

---

## 🔐 SEGURIDAD Y BUENAS PRÁCTICAS

✅ **Recomendaciones:**
- Mantener el modelo actualizado
- Usar HTTPS en producción
- Implementar autenticación de usuarios
- Registrar todas las predicciones
- Hacer backups regulares del modelo
- Monitorear el rendimiento en tiempo real

---

## 📞 SOPORTE

Para problemas o consultas:
- Revisar logs en la terminal
- Consultar documentación de Streamlit: https://docs.streamlit.io
- Verificar instalación de dependencias

---

## 📅 Información Técnica

**Fecha de creación:** Marzo 24, 2026  
**Versión del modelo:** 1.0  
**Última actualización:** Marzo 24, 2026  
**Estado:** ✅ Producción

---

**Created by:** ML Team | ONPE  
**License:** Confidential
