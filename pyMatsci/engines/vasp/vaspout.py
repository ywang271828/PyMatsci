
class VaspOut:

    def __init__(self, path):
        self.path = path
        

    def find_fail_cause(path):
        """
        Attempt to find the cause of calculation failure.
        """
        problems = []
        with open(path) as file:
            lines = file.readlines()
        # Only look at the bottom of the output file.
        for i in range(len(lines) - 10, len(lines)):
            line = lines[i]
            if "ZBRENT" in line:
                if "fatal error in bracketing" in line:
                    problems.append("ZBRENT_error_bracketing")
                elif "accuracy reached" in line:
                    problems.append("ZBRENT_accuracy_reached")
                else:
                    problems.append("ZBRENT")
            elif "Error EDDDAV:" in line:
                if "Call to ZHEGV failed.":
                    terms = line.split()
                    # Also put the return codes in there. These codes might be different.
                    problems.append("Error_EDDDAV_ZHEGV_{:s}_{:s}_{:s}".format(terms[-3], terms[-2], terms[-1]))
                else:
                    problems.append("Error_EDDDAV")
        return problems
                    

            
