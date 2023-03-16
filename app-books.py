import pandas as pd
import streamlit as st
import codecs
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Good Reads Books",
                   page_icon="libros.png")

name_link =codecs.open('books.csv','rU','latin1')
DATE_COLUMN='publication_date'

#--- PAGE CONFIG ---#
#st.set_page_config(page_title="Good Reads Books", page_icon=None)

st.title('Good Reads Books')
#--- LOGO ---#
st.sidebar.image("LogoBooks.png")
st.sidebar.markdown("##")
st.sidebar.text('ZURISADDAI REYES JUÁREZ')
st.sidebar.text('Correo Electrónico: zS20006762@estudiantes.uv.mx')

@st.cache
def load_data(nrows):
    name_link = codecs.open('books.csv','rU','latin1')
    data = pd.read_csv(name_link, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis=1, inplace=True)
    #data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def filter_data_by_title(book):
    filtered_data_title = data[data['title'].str.upper().str.contains(book)]
    return filtered_data_title

def filter_data_by_authors(authors):
    filtered_data_authors = data[data['authors'] == authors]
    return filtered_data_authors

data_load_state = st.text('cargando')
data = load_data(500)
data_load_state.text('Good Reads Books!! (using st.cache)')

if st.sidebar.checkbox('Mostrar todos los Libros'):
    st.subheader('Todos los Libros')
    st.write(data)

tituloLibro = st.sidebar.text_input('Titulo del Libro :')
btnBuscar = st.sidebar.button('Buscar Libro')

if (btnBuscar):
   data_title = filter_data_by_title(tituloLibro.upper())
   count_row = data_title.shape[0]  # Gives number of rows
   st.write(f"Total libros mostrados : {count_row}")
   st.dataframe(data_title)



selected_autor = st.sidebar.selectbox("Seleccionar Autor", data['authors'].unique())
btnFilterbyAutor = st.sidebar.button('Filtrar Autor')

if (btnFilterbyAutor):
   filterbydir = filter_data_by_authors(selected_autor)
   count_row = filterbydir.shape[0]  # Gives number of rows
   st.write(f"Total Libros : {count_row}")
   st.dataframe(filterbydir)

st.dataframe(data)
st.markdown("___")

#Multiselect
authors = st.sidebar.multiselect("Selecciona Autores(as)",
                                options=data['authors'].unique())

df_selection=data.query("authors == @authors")
st.write("Autores(as) Seleccionados",df_selection)

#---HISTOGRAMAS---#
sidebar = st.sidebar
st.sidebar.text('GRÁFICAS:')
agree = sidebar.checkbox("Histograma año de Publicación")
if agree:
  fig_genre=px.bar(data,
                    x=data[DATE_COLUMN],
                    y= data.index, #index es para que cuente la cantidad total
                    orientation="v",
                    title="Año en el que se publico cada Libro",
                    labels=dict(y="index", x="publication_date"),
                    color_discrete_sequence=["#7ECBB4"],
                    template="plotly_white")
  st.plotly_chart(fig_genre)

  st.markdown("**Explicación de la Gráfica**")
  st.markdown("En está gráfica se da a conocer los datos del año de publicación de cada libro.")
  st.markdown("___")

#if st.sidebar.checkbox('Histograma año de Publicación'):

    #st.subheader('Año de Publicación del Libro--HISTOGRAMA')

    #hist_values = np.histogram(data[DATE_COLUMN].dt.year,bins=2030, range=(0,2030))[0]

    #st.bar_chart(hist_values)

    #st.markdown("**Explicación de la Gráfica**")
    #st.markdown("En está gráfica se da a conocer los datos del año de publicación de cada libro.")
    #st.markdown("___")
#---GRÁFICA DE BARRAS---#

if st.sidebar.checkbox('Lenguaje del Libro'):
    st.subheader('Language of Books -- GRÁFICA DE BARRAS')

    fig, ax = plt.subplots()

    x_pos = data['language_code']
    y_pos = data['text_reviews_count']
    
    ax.bar(x_pos, y_pos,color = "#446000")

    ax.set_xlabel("Lenguaje Original")
    ax.set_ylabel("Reviews Book")
    ax.set_title('Gráfica de Barras de Lenguaje')
    st.pyplot(fig)

    st.markdown("**Explicación de la Gráfica**")
    st.markdown("En está gráfica se da a conocer el lenguaje original del libro de igual manera el reviews de está.")
    st.markdown("___")

#Chart to visualize the performance score distribution 
#name_link = pd.DataFrame()

#diagrama de SCATTER
#if st.sidebar.checkbox('Rating Average of Books'):
 #   st.subheader('Rating Average of Books -- SCATTER')

  #  fig, ax = plt.subplots()

   # x_pos = data['publication_date']
    #y_pos = data['average_rating']
    
    #ax.scatter(x_pos, y_pos,color = "#005242")

    #ax.set_xlabel("Año de Publicación")
   # ax.set_ylabel("Rating Average")
    #ax.set_title('Gráfica Scatter de Rating')
    #st.pyplot(fig)

    #st.markdown("**Explicación de la Gráfica**")
    #st.markdown("En está gráfica se da a conocer el rating medio que tuvo el libro en el año que se publico.")
    #st.markdown("___")


#::::::::::: grafica scatter :::::::::::

agree = sidebar.checkbox("Rating Average of Books")
if agree:
    st.header("Rating Average of Books -- SCATTER")
    year=data['publication_date']
    title=data['title']
    dnce=data['average_rating']
    fig_age=px.scatter(data,
                   x=year,
                   y=dnce,
                   color=title,
                   labels=dict(year="Publicación", title="Book", dnce="Rating"),
                   template="plotly_white")
    st.plotly_chart(fig_age)
    st.markdown("**Explicación de la Gráfica**")
    st.markdown("En está gráfica se da a conocer el rating medio que tuvo el libro en el año que se publico.")
    sidebar.markdown("___")


