import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# ==========================
# Função pura para separação
# ==========================
def separar_pares_impares(lista_ids):
    """Recebe uma lista de inteiros e retorna duas listas: pares e ímpares."""
    pares = [i for i in lista_ids if i % 2 == 0]
    impares = [i for i in lista_ids if i % 2 != 0]
    return pares, impares


# ==========================
# Configuração inicial
# ==========================
st.set_page_config(page_title="🧩 Particionador de IDs por Shard", page_icon="🔢")
st.title("🧩 Particionador de IDs por Shard (A/B)")
st.write("Simule a distribuição de pedidos entre shards com base no ID (par/ímpar).")

st.divider()

# ==========================
# Entrada de dados
# ==========================
st.subheader("📥 Parâmetros da simulação")

col1, col2 = st.columns(2)

with col1:
    qtd_ids = st.number_input("Quantidade de IDs a gerar/inserir:", min_value=1, max_value=1000, value=20, step=1)
    gerar_automatico = st.checkbox("Gerar IDs aleatórios automaticamente", value=True)

with col2:
    min_id = st.number_input("Valor mínimo do ID", min_value=0, value=0, step=1)
    max_id = st.number_input("Valor máximo do ID", min_value=1, value=9999, step=1)

st.divider()

# ==========================
# Geração ou entrada manual
# ==========================
if gerar_automatico:
    lista_ids = [random.randint(min_id, max_id) for _ in range(qtd_ids)]
    st.info(f"✅ Foram gerados automaticamente **{qtd_ids} IDs** aleatórios.")
else:
    ids_texto = st.text_area("✏️ Digite os IDs separados por vírgula (ex: 10, 23, 45, 66):")
    if ids_texto.strip():
        try:
            lista_ids = [int(x.strip()) for x in ids_texto.split(",")]
        except ValueError:
            st.error("⚠️ Certifique-se de digitar apenas números inteiros separados por vírgulas.")
            lista_ids = []
    else:
        lista_ids = []

# ==========================
# Execução da simulação
# ==========================
if lista_ids:
    pares, impares = separar_pares_impares(lista_ids)

    st.divider()
    st.subheader("📊 Resultados da Partição")

    colA, colB, colC = st.columns(3)
    colA.metric("Total IDs", len(lista_ids))
    colB.metric("Shard A (Pares)", len(pares))
    colC.metric("Shard B (Ímpares)", len(impares))

    st.write("### 🧾 Listas:")
    st.write(f"**Lista original:** {lista_ids}")
    st.write(f"**Shard A (PAR):** {pares}")
    st.write(f"**Shard B (ÍMPAR):** {impares}")

    # ==========================
    # Criar planilha (DataFrame)
    # ==========================
    df = pd.DataFrame({
        "ID": lista_ids,
        "Shard": ["A (Par)" if i % 2 == 0 else "B (Ímpar)" for i in lista_ids]
    })

    st.divider()
    st.subheader("📈 Distribuição visual")

    # Gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(["Shard A (Par)", "Shard B (Ímpar)"], [len(pares), len(impares)], color=["red", "blue"])
    ax.set_ylabel("Quantidade de IDs")
    ax.set_title("Distribuição de IDs por Shard")
    st.pyplot(fig)

    # Mostrar tabela
    with st.expander("📋 Ver tabela detalhada"):
        st.dataframe(df)

    # ==========================
    # Exportar planilha
    # ==========================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar planilha CSV",
        data=csv,
        file_name="distribuicao_shards.csv",
        mime="text/csv"
    )

else:
    st.warning("🕐 Aguarde ou insira os IDs para iniciar a simulação.")
