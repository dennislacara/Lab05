import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio
from datetime import datetime
from flet import Row

data = datetime.now().date()
FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD)

    # TextField per responsabile
    input_responsabile = ft.TextField( label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label = 'Marca')
    input_modello = ft.TextField(label='Modello')
    input_anno = ft.TextField(label='Anno')

    # Tutti i TextField per le info necessarie per il noleggio di un automobile
    input_idAuto = ft.TextField(label='Codice univoco automobile')
    input_cognomeCliente = ft.TextField(label='Cognome del cliente')

    # ------------------------------------------Costruzione del counter ------------------------------------------------
    counterTextField = ft.TextField(label = 'Posti',width=100, text_size=24,
                           disabled = True, border_color="green",
                           text_align=ft.TextAlign.CENTER)
    #auto di almeno un posto
    counterTextField.value = 1

    def handlerMinus(e):
        currentVal = counterTextField.value
        if(currentVal > 1):
            currentVal = currentVal - 1
            counterTextField.value = currentVal
            counterTextField.update()

    def handlerPlus(e):
        currentVal = counterTextField.value
        currentVal = currentVal + 1
        counterTextField.value = currentVal
        counterTextField.update()


    btnMinus = ft.IconButton(icon = ft.Icons.REMOVE_CIRCLE_ROUNDED,
                             icon_size = 24, icon_color = "green",
                             on_click=handlerMinus)
    btnPlus = ft.IconButton(icon = ft.Icons.ADD_CIRCLE_ROUNDED,
                            icon_size = 24, icon_color = "green",
                            on_click=handlerPlus)
    # TODO

    # --------------------------------------------- FUNZIONI APP -------------------------------------------------------
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # ----------------------------------------- HANDLERS APP -------------------------------------------------------
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        input_responsabile.value = ''
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento/noleggio di un auto
    def aggiungi_auto(e):
        try:
            marca, modello, anno, posti = input_marca.value, input_modello.value, input_anno.value, counterTextField.value
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            print("Automobile aggiunta alla struttura dati dell'autonoleggio")
        except ValueError as a:
            print(f'ValueError: {a}; Linea 69 di Lab05/main.py')
            alert.show_alert('Errore: inserisci valori numerici validi per anno e posti!')
        aggiorna_lista_auto()

        #pulizia dei campi di testo della pagina
        for campo in [input_marca, input_modello, input_anno]:
            campo.value = ""
        counterTextField.value = 1

        page.update()
    # TODO

    def noleggio_automobili(e):
        try:
            autonoleggio.nuovo_noleggio(data, input_idAuto.value, input_cognomeCliente.value)
        except Exception as a:
            alert.show_alert('Errore: codice univoco automobile non trovato')
            print(a)
        aggiorna_lista_auto()

        for campo in [input_idAuto, input_cognomeCliente]:
            campo.value = ""
        page.update()

    # ---------------------------------------EVENTI ---------------------------------------------------
    #bottone per gestire il tema
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    #bottone per gestire il responsabile
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    # Bottoni per la gestione dell'inserimento/noleggio di una nuova auto
    pulsante_aggiungi_automobile = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_auto)
    pulsante_noleggio = ft.ElevatedButton("Avvia noleggio", on_click=noleggio_automobili)

    # ---------------------------------------------LAYOUT ---------------------------------------------
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=30,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        ft.Text(value='Aggiungi nuova automobile', size=20),
        ft.Row(spacing=8,
               controls=[input_marca, input_modello, input_anno, btnMinus, counterTextField, btnPlus],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_aggiungi_automobile], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        # TODO

        #sezione 4 (extra)
        ft.Text(value='Noleggio', size=20),
        ft.Row(spacing=30, controls=[input_idAuto, input_cognomeCliente], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_noleggio], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 5
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
