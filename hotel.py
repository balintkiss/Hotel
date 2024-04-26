
# Hotel szoba foglalás program, melyben lefoglalhatunk, lemondhatunk szobaszámot, dátumot 
# Lefoglalt szobák, dátumok, árak kilistázása

from abc import ABC, abstractmethod
from datetime import datetime

# Absztrakt alaposztály a különböző szobatípusokhoz
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
    
    @abstractmethod
    def info(self):
        pass # Absztrakt metódus, amit az alosztályokban kell megvalósítani

# Egyágyas szoba osztály
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=50000):
        super().__init__(szobaszam, ar)
    
    def info(self):
        return f"Egyágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"

# Kétágyas szoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=100000):
        super().__init__(szobaszam, ar)
    
    def info(self):
        return f"Ketagyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"

# Szálloda osztály a szálloda működésének kezelésére
class Szalloda:
    def __init__(self, nev):
        self.nev = nev # Szálloda neve
        self.szobak = [] # Szobák listája
        self.foglalasok = [] # Foglalások listája
    
    # Szoba hozzáadása a szállodához
    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)
    
    # Szoba foglalása
    def foglalas(self, szobaszam, kezdet, veg):
        try:
            start_date = datetime.strptime(kezdet, '%Y-%m-%d').date()
            end_date = datetime.strptime(veg, '%Y-%m-%d').date()
        except ValueError:
            return "Érvénytelen dátumformátum."
        if not self._datum_ervenyes(start_date) or not self._datum_ervenyes(end_date) or end_date <= start_date:
            return "Érvénytelen foglalási dátum."
        for foglalas in self.foglalasok:
            if (foglalas.szobaszam == szobaszam and 
                not (end_date < foglalas.kezdet or start_date > foglalas.veg)):
                return "Ez a szoba már foglalt ebben az időszakban."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                napok_szama = (end_date - start_date).days
                teljes_ar = napok_szama * szoba.ar
                self.foglalasok.append(Foglalas(szobaszam, start_date, end_date, teljes_ar))
                return f"\nFoglalás rögzítve. Ár: {teljes_ar} Ft a teljes tartózkodásra ({napok_szama} éj)."
        return "Nincs ilyen szobaszám."
    
    # Foglalás törlése a szállodából
    def foglalas_torles(self, szobaszam, kezdet, veg):
        try:
            kezdet_date = datetime.strptime(kezdet, '%Y-%m-%d').date()
            veg_date = datetime.strptime(veg, '%Y-%m-%d').date()
        except ValueError:
            return "Érvénytelen dátumformátum."

        for i, foglalas in enumerate(self.foglalasok):
            if (foglalas.szobaszam == szobaszam and 
                foglalas.kezdet == kezdet_date and 
                foglalas.veg == veg_date):
                del self.foglalasok[i]
                return f"Foglalás törölve: Szobaszám {szobaszam}, Kezdet: {kezdet}, Vég: {veg}."
        return "Nem található ilyen foglalás."


    # Dátum érvényességének ellenőrzése
    def _datum_ervenyes(self, datum):
        return datum > datetime.now().date()
    
    # Foglalások listázása
    def foglalasok_listaja(self):
        if not self.foglalasok:
            return "Nincsenek aktív foglalások."
        return '\n'.join(f"Szobaszám: {f.szobaszam}, Kezdet: {f.kezdet}, Vég: {f.veg}, Ár: {f.ar} Ft" for f in self.foglalasok)

# Foglalás osztály
class Foglalas:
    def __init__(self, szobaszam, kezdet, veg, ar):
        self.szobaszam = szobaszam
        self.kezdet = kezdet
        self.veg = veg
        self.ar = ar
# Rendelkezésre álló szobák (1-5)
def main_menu():
    szalloda = Szalloda("Budapest Hotel Four Seasons")
    szalloda.szoba_hozzaadas(EgyagyasSzoba(1))
    szalloda.szoba_hozzaadas(EgyagyasSzoba(2))
    szalloda.szoba_hozzaadas(KetagyasSzoba(3))
    szalloda.szoba_hozzaadas(KetagyasSzoba(4))
    szalloda.szoba_hozzaadas(KetagyasSzoba(5))
    
    # Program előtőltése adatokkal
    szalloda.foglalas(1, '2024-05-10', '2024-05-15')  
    szalloda.foglalas(2, '2024-06-01', '2024-06-03')  
    szalloda.foglalas(3, '2024-06-10', '2024-06-12') 
    szalloda.foglalas(2, '2024-07-01', '2024-07-05')  
    szalloda.foglalas(1, '2024-08-15', '2024-08-20')  

    # Program interface a kezeléshez
    while True:
        print("\nBudapest Hotel Four Seasons Booking")
        print("1. Szoba foglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasz = input("Válassz egy opciót: ")
        
        if valasz == '1':
            szobaszam = input("Add meg a szobaszámot (1-2 egyágyas, 3-5 kétágyas): ")
            try:
                szobaszam = int(szobaszam)
                kezdet = input("Add meg a kezdő dátumot (YYYY-MM-DD formátumban): ")
                veg = input("Add meg a vég dátumot (YYYY-MM-DD formátumban): ")
                print(szalloda.foglalas(szobaszam, kezdet, veg))
            except ValueError:
                print("Érvénytelen bemenet.")
        elif valasz == '2':
            szobaszam = input("Add meg a szobaszámot: ")
            try:
                szobaszam = int(szobaszam)
                kezdet = input("Add meg a kezdő dátumot (YYYY-MM-DD formátumban): ")
                veg = input("Add meg a vég dátumot (YYYY-MM-DD formátumban): ")
                print(szalloda.foglalas_torles(szobaszam, kezdet, veg))
            except ValueError:
                print("Érvénytelen bemenet.")
        elif valasz == '3':
            print(szalloda.foglalasok_listaja())
        elif valasz == '4':
            print("Kilépés a foglalásból.")
            break
        else:
            print("Érvénytelen opció.")

if __name__ == "__main__":
    main_menu()
