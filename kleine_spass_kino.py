import sys
import random
from abc import ABC, abstractmethod


# Interface
class BisaDicetak(ABC):
    @abstractmethod
    def cetak(self):
        pass


# Encapsulation
class Kursi:
    def __init__(self, nomor):
        self.__nomor = nomor
        self.__terpesan = False

    def get_nomor(self):
        return self.__nomor

    def is_terpesan(self):
        return self.__terpesan

    def pesan(self):
        if self.__terpesan:
            raise ValueError(f"Kursi {self.__nomor} sudah terbooking")
        self.__terpesan = True

    def is_berhadiah(self):
        return False


# Inheritance
class KursiHadiah(Kursi):
    def is_berhadiah(self):
        return True


# Tiket mengimplementasikan interface BisaDicetak.
# Relasi has-a: Tiket memiliki kumpulan Kursi.
class Tiket(BisaDicetak):
    def __init__(self, kursi):
        self.__kursi = tuple(kursi)

    def cetak(self):
        nomor = ", ".join(k.get_nomor() for k in self.__kursi)

        print("  Tiket tercetak anda anda :")
        print()
        print("  " + "#" * 39)
        self.__baris("Kino KleinSpass")
        self.__baris(f"Nomer bangku : {nomor}")
        self.__baris("")

        for kursi in self.__kursi:
            if kursi.is_berhadiah():
                self.__baris("Anda beruntung,")
                self.__baris(
                    f"{kursi.get_nomor()} silahkan cek bawah kursi anda"
                )

        print("  " + "#" * 39)

    def __baris(self, teks):
        print(f"  ## {teks:<33} ##")


# Relasi has-a: Kino memiliki 24 Kursi.
class Kino:
    def __init__(self):
        self.__kursi = {}

    def __siapkan_kursi(self, gifts_number):
        if type(gifts_number) is not int or not 0 <= gifts_number <= 24:
            raise ValueError(
                "Jumlah hadiah harus bilangan bulat dari 0 sampai 24."
            )

        nomor_kursi = [
            baris + str(i)
            for baris in "ABCD"
            for i in range(1, 7)
        ]

        hadiah = set(random.sample(nomor_kursi, gifts_number))
        self.__kursi = {}

        for nomor in nomor_kursi:
            if nomor in hadiah:
                self.__kursi[nomor] = KursiHadiah(nomor)
            else:
                self.__kursi[nomor] = Kursi(nomor)

    def __tampilkan_denah(self, tampilkan_hadiah=False):
        print("\n" + "X" * 30)
        print("X" + " " * 28 + "X")
        print("X" + "Kinoleinwand".center(28) + "X")
        print("X" + " " * 28 + "X")
        print("X" * 30)

        for baris in "ABCD":
            atas = []
            tengah = []

            for i in range(1, 7):
                kursi = self.__kursi[baris + str(i)]

                simbol = "XXXX"
                if tampilkan_hadiah and kursi.is_berhadiah():
                    simbol = "GIFT"

                atas.append(simbol)

                if kursi.is_terpesan():
                    tengah.append("XXXX")
                else:
                    tengah.append(f"X{kursi.get_nomor()}X")

            print()
            print(" ".join(atas))
            print(" ".join(tengah))
            print(" ".join(atas))

    def beli_tiket(self, masukan):
        nomor_kursi = [
            nomor.strip().upper()
            for nomor in masukan.split(",")
        ]

        if any(not nomor for nomor in nomor_kursi):
            raise ValueError(
                "Masukkan nomor kursi, misalnya A3, A4, A5."
            )

        if len(nomor_kursi) != len(set(nomor_kursi)):
            raise ValueError("Nomor kursi tidak boleh berulang.")

        # Periksa semua kursi sebelum melakukan pemesanan.
        for nomor in nomor_kursi:
            if nomor not in self.__kursi:
                raise ValueError(
                    f"Kursi {nomor} tidak tersedia. Pilih A1 sampai D6."
                )

            if self.__kursi[nomor].is_terpesan():
                raise ValueError(f"Kursi {nomor} sudah terbooking")

        kursi_dipilih = [
            self.__kursi[nomor]
            for nomor in nomor_kursi
        ]

        for kursi in kursi_dipilih:
            kursi.pesan()

        return Tiket(kursi_dipilih)

    def laporan(self):
        self.__tampilkan_denah(tampilkan_hadiah=True)

        semua = list(self.__kursi.values())

        terpesan = sum(
            kursi.is_terpesan()
            for kursi in semua
        )

        total_hadiah = sum(
            kursi.is_berhadiah()
            for kursi in semua
        )

        hadiah_diberikan = sum(
            kursi.is_berhadiah() and kursi.is_terpesan()
            for kursi in semua
        )

        print(f"\nBooked/Available: {terpesan}/{len(semua)}")
        print(f"Total/Delivered Gift: {total_hadiah}/{hadiah_diberikan}")

    def starts(self, gifts_number):
        self.__siapkan_kursi(gifts_number)
        self.__tampilkan_denah()

        while True:
            print("\nMenu Utama:")
            print("1. Membeli ticket?")
            print("2. Laporan bangku terpesan, berhadiah dan kosong?")
            print("3. Exit")

            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                print("\n1. Membeli ticket?\n")
                masukan = input("  Masukkan nomer kursi: ")

                try:
                    tiket = self.beli_tiket(masukan)
                    tiket.cetak()
                except ValueError as error:
                    print("  " + str(error))

            elif pilihan == "2":
                print(
                    "\n2. Laporan bangku terpesan, berhadiah dan kosong?"
                )
                self.laporan()

            elif pilihan == "3":
                break

            else:
                print("Pilih menu 1, 2, atau 3.")

    # Mendukung nama start() maupun starts() sesuai soal.
    def start(self, gifts_number):
        self.starts(gifts_number)


# Main program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cara menjalankan: python kleine_spass_kino.py 3")
        sys.exit(1)

    try:
        jumlah_hadiah = int(sys.argv[1])

        kino = Kino()
        kino.starts(jumlah_hadiah)

    except ValueError as error:
        print(error)
        sys.exit(1)

    except (EOFError, KeyboardInterrupt):
        print("\nProgram ditutup.")