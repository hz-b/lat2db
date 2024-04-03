import at

from lat2db.model.accelerator import Accelerator

acc = Accelerator("6602a1b4ea5f066ab6e502af")
element_coordinate = acc.machine.retrieve_element_coordinate("Q5M1T1R")
filter_res_h = acc.machine.filter_element_by_tags("sextupoles",["H"])
filter_res_v = acc.machine.filter_element_by_tags("sextupoles",["V"])
orbit = acc.ring.find_orbit(at.All)

