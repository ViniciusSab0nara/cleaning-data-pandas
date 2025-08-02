import pandas


cadastros = [
    {
        "nome": "Ana", 
        "idade": "25",
        "email": "ana@email.com",
        "cidade": "Guarulhos"
    },
    {
        "nome": "Vinicius", 
        "idade": "21",
        "email": "vinicius@email.com",
        "cidade": "Suzano"

    },
    {
        "nome": "Raquel", 
        "idade": "41",
        "email": "raquel@email.com",
        "cidade": "Mogi das Cruzes"
    }
]

df = pandas.DataFrame(data = cadastros) ## -traz os dados em tabela

df = df.rename(columns={'nome': 'Nome', 'email': 'Email', 'cidade': "Cidade"})
df["idade"] = df["idade"].astype(int)

print(df)