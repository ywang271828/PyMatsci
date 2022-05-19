import os
from pyMatsci.engines.vasp.vaspout import VaspOut

class Outcar:
    """
    Developed and tested on VASP 5.4.4.
    """

    KEYS_in_ORDER = [
                        "successful", "energy_sigma_0", "elapsed", "total_mag", "mag_up", "mag_down", \
                        "problems", "ionic_steps", "NIONS", "NKPTS", "ENCUT", "ISPIN", "ISIF", "ISYM", "NBANDS", \
                        "POTCAR", "IBRION", "ISMEAR", "SIGMA", "PREC", "EDIFF", "EDIFFG", "NSW", "NELM", \
                        "NELECT", "NPAR", "LORBIT", "total_cores", "NCORES_PER_BAND", "start_time", \
                        "vasp_version", "vasp_built_time" \
                    ]

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_path_abs = os.path.abspath(file_path)
        self.results = Outcar.init()

        results = Outcar.parse_outcar(self.file_path)
        for key in self.results.keys():
            if key in results:
                self.results[key] = results[key]

    def init():
        results = {}
        # Structure
        results["NIONS"] = 0

        # Results
        results["successful"] = False
        results["energy_sigma_0"] = float("nan")
        results["total_mag"] = float("nan")
        results["mag_up"] = float("nan")
        results["mag_down"] = float("nan")
        results["ionic_steps"] = 0
        results["elapsed"] = float("nan")
        results["problems"] = ["None"]

        # Calculation Settings
        results["ENCUT"] = float("nan")
        results["ISPIN"] = "nan"
        results["ISIF"] = "nan"
        results["ISYM"] = "nan"
        results["IBRION"] = "nan"
        results["ISMEAR"] = float("nan")
        results["SIGMA"] = float("nan")
        results["PREC"] = "nan"
        results["EDIFF"] = float("nan")
        results["EDIFFG"] = float("nan")
        results["NSW"] = "nan"
        results["NELM"] = "nan"
        results["NELECT"] = "nan"
        results["NBANDS"] = 0
        results["NKPTS"] = 0
        results["NPAR"] = 0
        results["POTCAR"] = "nan"  # Title of functional of each element.
        results["LORBIT"] = "nan"

        # Job Setting
        results["total_cores"] = 0
        results["NCORES_PER_BAND"] = 0
        results["start_time"] = "nan"
        results["vasp_version"] = "nan"
        results["vasp_built_time"] = "nan"

        return results

    def parse_outcar(file_path):
        """
        Parse OUTCAR and return extracted values in a dict.

        For OUTCARs of ionic relaxation (i.e. multiple ionic steps), only the final state is read
        and return (for now).

        TODO: Return values as a list for calculations with multiple ionic steps. Or make two
              sets of functions, one for the final state and the other for all ionic steps.

        Hard-coded interested values:
            # Structure
            NIONS;
            
            # Results:
            successful; energy_sigma_0; total_mag; mag_up; mag_down; ionic_steps; elapsed;
            
            # Calc settings (INCAR, POTCAR, KPOINTS)
            ENCUT; ISPIN; ISIF; ISYM; NBANDS; NKPTS; PREC; EDIFF; EDIFFG; IBRION; ISMEAR; 
            NSW; NELM; NELECT; NPAR; POTCAR; LORBIT
            
            # Running config
            total_cores; NCORES_PER_BAND; start_time; vasp_version; vasp_built_time;
        
        Extracting some of the values depends on the sequence of extracting values. For example,
        reading mag_up and mag_down requires the knowledge of NIONS. The values are extracted in
        the order of OUTCAR.

        Note:
        1. If the calculation fails, it attempts to read "vasp.out" or "stdout" in the same folder
           to find an error message about the cause of failure.
        2. If the calculation fails, the "energy_sigma_0" and a few other parameters are from the
           last reported ionic/electronic step.
        3. Even if the calculation succeeded, there could still exist a problem. For example,
           highest band is filled during some steps of the run and the final result could be off.
           Always check "problems".
        """
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        results = {}
        results["problems"] = []
        ispin = 1; lorbit = 0
        for i in range(0, len(lines)):
            line = lines[i]
            terms = line.split()
            if i == 0 and "build" in line:
                terms = line.split("(") # Some versions have a long name and the string is padded.
                version = terms[0].strip().replace(" ", "_")
                built_time = terms[1].split(")")[0].replace("build ", "").replace(" ", "_")

                results["vasp_version"] = version
                results["vasp_built_time"] = built_time
            elif "executed on" in line:
                start_time = "{:s}_{:s}".format(terms[4], terms[5])
                results["start_time"] = start_time
            elif "running on" in line:
                total_core = int(terms[2])
                results["total_cores"] = total_core
            elif "NCORES_PER_BAND" in line:
                results["NCORES_PER_BAND"] = int(terms[5])
                results["NPAR"] = int(terms[-2])
            elif "ENCUT" in line:
                results["ENCUT"] = float(terms[2]) # eV
            elif "ISPIN" in line:
                results["ISPIN"] = int(terms[2])
                ispin = results["ISPIN"]
            elif "ISIF" in line:
                results["ISIF"] = int(terms[2])
            elif " ISYM " in line:
                results["ISYM"] = int(terms[2])
            elif "IBRION" in line:
                results["IBRION"] = int(terms[2])
            elif "ISMEAR" in line:
                results["ISMEAR"] = int(terms[2].strip(";"))
                results["SIGMA"] = float(terms[5])
            elif "PREC" in line:
                results["PREC"] = terms[2]
            elif "stopping-criterion for ELM" in line:
                results["EDIFF"] = float(terms[2])
            elif "EDIFFG" in line:
                results["EDIFFG"] = float(terms[2])
            elif "NSW" in line:
                results["NSW"] = int(terms[2])
            elif "NELECT" in line:
                results["NELECT"] = int(float(terms[2]))
            elif "NELM " in line:
                results["NELM"] = int(terms[2].strip(";"))
            elif "NBANDS" in line:
                if "NBANDS" not in line:
                    results["NBANDS"] = int(terms[-1])
                    results["NKPTS"] = int(terms[3])
                elif "the highest band":
                    results.append("Highest_band_filled")
            elif "TITEL" in line:
                terms = line.split("=")
                if "POTCAR" not in results:
                    results["POTCAR"] = [terms[1].strip().replace(" ", "_")]
                else:
                    results["POTCAR"].append(terms[1].strip().replace(" ", "_"))
            elif "LORBIT" in line:
                results["LORBIT"] = int(terms[2])
                lorbit = results["LORBIT"]
            elif "GGA    =" in line:
                results["functional"] = terms[2]
            elif "NIONS" in line:
                results["NIONS"] = terms[-1]
            elif ispin == 2 and lorbit >= 11 and "magnetization (x)" in line:
                # TODO: check whether "lorbit >= 11" is a correct condition. 
                # i.e. mag in written out for each ion.
                j = i + 4   # a second counter
                positive = negative = 0.0
                while j < len(lines):
                    line = lines[j]
                    if not line.split()[0].isdigit():
                        break
                    mag_partial = float(lines[j].split()[-1])
                    if mag_partial >= 0:
                        positive += mag_partial
                    else:
                        negative += mag_partial
                    j += 1
                else:
                    # Calculation not finished successfully and stops in the middle of writing
                    # the mag list.
                    positive = negative = float("nan")
                results["mag_up"] = positive
                results["mag_down"] = negative
            elif ispin == 2 and "number of electron" in line and "magnetization  " in line:
                results["total_mag"] = float(terms[-1]) # The same as in OSZICAR.
            elif "reached required accuracy" in line:
                # TODO: might not be the case for all calculations. Like static.
                results["successful"] = True
            elif "energy  without entropy" in line:
                results["energy_sigma_0"] = terms[-1]
            elif "- Iteration" in line:
                results["ionic_steps"] = int(line.split("(")[0].split()[-1])
            elif "Elapsed" in line:
                results["elapsed"] = float(terms[-1])
            elif "Error EDDDAV: Call to ZHEGV failed." in line:
                results["successful"] = False
                results["problems"].append("Error_EDDDAV")

        # Sanity check.
        if "elapsed" not in results:
            results["successful"] = False
        
        # Check possbile problems:
        if results["ionic_steps"] == results["NSW"] and results["NSW"] >= 1:
            results["successful"] = False
            results["problems"].append("Reach_ionic_step_limit")

        # Deemed not successful but can't find an error message in OUTCAR.
        # Try to look at "stdout" or "vasp.out".
        if not results["successful"]:
            if len(results["problems"]) == 0:
                parent_dir = os.path.dirname(os.path.abspath(file_path))
                if os.path.exists(os.path.join(parent_dir, "vasp.out")):
                    vaspout = os.path.join(parent_dir, "vasp.out")
                elif os.path.exists(os.path.join(parent_dir, "stdout")):
                    vaspout = os.path.join(parent_dir, "stdout")
                problems = VaspOut.find_fail_cause(vaspout)
                results += problems

                # Still unknown.
                if len(results["problems"]) == 0:
                    results["problems"].append("Unknown_without_wall_time")
        else:
            # The calculation could successfully finish but with a potential problem.
            # Like Highest band occupied in some ionic steps (not necessarily the last step).
            if len(results["problems"]) == 0:
                results["problems"].append("None")
        
        return results

    def help():
        """
        Print a list of parameters currently monitored in this class, separated by space.
        """
        results = Outcar.init()
        string = "file_path "
        for key in Outcar.KEYS_in_ORDER:
            string += key + " "
        return string.strip()

    def __str__(self):
        """
        Formatted output without headers in a curated order.
        """
        string = self.file_path_abs + " "
        for key in Outcar.KEYS_in_ORDER:
            if key == "POTCAR":
                str_potcar = ""
                for i in self.results["POTCAR"]:
                    str_potcar += i + ";"
                string += str_potcar.strip(";") + " "
            elif key == "problems":
                pass
            else:
                string += str(self.results[key]) + " "
        return string.strip()

