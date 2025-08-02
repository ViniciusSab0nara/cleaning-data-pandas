import pandas as pd
import dateparser

df = pd.read_excel(r"C:\Users\vinic\Downloads\planilha_caotica_100_linhas.xlsx")

# limpeza e padronização do nome das colunas 

df = df.replace("-", pd.NA)
df = df.fillna('nenhum valor informado')

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
    .str.replace(r'[^a-z0-9_]', '', regex= True)
)


# renomeando algumas colunas específicas
df.rename(columns={'valor_r': 'valor_real', 'observaes_' : 'observacoes'}, inplace= True)


# padronizando dados das linhas
cols_texto_lower = ['nome_completo','cidade_de_origem','observacoes']
for col in cols_texto_lower:
    df[col] = df[col].str.strip().str.lower()

column_title = ['nome_completo']
for linhas in column_title:
    df[linhas] = df[linhas].str.title()

"""print(df['data_do_cadastro'].dropna().unique())"""

# função auxiliar do for para validação dos formatos de ISO (data)
def try_convert(data_str):
    formatos = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d/%m/%y",
        "%d.%m.%y",
        "%d de %B de %Y",
        "%d-%b-%Y",
        "%d-%m-%Y"
    ]

    for fmt in formatos:
        try: 
            converted = pd.to_datetime(data_str, format=fmt)
            return converted
        except:
            continue


# caso o to_datetime não identificar, usamos o import dateparse que identifica
# melhor as traduçõe de datas.
    parsed = dateparser.parse(data_str, languages=['pt'])
    if parsed: #se o valor não for nulo o pd.timestramp(parsed) transforma o valor no timestamp atual
        return pd.Timestamp(parsed)
    return pd.NaT 

# cria nova coluna com valor do data_do_cadastro aplicando a função
df['data_do_cadastro'] = df['data_do_cadastro'].apply(try_convert)
df['data_do_cadastro'] = df['data_do_cadastro'].apply(
    lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else "Data não informada")

df['cidade_de_origem'] = df['cidade_de_origem'].str.replace('rj','rio de janeiro')
df['cidade_de_origem'] = df['cidade_de_origem'].str.replace('sao paulo','são paulo')

df['valor_real'] = df['valor_real'].str.replace('R\$', '', regex= True)  
df['valor_real'] = df['valor_real'].str.replace('.', '', regex= False)
df['valor_real'] = df['valor_real'].str.replace(',', '.', regex= False)
df['valor_real'] = pd.to_numeric(df['valor_real'], errors= 'coerce') 


print(df.head(50))

df.to_excel("cleaned_excel.xlsx", index= False)

"""
R$ 1.200,50
1      R$ 1000,00
2      R$ 1000,00
3     R$ 1.200,00
4     R$ 1.200,50
5     R$ 1.200,50
6       R$1250.50
7     R$ 1.200,00
8       R$1250.50
9     R$ 1.150,00
10           1000
11       1.150,00
12     R$ 1000,00
13    R$ 1.200,50
14    R$ 1.200,00
15        R$1.200
16      R$1250.50
17       1.150,00
18    R$ 1.150,00
19           1000
20      R$1250.50
21    R$ 1.200,00
22    R$ 1.150,00
23    R$ 1.150,00
24    R$ 1.200,50
25    R$ 1.200,00
26      R$1250.50
27     R$ 1000,00
28          950.0
29    R$ 1.200,50
30          950.0
31     R$ 1000,00
32       1.150,00
33       R$950,00
34       R$950,00
35        R$1.200
36       1.150,00
37       R$950,00
38        R$1.200
39        R$1.200
40          950.0
41     R$ 1000,00
42     R$ 1000,00
43          950.0
44    R$ 1.200,50
45    R$ 1.200,00
46           1000
47       R$950,00
48      R$1250.50
49       R$950,00
"""