import sys
import retriever
import visualize
import cleaner
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        exit()
    try:
        retriever.main(sys.argv[1])
        result = visualize.main()
    except Exception:
        print("Something went wrong!")
    finally:
        cleaner.clean()
