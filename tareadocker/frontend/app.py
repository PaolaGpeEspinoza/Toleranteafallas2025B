import streamlit as st
import requests
import os

AUTH_URL = os.environ.get("AUTH_URL")
PRODUCTS_URL = os.environ.get("PRODUCTS_URL")



# ----------------------------------
# Funciones de Auth
# ----------------------------------

def signup(username, password):
    res = requests.post(f"{AUTH_URL}/signup", json={"username": username, "password": password})
    return res

def login(username, password):
    data = {"username": username, "password": password}
    res = requests.post(f"{AUTH_URL}/login", data=data)
    if res.status_code == 200:
        return res.json()["access_token"]
    return None

# ----------------------------------
# Funciones de Products
# ----------------------------------

def get_products(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{PRODUCTS_URL}/products", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []

def add_product(token, name, price):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "price": price}
    res = requests.post(f"{PRODUCTS_URL}/products/add", json=data, headers=headers)
    return res

def delete_product(token, index):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(f"{PRODUCTS_URL}/products/delete/{index}", headers=headers)
    return res

# ----------------------------------
# Interfaz Streamlit
# ----------------------------------

st.title("Microcatalog - Frontend")

# Registro / Login
if "token" not in st.session_state:
    choice = st.radio("¿Qué quieres hacer?", ["Login", "Registro"])
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button(choice):
        if choice == "Registro":
            res = signup(username, password)
            if res.status_code == 200:
                st.success("Usuario registrado correctamente. Haz login.")
            else:
                st.error(res.json()["detail"])
        else:
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.success(f"¡Bienvenido {username}!")
            else:
                st.error("Usuario o contraseña incorrectos")

# Panel principal
if "token" in st.session_state:
    token = st.session_state.token

    st.subheader("Agregar producto")
    name = st.text_input("Nombre del producto")
    price = st.number_input("Precio", min_value=0.0)

    if st.button("Agregar producto"):
        res = add_product(token, name, price)
        if res.status_code == 200:
            st.success("Producto agregado")
        else:
            st.error("Error al agregar producto")

    st.subheader("Productos actuales")
    products = get_products(token)

    for i, p in enumerate(products):
        col1, col2, col3 = st.columns([4,2,1])
        col1.write(p["name"])
        col2.write(f"${p['price']}")
        if col3.button("Eliminar", key=i):
            delete_product(token, i)
            st.rerun()

    if st.button("Cerrar sesión"):
        del st.session_state.token
        st.rerun()
