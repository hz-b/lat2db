
def update_quad(machine):
    if "quadrupoles" in machine:
        # you should be able to call your normal quad update after a new record is created
        # e.g: simply call two functions under the new service (duplicateMachine)
        # whenever the duplicate machine service is called from UI then call two functions
        #   1. create new machine
        #       1.1 get existing machine call the service (see get_machine_output.py)
        #       1.2 make your changes (change name and assign a new id)
        #       1.3 insert the updated machine into db
        #   2. update quad (this you already have) just move the functionality under a function
        #   and move that function to a different file called machine_update_helper.
        #   this function should be dynamic so that a quad/sextupole or any other type of element can be updated.
        #   this means you don't write  the code again and again with very little changes.

        if "quadrupoles" in machine:
            quadrupoles_list = machine.get("quadrupoles", [])
            sequences_list = machine.get("sequences", [])
            operations = None
            difference = 0
            for quad_index, quad in enumerate(quadrupoles_list):
                print("quad indexis ", quad_index)
                if quad.get("name") == request_body.updated_data.name:
                    quad_length = quad.get("length")
                    if float(quad_length) > float(request_body.updated_data.length):
                        operations = "+"
                        difference = float(quad_length) - float(request_body.updated_data.length)
                    else:
                        operations = "-"
                        difference = float(request_body.updated_data.length) - float(quad_length)

                    removed_quadrupole = quadrupoles_list.pop(quad_index)
                    update_data_dict = request_body.updated_data

                    quadrupoles_list.insert(quad_index, asdict(request_body.updated_data))
                    break

            database.update_one({"id": str(pre_id)}, {"$set": {"quadrupoles": quadrupoles_list}})
            affected_drift = request_body.affected_drift
            # update sequence
            if "sequences" in machine:
                sequences_list = machine.get("sequences", [])
                for item_index, item in enumerate(sequences_list):
                    if item.get("name") == request_body.updated_data.name and item.get("type") == "Quadrupole":
                        removed_quadrupole = sequences_list.pop(item_index)
                        # affected_drift=item.get("index")
                        print("******* affected drif index is ", affected_drift)
                        sequences_list.insert(item_index, asdict(request_body.updated_data))
                        break
                if affected_drift != "-1":
                    for item_index, item in enumerate(sequences_list):
                        if int(item.get("index")) == int(affected_drift):
                            if operations == "+":
                                item["length"] = float(item.get("length")) + difference
                                print("drift length is in seq seq ", item["length"])

                            else:
                                item["length"] = float(item.get("length")) - difference
                                print("drift length is in seq seq ", item["length"])

                            sequences_list[item_index] = item
                            print("**** drift in the sequence is updated")
                            # sequences_list.insert(item_index, asdict(request_body.updated_data))
                            break

            database.update_one({"id": str(pre_id)}, {"$set": {"sequences": sequences_list}})
            # update drift
            print("affected dfridt is ", affected_drift)
            if "drifts" in machine and affected_drift != "-1":
                print("drift update is intiated")
                drift_list = machine.get("drifts", [])
                for drift_index, drift in enumerate(drift_list):
                    if int(drift.get("index")) == int(affected_drift):
                        if operations == "+":
                            drift["length"] = float(drift.get("length")) + difference
                            print("drift length is in drift seq ", drift["length"])
                        else:
                            drift["length"] = float(drift.get("length")) - difference
                            print("drift length is iin drift seq ", drift["length"])
                        break
                database.update_one({"id": str(pre_id)}, {"$set": {"drifts": drift_list}})

                print("**** drift in the drift list is updated")

            return JSONResponse(status_code=200, content={"message": f"Quadrupole updated"})
