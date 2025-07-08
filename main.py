# import library yang dibutuhkan
from fastapi import FastAPI, HTTPException
import pandas as pd

# buat object
app = FastAPI()

# buat endpoint home
@app.get("/")
def home():
    return "Selamat datang di Toko Hacktiv8!"

# buat endpoint baca dataToko
@app.get("/data")
def readData():
    df = pd.read_csv("dataToko.csv")
    return df.to_dict(orient='records')

# buat endpoint baca dataToko berdasarkan id
@app.get("/data/{user_input}")
def searchById(user_input: int):
    # baca data
    df = pd.read_csv("dataToko.csv")

    # matching apakah user_input sesuai dengan data yang ada atau tidak
    filter = df[df["id"] == user_input]

    # buat kondisi jika tidak ada -> len()
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="Barang tidak ada.")

    # jika ada maka ditampilkan melalui return
    return filter.to_dict(orient='records')

# buat endpoint untuk update data ke data yang sudah ada di server
@app.post("/item/{item_id}")
def addData(item_id: int, item_name: str, item_price: float):
    # baca data yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # buat dict baru untuk tempat data baru
    new_data = {
        "id":item_id,
        "namaBarang":item_name,
        "harga":item_price
    }

    # ubah dict data baru ke dataframe
    new_df = pd.DataFrame(new_data, index=[0])

    # kita gabungkan(concat) data baru dengan data yang sudah ada
    df = pd.concat([df,new_df], ignore_index=True)

    # save data yang sudah terupdate ke csv
    df.to_csv("dataToko.csv", index=False)

    return f"Data dengan id {item_id} nama barang {item_name} dan harga {item_price} sudah ditambahkan."

# buat endpoint baru untuk update isi data yang sudah ada di server (bukan menambah baris baru)
@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: float):
    # baca data yang sudah ada
    df = pd.read_csv("dataToko.csv")

    # buat dict baru untuk tempat data baru
    update_data = {
        "id":item_id,
        "namaBarang":item_name,
        "harga":item_price
    }

    # cek jika id yang dimasukkan tidak ditemukan
    if update_data["id"] not in df["id"].values:
        return "Data dengan id {item_id} tidak ditemukan."
    
    # replace/update data jika id ditemukan
    df.loc[df["id"]==update_data["id"], "namaBarang"] = update_data["namaBarang"]
    df.loc[df["id"]==update_data["id"], "harga"] = update_data["harga"]

    # simpan data terupdate ke csv
    df.to_csv("dataToko.csv", index=False)

    return "Barang dengan id {item_id} nama barang {item_name} sudah terupdate."


# buat endpoint untuk memasukkan data baru
@app.get("/income")
def readIncome():
    df_income = pd.read_csv("dataIncome.csv")
    return df_income.to_dict(orient="records")