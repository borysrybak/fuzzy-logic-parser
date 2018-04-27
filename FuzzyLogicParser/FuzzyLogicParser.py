import importer
import parser

def run_azure_ocr():
    importer.main()

def parse_results():
    parser.main()

def main():
    run_azure_ocr()
    parse_results()

if __name__ == "__main__":
    main()