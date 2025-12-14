from db import fetch_all

rows = fetch_all("SELECT * FROM CHAMBRE;")
print(rows)
