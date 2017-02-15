import unittest
import pychemia
from pychemia.utils.serializer import generic_serializer
import numpy as np


class PopulationTest(unittest.TestCase):
    def test_orbital(self):
        """
        Tests (pychemia.population.OrbitalDFTU)                      :
        """
        if not pychemia.db.has_connection():
            return

        pychemia_path = pychemia.__path__[0]
        abiinput = pychemia.code.abinit.InputVariables(pychemia_path + '/test/data/abinit_dmatpawu/abinit.in')
        dmatpawu = np.array(abiinput['dmatpawu']).reshape(-1, 5, 5)
        params = pychemia.population.orbitaldftu.dmatpawu2params(dmatpawu, 5)
        dmatpawu_new = pychemia.population.orbitaldftu.params2dmatpawu(params)

        self.assertLess(np.min(dmatpawu-dmatpawu_new), 0.01)

        with self.assertRaises(ValueError) as context:
            pychemia.population.orbitaldftu.OrbitalDFTU('test', '/tmp/no_abinit.in')

        with self.assertRaises(ValueError) as context:
            pychemia.population.orbitaldftu.OrbitalDFTU('test', input_path=pychemia_path +
                                                        '/test/data/abinit_01/abinit.in')

        popu = pychemia.population.orbitaldftu.OrbitalDFTU('test', input_path=pychemia_path +
                                                           '/test/data/abinit_dmatpawu/abinit.in')

        ea = [[-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0],
              [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        params['euler_angles'] = ea
        params = generic_serializer(params)
        entry_id = popu.new_entry(params)

        ea = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
              [-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        params['euler_angles'] = ea
        params = generic_serializer(params)
        entry_jd = popu.new_entry(params)

        popu.add_random()
        popu.random_population(16)
        popu.cross([entry_id, entry_jd])
        print(popu)

        self.assertFalse(popu.is_evaluated(entry_id))

        popu.check_duplicates(popu.members)

        entry_idm = popu.move_random(entry_id)
        popu.get_entry(entry_idm, {'properties': 1})

        entry_imj = popu.move(entry_id, entry_jd)
        popu.get_entry(entry_imj, {'properties': 1})
