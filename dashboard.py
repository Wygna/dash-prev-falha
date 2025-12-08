import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from config import db
# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class CadastroApp:
            def __init__(self):
                self.cursor = db.cursor
                self.db = db.mydb

            def create(self):
                st.subheader("Criação de Usuário")
                name = st.text_input("Nome")
                password= st.text_input("Senha")

                if st.button("Criar"):
                    sql = "INSERT INTO users (name, password) VALUES (%s, %s)"
                    val = (name, password)
                    self.cursor.execute(sql, val)
                    self.db.commit()
                    st.success("Usuário cadastrado!")

            def run(self):
                self.create()

# Inicialização do st.session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Tela de login
def login():
        st.title("Autenticação")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if username == os.getenv("USER") and password == os.getenv("PASSWORD"):
                st.session_state.logged_in = True
                st.success("Login bem-sucedido!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")    
        if st.button("Cadastrar"):
             st.switch_page("pages/cadastro.py")
    
                       
# Página principal com login obrigatório
if not st.session_state.logged_in:
    login()
else:
    #título da página
    st.title('DASHBOARD DE PREVISÃO DE FALHA 📉')

    #alargar a tela
    st.set_page_config(layout= 'wide')

    #separar o layout em tabs
    tab1, tab2 = st.tabs(["Fonte", "Insights"])

    with tab1:
        #carga da fonte de dados
        uploaded_file = st.file_uploader("Cadastre uma fonte")

    with tab2:
        # Processamento
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            #print(len(df))
            #print(df.columns)
            #df.isna().sum()
            #qtd_fault = len(df[df['Fault_Status']==1]) #qtd de sensores com falhas
            #qtd_not_fault = len(df[df['Fault_Status']==0]) #qtd de sensores sem falhas
            #print(f'Quantidade de falhas: {qtd_fault}')
            #print(f'Quantidade de não falhas: {qtd_not_fault}')

            #remover colunas irrelevantes para classificação binária
            cols_to_drop = [
                 'Timestamp',
                 'Sensor_ID',
                 'Temperature',
                 'Vibration',
                 'Pressure',
                 'Voltage',
                 'Current',
                 'Fault_Type'
            ]

            classification_df = df.copy()
            classification_df = classification_df.drop(columns=cols_to_drop)   
            print(classification_df.columns)

            #Separação treino / teste
            X = classification_df.drop('Fault_Status', axis=1) #criando o conjunto de variáveis independentes (features). #Pega o dataframe classification_df e remove a coluna Fault_Status. O axis=1 significa “remova uma coluna”.
            y = classification_df['Fault_Status'] #O y é a variável dependente, ou seja, aquilo que eu quer prever

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) 
            #X_train → features do treino
            #X_test → features do teste
            #y_train → alvo do treino
            #y_test → alvo do teste
            #test_size=0.2 -> Separa 20% dos dados para teste e 80% para treino.
            #random_state=42 -> Garante que a divisão sempre saia igual ao rodar novamente o código. É um seed de reprodutibilidade.
            #stratify=y -> Ele faz a divisão preservando a proporção das classes de y tanto no treino quanto no teste.
                        #-> Exemplo: Se o dataset tem 90% de “normal” e 10% de “fault”, então o treino e o teste também terão essa proporção.
                        # Sem o stratify, o conjunto de teste poderia ficar totalmente desbalanceado. 

            from imblearn.under_sampling import RandomUnderSampler
            #biblioteca focada em tratamento de dados desbalanceados.
            x_ba, y_ba = RandomUnderSampler(sampling_strategy=1).fit_resample(X_train, y_train)
            #RandomUnderSampler: Ele remove exemplos aleatórios da classe que tem mais amostras para igualar com a classe que tem menos.
            #sampling_strategy=1: você quer que cada classe tenha a mesma quantidade #a proporção final será 1:1
            #x_ba → features balanceadas
            #y_ba → labels balanceados

            rf = RandomForestClassifier(n_estimators=200) #o modelo terá 200 árvores na floresta.
            #Treinamento do modelo
            rf.fit(x_ba, y_ba)

            y_pred = rf.predict(X_test) 
            #O método .predict() pega o conjunto de teste (X_test) — que o modelo nunca viu antes — e gera uma previsão da classe para cada amostra.
            #y_pred passa a ser um array com as previsões, exemplo: [0, 0, 1, 0, 1, 0, 0, ...]
            #Esse array é usado para comparar com y_test

            #construindo um dataframe final de comparação
            df_pred = X_test #copiando o dataframe X_test para uma nova variável chamada df_pred.
            df_pred['y_test'] = y_test #adiciona ao dataframe uma nova coluna: y_test → o valor verdadeiro (real) da classe para cada linha de teste.
            df_pred['y_pred'] = y_pred #adiciona outra coluna: y_pred → a classe prevista pelo modelo Random Forest.

            #GRÁFICOS
            lista_sensor_id = []
            for i in df_pred.index:
                 lista_sensor_id.append(df['Sensor_ID'][i])
            df_pred['Sensor_ID'] = lista_sensor_id
            df_top10 = df_pred[['Sensor_ID', 'y_pred']][df_pred['y_pred'] == 1]
            if(len(df_top10) > 10):
                 df_top10 = df_top10.head(10)
            st.header('Equipamentos com alta probabiblidade de falha')
            st.table(pd.DataFrame(df_top10))

            #---

            lista_tipo_falha = []
            for i in df_pred.index:
                 lista_tipo_falha.append(df['Fault_Type'][i])
            df_pred['Fault_Type'] = lista_tipo_falha

            qtd_tipos_falha = df_pred['Fault_Type'].value_counts()

            fig = px.bar(qtd_tipos_falha, x=qtd_tipos_falha.index, y=qtd_tipos_falha.values, text_auto=True)
            
            st.header('Frequência de Tipo de Falha')
            st.plotly_chart(fig, use_container_width=True)
            
            #---

            radar_df = df_pred[['Normalized_Temp','Normalized_Vibration', 'Normalized_Pressure', 'Normalized_Voltage','Normalized_Current']]
            radar_df_mean = radar_df.mean()
            radar_df_median = radar_df.median()

            categories = radar_df_mean.index

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                 r=radar_df_mean.values,
                 theta=categories,
                 fill='toself',
                 name='Mean'
            ))

            fig.add_trace(go.Scatterpolar(
                 r=radar_df_median.values,
                 theta=categories,
                 fill='toself',
                 name='Median'
            ))

            fig.update_layout(
                 polar=dict(
                      radialaxis=dict(
                           visible=True,
                           range=[0, 0.6]
                      )
                 )
            ) 
            st.header('Gráfico de Radar')
            st.plotly_chart(fig, use_container_width=True)

            #---

            df_freq = df_pred[['Normalized_Temp',
       'Normalized_Vibration', 'Normalized_Pressure', 'Normalized_Voltage',
       'Normalized_Current','Fault_Type']]
            
            st.header('Frequência de atributo vs Tipo de Falha')
            opcao = st.selectbox("Selecione um atributo:", ["Normalized_Temp", "Normalized_Vibration", "Normalized_Pressure", "Normalized_Voltage", "Normalized_Current"])
            atributo = opcao
            falha = 'Overheating'

            df_freq_filter = df_freq[atributo][df_freq['Fault_Type'] == falha]

            arr = df_freq_filter.to_list()

            arr_max = np.max(arr)
            arr_min = np.min(arr)

            faixas = np.arange(arr_min, arr_max, (arr_max/5))

            aux = 0
            freq_arr = []
            for faixa in faixas:
                 min_f = aux
                 max_f = faixa

                 qtd = len(df_freq_filter[(df_freq_filter>min_f) & (df_freq_filter<=max_f)])

                 #Atualiza auxiliar

                 dict_tmp = {
                      'faixa': f'{round(min_f, 3)}-{round(max_f,3)}',
                      'freq': qtd
                 }

                 freq_arr.append(dict_tmp)

                 aux = faixa
            df_freq_atributo = pd.DataFrame(freq_arr)
            fig = px.bar(df_freq_atributo, x=df_freq_atributo['faixa'], y=df_freq_atributo['freq'], text_auto=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
               
        
            




                 
            


            







