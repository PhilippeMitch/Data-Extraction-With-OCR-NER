import os
import fitz
import string
import argparse
import cv2 as cv
import pytesseract
import pandas as pd
from glob import glob

from time import sleep
from pathlib import Path
from rich.progress import track
from rich.console import Console

import warnings
warnings.filterwarnings('ignore')

class Extract:

    def __init__(self, args, console) -> None:
        self.console = console
        self.args = args

    def clean_text(self, txt):
        whitespace = string.whitespace
        punctuation = "!#$%&\'()*+:;<=>?[\\]^`{|}~"
        tableWhitespace = str.maketrans('','',whitespace)
        tablePunctuation = str.maketrans('','',punctuation)
        text = str(txt)
        text = text.lower()
        removewhitespace = text.translate(tableWhitespace)
        removepunctuation = removewhitespace.translate(tablePunctuation)
    
        return str(removepunctuation)

    def _extract_from_dir(self):
        image_list = glob(f"{self.args.input}/*.png")
        # image_list = os.listdir(self.args.input)
        boarding_data = pd.DataFrame(columns=['id','text'])
        for img_path in track(image_list, description="Extracting text from images..."):
            _, filename = os.path.split(img_path)
            # extract data and text
            image = cv.imread(img_path)
            try:
                data = pytesseract.image_to_data(image)
                img_content_list = list(map(lambda x: x.split('\t'),data.split('\n')))
                img_content_df = pd.DataFrame(img_content_list[1:],columns=img_content_list[0])
                img_content_df.dropna(inplace=True)
                img_content_df['conf'] = img_content_df['conf'].astype(int)
                valuable_data_df = img_content_df.query('conf >= 15')
                # Dataframe
                boarding_form = pd.DataFrame()
                boarding_form['text'] = valuable_data_df['text']
                boarding_form['id'] = filename

                # concatenation
                boarding_data = pd.concat((boarding_data, boarding_form))
            except TypeError as ex:
                from rich import print
                print(f":warning: Unsupported image object for {img_path}")

        if self.args.output != None:
            boarding_data.to_csv(f'{self.args.output}/boarding_pass.csv',index=False)
            console.print("Extracted data have been save in", self.args.output, style="bold turquoise4")

    def _extract_from_file(self):
        # Load Image
        image = cv.imread(self.args.input)
        # extract data using Pytesseract 
        text = pytesseract.image_to_data(image)
        # convert into dataframe
        text_list = list(map(lambda x:x.split('\t'), text.split('\n')))
        df = pd.DataFrame(text_list[1:],columns=text_list[0])
        df.dropna(inplace=True) # drop missing values
        df['text'] = df['text'].apply(clean_text)
        # convet data into content
        df_clean = df.query('text != "" ')
        content = " ".join([w for w in df_clean['text']])
        return content

    def _extract(self):
        if Path(self.args.input).is_dir():
            self._extract_from_dir()
        else:
            self._extract_from_file()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Text extraction', description='Extract text from image')
    parser.add_argument("-i", "--input", type=str, default='../images',
                        help="Path to the pdf file or folder of pdf files")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help="Path to save the images")

    args = parser.parse_args()
    console = Console()
    converter = Extract(args, console)
    converter._extract()







