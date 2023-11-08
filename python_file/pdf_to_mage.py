import os
import fitz
import argparse
from time import sleep
from pathlib import Path
from rich.console import Console

class Converter:

    def __init__(self, args, console)-> None:
        self.args = args
        self.console = console

    def _convert(self, pdf_file, save_path):
        
        console.print("Extract data from", pdf_file, style="bold turquoise4")
        dpi = 300  # choose desired dpi here
        zoom = dpi / 72  # zoom factor, standard: 72 dpi
        magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
        docs = fitz.open(pdf_file)  # open document

        for page_number, page in enumerate(docs, start=1):
            pix = page.get_pixmap(matrix=magnify)  # render page to an image
            with console.status("[bold green]Working on tasks...") as status:
                # Create a file name to store the image
                
                filename = f"{os.path.basename(pdf_file).split('.')[0]}"
                sleep(0.3)
                # Save the image of the page in system
                pix.save(save_path + "/" + f"{filename}-{page.number + 1}.png", "png")
                console.log(f"page {page_number} of {pdf_file} complete", style="orange1")
                
    def _execute(self):
        if Path(self.args.input).is_dir():
            for pdf_file in os.listdir(self.args.input):
                self._convert(pdf_file, self.args.output)
        else:
            self._convert(self.args.input, self.args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PDF to Image', description='Convert pdf file to image')
    parser.add_argument("-i", "--input", type=str, default='../pdf/boarding_pass.pdf',
                        help="Path to the pdf file or folder of pdf files")
    parser.add_argument('-o', '--output', type=str, default='../images',
                        help="Path to save the images")

    args = parser.parse_args()
    console = Console()
    converter = Converter(args, console)
    converter._execute()
    
    