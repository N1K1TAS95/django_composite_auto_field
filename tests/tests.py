from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import now

from tests.models import TestModelA, TestModelB


def mock_now(year):
    def inner_mock_now():
        return timezone.datetime(year, 1, 1, tzinfo=timezone.utc)

    return inner_mock_now


class CompositeAutoFieldTestCase(TestCase):

    def test_auto_increment(self):
        # Crea e salva due istanze del modello di test
        test_model1 = TestModelA.objects.create()
        test_model2 = TestModelA.objects.create()

        # Controlla se i valori del campo custom_code sono diversi
        self.assertNotEqual(test_model1.custom_code, test_model2.custom_code)

    def test_prefix(self):
        # Crea un'istanza del modello di test
        test_model = TestModelA.objects.create()

        # Controlla se il prefisso è corretto
        self.assertTrue(test_model.custom_code.startswith('AA'))

    def test_year_change(self):
        # Crea un modello nell'anno corrente
        test_model_current_year = TestModelA()
        test_model_current_year.save()

        # Avanza l'anno corrente di un anno
        next_year = now().year + 1

        # Utilizza un decoratore per sovrascrivere il metodo now() di timezone
        with patch('django.utils.timezone.now', new=mock_now(next_year)):
            # Crea un modello nell'anno successivo
            test_model_next_year = TestModelA()
            test_model_next_year.save()

            # Verifica che l'anno nel campo custom_code sia stato aggiornato
            current_year = str(test_model_current_year.custom_code[2:4])
            next_year_str = str(test_model_next_year.custom_code[2:4])
            self.assertEqual(next_year_str, str(next_year)[2:])

            # Verifica che il contatore sia stato resettato
            counter_current_year = int(test_model_current_year.custom_code[4:])
            counter_next_year = int(test_model_next_year.custom_code[4:])
            self.assertEqual(counter_current_year + 1, counter_next_year)

    def test_zeros(self):
        # Crea e salva un'istanza del modello di test
        test_model = TestModelA.objects.create()

        # Controlla se il numero di zeri è corretto
        number_of_zeros = 4
        zeros = test_model.custom_code[4:4 + number_of_zeros]
        self.assertEqual(len(zeros), number_of_zeros)

    def test_prefix_variations(self):
        test_model_a = TestModelA.objects.create()
        test_model_b = TestModelB.objects.create()

        self.assertTrue(test_model_a.custom_code.startswith('AA'))
        self.assertTrue(test_model_b.custom_code.startswith('BB'))

    def test_zeros_variations(self):
        test_model_a = TestModelA.objects.create()
        test_model_b = TestModelB.objects.create()

        number_of_zeros_a = 4
        number_of_zeros_b = 5

        zeros_a = test_model_a.custom_code[4:4 + number_of_zeros_a]
        zeros_b = test_model_b.custom_code[2:2 + number_of_zeros_b]

        self.assertEqual(len(zeros_a), number_of_zeros_a)
        self.assertEqual(len(zeros_b), number_of_zeros_b)

    def test_custom_code_override(self):
        custom_code_value = 'AA230001'
        test_model_a = TestModelA.objects.create(custom_code=custom_code_value)
        self.assertEqual(test_model_a.custom_code, custom_code_value)
