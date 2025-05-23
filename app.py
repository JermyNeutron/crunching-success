import random
import platform
import sys
import time
from PyQt5 import QtWidgets, QtCore # Import necessary PyQt5 modules

# IMPORTANT: Import your generated UI class
# Make sure 'test_app_ui.py' (generated by pyuic5) is in the same directory
from qt_designer.ui_mainwindow import Ui_MainWindow
import fixed_return_pct

class MainWindow(QtWidgets.QMainWindow):
    """
    This is your main application window class.
    It inherits from QtWidgets.QMainWindow because your UI is a QMainWindow.
    """
    def __init__(self):
        """
        The constructor for your MainWindow.
        This is where you'll set up your UI and connect signals.
        """
        super().__init__() # Call the constructor of the parent class (QMainWindow)

        # Create an instance of your UI from the generated class
        self.ui = Ui_MainWindow()
        # Set up the UI on this MainWindow instance
        self.ui.setupUi(self)

        self.setWindowTitle("Crunching Success")
        # --- Place for Initial UI Setup (e.g., table headers, default labels) ---
        # Example: Setting initial text for a label
        # self.ui.sum_label.setText("Welcome! Enter values and generate data.")
        self.ui.sum_label.setText("... waiting for some numbers to CRUNCH lol ...")

        # --- Place for Connecting Signals to Slots (Widget Interactions) ---
        # Connect a button click:
        self.ui.button_generate.clicked.connect(self.my_generate_function)

        # Connect a combobox selection change:
        self.ui.brok_combo.currentIndexChanged.connect(self.my_validation_function)

        # --- Place for Initial Validation Call (if needed) ---
        # If your button starts disabled based on combobox selection,
        # call the validation function once after setup to set the correct initial state.
        # self.my_validation_function()


    # --- Place for Your Custom Methods (Slots) ---


    # Example: A slot for the generate button
    def my_generate_function(self):
        """
        This method will be called when the 'Generate' button is pressed.
        It's where you'll:
        1. Get values from spinboxes and the combobox (e.g., self.ui.sb_spin.value()).
        2. Call your data calculation logic.
        3. Update the summary label (e.ui.sum_label.setText()).
        4. Populate the QTableWidget (e.g., self.ui.sum_table.setRowCount(), self.ui.sum_table.setItem()).
        """
        print("Generate button clicked!") # For testing
        # Replace with your actual logic
        # value1 = self.ui.sb_spin.value()
        # selected_text = self.ui.brok_combo.currentText()
        # self.ui.sum_label.setText(f"You entered: {value1} and selected: {selected_text}")


        cap_start = self.ui.sb_spin.value()
        threshold = self.ui.eb_spin.value()
        util_pct_max = self.ui.util_spin.value()
        adj_gain = self.ui.tgt_spin.value()
        contract_cost = self.ui.prem_spin.value()
        brok_index = self.ui.brok_combo.currentIndex()

        meta_list, summary = fixed_return_pct.prompt(cap_start, threshold, util_pct_max,
                                adj_gain, contract_cost, brok_index, os_type)

        summary_statement = (f"To reach ${summary[3]} from ${summary[2]}, "
                             f"you'd need {summary[0]} trades."
                             f"\nDuration: {summary[1]}")

        self.ui.sum_label.setText(summary_statement)

    # Example: A slot for combobox validation
    def my_validation_function(self):
        """
        This method will be called when the combobox selection changes.
        It's where you'll:
        1. Check the combobox's current index (e.g., self.ui.brok_combo.currentIndex()).
        2. Enable or disable the generate button (e.g., self.ui.button_generate.setEnabled(True/False)).
        """
        if self.ui.brok_combo.currentIndex() > 0:
            self.ui.button_generate.setEnabled(True)
        else:
            self.ui.button_generate.setEnabled(False)


# --- Main Application Execution Block ---
# This is standard boilerplate code for all PyQt applications.
def main():
    """
    The main entry point of the application.
    """
    app = QtWidgets.QApplication(sys.argv) # Create the application instance
    window = MainWindow()                  # Create an instance of your main window
    window.show()                          # Display the window
    print(os_type)
    sys.exit(app.exec_())                  # Start the application's event loop

if __name__ == "__main__":
    os_type = platform.system()
    main() # Run the main function if the script is executed directly