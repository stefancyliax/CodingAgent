from functions.get_files_info import get_files_info

def main():

    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

    
if __name__ == "__main__":
    main()
