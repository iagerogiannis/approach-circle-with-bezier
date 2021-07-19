class ScreenPrinter:

    @staticmethod
    def print_results(i, parameters, error_f):

        def print_headers():
            print("Iter      {:<25} {:<25} {:<25} {:<25} {:<25} {:<25}".format("Parameter a", "Parameter b",
                                                                               "Parameter c", "Parameter d",
                                                                               "Parameter e", "Error Function"))
            print(160 * "-")

        if i % 20 == 0:
            print_headers()

        print("{:<4} :    {:<25} {:<25} {:<25} {:<25} {:<25} {:<25}".format(str(i), *parameters, error_f))
