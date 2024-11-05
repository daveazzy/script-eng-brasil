import pandas as pd
import requests

url = "https://independent-minnow-daveazzy-f6c4f298.koyeb.app/participants" 

file_path = "./csv/engbrasil24-nocpf.csv"  
data = pd.read_csv(file_path)

failed_users = []

data = data.fillna("")  

for index, row in data.iterrows():
    payload = {
        "name": row["name"],
        "email": row["email"],
        "institution": row["institution"],
        "state": row["state"],
        "academicBackground": row["academicBackground"],
        "password": row["password"]
    }

    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            print(f"Usuário {row['name']} cadastrado com sucesso.")
        else:
            if "email already exists" in response.text.lower():
                print(f"Usuário {row['name']} já cadastrado: {response.status_code} - {response.text}")
            else:
                print(f"Falha ao cadastrar usuário {row['name']}: {response.status_code} - {response.text}")
                failed_users.append(row.to_dict()) 
    except Exception as e:
        print(f"Ocorreu um erro ao cadastrar o usuário {row['name']}: {e}")
        failed_users.append(row.to_dict()) 

if failed_users:
    failed_df = pd.DataFrame(failed_users)
    failed_df.to_csv("./csv/usuarios_falhados.csv", index=False)
    print(f"\n{len(failed_users)} usuários falharam ao cadastrar e foram salvos em 'usuarios_falhados.csv'.")
