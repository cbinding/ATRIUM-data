# PDF text extraction from a folder of files
import argparse 
import os, json
from datetime import datetime as DT # for timestamps
from pdf_to_json import convert # using Mark's script to extract PDF text to structured output

def process_pdf(input_file: str="", output_path: str="") -> None:
    data = convert(input_file)
    
    # use given output path, or folder of input file
    if output_path.strip() == "":
        output_path = os.path.dirname(input_file)

    # ensure output folder structure exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # build json file name for output data
    file_name = os.path.basename(input_file)
    file_path = os.path.join(output_path, f"text_extraction_{file_name}.json")

    # write the output
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # set up command line arg parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="Extract text from PDF files")

    # add long and short command line argument descriptions
    parser.add_argument("--input", "-i", required=False,
                        help="Input file or folder name")

    parser.add_argument("--output", "-o", required=False,            
                        help="Output folder name")
     
    # parse command line arguments
    args = parser.parse_args()

    # get clean input values if passed in and override defaults
    timestamp: str = DT.now().strftime('%Y%m%d')
    input_name: str = "./data/journals_july_2024"
    output_folder: str = os.path.join(input_name, f"text_extraction-{timestamp}")
   
    if args.input:
        input_name = args.input.strip()

    if args.output:
        output_folder = args.output.strip()

    # input may be either a directory or an individual file
    if os.path.isfile(input_name):
        process_pdf(input_name)        
    elif os.path.isdir(input_name):
        # list only the PDF files in the directory
        files = [file for file in os.scandir(input_name) if os.path.isfile(file.path) and file.name.lower().endswith(".pdf")]
       
        if(len(files) == 0):
            print("nothing to process")

        # process each file found    
        for file in files:
            print(f"processing '{file.name}'")
            process_pdf(file.path, output_folder)
            
    else:
        raise(f"{input_name} is not a file or directory")
    
    print("finished")
    