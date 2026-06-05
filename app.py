import streamlit as st
import pandas as pd
import database

# Inicializar base de datos de pedidos al arrancar la aplicación
database.crear_tablas()
database.insertar_datos_demo()

def cambiar_voz_vapi(private_key, assistant_id, voice_provider, voice_id, model):
    import urllib.request
    import json
    
    url = f"https://api.vapi.ai/assistant/{assistant_id}"
    payload = {
        "voice": {
            "provider": voice_provider,
            "voiceId": voice_id,
            "model": model
        }
    }
    
    headers = {
        "Authorization": f"Bearer {private_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    
    try:
        # Añadir un timeout de 10 segundos para evitar bloqueos indefinidos
        with urllib.request.urlopen(req, timeout=10) as response:
            return True, "¡Voz actualizada con éxito! Inicia una nueva llamada para probarla."
    except urllib.error.HTTPError as e:
        try:
            error_details = e.read().decode("utf-8")
            return False, f"Error API Vapi (HTTP {e.code}): {error_details}"
        except Exception as read_err:
            return False, f"Error API Vapi (HTTP {e.code}): {str(e)} (Detalles inaccesibles: {str(read_err)})"
    except Exception as e:
        return False, f"Error al actualizar la voz: {str(e)}"

# Configuración de página con título y estilo premium
st.set_page_config(
    page_title="AlphaTech AI Voice Assistant",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de estilos CSS premium (Glassmorphism, gradientes, animaciones)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Configuración de tipografía */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at top right, #111827 0%, #030712 100%);
        color: #f3f4f6;
    }
    
    /* Encabezado Principal */
    .header-container {
        text-align: center;
        padding: 30px 0 20px 0;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .header-subtitle {
        color: #9ca3af;
        font-size: 1.15rem;
        font-weight: 400;
    }

    /* Tarjetas de diseño Glassmorphic */
    .glass-card {
        background: rgba(17, 24, 39, 0.55);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    .glass-card-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: #f3f4f6;
        border-left: 4px solid #10b981;
        padding-left: 12px;
    }

    /* Estados de Llamada */
    .status-badge {
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
    }
    .status-badge-waiting {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .status-badge-active {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Animación del Micrófono */
    .mic-outer {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 140px;
        margin: 15px 0 25px 0;
    }
    .mic-circle {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.5s ease;
    }
    .mic-circle-waiting {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #9ca3af;
        box-shadow: 0 0 0 0 rgba(156, 163, 175, 0.4);
    }
    .mic-circle-active {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-green 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }
    
    @keyframes pulse-green {
        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 25px rgba(16, 185, 129, 0);
        }
        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }

    /* Prompts Sugeridos */
    .prompt-box {
        background: rgba(31, 41, 55, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        font-size: 0.92rem;
        color: #d1d5db;
        border-left: 3px solid #3b82f6;
    }
    .prompt-box-accent {
        border-left: 3px solid #8b5cf6;
    }
    
    /* Ocultar botón flotante por defecto de Vapi */
    #vapi-support-btn {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado de la Aplicación
st.markdown("""
<div class="header-container">
    <div class="header-title">📞 Central de Atención AlphaTech</div>
    <div class="header-subtitle">Prueba en tiempo real el Agente de IA para Ventas y Soporte al Cliente</div>
</div>
""", unsafe_allow_html=True)

# Credenciales de Vapi por defecto (Private API Key y Assistant ID)
DEFAULT_PRIVATE_KEY = "1a4bf0ff-9c42-44e3-b657-dabaff62f157"
DEFAULT_ASSISTANT_ID = "d9c26c6f-d775-488c-a3a1-7db1d851e99b"

# Inicializar estado de llamada en la sesión de Streamlit
if "llamando" not in st.session_state:
    st.session_state.llamando = False

# Crear columnas principales de la interfaz
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Contenedor de Configuración de Credenciales
    with st.expander("⚙️ CONFIGURACIÓN DE CREDENCIALES (VAPI)"):
        st.info("⚠️ Vapi requiere tu **Public API Key** para el navegador web. Puedes encontrarla en tu panel de Vapi (Account -> API Keys).")
        vapi_key = st.text_input(
            "Vapi Public API Key (Token Público)",
            value=DEFAULT_PRIVATE_KEY,
            help="Ingresa tu Public API Key para evitar el error 401 Unauthorized."
        )
        assistant_id = st.text_input(
            "Vapi Assistant ID",
            value=DEFAULT_ASSISTANT_ID
        )
        
        st.markdown("---")
        st.markdown("### 🗣️ Cambiar Acento / Voz del Asistente")
        st.write("Selecciona una de las voces en español nativo para corregir el acento robótico o extranjero:")
        
        opciones_voz = {
            "Alisson (ElevenLabs) - Femenino, Acento Colombiano (Cálido y Natural)": {
                "provider": "11labs",
                "id": "SmgKjOvC1aIujLWcMzqq",
                "model": "eleven_multilingual_v2"
            },
            "Antoni (ElevenLabs) - Español de España (Masculino - Altísima Calidad)": {
                "provider": "11labs",
                "id": "ErXwobaYiN019PkySvjV",
                "model": "eleven_multilingual_v2"
            },
            "Rachel (ElevenLabs) - Femenino Multilingüe (Dulce y Natural)": {
                "provider": "11labs",
                "id": "21m00Tcm4TlvDq8ikWAM",
                "model": "eleven_multilingual_v2"
            },
            "Javier (Cartesia) - Español de España (Masculino - Ultra Baja Latencia)": {
                "provider": "cartesia",
                "id": "e30c6a58-868d-4e92-af0f-b4b105494d13",
                "model": "sonic-multilingual"
            },
            "María (Cartesia) - Español de España (Femenino - Ultra Baja Latencia)": {
                "provider": "cartesia",
                "id": "5345cf08-6f37-424d-a5d9-8ae1101b9377",
                "model": "sonic-multilingual"
            },
            "Personalizado (Ingresar ID de voz manual)": {
                "provider": "custom",
                "id": "custom",
                "model": "custom"
            }
        }
        
        voz_seleccionada = st.selectbox(
            "Voces en Español disponibles:",
            options=list(opciones_voz.keys())
        )
        
        # Campos personalizados si selecciona la opción manual
        if voz_seleccionada == "Personalizado (Ingresar ID de voz manual)":
            custom_provider = st.selectbox("Proveedor de voz:", ["11labs", "cartesia", "playht"])
            custom_id = st.text_input("ID de la voz (Voice ID):", value="", placeholder="Ej: SmgKjOvC1aIujLWcMzqq")
            custom_model = st.text_input("Modelo de voz:", value="eleven_multilingual_v2" if custom_provider == "11labs" else "sonic-multilingual")
            
            datos_voz = {
                "provider": custom_provider,
                "id": custom_id,
                "model": custom_model
            }
        else:
            datos_voz = opciones_voz[voz_seleccionada]
        
        vapi_private_key = st.text_input(
            "Vapi Private API Key (Requerido para actualizar la voz)",
            value=DEFAULT_PRIVATE_KEY,
            type="password",
            help="Esta clave secreta se utiliza para enviar la actualización al servidor de Vapi."
        )
        
        if st.button("💾 Aplicar y Cambiar Voz", type="primary", use_container_width=True):
            if datos_voz["provider"] == "custom" or not datos_voz["id"]:
                st.warning("⚠️ Por favor completa los campos de la voz personalizada.")
            else:
                with st.spinner("Actualizando la voz del asistente en Vapi..."):
                    exito, mensaje = cambiar_voz_vapi(
                        private_key=vapi_private_key,
                        assistant_id=assistant_id,
                        voice_provider=datos_voz["provider"],
                        voice_id=datos_voz["id"],
                        model=datos_voz["model"]
                    )
                    if exito:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)

    # ====================================================
    # INYECCIÓN DEL PUENTE DE JAVASCRIPT (PARENT WINDOW BRIDGE)
    # ====================================================
    st.components.v1.html("""
    <script>
      (function() {
        const parentDoc = window.parent.document;
        const parentWin = window.parent;
        
        console.log("[Vapi Bridge] Inicializando puente en ventana principal...");
        
        // 1. Cargar el SDK en el Head del documento principal si no existe
        if (!parentDoc.getElementById("vapi-sdk-script")) {
          const sdkScript = parentDoc.createElement("script");
          sdkScript.id = "vapi-sdk-script";
          sdkScript.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
          sdkScript.defer = true;
          sdkScript.async = true;
          parentDoc.head.appendChild(sdkScript);
          console.log("[Vapi Bridge] SDK inyectado en el Head principal.");
        }
        
        // 2. Definir función de inicio de llamada en el objeto window principal
        parentWin.startVapiCall = function(apiKey, assistantId) {
          console.log("[Vapi Bridge] Iniciar llamada invocado.");
          
          function updateStatus(text, borderColor, background) {
            const el = parentDoc.getElementById("vapi-live-status");
            if (el) {
              if (text) el.innerHTML = text;
              if (borderColor) el.style.borderColor = borderColor;
              if (background) el.style.background = background;
              return true;
            }
            return false;
          }

          // Reintentar cambiar a estado verificando micrófono mientras se monta el DOM
          let attempts = 0;
          function initStatus() {
            const success = updateStatus(
              "🎙️ Verificando permisos de micrófono...",
              "rgba(245, 158, 11, 0.3)",
              "rgba(245, 158, 11, 0.05)"
            );
            if (!success && attempts < 20) {
              attempts++;
              setTimeout(initStatus, 100);
            }
          }
          initStatus();

          // Solicitar micrófono en contexto del parent window
          if (parentWin.navigator.mediaDevices && parentWin.navigator.mediaDevices.getUserMedia) {
            parentWin.navigator.mediaDevices.getUserMedia({ audio: true })
              .then(function(stream) {
                console.log("[Vapi Bridge] Micrófono aprobado.");
                stream.getTracks().forEach(track => track.stop()); // Apagar micrófono de prueba
                
                updateStatus("📶 Estableciendo conexión WebRTC...", "rgba(59, 130, 246, 0.3)", "rgba(59, 130, 246, 0.05)");
                
                // Esperar a que vapiSDK esté disponible en el window principal
                let sdkAttempts = 0;
                function checkSDK() {
                  if (parentWin.vapiSDK) {
                    // Limpiar cualquier llamada previa
                    if (parentWin.vapiSDK.vapi) {
                      try { parentWin.vapiSDK.vapi.stop(); } catch(e) {}
                    }
                    
                    console.log("[Vapi Bridge] Inicializando Vapi SDK...");
                    const vapiInstance = parentWin.vapiSDK.run({
                      apiKey: apiKey,
                      assistant: assistantId,
                      config: {}
                    });
                    
                    vapiInstance.on("call-start", () => {
                      updateStatus(
                        "📞 <span style='color: #10b981;'>Llamada Activa</span> - El agente te escucha",
                        "#10b981",
                        "rgba(16, 185, 129, 0.08)"
                      );
                    });
                    
                    vapiInstance.on("call-end", () => {
                      updateStatus(
                        "🔌 Llamada finalizada.",
                        "rgba(255, 255, 255, 0.05)",
                        "rgba(31, 41, 55, 0.45)"
                      );
                    });
                    
                    vapiInstance.on("speech-start", () => {
                      updateStatus(
                        "🗣️ <span style='color: #60a5fa;'>El asistente está hablando...</span>",
                        "#3b82f6",
                        "rgba(59, 130, 246, 0.08)"
                      );
                    });
                    
                    vapiInstance.on("speech-end", () => {
                      updateStatus(
                        "🤫 <span style='color: #34d399;'>Escuchando tu voz...</span>",
                        "#10b981",
                        "rgba(16, 185, 129, 0.08)"
                      );
                    });
                    
                    vapiInstance.on("error", (err) => {
                      console.error("[Vapi Bridge] Error en llamada:", err);
                      let errMsg = "Error en la conexión.";
                      if (err) {
                        if (typeof err === "object") {
                          const details = [];
                          if (err.message) details.push("message: " + err.message);
                          if (err.error) details.push("error: " + err.error);
                          if (err.name) details.push("name: " + err.name);
                          if (err.code) details.push("code: " + err.code);
                          if (err.status) details.push("status: " + err.status);
                          if (err.statusText) details.push("statusText: " + err.statusText);
                          if (err.reason) details.push("reason: " + err.reason);
                          
                          if (details.length > 0) {
                            errMsg = details.join(" | ");
                          } else {
                            try {
                              const jsonStr = JSON.stringify(err);
                              errMsg = jsonStr === "{}" ? err.toString() : jsonStr;
                            } catch(e) {
                              errMsg = err.toString();
                            }
                          }
                        } else {
                          errMsg = err.toString();
                        }
                      }
                      updateStatus(
                        "❌ <span style='color: #ef4444;'>Error: " + errMsg + "</span>",
                        "#ef4444",
                        "rgba(239, 68, 68, 0.1)"
                      );
                    });
                    
                    setTimeout(() => {
                      if (parentWin.vapiSDK.vapi) {
                        parentWin.vapiSDK.vapi.start(assistantId);
                        console.log("[Vapi Bridge] .start() ejecutado.");
                      }
                    }, 500);
                  } else if (sdkAttempts < 30) {
                    sdkAttempts++;
                    setTimeout(checkSDK, 100);
                  } else {
                    updateStatus("❌ Error: SDK de Vapi no cargó.", "#ef4444", "rgba(239, 68, 68, 0.1)");
                  }
                }
                checkSDK();
              })
              .catch(function(err) {
                console.error("[Vapi Bridge] Micrófono denegado o error:", err);
                updateStatus("❌ Permiso de micrófono denegado.", "#ef4444", "rgba(239, 68, 68, 0.1)");
                alert("⚠️ MICRÓFONO REQUERIDO:\\n\\nPor favor concede permisos de micrófono en el candado de la barra de direcciones.");
              });
          } else {
            updateStatus("❌ Contexto de navegador inseguro.", "#ef4444", "rgba(239, 68, 68, 0.1)");
          }
        };
        
        // 3. Definir función de detener llamada en el objeto window principal
        parentWin.stopVapiCall = function() {
          console.log("[Vapi Bridge] Detener llamada invocado.");
          if (parentWin.vapiSDK && parentWin.vapiSDK.vapi) {
            try {
              parentWin.vapiSDK.vapi.stop();
            } catch(e) {
              console.error(e);
            }
          }
          const el = parentDoc.getElementById("vapi-live-status");
          if (el) {
            el.innerHTML = "🟢 Listo para conectar";
            el.style.borderColor = "rgba(255, 255, 255, 0.05)";
            el.style.background = "rgba(31, 41, 55, 0.45)";
          }
        };
      })();
    </script>
    """, height=0)

    # Contenedor Glassmorphic para la simulación
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">Panel de Simulación</div>', unsafe_allow_html=True)
    
    if not st.session_state.llamando:
        st.markdown('<div class="status-badge status-badge-waiting">🟢 SISTEMA EN ESPERA</div>', unsafe_allow_html=True)
        
        # Animación estática del micrófono apagado
        st.markdown("""
        <div class="mic-outer">
            <div class="mic-circle mic-circle-waiting">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("El asistente está listo para recibir tu llamada. Presiona el botón de abajo para activar tu micrófono e iniciar la conversación.")
        
        if st.button("🟩 Iniciar Llamada de Voz", type="primary", use_container_width=True):
            st.session_state.llamando = True
            st.rerun()
            
    else:
        st.markdown('<div class="status-badge status-badge-active">🎙️ LLAMADA EN CURSO</div>', unsafe_allow_html=True)
        
        # Animación pulsante del micrófono activo
        st.markdown("""
        <div class="mic-outer">
            <div class="mic-circle mic-circle-active">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("El micrófono está transmitiendo audio. El agente virtual te está escuchando.")
        
        if st.button("🟥 Finalizar Llamada", type="secondary", use_container_width=True):
            st.session_state.llamando = False
            st.rerun()
            
    # Contenedor de Estado del Micrófono/Llamada
    # Inicialmente muestra "🟢 Listo para conectar" cuando no se está en llamada
    estado_inicial = "🟢 Listo para conectar" if not st.session_state.llamando else "🔌 Esperando conexión..."
    st.markdown(f"""
    <div id="vapi-live-status" style="background: rgba(31, 41, 55, 0.45); padding: 14px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 15px; font-weight: 600; text-align: center; font-size: 0.95rem; transition: all 0.3s ease; color: #f3f4f6;">
        {estado_inicial}
    </div>
    """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Sugerencias para hablar con el Agente
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">Preguntas Sugeridas para el Agente</div>', unsafe_allow_html=True)
    st.write("Puedes realizar consultas de prueba sobre pedidos y políticas:")
    
    st.markdown("""
    <div class="prompt-box">
        🗣️ <b>Consultar Pedido:</b><br>"Hola, ¿cuál es el estado de mi pedido ALFA-102?"
    </div>
    <div class="prompt-box prompt-box-accent">
        🗣️ <b>Validar Políticas de Devolución:</b><br>"¿Puedo devolver una licencia de software (pedido ALFA-104)?"
    </div>
    <div class="prompt-box">
        🗣️ <b>Preguntar sobre Envíos:</b><br>"¿Cuánto tiempo tarda un envío exprés y uno estándar?"
    </div>
    <div class="prompt-box prompt-box-accent">
        🗣️ <b>Garantías de Artículos:</b><br>"¿Qué garantía tiene una laptop Pro 15?"
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_right:
    # Contenedor de Base de Datos
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">Base de Datos de Pedidos ( Fresh SQLite )</div>', unsafe_allow_html=True)
    st.write("Esta tabla contiene los pedidos en el sistema que el agente puede consultar en tiempo real:")
    
    df_pedidos = database.obtener_pedidos_df()
    st.dataframe(
        df_pedidos,
        width="stretch",
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Políticas de la tienda
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">Políticas de la Empresa (AlphaTech)</div>', unsafe_allow_html=True)
    
    with open("politicas.txt", "r", encoding="utf-8") as f:
        politicas_texto = f.read()
    
    st.text_area(
        label="Documento de referencia del asistente",
        value=politicas_texto,
        height=180,
        disabled=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================
# CONTROLADOR DE ACTIVACIÓN DE LLAMADA DESDE IFRAME
# ==============================================
if st.session_state.llamando:
    # Disparar inicio de llamada en la ventana principal
    st.components.v1.html(f"""
    <script>
      (function() {{
        let attempts = 0;
        function triggerCall() {{
          if (window.parent && window.parent.startVapiCall) {{
            window.parent.startVapiCall("{vapi_key}", "{assistant_id}");
            console.log("[Vapi Controller] Invocado startVapiCall con éxito.");
          }} else if (attempts < 20) {{
            attempts++;
            setTimeout(triggerCall, 100);
          }} else {{
            console.error("[Vapi Controller] No se pudo encontrar startVapiCall en window.parent.");
          }}
        }}
        triggerCall();
      }})();
    </script>
    """, height=0)
else:
    # Disparar fin de llamada en la ventana principal
    st.components.v1.html("""
    <script>
      (function() {
        if (window.parent && window.parent.stopVapiCall) {
          window.parent.stopVapiCall();
          console.log("[Vapi Controller] Invocado stopVapiCall con éxito.");
        }
      })();
    </script>
    """, height=0)

