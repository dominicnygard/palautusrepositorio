"""Module containing the Varasto (Warehouse) class for managing storage."""


class Varasto:
    """A class representing a warehouse with limited capacity."""

    def __init__(self, tilavuus, alku_saldo=0):
        """Initialize the warehouse with volume and optional initial balance."""
        self.tilavuus = self._validoi_tilavuus(tilavuus)
        self.saldo = self._validoi_saldo(alku_saldo, self.tilavuus)

    def _validoi_tilavuus(self, tilavuus):
        """Validate and return the volume. Returns 0 if invalid."""
        if tilavuus > 0.0:
            return tilavuus
        return 0.0

    def _validoi_saldo(self, alku_saldo, tilavuus):
        """Validate and return the initial balance."""
        if alku_saldo < 0.0:
            return 0.0
        if alku_saldo <= tilavuus:
            return alku_saldo
        return tilavuus

    def paljonko_mahtuu(self):
        """Return how much space is available in the warehouse."""
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        """Add items to the warehouse."""
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        """Take items from the warehouse. Returns the amount actually taken."""
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0
            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara
        return maara

    def __str__(self):
        """Return string representation of the warehouse."""
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
