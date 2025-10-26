import platform
import fixed_return_pct
import compound_return_pct


def main():


    os_type = platform.system()

    while True:
        user_choice = input("""Select a program:
        1) Fixed Returns
        2) Compound Returns
        Q) Exit
        
        : """)
        if user_choice == "1":
            fixed_return_pct.main(os_type)
        elif user_choice == "2":
            compound_return_pct.main(os_type)
        elif user_choice.upper() == "Q":
            return False
        else:
            print("Invalid input. Select a valid input.\n")
        

if __name__ == "__main__":
    main()