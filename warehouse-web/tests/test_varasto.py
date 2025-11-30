"""Tests for the Varasto class."""
import pytest
from src.varasto import Varasto


class TestVarastoInitialization:
    """Tests for Varasto initialization."""

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Constructor creates an empty warehouse with given volume."""
        varasto = Varasto(10)
        assert varasto.tilavuus == pytest.approx(10)
        assert varasto.saldo == pytest.approx(0)

    def test_konstruktori_luo_varaston_alkusaldolla(self):
        """Constructor creates a warehouse with initial balance."""
        varasto = Varasto(10, 5)
        assert varasto.saldo == pytest.approx(5)

    def test_negatiivinen_tilavuus_nollataan(self):
        """Negative volume is set to 0."""
        varasto = Varasto(-10)
        assert varasto.tilavuus == pytest.approx(0)

    def test_nolla_tilavuus_nollataan(self):
        """Zero volume remains 0."""
        varasto = Varasto(0)
        assert varasto.tilavuus == pytest.approx(0)

    def test_negatiivinen_alkusaldo_nollataan(self):
        """Negative initial balance is set to 0."""
        varasto = Varasto(10, -5)
        assert varasto.saldo == pytest.approx(0)

    def test_ylisuurialkusaldo_tayttaa_varaston(self):
        """Initial balance larger than volume fills the warehouse."""
        varasto = Varasto(10, 50)
        assert varasto.saldo == pytest.approx(10)


class TestPaljonkoMahtuu:
    """Tests for the paljonko_mahtuu method."""

    def test_tyhjalla_varastolla_koko_tilavuus(self):
        """Empty warehouse has full capacity available."""
        varasto = Varasto(10)
        assert varasto.paljonko_mahtuu() == pytest.approx(10)

    def test_tayden_varaston_mahtuu_nolla(self):
        """Full warehouse has no capacity available."""
        varasto = Varasto(10, 10)
        assert varasto.paljonko_mahtuu() == pytest.approx(0)

    def test_osittain_tayden_varaston_tilaa(self):
        """Partially filled warehouse has correct capacity available."""
        varasto = Varasto(10, 3)
        assert varasto.paljonko_mahtuu() == pytest.approx(7)


class TestLisaaVarastoon:
    """Tests for the lisaa_varastoon method."""

    def test_lisays_lisaa_saldoa(self):
        """Adding items increases the balance."""
        varasto = Varasto(10)
        varasto.lisaa_varastoon(5)
        assert varasto.saldo == pytest.approx(5)

    def test_liikaa_lisaaminen_tayttaa_varaston(self):
        """Adding more than capacity fills the warehouse."""
        varasto = Varasto(10)
        varasto.lisaa_varastoon(15)
        assert varasto.saldo == pytest.approx(10)

    def test_negatiivinen_lisays_ei_muuta(self):
        """Adding negative amount does not change balance."""
        varasto = Varasto(10, 5)
        varasto.lisaa_varastoon(-3)
        assert varasto.saldo == pytest.approx(5)

    def test_lisays_taynna_olevaan_varastoon(self):
        """Adding to a full warehouse keeps it full."""
        varasto = Varasto(10, 10)
        varasto.lisaa_varastoon(5)
        assert varasto.saldo == pytest.approx(10)


class TestOtaVarastosta:
    """Tests for the ota_varastosta method."""

    def test_ottaminen_palauttaa_otetun_maaran(self):
        """Taking items returns the taken amount."""
        varasto = Varasto(10, 5)
        otettu = varasto.ota_varastosta(3)
        assert otettu == pytest.approx(3)

    def test_ottaminen_vahentaa_saldoa(self):
        """Taking items decreases the balance."""
        varasto = Varasto(10, 5)
        varasto.ota_varastosta(3)
        assert varasto.saldo == pytest.approx(2)

    def test_liikaa_ottaminen_palauttaa_saldon(self):
        """Taking more than balance returns all balance."""
        varasto = Varasto(10, 5)
        otettu = varasto.ota_varastosta(10)
        assert otettu == pytest.approx(5)

    def test_liikaa_ottaminen_tyhjentaa_varaston(self):
        """Taking more than balance empties the warehouse."""
        varasto = Varasto(10, 5)
        varasto.ota_varastosta(10)
        assert varasto.saldo == pytest.approx(0)

    def test_negatiivinen_otto_palauttaa_nollan(self):
        """Taking negative amount returns 0."""
        varasto = Varasto(10, 5)
        otettu = varasto.ota_varastosta(-3)
        assert otettu == pytest.approx(0)

    def test_negatiivinen_otto_ei_muuta_saldoa(self):
        """Taking negative amount does not change balance."""
        varasto = Varasto(10, 5)
        varasto.ota_varastosta(-3)
        assert varasto.saldo == pytest.approx(5)


class TestStr:
    """Tests for the __str__ method."""

    def test_str_palauttaa_oikean_muodon(self):
        """String representation is correct."""
        varasto = Varasto(10, 3)
        tulos = str(varasto)
        assert "saldo = 3" in tulos
        assert "tilaa 7" in tulos
