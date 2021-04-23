import unittest
import SPD1i2i3 as rpq


class TestRPQ_data10(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data10.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 927)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 746)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 746)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 687)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 687)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    def test_carlier(self):
        nowe_zadania = rpq.carlier(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 641)

class TestRPQ_data20(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data20.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 1905)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 1594)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 1594)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1299)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1299)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    def test_carlier(self):
        nowe_zadania = rpq.carlier(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1267)

class TestRPQ_data50(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data50.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 2843)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 1915)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 1915)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1513)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1513)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    def test_carlier(self):
        nowe_zadania = rpq.carlier(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 1492)

class TestRPQ_data100(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data100.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 5324)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 3936)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 3936)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 3076)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 3076)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    def test_carlier(self):
        nowe_zadania = rpq.carlier(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 3070)

class TestRPQ_data200(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data200.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 11109)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 8210)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 8210)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 6416)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 6416)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    #def test_carlier(self):
    #    nowe_zadania = rpq.carlier(self.zadania)
    #    self.assertEqual(rpq.calculate_Cmax(nowe_zadania), ?)

class TestRPQ_data500(unittest.TestCase):
    def setUp(self):
        self.zadania = rpq.loadData("data/data500.txt")

    def test_1234(self):
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 26706)

    def test_sortR(self):
        rpq.sortR(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 19609)

    def test_sortRQ(self):
        rpq.sortRQ(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(self.zadania), 19609)

    def test_schrage(self):
        nowe_zadania = rpq.schrage(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 14822)

    def test_schrageWithHeap(self):
        nowe_zadania = rpq.schrageWithHeap(self.zadania)
        self.assertEqual(rpq.calculate_Cmax(nowe_zadania), 14822)

    #def test_schragePMTN(self):
    #    self.assertEqual(rpq.schragePMTN(self.zadania), ?)

    #def test_schragePMTNWithHeap(self):
    #    self.assertEqual(rpq.schrageWithHeap(self.zadania), ?)

    #def test_carlier(self):
    #    nowe_zadania = rpq.carlier(self.zadania)
    #    self.assertEqual(rpq.calculate_Cmax(nowe_zadania), ?)



# ----- Main ----- #
if __name__ == '__main__':
    unittest.main()