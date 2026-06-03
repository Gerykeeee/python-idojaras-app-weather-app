import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WeatherApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Időjárás App")
        self.geometry("400x500")

        self.label_title = ctk.CTkLabel(self, text="Időjárás", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.entry_city =ctk.CTkEntry(self, placeholder_text=("Város neve..."), width=250)
        self.entry_city.pack(pady=10)

        self.button_search = ctk.CTkButton(self, text=('Lekérdezés'), command=self.weather)
        self.button_search.pack(pady=10)

        self.result_frame = ctk.CTkFrame(self, width=350, height=250)
        self.result_frame.pack(pady=20, padx=(20), fill="both", expand=True)

        self.label_city_name = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 20, "bold"))
        self.label_city_name.pack(pady=10)

        self.label_temp = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 40))
        self.label_temp.pack(pady=5)

        self.label_desc = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 14, "italic"))
        self.label_desc.pack(pady=5)

        self.label_advice = ctk.CTkLabel(self.result_frame, text="", font=("Arial", 12), wraplength=300)
        self.label_advice.pack(pady=15)





    def weather(self):
        city = self.entry_city.get().lower()
        if not city:
            return

        api_key = "A_TE_API_KULCSOD"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=hu"

        try:
            valasz = requests.get(url)
            adat = valasz.json()

            if adat["cod"] == 200:
                homerseklet = int(adat["main"]["temp"])
                leiras = adat["weather"][0]["description"]
                paratartalom = adat["main"]["humidity"]

                self.label_city_name.configure(text=city.title())
                self.label_temp.configure(text=f"{homerseklet} Celsius")
                self.label_desc.configure(text=leiras.capitalize())

                
                if homerseklet < 0:
                    advice = "Kelleni fog a nagykabát :D "
                elif homerseklet < 15:
                    advice = "Átmeneti kabát :) "
                elif homerseklet < 22:
                    advice = "Pulcsi kelleni fog.... "
                elif homerseklet < 30:
                    advice = "Póló megfelel.... "
                else:
                    advice = "Ez már nem emberi ! "
                    
                self.label_advice.configure(text=advice)

            else:
                self.label_city_name.configure(text="Hiba!")
                self.label_temp.configure(text="")
                self.label_desc.configure(text="A város nem található")
                self.label_advice.configure(text="")

        except requests.exceptions.RequestException:
            self.label_desc.configure(text="Hiba, nincs internet kapcsolat...")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
    