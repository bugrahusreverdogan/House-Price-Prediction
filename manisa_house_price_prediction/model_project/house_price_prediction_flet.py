from __future__ import print_function
import pandas as pd
import numpy as np
from  sklearn.model_selection import train_test_split, ShuffleSplit, cross_validate
import xgboost as xgb
import flet as ft
from sklearn.metrics import mean_squared_error, r2_score
from flet import Page, Text, ElevatedButton, Dropdown, dropdown, TextField, Slider, Container, alignment, colors, margin, padding, border_radius, border


def main(page: ft.Page):

    page.title = 'House Price Prediction'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_height = 800
    page.window_width = 1200
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

   
    def function_button_clicked(e):

        if neighborhood.value == "Guzelyurt":
            neighborhood_test = 1
        if neighborhood.value == "Uncubozkoy":
            neighborhood_test = 2
        if neighborhood.value == "Laleli":
            neighborhood_test = 3
        if neighborhood.value == "Yeni Mahalle":
            neighborhood_test = 4
        if neighborhood.value == "Adnan Menderes":
            neighborhood_test = 5
        if neighborhood.value == "Muradiye":
            neighborhood_test = 6
        
        if site_selection.value == "Yes":
            site_selection_test = 1
        if site_selection.value == "No":
            site_selection_test = 0
        
        nsm_test = float(nsm.value)
        nor_test = int(nor.value)
        
        gsm_test = float(gsm.value)
        nob_test = int(nob.value)

        tnofotB_test = int(tnofotB.value)

        pred = prediction_of_price(gsm_test, nsm_test, nob_test, nor_test, neighborhood_test, tnofotB_test, site_selection_test)

        prediction = TextField(value=pred, text_align=ft.TextAlign.CENTER)

        page.add(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                ft.Text(
                "PRICE :",
                size=40,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_600,
                weight=ft.FontWeight.W_100
                ),
                prediction
                ]
            )
        )
        page.update()



    neighborhood = Dropdown(
        label = "Neighborhood",
        hint_text ="Select The Neighborhood",
        options = [
            dropdown.Option("Guzelyurt"),
            dropdown.Option("Uncubozkoy"),
            dropdown.Option("Laleli"),
            dropdown.Option("Yeni Mahalle"),
            dropdown.Option("Adnan Menderes"),
            dropdown.Option("Muradiye"),
        ],
    )
    nsm = TextField(label = "Net Square Meters", hint_text = "Enter Net Square Meters")
    nor = TextField(label = "Number of Rooms", hint_text = "Enter Number of Rooms")
    

    site_selection = Dropdown(
        label = "Inside the site?",
        hint_text ="Select Yes or No",
        options = [
            dropdown.Option("Yes"),
            dropdown.Option("No"),
        ],
    )
    gsm= TextField(label = "Gross Square Meters", hint_text = "Enter Gross Square Meters")
    nob = TextField(label = "Number of Bathrooms", hint_text = "Enter Number of Bathrooms")

    tnofotB = TextField(label = "The Number of Floors of the Building", hint_text = "Enter The Number of Floors of the Building")
    submit_button = ElevatedButton(text="Submit", on_click=function_button_clicked)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.Text(
                "LET US PREDICT YOUR HOUSE PRICE",
                size=40,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_600,
                weight=ft.FontWeight.W_100
                )
                ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                neighborhood,
                nsm,
                nor
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                site_selection,
                gsm,
                nob
            ] 
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                tnofotB,
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                submit_button
                ]
        )
    )

    def prediction_of_price(gsm_test, nsm_test, nob_test, nor_test, neighborhood_test, tnofotB_test, site_selection_test):

        model = xgb.XGBRegressor()
        model.load_model("model_sklearn.json")
        labels= ["Gross Square Meters", "Net Square Meters", "Number of Bathrooms" , "Number of Rooms", "Neighborhood", "The Number of Floors of the Building", "Inside the Site"]
        df = {}
        df = pd.DataFrame(columns = labels)
        df = df.append({
                "Gross Square Meters" : gsm_test,
                "Net Square Meters" :nsm_test,
                "Number of Bathrooms" : nob_test, 
                "Number of Rooms" : nor_test,
                "Neighborhood" : neighborhood_test,
                "The Number of Floors of the Building" : tnofotB_test,
                "Inside the Site" : site_selection_test
            }, ignore_index = True)

        price_prediction = model.predict(df)

        return str(price_prediction[0])

    page.update()

ft.app(target=main)





