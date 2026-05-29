import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import OllamaLLM
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Agente Analista de Ventas", page_icon="📊", layout="wide")

with st.sidebar:
    st.title("⚙️ Configuración")
    st.write("Agente Inteligente con capacidad de análisis de datos.")
    st.markdown("---")
    st.caption("Desarrollado para la presentación del proyecto.")

st.title("📊 Agente IA - Analista de Ventas y Finanzas")
st.write("Sube tu archivo y conversa con el agente para auditar tus datos de ventas.")

# Componente de carga de archivos
archivo_cargado = st.file_uploader("Arrastra aquí tu archivo de datos", type=["csv", "xlsx"])

if archivo_cargado is not None:
    try:
        # Leer el archivo según su extensión
        if archivo_cargado.name.endswith('.csv'):
            df = pd.read_csv(archivo_cargado)
        else:
            df = pd.read_excel(archivo_cargado)
        
        st.success("¡Archivo cargado con éxito!")
        
        # Mostrar vista previa
        st.subheader("👀 Vista previa de los datos:")
        st.dataframe(df.head(5))
        
        st.markdown("---")
        st.subheader("💬 Consulta al Agente Analista")
        
        # Configurar el "Cerebro". 
        # Usaremos Ollama con un modelo rápido como 'llama3' o 'mistral'.
        # Si prefieres usar OpenAI, cambiarías esta línea por: desde langchain_openai import ChatOpenAI
        llm = OllamaLLM(model="llama3", temperature=0)
        
        # Crear el agente experto en DataFrames de Pandas
        agente = create_pandas_dataframe_agent(
            llm, 
            df, 
            verbose=True, 
            allow_dangerous_code=True # Requerido en versiones recientes para permitir análisis local
        )
        
        # Input del chat
        pregunta = st.chat_input("Ej: ¿Cuál es el total de ingresos o qué producto se vendió más?")
        
        if pregunta:
            with st.chat_message("user"):
                st.write(pregunta)
                
            with st.chat_message("assistant"):
                with st.spinner("Analizando los datos..."):
                    try:
                        # El agente procesa la pregunta ejecutando código Pandas internamente
                        respuesta = agente.run(pregunta)
                        st.write(respuesta)
                    except Exception as error_agente:
                        st.error(f"El agente tuvo un problema al procesar la respuesta: {error_agente}")
                        
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")