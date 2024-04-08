import at

from lat2db.model.accelerator import Accelerator

acc = Accelerator("660cfbde6507650b2d41a49e") # accelerator from db
#todo create accelerator from json file
element_coordinate = acc.machine.retrieve_element_coordinate("Q5M1T1R")
filter_res_h = acc.machine.filter_element_by_tags("quadrupoles",["Q2"])
filter_res_v = acc.machine.filter_element_by_tags("sextupoles",["V"])
orbit = acc.ring.find_orbit(at.All)
orbit
