# -*- encoding: utf-8 -*-
"""
Demos for the h2o-py library.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import h2o
import linecache
from h2o.utils.compatibility import *  # NOQA



def gbm(interactive=True, echo=True, testing=False):
    """GBM model demo."""
    def demo_body(go):
        """
        Demo of H2O's Gradient Boosting estimator.

        This demo uploads a dataset to h2o, parses it, and shows a description.
        Then it divides the dataset into training and test sets, builds a GLM
        from the training set, and makes predictions for the test set.
        Finally, default performance metrics are displayed.
        """
        go()
        # Connect to H2O
        h2o.init()

        go()
        # Upload the prostate dataset that comes included in the h2o python package
        prostate = h2o.upload_file(h2o.data_file("h2o_data/prostate.csv"))

        go()
        # Print a description of the prostate data
        prostate.summary()

        go()
        # Randomly split the dataset into ~70/30, training/test sets
        r = prostate[0].runif()
        train = prostate[r < 0.70]
        test = prostate[r >= 0.70]

        go()
        # Convert the response columns to factors (for binary classification problems)
        train["CAPSULE"] = train["CAPSULE"].asfactor()
        test["CAPSULE"] = test["CAPSULE"].asfactor()

        go()
        # Build a (classification) GLM
        from h2o.estimators import H2OGradientBoostingEstimator
        prostate_gbm = H2OGradientBoostingEstimator(distribution="bernoulli", ntrees=10, max_depth=8,
                                                    min_rows=10, learn_rate=0.2)
        prostate_gbm.train(x=["AGE", "RACE", "PSA", "VOL", "GLEASON"],
                           y="CAPSULE", training_frame=train)

        go()
        # Show the model
        prostate_gbm.show()

        go()
        # Predict on the test set and show the first ten predictions
        predictions = prostate_gbm.predict(test)
        predictions.show()

        go()
        # Show default performance metrics
        performance = prostate_gbm.model_performance(test)
        performance.show()

    # Execute:
    _run_demo(demo_body, interactive, echo, testing)



def deeplearning(interactive=True, echo=True, testing=False):
    """DeepLearning model demo."""
    def demo_body(go):
        """
        Demo of H2O's Deep Learning model.

        This demo uploads a dataset to h2o, parses it, and shows a description.
        Then it divides the dataset into training and test sets, builds a GLM
        from the training set, and makes predictions for the test set.
        Finally, default performance metrics are displayed.
        """
        go()
        # Connect to H2O
        h2o.init()

        go()
        # Upload the prostate dataset that comes included in the h2o python package
        prostate = h2o.upload_file(h2o.data_file("h2o_data/prostate.csv"))

        go()
        # Print a description of the prostate data
        prostate.summary()

        go()
        # Randomly split the dataset into ~70/30, training/test sets
        r = prostate[0].runif()
        train = prostate[r < 0.70]
        test = prostate[r >= 0.70]

        go()
        # Convert the response columns to factors (for binary classification problems)
        train["CAPSULE"] = train["CAPSULE"].asfactor()
        test["CAPSULE"] = test["CAPSULE"].asfactor()

        go()
        # Build a (classification) GLM
        from h2o.estimators import H2ODeepLearningEstimator
        prostate_dl = H2ODeepLearningEstimator(activation="Tanh", hidden=[10, 10, 10], epochs=10000)
        prostate_dl.train(x=list(set(prostate.col_names) - {"ID", "CAPSULE"}),
                          y="CAPSULE", training_frame=train)

        go()
        # Show the model
        prostate_dl.show()

        go()
        # Predict on the test set and show the first ten predictions
        predictions = prostate_dl.predict(test)
        predictions.show()

        go()
        # Show default performance metrics
        performance = prostate_dl.model_performance(test)
        performance.show()

    # Execute:
    _run_demo(demo_body, interactive, echo, testing)



def glm(interactive=True, echo=True, testing=False):
    """GLM model demo."""
    def demo_body(go):
        """
        Demo of H2O's Generalized Linear Estimator.

        This demo uploads a dataset to h2o, parses it, and shows a description.
        Then it divides the dataset into training and test sets, builds a GLM
        from the training set, and makes predictions for the test set.
        Finally, default performance metrics are displayed.
        """
        go()
        # Connect to H2O
        h2o.init()

        go()
        # Upload the prostate dataset that comes included in the h2o python package
        prostate = h2o.upload_file(h2o.data_file("h2o_data/prostate.csv"))

        go()
        # Print a description of the prostate data
        prostate.summary()

        go()
        # Randomly split the dataset into ~70/30, training/test sets
        r = prostate[0].runif()
        train = prostate[r < 0.70]
        test = prostate[r >= 0.70]

        go()
        # Convert the response columns to factors (for binary classification problems)
        train["CAPSULE"] = train["CAPSULE"].asfactor()
        test["CAPSULE"] = test["CAPSULE"].asfactor()

        go()
        # Build a (classification) GLM
        from h2o.estimators import H2OGeneralizedLinearEstimator
        prostate_glm = H2OGeneralizedLinearEstimator(family="binomial", alpha=[0.5])
        prostate_glm.train(x=["AGE", "RACE", "PSA", "VOL", "GLEASON"],
                           y="CAPSULE", training_frame=train)

        go()
        # Show the model
        prostate_glm.show()

        go()
        # Predict on the test set and show the first ten predictions
        predictions = prostate_glm.predict(test)
        predictions.show()

        go()
        # Show default performance metrics
        performance = prostate_glm.model_performance(test)
        performance.show()

    # Execute:
    _run_demo(demo_body, interactive, echo, testing)



def _run_demo(body_fn, interactive, echo, testing):
    """
    Execute the demo, echoing commands and pausing for user input.

    :param body_fn: function that contains the sequence of demo's commands.
    :param interactive: If True, the user will be prompted to continue the demonstration after every segment.
    :param echo: If True, the python commands that are executed will be displayed.
    :param testing: Used for pyunit testing. h2o.init() will not be called if set to True.
    :type body_fn: function
    """
    import colorama
    from colorama import Style, Fore
    colorama.init()

    class StopExecution(Exception):
        """Helper class for cancelling the demo."""
        pass

    assert_is_type(body_fn, "body_fn", type(_run_demo))
    # Reformat description by removing extra spaces; then print it.
    if body_fn.__doc__:
        desc_lines = body_fn.__doc__.split("\n")
        while desc_lines[0].strip() == "":
            desc_lines = desc_lines[1:]
        while desc_lines[-1].strip() == "":
            desc_lines = desc_lines[:-1]
        strip_spaces = min(len(line) - len(line.lstrip(" ")) for line in desc_lines[1:] if line.strip() != "")
        maxlen = max(len(line) for line in desc_lines)
        print(Fore.CYAN)
        print("-" * maxlen)
        for line in desc_lines:
            print(line[strip_spaces:].rstrip())
        print("-" * maxlen)
        print(Style.RESET_ALL, end="")

    # Prepare the executor function
    def controller():
        """Print to console the next block of commands, and wait for keypress."""
        try:
            raise RuntimeError("Catch me!")
        except RuntimeError:
            print()
            # Extract and print lines that will be executed next
            if echo:
                tb = sys.exc_info()[2]
                fr = tb.tb_frame.f_back
                filename = fr.f_code.co_filename
                linecache.checkcache(filename)
                line = linecache.getline(filename, fr.f_lineno, fr.f_globals).rstrip()
                indent_len = len(line) - len(line.lstrip(" "))
                assert line[indent_len:] == "go()"
                i = fr.f_lineno
                output_lines = []
                n_blank_lines = 0
                while True:
                    i += 1
                    line = linecache.getline(filename, i, fr.f_globals).rstrip()
                    # Detect dedent
                    if line[:indent_len].strip() != "": break
                    line = line[indent_len:]
                    if line == "go()": break
                    style = Fore.LIGHTBLACK_EX if line.lstrip().startswith("#") else Style.BRIGHT
                    prompt = "... " if line.startswith(" ") else ">>> "
                    output_lines.append(Fore.CYAN + prompt + Fore.RESET + style + line + Style.RESET_ALL)
                    del style  # Otherwise exception print-outs may get messed-up...
                    if line.strip() == "":
                        n_blank_lines += 1
                        if n_blank_lines > 5: break  # Just in case we hit file end or something
                    else:
                        n_blank_lines = 0
                for line in output_lines[:-n_blank_lines]:
                    print(line)

            # Prompt for user input
            if interactive:
                print("\n" + Style.DIM + "(press any key)" + Style.RESET_ALL, end="")
                key = _wait_for_keypress()
                print("\r                     \r", end="")
                if key.lower() == "q":
                    raise StopExecution()

    # Replace h2o.init() with a stub when running in "test" mode
    _h2o_init = h2o.init
    if testing:
        h2o.init = lambda *args, **kwargs: None

    # Run the test
    try:
        body_fn(controller)
        print("\n" + Fore.CYAN + "---- End of Demo ----" + Style.RESET_ALL)
    except StopExecution:
        print("\n" + Fore.RED + "---- Demo aborted ----" + Style.RESET_ALL)

    # Clean-up
    if testing:
        h2o.init = _h2o_init
    print()
    colorama.deinit()


def _wait_for_keypress():
    """
    Wait for a key press on the console and return it.

    Borrowed from http://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
    """
    result = None
    if os.name == "nt":
        # noinspection PyUnresolvedReferences
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result
